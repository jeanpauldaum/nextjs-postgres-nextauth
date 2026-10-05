#!/usr/bin/env bash
# Install the explainer-video toolchain: ffmpeg, Cairo/Pango (for Manim), and a
# Python venv with Manim + Kokoro TTS. Safe to run again.
#
#   setup.sh                 # system packages + venv + Kokoro model files
#   setup.sh --no-system     # skip apt/brew (packages already installed)
#   setup.sh --no-kokoro     # skip the local TTS (you use Speechify, Fish, or ElevenLabs)
#
# Venv path: $EXPLAINER_VENV (default ~/.venvs/explainer).
set -euo pipefail

VENV="${EXPLAINER_VENV:-$HOME/.venvs/explainer}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM=1
KOKORO=1
for arg in "$@"; do
  case "$arg" in
    --no-system) SYSTEM=0 ;;
    --no-kokoro) KOKORO=0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

if [ "$SYSTEM" = 1 ]; then
  if command -v apt-get >/dev/null 2>&1; then
    SUDO=""; [ "$(id -u)" != 0 ] && SUDO="sudo"
    $SUDO apt-get update -qq
    $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
      ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-dev python3-venv
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg cairo pango pkg-config
  else
    echo "Install ffmpeg, Cairo, Pango, and pkg-config with your package manager, then run: $0 --no-system" >&2
    exit 1
  fi
fi

command -v ffmpeg >/dev/null || { echo "ffmpeg is still missing" >&2; exit 1; }

if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q manim
if [ "$KOKORO" = 1 ]; then
  "$VENV/bin/pip" install -q kokoro-onnx soundfile
  "$VENV/bin/python" "$HERE/tts.py" --download-kokoro
fi

"$VENV/bin/python" -c "import manim; print('manim', manim.__version__)"
"$VENV/bin/python" "$HERE/tts.py" --list
echo "ready: $VENV"
