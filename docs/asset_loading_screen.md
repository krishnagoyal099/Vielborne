# ASSET SPEC: LOADING SCREEN
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The loading screen is the player's first impression of SHADOWSELF.  
It must immediately communicate: **dark, psychological, ritualistic, beautiful**.  
The player should feel mild unease before a single word of dialogue has appeared.

---

## SCENE COMPOSITION

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              [ECLIPSE SYMBOL]  ← top center         │
│                                                     │
│          S H A D O W S E L F                        │
│             [logo lettermark]                       │
│                                                     │
│      [silhouette rising from fog — center]          │
│                                                     │
│      ────────────[loading bar]────────────          │
│         "The mirror remembers everything."          │
│                                                     │
│                                     [v0.1]          │
└─────────────────────────────────────────────────────┘
```

---

## ELEMENT 1: SHADOWSELF LOGO

### Typography
- Font: **"Cinzel Decorative"** (Google Fonts) — serif, ancient-feeling
- Letter spacing: `0.35em`
- Style: All caps, stacked or inline
- Color: Pure white (`#FFFFFF`) with a subtle silver glow
- Glow: `text-shadow: 0 0 24px rgba(200, 180, 255, 0.7)`
- Size: `clamp(2.5rem, 6vw, 5rem)`

### Tagline (below logo)
- Text: *"Every shadow has a name."*
- Font: **"Cormorant Garamond"** Italic
- Color: `rgba(200, 180, 255, 0.6)`
- Size: `1rem`
- Letter spacing: `0.2em`

### Animation
- Logo fades in from `opacity: 0` over `2.5s`
- Each letter appears with a `0.08s` stagger (left to right)
- After full appearance: subtle breathing pulse — scale `1.0 → 1.005 → 1.0` every `4s`

---

## ELEMENT 2: ECLIPSE SYMBOL

### Shape
- A perfect circle (the sun) occluded by another circle (the moon)
- Renders as an SVG: outer ring in silver, inner dark disc in `#0a0a0f`
- Corona rays: 8 thin lines radiating outward, very faint silver

### Size
- `80px × 80px` centered above the logo

### Animation
- Slow rotation: `360deg` over `20s` linear, infinite
- Corona rays pulse opacity: `0.3 → 0.8 → 0.3` every `3s`
- On load complete: eclipse briefly flares bright white, then fades

### Color
- Outer ring: `#C0B0E0` (silver-purple)
- Dark disc: `#08080D`
- Corona: `rgba(255, 255, 255, 0.25)`

---

## ELEMENT 3: SILHOUETTE FIGURE

### Description
- A humanoid figure, perfectly black (`#000000`)
- Emerging upward from ground-level fog/mist
- Figure is featureless — no face, no details
- Proportions: tall and slightly elongated (eerie)
- Positioned: bottom-center of screen, rising to mid-center

### Fog / Mist Base
- Layered radial gradient at ground: `rgba(80, 40, 120, 0.4)` → transparent
- 2–3 CSS layers with slow drift animation (`translateX` ±20px over 8s)

### Animation Sequence
1. **Rise**: Figure translates from `translateY(60px)` to `translateY(0)` over `3s`, eased
2. **Dissolve edges**: Figure has soft feathered edges using CSS `mask-image` radial gradient
3. **Idle breath**: Subtle `scaleY(1.0 → 1.015 → 1.0)` loop every `5s`
4. **Parallax**: On mouse move, figure shifts ±5px (creates depth illusion)

### Visual Execution (CSS/SVG)
```css
.silhouette-figure {
  width: 180px;
  height: 340px;
  background: #000000;
  clip-path: url(#human-silhouette-path);
  mask-image: radial-gradient(ellipse 100% 90% at 50% 50%, black 60%, transparent 100%);
  filter: drop-shadow(0 0 30px rgba(120, 60, 200, 0.6));
  animation: silhouette-rise 3s cubic-bezier(0.22, 1, 0.36, 1) forwards,
             silhouette-breathe 5s ease-in-out 3s infinite;
}
```

---

## ELEMENT 4: ANIMATED LOADING BAR

### Container
- Width: `320px`, centered horizontally
- Height: `3px`
- Background: `rgba(255, 255, 255, 0.08)`
- Border: `1px solid rgba(200, 180, 255, 0.2)`
- Border radius: `2px`

### Fill Bar
- Color: Linear gradient — `#6B21A8` → `#A855F7` → `#E9D5FF`
- Animation: Fills left-to-right over the actual loading duration
- Glow: `box-shadow: 0 0 12px rgba(168, 85, 247, 0.8)`

### Loading Text
- Below the bar, centered
- Cycling messages (rotate every 1.5s):
  1. *"Summoning your shadow…"*
  2. *"Polishing the mirror…"*
  3. *"The darkness is listening…"*
  4. *"Preparing the ritual table…"*
  5. *"Your other self is waiting…"*
- Font: Cormorant Garamond, Italic, `0.85rem`, `rgba(200, 180, 255, 0.5)`

---

## ELEMENT 5: CINEMATIC SPLASH BACKGROUND

### Base Layer
- Full-screen dark background: `#06050D` (near-black, very slightly purple)

### Vignette Overlay
- Radial gradient: transparent center → `rgba(0,0,0,0.85)` edges
- Creates depth, focuses eye on center

### Ambient Particles
- 15–20 very small floating particles (`2px` circles)
- Color: `rgba(168, 85, 247, 0.4)`
- Slow upward drift with random horizontal wobble
- Each particle has `opacity: 0 → 0.6 → 0` cycle as it rises and disappears

### Subtle Grid
- Extremely faint radial grid lines (`rgba(255,255,255,0.02)`)
- Gives sense of a mystical coordinate space

---

## FULL ANIMATION TIMELINE

```
t=0.0s  Background fades in (black → #06050D)
t=0.5s  Eclipse symbol fades in + begins rotation
t=1.0s  Logo letters begin stagger reveal
t=2.5s  Logo fully visible; tagline fades in
t=3.0s  Silhouette begins rising from fog
t=4.0s  Loading bar appears + begins filling
t=4.5s  Loading text begins cycling
t=Xs    Loading complete → loading bar flare → transition to camera capture
```

---

## CSS IMPLEMENTATION NOTES

All animations implemented with CSS `@keyframes`.  
No heavy JS animation libraries.  
Use `will-change: transform, opacity` on animated elements.  
Total loading screen weight target: **< 50KB** (pure CSS/SVG, no images).

---

## COLOR TOKENS (LOADING SCREEN)

```css
--bg-deep:        #06050D;
--bg-void:        #000000;
--accent-purple:  #A855F7;
--accent-silver:  #C0B0E0;
--glow-purple:    rgba(168, 85, 247, 0.7);
--text-primary:   #FFFFFF;
--text-secondary: rgba(200, 180, 255, 0.6);
--text-muted:     rgba(200, 180, 255, 0.3);
```
