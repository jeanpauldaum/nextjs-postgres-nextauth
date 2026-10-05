"""Narrated explainer scene. Copy next to storyboard.json and edit construct().

Each `with self.beat("<id>") as d:` block matches one storyboard beat. `d` is
the narration length in seconds. Keep the animations in a block shorter than
`d`; the scene then waits until the narration for the beat ends.

Build: python3 <skill>/scripts/build_video.py storyboard.json
"""

from manim import (DOWN, LEFT, RIGHT, UP, Create, CurvedArrow, FadeIn, FadeOut, GrowArrow, Indicate,
                   LaggedStart, VGroup, Write)
from narrated import BRAND, FAIL, NarratedScene, arrow, box, caption, mono, source_line, text


class Explainer(NarratedScene):
    def construct(self):
        with self.beat("text") as d:
            brief = box("Brief", "brief.md", accent=True).shift(LEFT * 4)
            title = text("Text first, views second", size=40, weight="SEMIBOLD").to_edge(UP, buff=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(brief, shift=UP * 0.2), run_time=1.0)
            cap = caption("The text is the source of truth")
            self.play(FadeIn(cap), run_time=min(0.8, d / 4))

        with self.beat("views") as d:
            views = VGroup(box("Sheet", "sheet.png"), box("Page", "page.html"), box("Video", "video.mp4"))
            views.arrange(DOWN, buff=0.4).shift(RIGHT * 2.6 + DOWN * 0.3)
            arrows = VGroup(*[arrow(brief, v) for v in views])
            self.play(FadeOut(cap), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(v, shift=RIGHT * 0.2) for v in views], lag_ratio=0.2),
                      run_time=min(2.4, d * 0.6))

        with self.beat("check") as d:
            marks = VGroup(*[mono("\u2713", size=40, color=BRAND).next_to(v, RIGHT, buff=0.35) for v in views])
            cap = caption("Compare each label and number with the text")
            self.play(LaggedStart(*[Write(m) for m in marks], lag_ratio=0.3), FadeIn(cap),
                      run_time=min(1.8, d * 0.5))

        with self.beat("fix") as d:
            wrong = mono("\u2715", size=40, color=FAIL).move_to(marks[0])
            back = CurvedArrow(views[0].get_top() + UP * 0.05, brief.get_top() + UP * 0.05, angle=0.9, color=FAIL)
            fix_cap = caption("Fix the text first, then make the view again")
            self.play(FadeOut(marks[0]), FadeIn(wrong), views[0][0].animate.set_stroke(FAIL),
                      FadeOut(cap), FadeIn(fix_cap), run_time=0.6)
            self.play(Create(back), Indicate(brief, color=BRAND), run_time=min(1.4, d * 0.35))
            self.play(FadeOut(wrong), FadeIn(marks[0]), views[0][0].animate.set_stroke("#F7F8FB"),
                      FadeOut(back), FadeIn(source_line("brief.md")), run_time=0.8)
