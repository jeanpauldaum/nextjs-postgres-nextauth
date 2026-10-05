#!/usr/bin/env python3
"""Offline checks for tts.py. No API keys and no network; HTTP is mocked.

Covers the provider order, --provider forcing, the env-file loader, and the
Speechify, Fish, and ElevenLabs request and response handling. Needs ffmpeg.

  python3 selftest_tts.py
"""

import base64
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import wave
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tts  # noqa: E402


def tone_wav(seconds=0.6, rate=24000) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x10" * int(seconds * rate))
    return buf.getvalue()


def wav_seconds(path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / float(w.getframerate())


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Recorder:
    """Stands in for urllib.request.urlopen and keeps each request."""

    def __init__(self, payload: bytes):
        self.payload = payload
        self.requests = []

    def __call__(self, req, timeout=None):
        self.requests.append(req)
        return FakeResponse(self.payload)

    @property
    def body(self):
        return json.loads(self.requests[-1].data)


def speechify_payload(audio: bytes, fmt="wav") -> bytes:
    return json.dumps({"audio_data": base64.b64encode(audio).decode(), "audio_format": fmt,
                       "billable_characters_count": 10, "speech_marks": {}}).encode()


class TTSTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        for key in list(os.environ):
            if tts.ENV_FILE_KEY_RE.match(key):
                del os.environ[key]
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "out.wav"

    def synth(self, recorder, text, **kw):
        with mock.patch.object(tts.urllib.request, "urlopen", recorder):
            return tts.synthesize(text, self.out, **kw)

    # --- order and forcing -------------------------------------------------

    def test_order_puts_speechify_first(self):
        self.assertEqual(tts.ORDER[:4], ["speechify", "fish", "elevenlabs", "kokoro"])
        os.environ.update(SPEECHIFY_API_KEY="sk_test", FISH_API_KEY="f", ELEVENLABS_API_KEY="e")
        self.assertEqual(tts.pick_provider(), "speechify")
        del os.environ["SPEECHIFY_API_KEY"]
        self.assertEqual(tts.pick_provider(), "fish")
        del os.environ["FISH_API_KEY"]
        self.assertEqual(tts.pick_provider(), "elevenlabs")

    def test_force_provider(self):
        os.environ.update(SPEECHIFY_API_KEY="sk_test", ELEVENLABS_API_KEY="e")
        self.assertEqual(tts.pick_provider("elevenlabs"), "elevenlabs")
        with self.assertRaises(tts.TTSError):
            tts.pick_provider("fish")

    # --- Speechify ---------------------------------------------------------

    def test_speechify_request_and_decode(self):
        os.environ["SPEECHIFY_API_KEY"] = "sk_test_123"
        rec = Recorder(speechify_payload(tone_wav(0.6)))
        info = self.synth(rec, "[calm] Ship it now & check <it>.")
        req = rec.requests[-1]
        self.assertEqual(req.full_url, "https://api.speechify.ai/v1/audio/speech")
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.get_header("Authorization"), "Bearer sk_test_123")
        self.assertEqual(req.get_header("Content-type"), "application/json")
        self.assertEqual(rec.body, {"input": "Ship it now & check <it>.", "voice_id": "geffen_32",
                                    "model": "simba-3.2", "audio_format": "wav"})
        self.assertEqual(info, {"provider": "speechify", "voice": "geffen_32", "path": str(self.out)})
        self.assertAlmostEqual(wav_seconds(self.out), 0.6, places=2)

    def test_speechify_speed_uses_ssml_prosody(self):
        os.environ["SPEECHIFY_API_KEY"] = "sk_test"
        rec = Recorder(speechify_payload(tone_wav()))
        self.synth(rec, "Fish & chips <now>", speed=1.1)
        self.assertEqual(rec.body["input"],
                         '<speak><prosody rate="+10%">Fish &amp; chips &lt;now&gt;</prosody></speak>')
        self.synth(rec, "Slower.", speed=0.85)
        self.assertEqual(rec.body["input"], '<speak><prosody rate="-15%">Slower.</prosody></speak>')

    def test_speechify_env_overrides_voice_and_model(self):
        os.environ.update(SPEECHIFY_API_KEY="sk_test", SPEECHIFY_VOICE_ID="other_voice",
                          SPEECHIFY_MODEL="simba-3.0")
        rec = Recorder(speechify_payload(tone_wav()))
        self.synth(rec, "Hello.")
        self.assertEqual((rec.body["voice_id"], rec.body["model"]), ("other_voice", "simba-3.0"))

    def test_speechify_mp3_response_is_converted(self):
        os.environ["SPEECHIFY_API_KEY"] = "sk_test"
        mp3 = Path(self.tmp.name) / "a.mp3"
        src = Path(self.tmp.name) / "a.wav"
        src.write_bytes(tone_wav(0.5))
        tts._ffmpeg_to_wav(src, mp3, rate=24000)
        self.synth(Recorder(speechify_payload(mp3.read_bytes(), "mp3")), "Hello.")
        self.assertGreater(wav_seconds(self.out), 0.4)

    def test_speechify_http_error_names_status_not_key(self):
        os.environ["SPEECHIFY_API_KEY"] = "sk_secret_value"
        body = io.BytesIO(b'{"error":{"code":"unauthorized","message":"bad key"}}')
        err = urllib.error.HTTPError(tts.SPEECHIFY_URL, 401, "Unauthorized", {}, body)
        with mock.patch.object(tts.urllib.request, "urlopen", side_effect=err):
            with self.assertRaises(tts.TTSError) as ctx:
                tts.synthesize("Hello.", self.out)
        self.assertIn("401", str(ctx.exception))
        self.assertIn("unauthorized", str(ctx.exception))
        self.assertNotIn("sk_secret_value", str(ctx.exception))

    def test_speechify_empty_or_bad_response(self):
        os.environ["SPEECHIFY_API_KEY"] = "sk_test"
        for payload in (b'{"audio_format": "wav"}', b"<html>not json</html>",
                        speechify_payload(b"raw", "pcm")):
            with self.subTest(payload=payload[:20]):
                with self.assertRaises(tts.TTSError):
                    self.synth(Recorder(payload), "Hello.")

    # --- Fish and ElevenLabs ------------------------------------------------

    def test_fish_request_shape(self):
        os.environ.update(FISH_API_KEY="fish_test", FISH_REFERENCE_ID="ref123")
        rec = Recorder(tone_wav(0.5))
        info = self.synth(rec, "[calm] Hello.", provider="fish")
        req = rec.requests[-1]
        self.assertEqual(req.full_url, "https://api.fish.audio/v1/tts")
        self.assertEqual(req.get_header("Authorization"), "Bearer fish_test")
        self.assertEqual(rec.body["text"], "[calm] Hello.")
        self.assertEqual(rec.body["reference_id"], "ref123")
        self.assertEqual(info["provider"], "fish")
        self.assertGreater(wav_seconds(self.out), 0.4)

    def test_elevenlabs_request_shape(self):
        os.environ["ELEVENLABS_API_KEY"] = "xi_test"
        rec = Recorder(tone_wav(0.5))
        self.synth(rec, "Hello.", provider="elevenlabs", context=("Before.", "After."))
        req = rec.requests[-1]
        self.assertTrue(req.full_url.startswith(
            "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format="))
        self.assertEqual(req.get_header("Xi-api-key"), "xi_test")
        self.assertEqual((rec.body["text"], rec.body["previous_text"], rec.body["next_text"]),
                         ("Hello.", "Before.", "After."))

    # --- env file -----------------------------------------------------------

    def test_env_file_loads_only_voice_keys(self):
        env = Path(self.tmp.name) / ".env"
        env.write_text("# comment\nSPEECHIFY_API_KEY=\"sk_from_file\"\nexport FISH_API_KEY=fish_file\n"
                       "OPENAI_API_KEY=not_for_us\nELEVENLABS_API_KEY=keep_existing\n"
                       "SPEECHIFY_VOICE_ID=geffen_32 # trailing comment\n")
        os.environ["ELEVENLABS_API_KEY"] = "already_set"
        other_before = os.environ.get("OPENAI_API_KEY")
        loaded = tts.load_env_file(env)
        self.assertEqual(loaded, ["SPEECHIFY_API_KEY", "FISH_API_KEY", "SPEECHIFY_VOICE_ID"])
        self.assertEqual(os.environ["SPEECHIFY_API_KEY"], "sk_from_file")
        self.assertEqual(os.environ["SPEECHIFY_VOICE_ID"], "geffen_32")
        self.assertEqual(os.environ["ELEVENLABS_API_KEY"], "already_set")
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), other_before)
        self.assertEqual(tts.pick_provider(), "speechify")


if __name__ == "__main__":
    unittest.main(verbosity=2)
