#!/usr/bin/env python3
"""Build a narrated explainer video from a storyboard and a Manim scene.

Usage:
  build_video.py storyboard.json [--scene scene.py] [--class Explainer] [--out video.mp4]
                 [--quality draft|final]
                 [--provider auto|speechify|fish|elevenlabs|kokoro|piper|espeak]
                 [--voice ID] [--env-file PATH] [--workdir DIR] [--no-lint] [--strict-lint]

--provider forces one voice provider; auto takes the first that works
(Speechify, Fish, ElevenLabs, Kokoro, Piper, espeak). --env-file (or
EXPLAINER_ENV_FILE) loads only voice API keys from a dotenv file into this
process; it never prints or writes their values.

Steps:
  1. Lint the narration (explainer-plain-writing/scripts/ste_lint.py).
  2. Synthesize each beat with tts.py (cached by text + voice).
  3. Write build/timings.json, then render the scene with Manim.
  4. Place each beat's audio at the beat's actual start time and mix one track.
  5. Write captions.srt, mux video + audio + soft captions into one MP4.
  6. Write build/contact.png (one frame at the end of each beat) and a report.

Needs: ffmpeg, and Manim in this Python or in the explainer venv
(~/.venvs/explainer, made by setup.sh). The script re-runs itself in the venv
when this Python has no Manim.
"""

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import textwrap
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT = HERE.parent.parent / "explainer-plain-writing" / "scripts" / "ste_lint.py"
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import tts  # noqa: E402


def manim_ok() -> bool:
    try:
        import manim  # noqa: F401
    except ImportError:
        return False
    return True


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def duration_of(path: Path) -> float:
    try:
        with wave.open(str(path)) as w:
            return w.getnframes() / float(w.getframerate())
    except (wave.Error, EOFError):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                              "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
        return float(out.stdout.strip())


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def caption_cues(text: str, start: float, dur: float, width: int = 42):
    """Split a beat into sentence cues of at most two lines, timed by word count."""
    clean = re.sub(r"\[[a-z ]+\]\s*", "", text).strip()
    parts = []
    for sentence in re.split(r"(?<=[.!?])\s+", clean):
        lines = textwrap.wrap(sentence, width)
        for i in range(0, len(lines), 2):
            parts.append("\n".join(lines[i:i + 2]))
    words = [max(1, len(p.split())) for p in parts]
    total = float(sum(words))
    t = start
    for p, w in zip(parts, words):
        d = dur * w / total
        yield t, t + d, p
        t += d


def lint_storyboard(path: Path, strict: bool) -> str:
    if not LINT.exists():
        return "lint skipped (ste_lint.py not found next to this skill)"
    proc = subprocess.run([sys.executable, str(LINT), str(path)], capture_output=True, text=True)
    print(proc.stdout.rstrip())
    if strict and proc.returncode != 0:
        sys.exit("build_video: narration failed the lint (--strict-lint)")
    return proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""


def contact_sheet(video: Path, times, work: Path) -> Path:
    frames = work / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    for i, t in enumerate(times):
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.3f" % max(0.0, t), "-i", video,
             "-frames:v", "1", "-vf", "scale=640:-2", frames / ("f%02d.png" % i)])
    cols = min(3, len(times))
    rows = math.ceil(len(times) / cols)
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height", "-of", "csv=p=0", str(frames / "f00.png")],
                           capture_output=True, text=True, check=True)
    size = probe.stdout.strip().replace(",", "x")
    for i in range(len(times), cols * rows):
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0xF7F8FB:s=%s" % size,
             "-frames:v", "1", frames / ("f%02d.png" % i)])
    sheet = work / "contact.png"
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", frames / "f%02d.png", "-vf",
         "tile=%dx%d:padding=12:margin=12:color=0xF7F8FB" % (cols, rows), "-frames:v", "1", sheet])
    return sheet


def main() -> int:
    tts.reexec_in_venv(manim_ok)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("--scene")
    ap.add_argument("--class", dest="scene_class")
    ap.add_argument("--out")
    ap.add_argument("--quality", choices=["draft", "final"], default="final")
    ap.add_argument("--provider", choices=["auto"] + tts.ORDER)
    ap.add_argument("--voice")
    ap.add_argument("--env-file", default=os.environ.get("EXPLAINER_ENV_FILE", ""))
    ap.add_argument("--workdir")
    ap.add_argument("--no-lint", action="store_true")
    ap.add_argument("--strict-lint", action="store_true")
    args = ap.parse_args()
    if args.env_file:
        tts.report_env_file(args.env_file)

    if not shutil.which("ffmpeg"):
        sys.exit("build_video: ffmpeg not found. Run setup.sh.")
    if not manim_ok():
        sys.exit("build_video: Manim not found. Run setup.sh (makes ~/.venvs/explainer).")

    sb_path = Path(args.storyboard).resolve()
    sb = json.loads(sb_path.read_text())
    base = sb_path.parent
    scene_path = (base / (args.scene or sb.get("scene", "scene.py"))).resolve()
    scene_class = args.scene_class or sb.get("scene_class", "Explainer")
    out = (base / (args.out or sb.get("out", "video.mp4"))).resolve()
    work = (base / (args.workdir or sb.get("workdir", "build"))).resolve()
    work.mkdir(parents=True, exist_ok=True)
    beats = sb["beats"]
    ids = [b["id"] for b in beats]
    if len(set(ids)) != len(ids) or not all(b.get("say", "").strip() for b in beats):
        sys.exit("build_video: each beat needs a unique id and a non-empty 'say'")
    voice_cfg = sb.get("voice", {})
    speed = float(voice_cfg.get("speed", 1.0))

    print("== 1/6 lint narration")
    lint_summary = "lint skipped" if args.no_lint else lint_storyboard(sb_path, args.strict_lint)

    print("== 2/6 narration (TTS)")
    provider = tts.pick_provider(args.provider or voice_cfg.get("provider", "auto"))
    voice = args.voice or voice_cfg.get(provider) or voice_cfg.get("voice") or tts.default_voice(provider)
    timings = {"lead_in": float(sb.get("lead_in", 0.4)), "gap": float(sb.get("gap", 0.35)),
               "tail": float(sb.get("tail", 1.2)), "provider": provider, "voice": voice, "beats": {},
               "order": ids}
    spoken = [b.get("speak") or b["say"] for b in beats]
    for i, b in enumerate(beats):
        wav = work / "audio" / ("%s.wav" % b["id"])
        meta = wav.with_suffix(".json")
        key = hashlib.sha1(json.dumps([provider, voice, speed, spoken[i]]).encode()).hexdigest()
        cached = wav.exists() and meta.exists() and json.loads(meta.read_text()).get("key") == key
        if not cached:
            context = (spoken[i - 1] if i else "", spoken[i + 1] if i + 1 < len(beats) else "")
            tts.synthesize(spoken[i], wav, provider, voice, speed, context)
            meta.write_text(json.dumps({"key": key, "provider": provider, "voice": voice}))
        d = duration_of(wav)
        timings["beats"][b["id"]] = {"duration": round(d, 3), "say": b["say"]}
        print("  %-12s %5.2fs %s" % (b["id"], d, "(cached)" if cached else ""))
    (work / "timings.json").write_text(json.dumps(timings, indent=2))

    print("== 3/6 render (Manim, %s)" % args.quality)
    quality = ["-ql"] if args.quality == "draft" else ["-qh", "-r", "1920,1080", "--fps", "30"]
    actual_path = work / "actual.json"
    if actual_path.exists():
        actual_path.unlink()
    env = dict(os.environ, EXPLAINER_TIMINGS=str(work / "timings.json"), EXPLAINER_ACTUAL=str(actual_path),
               PYTHONPATH=str(HERE) + os.pathsep + os.environ.get("PYTHONPATH", ""), PYTHONDONTWRITEBYTECODE="1")
    run([sys.executable, "-m", "manim", "render", scene_path, scene_class, *quality, "--media_dir",
         work / "media", "-o", "scene", "--disable_caching", "--progress_bar", "none", "-v", "WARNING"],
        cwd=scene_path.parent, env=env)
    videos = sorted((work / "media" / "videos").rglob("scene.mp4"), key=lambda p: p.stat().st_mtime)
    if not videos or not actual_path.exists():
        sys.exit("build_video: render produced no video or no actual.json (does the scene use NarratedScene?)")
    video = videos[-1]
    actual = json.loads(actual_path.read_text())
    total = duration_of(video)

    print("== 4/6 narration track")
    inputs, chains, used = [], [], []
    for b in beats:
        start = actual["beats"].get(b["id"], {}).get("start")
        if start is None:
            print("  warning: beat %s is not in the scene; its audio is skipped" % b["id"])
            continue
        ms = int(round(start * 1000))
        inputs += ["-i", work / "audio" / ("%s.wav" % b["id"])]
        chains.append("[%d:a]aresample=48000,adelay=delays=%d:all=1[a%d]" % (len(used), ms, len(used)))
        used.append(b["id"])
    mix = "".join("[a%d]" % i for i in range(len(used)))
    graph = ";".join(chains) + ";%samix=inputs=%d:normalize=0:dropout_transition=0,apad,atrim=0:%.3f," \
        "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[out]" % (mix, len(used), total)
    narration = work / "narration.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[out]", "-ac", "1",
         narration])

    print("== 5/6 captions + mux")
    srt = work / "captions.srt"
    cues = []
    for bid in used:
        start = actual["beats"][bid]["start"]
        cues += list(caption_cues(timings["beats"][bid]["say"], start, timings["beats"][bid]["duration"]))
    srt.write_text("".join("%d\n%s --> %s\n%s\n\n" % (i + 1, srt_time(a), srt_time(b), t)
                           for i, (a, b, t) in enumerate(cues)))
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", narration, "-i", srt, "-map", "0:v:0",
         "-map", "1:a:0", "-map", "2:s:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-c:s", "mov_text",
         "-metadata:s:s:0", "language=eng", "-metadata", "title=" + sb.get("title", ""),
         "-movflags", "+faststart", out])

    print("== 6/6 review")
    rows, ends = [], []
    for i, bid in enumerate(used):
        a = actual["beats"][bid]
        end = a.get("end", total)
        span = end - a["start"]
        dur = timings["beats"][bid]["duration"]
        note = "long pause" if span - dur > 2.5 else ("audio overruns beat" if dur > span + 0.05 else "ok")
        rows.append({"beat": bid, "start": round(a["start"], 2), "narration": dur, "span": round(span, 2),
                     "note": note, "say": timings["beats"][bid]["say"]})
        ends.append(end - 0.12)
    sheet = contact_sheet(out, ends, work)
    report = {"out": str(out), "duration": round(duration_of(out), 2), "provider": provider, "voice": voice,
              "lint": lint_summary, "contact_sheet": str(sheet), "captions": str(srt), "beats": rows}
    (work / "report.json").write_text(json.dumps(report, indent=2))
    print("  %-12s %6s %6s %6s  %s" % ("beat", "start", "voice", "span", "note"))
    for r in rows:
        print("  %-12s %6.2f %6.2f %6.2f  %s" % (r["beat"], r["start"], r["narration"], r["span"], r["note"]))
    print("video:   %s (%.1fs, %s / %s)" % (out, report["duration"], provider, voice))
    print("frames:  %s  (tile i = beat i, left to right)" % sheet)
    print("report:  %s" % (work / "report.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
