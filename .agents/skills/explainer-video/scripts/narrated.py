"""Manim helpers for narrated explainers: brand style and beat timing.

A scene subclasses NarratedScene and wraps each storyboard beat in
`with self.beat("id") as d:`. The block runs its animations, then the scene
waits until the narration for that beat ends. build_video.py writes the
narration timings before the render and reads the actual beat start times
after it, so the audio stays in sync even when an animation runs long.
"""

import json
import os
from contextlib import contextmanager

from manim import DOWN, RIGHT, Arrow, RoundedRectangle, Scene, Text, VGroup, config

# Tokens: replace with the project's brand tokens (see AGENTS.md).
INK = "#12141A"
PORCELAIN = "#F7F8FB"
BRAND = "#4F6CF7"
MUTED = "#8C92A4"
FAIL = "#E8634F"
PANEL = "#1B1E27"
SANS = os.environ.get("EXPLAINER_SANS", "Inter")
MONO = os.environ.get("EXPLAINER_MONO", "JetBrains Mono")

config.background_color = INK


def text(s, size=36, color=PORCELAIN, weight="NORMAL", font=None, **kw):
    return Text(s, font=font or SANS, font_size=size, color=color, weight=weight, **kw)


def mono(s, size=28, color=MUTED, **kw):
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def box(label, sub=None, width=3.2, height=1.25, color=PORCELAIN, fill=PANEL, accent=False, pad=0.22):
    """A labeled node: rounded rectangle, title, optional mono sub-label.
    Text shrinks to fit inside the box; it never spills over the border."""
    stroke = BRAND if accent else color
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.08,
                            stroke_color=stroke, stroke_width=3 if accent else 2,
                            fill_color=fill, fill_opacity=1)
    parts = [text(label, size=30, weight="SEMIBOLD")]
    if sub:
        parts.append(mono(sub, size=20))
    for part in parts:
        if part.width > width - 2 * pad:
            part.scale_to_fit_width(width - 2 * pad)
    content = VGroup(*parts).arrange(DOWN, buff=0.14)
    if content.height > height - 2 * pad * 0.6:
        content.scale_to_fit_height(height - 2 * pad * 0.6)
    content.move_to(rect)
    return VGroup(rect, *parts)


def arrow(a, b, color=MUTED, buff=0.12, **kw):
    return Arrow(a.get_right() if a.get_center()[0] < b.get_center()[0] else a.get_bottom(),
                 b.get_left() if a.get_center()[0] < b.get_center()[0] else b.get_top(),
                 buff=buff, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.12, **kw)


def caption(s, size=26):
    """Lower-third on-screen text. Keep it short; the narration carries detail."""
    return text(s, size=size, color=MUTED).to_edge(DOWN, buff=0.55)


def source_line(path):
    return mono("Source: " + path, size=18).to_corner(DOWN + RIGHT, buff=0.35)


class NarratedScene(Scene):
    """Base scene. Paces each beat to its narration length."""

    def setup(self):
        path = os.environ.get("EXPLAINER_TIMINGS", "")
        if path and os.path.exists(path):
            with open(path) as fh:
                self._timings = json.load(fh)
        else:
            self._timings = {"beats": {}, "lead_in": 0.4, "gap": 0.35, "tail": 1.2}
        self._actual = {}

    def beat_duration(self, beat_id, default=3.0):
        """Narration length of a beat in seconds (default when no timings exist)."""
        return float(self._timings["beats"].get(beat_id, {}).get("duration", default))

    @contextmanager
    def beat(self, beat_id):
        if not self._actual:
            lead = float(self._timings.get("lead_in", 0.4)) - self.time
            if lead > 0:
                self.wait(lead)
        start = self.time
        self._actual[beat_id] = {"start": round(start, 4)}
        yield self.beat_duration(beat_id)
        remaining = start + self.beat_duration(beat_id) + float(self._timings.get("gap", 0.35)) - self.time
        if remaining > 1 / config.frame_rate:
            self.wait(remaining)
        self._actual[beat_id]["end"] = round(self.time, 4)

    def tear_down(self):
        self.wait(float(self._timings.get("tail", 1.2)))
        out = os.environ.get("EXPLAINER_ACTUAL", "")
        if out:
            with open(out, "w") as fh:
                json.dump({"beats": self._actual, "end": round(self.time, 4)}, fh, indent=2)


__all__ = ["INK", "PORCELAIN", "BRAND", "MUTED", "FAIL", "PANEL", "SANS", "MONO", "text", "mono", "box",
           "arrow", "caption", "source_line", "NarratedScene"]
