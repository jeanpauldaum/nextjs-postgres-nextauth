#!/usr/bin/env python3
"""Text to speech for explainer narration, with a provider chain.

Order for --provider auto:
  1. speechify   Speechify API    SPEECHIFY_API_KEY, SPEECHIFY_VOICE_ID (geffen_32), SPEECHIFY_MODEL (simba-3.2)
  2. fish        Fish Audio API   FISH_API_KEY (or FISH_AUDIO_API_KEY), FISH_REFERENCE_ID, FISH_MODEL
  3. elevenlabs  ElevenLabs API   ELEVENLABS_API_KEY (or XI_API_KEY), ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL_ID
  4. kokoro      local, free      pip install kokoro-onnx soundfile; model files in KOKORO_DIR
  5. piper       local, free      pip install piper-tts; PIPER_MODEL=/path/voice.onnx
  6. espeak      local, robotic   espeak-ng binary (last resort)

Usage:
  tts.py "Text to say." out.wav [--provider auto] [--voice ID] [--speed 1.0]
  tts.py --list                 # show which providers work here
  tts.py --env-file ~/umli/customer-voice-agent/.env --list
  tts.py --download-kokoro      # fetch the Kokoro model files (~350 MB)

--env-file loads only voice API keys (SPEECHIFY_*, FISH_*, ELEVENLABS_*,
XI_API_KEY) into this process. It never prints or writes their values.
Output is always mono WAV. API providers and format conversion need ffmpeg.
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

KOKORO_DIR = Path(os.environ.get("KOKORO_DIR", Path.home() / ".cache" / "explainer-tts" / "kokoro"))
KOKORO_FILES = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}
SPEECHIFY_URL = "https://api.speechify.ai/v1/audio/speech"
ORDER = ["speechify", "fish", "elevenlabs", "kokoro", "piper", "espeak"]
TAG_RE = re.compile(r"\[[a-z ]+\]\s*")
ENV_FILE_KEY_RE = re.compile(r"^(?:SPEECHIFY_\w+|FISH_\w+|ELEVENLABS_\w+|XI_API_KEY)$")


class TTSError(RuntimeError):
    pass


def _env(*names):
    for n in names:
        if os.environ.get(n):
            return os.environ[n]
    return ""


def default_voice(provider: str) -> str:
    """Voice for a provider. Read at call time so keys loaded by --env-file count."""
    return {
        "speechify": os.environ.get("SPEECHIFY_VOICE_ID", "geffen_32"),
        "fish": _env("FISH_REFERENCE_ID", "FISH_VOICE_ID"),
        "elevenlabs": os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        "kokoro": os.environ.get("KOKORO_VOICE", "af_heart"),
        "piper": os.environ.get("PIPER_MODEL", ""),
        "espeak": os.environ.get("ESPEAK_VOICE", "en-us"),
    }[provider]


def load_env_file(path) -> list:
    """Load voice API settings from a dotenv file into os.environ.

    Only SPEECHIFY_*, FISH_*, ELEVENLABS_*, and XI_API_KEY are read; other
    lines are ignored. Variables that are already set win. Returns the key
    names that were loaded, never the values.
    """
    loaded = []
    for raw in Path(path).expanduser().read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        if ENV_FILE_KEY_RE.match(key) and value and not os.environ.get(key):
            os.environ[key] = value
            loaded.append(key)
    return loaded


def _ffmpeg_to_wav(src: Path, dst: Path, rate: int = 44100) -> None:
    if not shutil.which("ffmpeg"):
        raise TTSError("ffmpeg is required to convert audio")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(rate), str(dst)],
                   check=True)


def _post(url: str, headers: dict, body: dict) -> bytes:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode(errors="replace")
        raise TTSError("%s returned HTTP %d: %s" % (url, exc.code, detail)) from None


def _kokoro_ready() -> bool:
    try:
        import kokoro_onnx  # noqa: F401
        import soundfile  # noqa: F401
    except ImportError:
        return False
    return True


def availability() -> dict:
    """Map provider -> (usable, reason)."""
    out = {}
    out["speechify"] = (bool(_env("SPEECHIFY_API_KEY")), "SPEECHIFY_API_KEY")
    out["fish"] = (bool(_env("FISH_API_KEY", "FISH_AUDIO_API_KEY")), "FISH_API_KEY")
    out["elevenlabs"] = (bool(_env("ELEVENLABS_API_KEY", "XI_API_KEY")), "ELEVENLABS_API_KEY")
    if _kokoro_ready():
        models = all((KOKORO_DIR / f).exists() for f in KOKORO_FILES)
        out["kokoro"] = (True, "kokoro-onnx" + ("" if models else " (models download on first use)"))
    else:
        out["kokoro"] = (False, "pip install kokoro-onnx soundfile")
    piper_ok = bool(shutil.which("piper")) and bool(DEFAULT_VOICES["piper"])
    out["piper"] = (piper_ok, "piper CLI + PIPER_MODEL")
    out["espeak"] = (bool(shutil.which("espeak-ng") or shutil.which("espeak")), "espeak-ng binary")
    return out


def pick_provider(preferred: str = "auto") -> str:
    avail = availability()
    if preferred != "auto":
        if not avail[preferred][0]:
            raise TTSError("provider %s is not available: needs %s" % (preferred, avail[preferred][1]))
        return preferred
    for p in ORDER:
        if avail[p][0]:
            return p
    raise TTSError("no TTS provider found. Run scripts/setup.sh, or set SPEECHIFY_API_KEY, FISH_API_KEY, "
                   "or ELEVENLABS_API_KEY.")


def download_kokoro() -> None:
    KOKORO_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in KOKORO_FILES.items():
        dst = KOKORO_DIR / name
        if dst.exists() and dst.stat().st_size > 0:
            continue
        print("downloading %s -> %s" % (url, dst), file=sys.stderr)
        tmp = dst.with_suffix(dst.suffix + ".part")
        with urllib.request.urlopen(url, timeout=600) as resp, open(tmp, "wb") as fh:
            shutil.copyfileobj(resp, fh)
        tmp.rename(dst)


def _ssml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&apos;"))


def _speechify(text: str, out: Path, voice: str, speed: float) -> None:
    # Voice and model must match the GlassTalk dashboard (geffen_32, simba-3.2).
    # WAV, not MP3: the build encodes to AAC later, so this skips one lossy step.
    spoken = text
    if abs(speed - 1.0) > 1e-3:
        spoken = '<speak><prosody rate="%+d%%">%s</prosody></speak>' % (round((speed - 1.0) * 100),
                                                                         _ssml_escape(text))
    headers = {"Authorization": "Bearer " + _env("SPEECHIFY_API_KEY"), "Content-Type": "application/json"}
    body = {"input": spoken, "voice_id": voice, "model": os.environ.get("SPEECHIFY_MODEL", "simba-3.2"),
            "audio_format": "wav"}
    try:
        data = json.loads(_post(SPEECHIFY_URL, headers, body))
    except ValueError:
        raise TTSError("speechify returned a response that is not JSON") from None
    fmt = data.get("audio_format", "wav")
    audio = base64.b64decode(data.get("audio_data") or "")
    if not audio:
        raise TTSError("speechify returned no audio_data")
    if fmt not in ("wav", "mp3", "ogg", "aac"):
        raise TTSError("speechify returned audio_format %r; expected wav, mp3, ogg, or aac" % fmt)
    with tempfile.NamedTemporaryFile(suffix="." + fmt, delete=False) as fh:
        fh.write(audio)
    try:
        _ffmpeg_to_wav(Path(fh.name), out)
    finally:
        os.unlink(fh.name)


def _fish(text: str, out: Path, voice: str, speed: float) -> None:
    headers = {"Authorization": "Bearer " + _env("FISH_API_KEY", "FISH_AUDIO_API_KEY"),
               "Content-Type": "application/json"}
    if os.environ.get("FISH_MODEL"):
        headers["model"] = os.environ["FISH_MODEL"]
    body = {"text": text, "format": "mp3", "mp3_bitrate": 192, "normalize": True, "latency": "normal",
            "prosody": {"speed": speed, "volume": 0}}
    if voice:
        body["reference_id"] = voice
    audio = _post("https://api.fish.audio/v1/tts", headers, body)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fh:
        fh.write(audio)
    _ffmpeg_to_wav(Path(fh.name), out)
    os.unlink(fh.name)


def _elevenlabs(text: str, out: Path, voice: str, speed: float, context: tuple) -> None:
    headers = {"xi-api-key": _env("ELEVENLABS_API_KEY", "XI_API_KEY"), "Content-Type": "application/json",
               "Accept": "audio/mpeg"}
    body = {"text": text, "model_id": os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": speed}}
    prev_text, next_text = context
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128" % voice
    audio = _post(url, headers, body)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fh:
        fh.write(audio)
    _ffmpeg_to_wav(Path(fh.name), out)
    os.unlink(fh.name)


_KOKORO = None


def _kokoro(text: str, out: Path, voice: str, speed: float) -> None:
    global _KOKORO
    import soundfile as sf
    from kokoro_onnx import Kokoro
    if _KOKORO is None:
        download_kokoro()
        _KOKORO = Kokoro(str(KOKORO_DIR / "kokoro-v1.0.onnx"), str(KOKORO_DIR / "voices-v1.0.bin"))
    samples, rate = _KOKORO.create(text, voice=voice, speed=speed, lang=os.environ.get("KOKORO_LANG", "en-us"))
    sf.write(str(out), samples, rate)


def _piper(text: str, out: Path, voice: str, speed: float) -> None:
    cmd = ["piper", "--model", voice, "--output_file", str(out), "--length_scale", "%.3f" % (1.0 / speed)]
    subprocess.run(cmd, input=text, text=True, check=True, capture_output=True)


def _espeak(text: str, out: Path, voice: str, speed: float) -> None:
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    subprocess.run([exe, "-v", voice, "-s", str(int(165 * speed)), "-w", str(out), text], check=True)


def synthesize(text: str, out, provider: str = "auto", voice: str = "", speed: float = 1.0,
               context: tuple = ("", "")) -> dict:
    """Write `text` as mono WAV to `out`. Returns {"provider", "voice", "path"}."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    provider = pick_provider(provider)
    voice = voice or default_voice(provider)
    spoken = text if provider == "fish" else TAG_RE.sub("", text).strip()
    if provider == "speechify":
        _speechify(spoken, out, voice, speed)
    elif provider == "fish":
        _fish(spoken, out, voice, speed)
    elif provider == "elevenlabs":
        _elevenlabs(spoken, out, voice, speed, context)
    elif provider == "kokoro":
        _kokoro(spoken, out, voice, speed)
    elif provider == "piper":
        _piper(spoken, out, voice, speed)
    else:
        _espeak(spoken, out, voice, speed)
    if not out.exists() or out.stat().st_size == 0:
        raise TTSError("%s produced no audio" % provider)
    return {"provider": provider, "voice": voice, "path": str(out)}


def venv_dir() -> Path:
    return Path(os.environ.get("EXPLAINER_VENV", Path.home() / ".venvs" / "explainer"))


def reexec_in_venv(module_ok) -> None:
    """Re-run this script with the explainer venv when a module is missing here."""
    py = venv_dir() / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if module_ok() or not py.exists() or Path(sys.prefix).resolve() == venv_dir().resolve():
        return
    if os.environ.get("EXPLAINER_REEXEC"):
        return
    os.environ["EXPLAINER_REEXEC"] = "1"
    os.execv(str(py), [str(py)] + sys.argv)


def report_env_file(path) -> None:
    """Load --env-file and say which key names it set (never the values)."""
    try:
        loaded = load_env_file(path)
    except OSError as exc:
        raise SystemExit("tts: cannot read env file %s: %s" % (path, exc.strerror))
    print("tts: loaded %s from %s" % (", ".join(loaded) or "no new voice keys", path), file=sys.stderr)


def main() -> int:
    reexec_in_venv(_kokoro_ready)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--provider", default="auto", choices=["auto"] + ORDER)
    ap.add_argument("--voice", default="")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--env-file", default=os.environ.get("EXPLAINER_ENV_FILE", ""),
                    help="dotenv file with voice API keys (also EXPLAINER_ENV_FILE)")
    ap.add_argument("--download-kokoro", action="store_true")
    args = ap.parse_args()
    if args.env_file:
        report_env_file(args.env_file)
    if args.download_kokoro:
        download_kokoro()
        print("kokoro models in %s" % KOKORO_DIR)
        return 0
    if args.list:
        chosen = None
        try:
            chosen = pick_provider()
        except TTSError:
            pass
        for p, (ok, why) in availability().items():
            print("%-11s %-4s %s%s" % (p, "yes" if ok else "no", why, "   <- auto" if p == chosen else ""))
        return 0
    if not (args.text and args.out):
        ap.error("give TEXT and OUT, or --list")
    try:
        info = synthesize(args.text, args.out, args.provider, args.voice, args.speed)
    except (TTSError, subprocess.CalledProcessError) as exc:
        print("tts: %s" % exc, file=sys.stderr)
        return 1
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
