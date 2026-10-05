# React Bits — back pocket (not the 115 MB zip)

**Use:** when choosing a visual for fleetscale.co. **Do not** merge the React Bits monorepo into `main`.

| Item | Where |
|------|--------|
| Zip (full playground) | `~/Downloads/react-bits-main.zip` (~115 MB, 2026-08-12, `c7109dc`) |
| TS+CSS sources only | `~/.grok/cache/react-bits-ts-default/` (~4 MB) — local read, not in git |
| Docs | https://www.reactbits.dev/ |
| Add one component | `npx shadcn@latest add @react-bits/<Name>-TS-CSS` then restyle to brand |
| License | MIT + Commons Clause — OK in FleetScale; do not resell the kit |

**FleetScale rule:** one signature motion per section. Hero is already the **video**. Do not stack another WebGL background on the first screen.

`umli/web` is **CSS**, not Tailwind — prefer **TS-CSS / JS-CSS** variants.

---

## Already in `umli/web/src/components`

| Bit | Live use (2026-08) |
|-----|-------------------|
| MetallicPaint | Second-hero liquid mark |
| Beams | Band above research |
| Threads | Copied; **not** on home (video replaced it) |
| Strands, BorderGlow | Avery `VoiceSession` only (voice off the landing) |
| ProfileCard, SpotlightCard, GlassSurface, BlurText, ShinyText, Magnet, Dock, ClickSpark, FadeContent, AnimatedList, GlareHover, ScrollReveal, SpecularButton, StarBorder | Copied, **unused** on the live page |

Prefer **activating or restyling** something already copied over adding a 20th Bit.

---

## Pocket catalog (pick by job)

### If the job is a **quiet institutional background**
Silk, SoftAurora, Threads, FloatingLines, Grainient, DarkVeil, LightRays, LineWaves, GradientWaves, WebThreads, Topography, DotField, DotGrid  
**Avoid on hero** while the video is the first visual.

### If the job is **metal / credit object** (same family as the card)
MetallicPaint (already), MoltenMetal, LiquidChrome, LiquidEther, Iridescence, Prism, SpecularButton  
**Don’t** put a second metal shader on the facility card.

### If the job is **type on the video / section titles**
BlurText, SplitText, ScrollReveal, ScrollFloat, GradientText, ShinyText, CountUp, TextType, TrueFocus  
**Avoid:** GlitchText, DecryptedText, ScrambledText, FuzzyText, ASCIIText — they read as hacker SaaS, not capital-grade.

### If the job is **a card or tile** (research, steps, about)
SpotlightCard, TiltedCard, PixelCard, BounceCards, Stack, ProfileCard, ReflectiveCard, DecayCard  
Resting state must stay **visible** (no opacity-0 until hover).

### If the job is **nav / chrome**
PillNav, CardNav, GooeyNav, StaggeredMenu, Dock, LineSidebar, BubbleMenu  
Only if we replace the current header — don’t add a second nav language.

### If the job is **cursor theater**
ClickSpark, Magnet, TargetCursor, BlobCursor, GhostCursor, SplashCursor, SwarmCursor, Crosshair  
**Default: no.** Fights a serious finance page.

### If the job is **scroll / section enter**
AnimatedContent, FadeContent, ScrollExpand, ScrollStack, ScrollReveal, GradualBlur, HalftoneReveal  
OK if `prefers-reduced-motion` is a hard cut.

---

## Full name index (from zip `src/ts-default/`)

**Animations:** AnimatedContent, Antigravity, BlobCursor, ClickSpark, Crosshair, Cubes, CursorGrid, ElasticMesh, ElectricBorder, FadeContent, GhostCursor, GlareHover, GradualBlur, HalftoneReveal, ImageTrail, LaserFlow, LogoLoop, MagicRings, Magnet, MagnetLines, MetaBalls, MetallicPaint, Noise, OrbitImages, PixelSwap, PixelTrail, PixelTransition, Ribbons, RippleDistortion, ScrollExpand, ShapeBlur, SplashCursor, StarBorder, StickerPeel, Strands, SwarmCursor, TargetCursor

**Backgrounds:** AcidSquares, Aurora, Balatro, Ballpit, Beams, ColorBends, DarkVeil, Dither, DotField, DotGrid, EvilEye, FaultyTerminal, Ferrofluid, FloatingLines, Galaxy, GradientBlinds, GradientWaves, Grainient, GridDistortion, GridMotion, GridScan, Hyperspeed, Iridescence, LetterGlitch, LightPillar, LightRays, LightTunnel, Lightfall, Lightning, LineWaves, LiquidChrome, LiquidEther, MoltenMetal, Orb, Particles, PixelBlast, PixelSnow, Plasma, PlasmaWave, Prism, PrismaticBurst, Radar, RippleGrid, Scanner, ShapeGrid, SideRays, Silk, SlicedWaves, SoftAurora, Threads, Topography, Waves, WebThreads

**Components:** AccordionGallery, AnimatedList, BorderGlow, BounceCards, BubbleMenu, CardNav, CardSwap, Carousel, ChromaGrid, CircularGallery, Counter, CurvedInput, DecayCard, DepthCarousel, Dock, DomeGallery, DriftWall, ElasticSlider, FlowingMenu, FluidGlass, FlyingPosters, Folder, GlassIcons, GlassSurface, GooeyNav, InfiniteMenu, Lanyard, LineSidebar, MagicBento, Masonry, ModelViewer, MorphSlider, OptionWheel, PillNav, PixelCard, ProfileCard, ReflectiveCard, ScrollStack, SpecularButton, SpotlightCard, Stack, StaggeredMenu, Stepper, TiltedCard

**Text:** ASCIIText, BlurText, CircularText, CountUp, CurvedLoop, DecryptedText, DepthText, EchoText, FallingText, FoldText, FuzzyText, GlitchText, GradientText, MaskedHeading, ParticleText, RotatingText, ScrambledText, ScrollFloat, ScrollReveal, ScrollVelocity, ShinyText, Shuffle, SplitFlapText, SplitText, StrokeText, TextCursor, TextLoop, TextPressure, TextType, TrueFocus, VariableProximity, WarpText

---

## Decision checklist before adding a Bit

1. What **job** does this do that copy/layout/video cannot?  
2. Is there already a copy in `web/src/components/`?  
3. Does it fight the hero video or the blue footer?  
4. Reduced-motion fallback?  
5. CSS variant (no Tailwind-only)?  
6. One per section?

If you cannot answer (1), do not add it.

*Catalog from react-bits-main.zip, Aug 2026. Not a vendor dump.*
