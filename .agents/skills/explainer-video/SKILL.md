---
name: explainer-video
description: >
  Make a short, narrated explainer video in the 3Blue1Brown style: a Manim
  animation, a TTS voice-over (Speechify with the GlassTalk voice first, then
  Fish Audio, ElevenLabs, or free local Kokoro / Piper), soft captions, and a
  frame contact sheet to check it. Use when an idea
  unfolds in time (cause and effect, an algorithm, a pipeline, a transform); when
  the reader is new or passive (onboarding, a pitch, a link to share); when the
  user asks for an explainer video, an animation, a "3b1b style" video, or
  narration; or when the format router picks step 3. Also /explainer-video.
---

# Explainer video

A video is a view of a text brief. The brief stays the source of truth
(`explainer-format-router`). The storyboard narration comes from the brief, and
each frame shows only facts that the brief states.

## Pipeline

```
brief.md → storyboard.json (beats: id + say) → TTS per beat → timings.json
        → scene.py (Manim, one `with self.beat(id)` block per beat) → render
        → narration placed at the actual beat starts → captions.srt → video.mp4
        → contact.png (one frame per beat) + report.json → you check it
```

`scripts/build_video.py` runs all of it. Each beat lasts as long as its
narration. If an animation runs long, the audio moves with the beat, so the
picture and the voice stay in sync.

## Setup (once per machine)

```bash
bash <skill>/scripts/setup.sh          # ffmpeg, Cairo, Pango, venv ~/.venvs/explainer, Manim, Kokoro
python3 <skill>/scripts/tts.py --list  # shows which voice provider "auto" picks
```

`<skill>` is this folder: `.agents/skills/explainer-video` in the repo, or
`~/.cursor/skills/explainer-video` for a user install. The scripts switch to the
venv when the current Python has no Manim.

## Voice

The first choice is the voice of JP's GlassTalk dashboard: Speechify, model
`simba-3.2`, voice `geffen_32`. `--provider auto` uses the first provider that
works:

| Order | Provider | Needs | Notes |
|-------|----------|-------|-------|
| 1 | Speechify | `SPEECHIFY_API_KEY`, optional `SPEECHIFY_VOICE_ID` (`geffen_32`), `SPEECHIFY_MODEL` (`simba-3.2`) | The GlassTalk voice. A speed other than 1.0 goes through SSML `<prosody rate>`. |
| 2 | Fish Audio | `FISH_API_KEY`, optional `FISH_REFERENCE_ID`, `FISH_MODEL` | The Avery voice stack in this repo uses Fish. |
| 3 | ElevenLabs | `ELEVENLABS_API_KEY`, optional `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID` | Sends the text before and after each beat for a smooth flow. |
| 4 | Kokoro (local, free) | `kokoro-onnx` + model files (setup.sh) | Default voice `af_heart`. Set `KOKORO_VOICE` to change it. CPU is enough. |
| 5 | Piper (local, free) | `piper` CLI + `PIPER_MODEL=/path/voice.onnx` | Fast and small. |
| 6 | espeak-ng | `espeak-ng` binary | Robotic. Use it only for a timing draft. |

To force one provider, pass `--provider <name>` to `build_video.py` or
`tts.py`, or set `"provider"` in the storyboard `voice` block. If the forced
provider is not available, the build stops and names the missing key.

Fish emotion tags such as `[calm]` go to Fish only. The script removes them for
the other providers.

### Keys

- Keys come from the environment. Never put a key in a storyboard, a script, a
  commit, a chat, or a log.
- On JP's Mac, the Speechify key is in `~/umli/customer-voice-agent/.env`.
  Load it into the build process with `--env-file`. Do not copy the file or its
  value anywhere:

  ```bash
  python3 <skill>/scripts/build_video.py storyboard.json --env-file ~/umli/customer-voice-agent/.env
  python3 <skill>/scripts/tts.py --env-file ~/umli/customer-voice-agent/.env --list
  ```

- `--env-file` (or `EXPLAINER_ENV_FILE`) reads only `SPEECHIFY_*`, `FISH_*`,
  `ELEVENLABS_*`, and `XI_API_KEY`. A variable that your shell already has
  keeps its value. The script prints the names of the keys that it loads,
  never the values.
- That `.env` file is inside the `~/umli` checkout, and the repo has no
  `.gitignore`. Stage files by name. Do not use `git add -A` there.
- For Cloud Agents, add `SPEECHIFY_API_KEY` as a secret (Cursor Dashboard →
  Cloud Agents → Secrets).
- To check the API code without a key, run
  `python3 <skill>/scripts/selftest_tts.py`. It tests the Speechify, Fish, and
  ElevenLabs requests against mocked HTTP.

## Storyboard rules

- 3 to 8 beats. One idea in each beat. A good length is 20 to 90 seconds.
- Narration speed is about 150 words per minute. 30 seconds is about 75 words.
- Write each `say` in plain writing (`explainer-plain-writing`). The build lints
  the storyboard first. Use `--strict-lint` to stop on a fail.
- `say` is the text of record: the lint and the captions use it. Add an optional
  `speak` to change only the pronunciation (for example `"speak": "fleetscale
  dot co"`). Keep the two the same in meaning.
- Keep on-screen text short (8 words or fewer for each line). The voice carries
  the detail, and the screen carries the structure.
- The last beat says what the viewer must do, or what to remember. The end
  frame names the brief path (`source_line("brief.md")`).

## Scene rules (3b1b style)

- Dark ink background, porcelain text, one brand accent, one fail color. Use
  the project's brand tokens (`narrated.py` holds FleetScale defaults).
- Build the picture step by step. Move objects to show change. Do not cut.
  `Transform`, `FadeIn(shift=...)`, `GrowArrow`, `Create`, and `LaggedStart`
  are the main tools.
- One motion at a time leads the eye. Keep the camera still.
- Keep the animations in a beat shorter than its narration `d`
  (`run_time=min(2, d * 0.6)`).
- Use `Text`, not `Tex` or `MathTex`, unless the machine has LaTeX.

Helpers in `scripts/narrated.py`: `NarratedScene`, `box`, `arrow`, `text`,
`mono`, `caption`, `source_line`, and the color tokens.

## Workflow

1. Write the brief. Lint it.
2. Copy the templates next to the brief:
   `cp <skill>/assets/storyboard.example.json <topic>/storyboard.json`
   `cp <skill>/assets/scene_template.py <topic>/scene.py`
3. Write the beats in `storyboard.json`.
4. Write one `with self.beat("<id>") as d:` block for each beat in `scene.py`.
5. Make a fast draft: `python3 <skill>/scripts/build_video.py <topic>/storyboard.json --quality draft`
6. Open `build/contact.png`. Tile *i* is the last frame of beat *i*. Compare
   each tile with the beat text and the brief.
7. Read the beat table in the output. Fix any "long pause" or "audio overruns
   beat" rows.
8. Make the final video (1080p, 30 fps): run the same command without
   `--quality draft`.
9. Check the final file. Open the contact sheet again. Confirm the duration
   and the audio stream (`ffprobe video.mp4`).

The build caches the audio for each beat. A change to one line synthesizes only
that beat again.

## Checks

- [ ] Each spoken and on-screen fact is in the brief.
- [ ] The storyboard passes the lint.
- [ ] Each contact-sheet tile shows what its beat says.
- [ ] All text is fully visible. No text overlaps other objects.
- [ ] The beat table has no "long pause" or "audio overruns beat" rows.
- [ ] The file has video, audio, and caption streams.
- [ ] The end frame names the brief path.
- [ ] If the video is for people outside the team, a human reviews it first.

## Red flags

- A video for a fact that changes every week. Use text or a sheet.
- A long voice-over on a static frame. Use a sheet.
- Visual effects that do not explain anything.
- You did not look at the contact sheet.

## Related

- `explainer-format-router` — when to make a video
- `explainer-plain-writing` — the narration rules and the lint
- `quality-first-authorship` — a video for a fixed public surface needs a human
  take or review (FleetScale repo)
