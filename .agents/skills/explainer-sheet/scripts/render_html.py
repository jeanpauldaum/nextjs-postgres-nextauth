#!/usr/bin/env python3
"""Render a local HTML file to PNG (or PDF) with headless Chrome / Chromium.

Usage:
  render_html.py sheet.html sheet.png                      # 1600x1000 CSS px at 2x
  render_html.py page.html shot.png --width 1280 --height 800 --scale 1
  render_html.py sheet.html sheet.pdf                      # print to PDF
  render_html.py page.html step2.png --hash step-2         # open page.html#step-2
  render_html.py page.html shot.png --console              # print console; exit 3 on a JS error

Set CHROME=/path/to/chrome to choose the browser. Standard library only.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CANDIDATES = [
    "google-chrome-stable", "chromium", "chromium-browser", "google-chrome", "chrome", "msedge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_chrome() -> str:
    env = os.environ.get("CHROME")
    if env:
        return env
    for c in CANDIDATES:
        path = shutil.which(c) or (c if os.path.isfile(c) else None)
        if path:
            return path
    sys.exit("render_html: no Chrome/Chromium found. Install one or set CHROME=/path/to/browser.")


def run_until_written(cmd, out: Path, log, timeout: float = 120.0):
    """Run the browser. Some wrappers keep Chrome alive after the screenshot, so
    stop it once the output file exists and its size is stable."""
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=log, text=True)
    deadline = time.time() + timeout
    last_size = -1
    while time.time() < deadline:
        if proc.poll() is not None:
            if proc.returncode != 0:
                log.seek(0)
                sys.stderr.write(log.read()[-2000:])
            return proc.returncode
        if out.exists():
            size = out.stat().st_size
            if size > 0 and size == last_size:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                return 0
            last_size = size
        time.sleep(0.5)
    proc.kill()
    return "timeout"


def console_lines(log) -> list:
    log.seek(0)
    keep = ("CONSOLE", "Uncaught", "ERROR:CONSOLE")
    return [line.rstrip() for line in log if any(k in line for k in keep)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("out", help=".png for a screenshot, .pdf to print")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--scale", type=float, default=2.0, help="device scale factor (PNG only)")
    ap.add_argument("--hash", default="", help="URL fragment to open, without #")
    ap.add_argument("--wait-ms", type=int, default=1500, help="virtual time budget for fonts and JS")
    ap.add_argument("--console", action="store_true",
                    help="print browser console messages; exit 3 if a JS error is logged")
    args = ap.parse_args()

    src = Path(args.html).resolve()
    if not src.is_file():
        sys.exit("render_html: %s not found" % src)
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    url = src.as_uri() + ("#" + args.hash if args.hash else "")

    with tempfile.TemporaryDirectory() as profile:
        cmd = [find_chrome(), "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
               "--no-first-run", "--no-default-browser-check", "--user-data-dir=" + profile,
               "--window-size=%d,%d" % (args.width, args.height),
               "--virtual-time-budget=%d" % args.wait_ms]
        if args.console:
            cmd += ["--enable-logging=stderr", "--v=0"]
        if out.suffix.lower() == ".pdf":
            cmd += ["--no-pdf-header-footer", "--print-to-pdf=" + str(out), url]
        else:
            cmd += ["--force-device-scale-factor=%g" % args.scale, "--screenshot=" + str(out), url]
        if out.exists():
            out.unlink()
        with tempfile.TemporaryFile(mode="w+") as log:
            code = run_until_written(cmd, out, log)
            messages = console_lines(log) if args.console else []
    if not out.exists():
        sys.exit("render_html: render failed (exit %s)" % code)
    print("%s (%d bytes)" % (out, out.stat().st_size))
    for m in messages:
        print("console: " + m)
    if any("Uncaught" in m or "ERROR:CONSOLE" in m for m in messages):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
