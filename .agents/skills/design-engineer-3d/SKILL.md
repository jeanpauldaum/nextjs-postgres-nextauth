---
name: design-engineer-3d
description: >
  Ship 3D/glTF on the web for design-engineer surfaces: gltfjsx, gltfpack,
  performance budgets, posters for reduced-motion, Rive/Spline boundaries.
  Use when adding 3D heroes, product viewers, or /design-engineer-3d /gltf.
---

# Design Engineer 3D — Shipping 3D on Marketing Sites

Catalog origin: [designengineer.tools](https://designengineer.tools/) **3D** + **glTF** (+ volumetric capture is offline content, not runtime default).

**Core principle:** 3D is progressive enhancement. The page must work and look intentional as a **static poster** first.

## When 3D is worth it

| Yes | No |
|-----|-----|
| Product is spatial / hardware / robot | Pure SaaS form UI |
| One hero viewer with poster fallback | Full-page WebGL on every route |
| Budget for perf QA on mid-tier mobile | “Looks cool” only |
| User can opt into orbit/configurator | Essential facts only after orbiting |

## Decision: which tool?

| Need | Prefer | Avoid |
|------|--------|--------|
| React product hero, configurator, clickable meshes | **Blender → glTF → gltfjsx + R3F** | Raw unoptimized GLB in `useGLTF` |
| Designer-owned interactive campaign scene | **Spline** (paid: no watermark / code export) | Spline when you need full mesh control in code |
| Stateful 2D / faux-3D UI motion | **Rive** | Full WebGL for micro-interactions |
| Linear marketing loop | Video/WebM or Lottie | Three.js |
| Inspect / share / progressive-host glTF | **Needle Viewer** / Needle Cloud | Emailing multi-MB source files |
| Geometry + texture size / GPU-ready glTF | **gltfpack** (± gltfjsx `--transform`) | Shipping Sketchfab dumps as-is |

```
True 3D (orbit, PBR, multi-mesh)?
  yes → designer-speed → Spline
        code control → Blender + gltfjsx
  no  → state machines → Rive
        linear loop → video / Lottie
```

---

## Tool reference

### gltfjsx — [pmndrs/gltfjsx](https://github.com/pmndrs/gltfjsx)

Turns GLB/glTF into a **declarative react-three-fiber JSX graph** (nodes + materials as props). Fixes whole-scene mount, traversal, mutation, and no-reuse.

**Use when:** React/Next + R3F; per-mesh events, material swaps, typed nodes, multi-instance reuse.  
**Skip when:** non-React (use `GLTFLoader`, `<model-viewer>`, Needle, Spline viewer).

```bash
npx gltfjsx model.glb --transform --types   # JSX + web-ready copy (often 70–90% smaller)
npx gltfjsx model.glb -T -t -k              # keep names for animations / external control
npx gltfjsx model.glb -T -i                 # instance repeated geometry
```

| Flag | Effect |
|------|--------|
| `-T` / `--transform` | Draco + prune + resize textures (default 1024) + WebP; writes `*-transformed.glb` via glTF-Transform |
| `-t` / `--types` | TypeScript `GLTFResult` |
| `-k` / `--keepnames` | Preserve node names |
| `-i` / `-I` | Instance recurring / all geometry |
| `-R` | Texture max edge (try 512 for secondary assets) |
| `-S` | Mesh simplification (careful on heroes) |

Web UI: [gltf.pmnd.rs](https://gltf.pmnd.rs/). Runtime: `three` ≥ r122, `@react-three/fiber`, `@react-three/drei`. Cap `dpr={[1, 1.5]}`; `useGLTF.preload` only for true ATF heroes.

### gltfpack — [meshoptimizer.org/gltf](https://meshoptimizer.org/gltf/)

CLI rewrite for smaller download + faster GPU: vertex-cache optimize, quantize, merge, prune, meshopt codecs, KTX2/WebP, simplify. Prefer **native binary** over npm for large files + texture compression.

```bash
gltfpack -i scene.glb -o scene.opt.glb                 # quantize (KHR_mesh_quantization)
gltfpack -i scene.glb -o scene.meshopt.glb -cc         # meshopt; needs MeshoptDecoder
gltfpack -i scene.glb -o scene.ktx.glb -cc -tc         # + KTX2 BasisU textures
gltfpack -i scene.glb -o scene.opt.glb -cc -kn -km     # keep named nodes/materials
gltfpack -i scene.glb -o scene.lod.glb -cc -si 0.5     # ~50% triangles
```

| Flag | Notes |
|------|--------|
| `-c` / `-cc` | `EXT_meshopt_compression`; `-cc` better + gzip-friendly |
| `-cz` | Stronger `KHR_meshopt_compression` |
| `-tc` / `-tw` | KTX2 BasisU / WebP textures |
| `-si R` | Simplify to ratio R |
| `-kn` / `-km` | Keep named nodes / materials |
| `-mi` | GPU instancing when meshes repeat |

three.js: `loader.setMeshoptDecoder(MeshoptDecoder)`. Serve with **gzip/brotli**.

**vs gltfjsx `-T`:** gltfpack = geometry/GPU + meshopt/KTX2; gltfjsx `-T` = glTF-Transform (Draco/WebP) **+** React component. Prefer **one** transform pass; verify visual parity if chaining.

### Needle Viewer — [viewer.needle.tools](https://viewer.needle.tools/)

Inspect/share glTF; Needle Cloud hosts/optimizes; `@needle-tools/gltf-progressive` streams LODs (multi‑MB → hundreds of KB first paint). Use for QA and progressive product pages—not mandatory lock-in if you own R3F.

### Spline — [spline.design](https://spline.design/) (commercial)

Browser 3D + events/states. Ship via `<spline-viewer>`, React, Webflow/Framer.

**Commercial (verify [pricing](https://spline.design/pricing)):** Free = limited files + **watermarked** web exports; Starter (~$12/seat/mo annual) = unlimited files, **no watermark**; Professional (~$20) = code/mobile exports, variables/APIs; Enterprise = self-host/SSO.

Perf: one scene max on a landing page; lazy-load; poster; dpr cap; test mobile GPU.

### Blender — [blender.org](https://www.blender.org/)

Canonical free authoring. Export checklist: apply scale → controlled polycount → join same-material meshes when no picks needed → bake normals/ORM → **glTF 2.0 Binary (.glb)** → name animatable nodes → **gltfpack** and/or **gltfjsx -T**.

### Rive — [rive.app](https://rive.app/)

Interactive **vector/state-machine** runtimes (not glTF). Prefer for mascots, feature explainers, toggles, scroll-driven 2D. Lottie = linear loops; Rive = stateful interaction. Neither replaces compressed glTF for real PBR/orbit.

---

## Performance budgets (marketing)

### File size (over the wire, compressed)

| Role | Target | Soft ceiling |
|------|--------|--------------|
| Icon / accent | ≤ 300 KB | 500 KB |
| Secondary section | ≤ 1–2 MB | 3 MB |
| Hero product | ≤ 2–4 MB | ~5–6 MB with meshopt/KTX2 |
| Configurator / high-detail PDP | ≤ 6–10 MB | ~15 MB only with progressive/LOD |

### Runtime

| Metric | Target |
|--------|--------|
| First meaningful 3D frame | ≤ 3 s mid mobile (or poster earlier) |
| Canvas DPR | `1` low-end; max `1.5`–`2` desktop |
| Lights / shadows | 0–2 lights; shadows off or one cheap |
| WebGL contexts | **One** per page |
| Offscreen | Pause render loop |

### Loading

1. Poster (AVIF/WebP) from first paint; reserve `aspect-ratio`  
2. Lazy-mount Canvas (IntersectionObserver or “View 3D” click)  
3. Dynamic-import three/R3F so JS doesn’t block TTI  
4. Preload only true ATF heroes after critical CSS/fonts  
5. Progressive/LOD for >3 MB assets  
6. CDN + brotli/gzip for `.glb`

**CWV:** LCP should be poster or HTML text—not a late WebGL frame. Cap INP (debounce controls). Zero CLS via fixed aspect box.

---

## Accessibility: reduced motion + static poster

1. Always ship a **static poster** (same framing as default camera)  
2. `prefers-reduced-motion: reduce` → **no autoplay** spin/parallax; show poster  
3. Optional accessible “View 3D” / “Show photo” control  
4. Decorative canvas: `aria-hidden="true"`; real content in DOM  
5. Meaningful product view: alt text / adjacent description + non-WebGL path  
6. Don’t make essential info hover-only orbit  

```tsx
// Poster-first: mount Scene only when user enables AND motion is OK
const show3D = active && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
```

Also pause Spline/Rive autoplay under reduced motion (or don’t mount).

---

## Recommended pipelines

**A. Owned brand product (default)**  
Blender → `.glb` → `gltfpack -cc -tc` (or `gltfjsx -T`) → `gltfjsx -t -k` → R3F + poster + reduced-motion → lazy dynamic import; dpr cap; one light.

**B. Designer-led campaign**  
Spline (paid if no watermark) → poster from same camera → lazy viewer → reduced-motion → poster only.

**C. Interactive illustration (not mesh 3D)**  
Rive state machine → web runtime → still hold idle state on reduced motion.

---

## Agent procedure

1. Prefer **static image / video** if engagement is equal  
2. If 3D: export **glTF/GLB**, run **gltfpack** (and/or gltfjsx `-T`), generate **gltfjsx** if R3F  
3. Lazy-load canvas; intersection observer or intent mount  
4. **Poster** + hide/skip canvas when `prefers-reduced-motion`  
5. Cap draw calls / polycount / dpr; test mid-tier mobile  
6. Confirm commercial license (Spline plan, model license)

## Red flags — stop before ship

- Raw 20–100 MB GLB in `/public`  
- Auto-rotating hero, no poster, no reduced-motion path  
- Multiple full WebGL scenes on one landing page  
- Shadows + bloom + 4k textures on mobile hero  
- Spline free watermark on production  
- gltfjsx without `-T` / gltfpack on multi‑MB source  
- LCP is a blank canvas waiting on WASM decoder  
- Essential product facts only after orbiting  
- Uncompressed Spline dump; 3D text for body copy  

## Slash

`/design-engineer-3d` · `/gltf`
