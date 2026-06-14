# ASSET SPEC: BATTLE BACKGROUND
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The confrontation chamber is the void in which player and Shadow meet.  
It must feel **infinite, ancient, and psychologically pressurizing**.  
The player should feel small — but not powerless.

---

## SCENE COMPOSITION (LAYERED)

```
Layer 7 (top)   : Eclipse overhead — slow rotation
Layer 6         : Floating mirror shards — drifting
Layer 5         : Purple fog mid-level — volumetric drift
Layer 4         : Distant vertical mirror surfaces — parallax
Layer 3         : Ground fog — low-lying mist
Layer 2         : Void gradient — deep dark space
Layer 1 (base)  : Absolute black (#000000)
```

---

## LAYER 1: ABSOLUTE BLACK BASE

```css
.battle-bg-base {
  position: fixed;
  inset: 0;
  background: #000000;
  z-index: 0;
}
```

Nothing else. Pure void.

---

## LAYER 2: VOID GRADIENT

A very subtle radial gradient creating the sense of depth.  
Center is slightly lighter — where the ritual table sits.  
Edges bleed to absolute black.

```css
.battle-bg-void {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 80% 60% at 50% 55%,
    #130B1E 0%,
    #0C0714 40%,
    #07040F 70%,
    #000000 100%
  );
  z-index: 1;
}
```

---

## LAYER 3: GROUND FOG

Low-lying mist at the bottom 30% of the screen.  
Gives the impression that the floor is hidden.  
The table appears to float in mist.

### Visual Properties
- Height: covers bottom `35%` of viewport
- Color: `rgba(60, 20, 100, 0.3)` → transparent upward
- 3 independently moving fog planes (parallax depth)

### CSS
```css
.ground-fog {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 35%;
  background: linear-gradient(
    to top,
    rgba(60, 20, 100, 0.35) 0%,
    rgba(60, 20, 100, 0.15) 50%,
    transparent 100%
  );
  filter: blur(12px);
  animation: fog-drift-1 12s ease-in-out infinite alternate;
  z-index: 3;
}

@keyframes fog-drift-1 {
  0%   { transform: translateX(-3%) scaleX(1.05); opacity: 0.8; }
  100% { transform: translateX(3%) scaleX(0.97); opacity: 1.0; }
}
```

3 fog layers with different speeds (12s, 17s, 22s) and directions create volumetric depth.

---

## LAYER 4: DISTANT MIRROR SURFACES

4–6 large, vertically-oriented mirror surfaces visible in the background.  
These are not reflective (too expensive) — they are **dark glass panels** with faint, distorted light.

### Visual Design
- Rectangular panels, `10–25vw` wide, `60–90vh` tall
- Tilted at various angles: `rotate(±5°–±15°)`
- Positioned at varying depths (via `opacity` and `scale`)
- Background mirror color: `rgba(20, 10, 40, 0.8)` with silver edge: `1px solid rgba(200, 180, 255, 0.15)`
- Internal glow: very faint purple radial from center of each panel

### Parallax Motion
On mouse move, each mirror plane shifts at a different rate (`0.5%` to `2%` of mouse delta).  
Creates sense of infinite depth.

### CSS
```css
.bg-mirror-panel {
  position: absolute;
  background: rgba(20, 10, 40, 0.8);
  border: 1px solid rgba(200, 180, 255, 0.12);
  box-shadow:
    inset 0 0 40px rgba(80, 40, 140, 0.15),
    0 0 20px rgba(80, 40, 140, 0.1);
  border-radius: 2px;
  transform-origin: center;
}

/* Example panel positions */
.mirror-panel-1 { width: 18vw; height: 75vh; left: 5vw;  top: 10vh; transform: rotate(-8deg);  opacity: 0.45; }
.mirror-panel-2 { width: 14vw; height: 60vh; left: 12vw; top: 18vh; transform: rotate(3deg);   opacity: 0.3; }
.mirror-panel-3 { width: 22vw; height: 85vh; right: 6vw; top: 5vh;  transform: rotate(10deg);  opacity: 0.5; }
.mirror-panel-4 { width: 12vw; height: 55vh; right: 15vw; top: 20vh; transform: rotate(-5deg); opacity: 0.25; }
```

---

## LAYER 5: PURPLE FOG — MID-LEVEL

This is the defining visual of the confrontation chamber.  
Rich, volumetric purple fog fills the middle of the scene.

### Visual Properties
- Vertical position: `20%–70%` of viewport height
- Color: Rich violet-purple — `rgba(80, 20, 140, 0.25)`
- Not a solid shape — rendered as multiple overlapping radial gradients

### Multiple Fog Clouds
Create 5–8 large radial gradient circles (SVG or CSS):
- Sizes: `200px–500px` radius
- Positions: Random within the mid-level zone
- Each drifts independently (slow translate, 15–25s periods)
- Opacity: `0.1–0.3` each

```css
.fog-cloud {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  pointer-events: none;
  mix-blend-mode: screen;
}

.fog-cloud-1 {
  width: 400px; height: 300px;
  background: radial-gradient(ellipse, rgba(100, 30, 180, 0.25) 0%, transparent 70%);
  top: 25%; left: 15%;
  animation: fog-float-1 20s ease-in-out infinite alternate;
}

@keyframes fog-float-1 {
  0%   { transform: translate(0, 0) scale(1.0); }
  100% { transform: translate(40px, -20px) scale(1.1); }
}
```

---

## LAYER 6: FLOATING MIRROR SHARDS

12–18 small mirror fragments drifting very slowly upward.  
These are the most visually distinctive element of the battle background.

### Individual Shard Design
- Irregular polygon shapes (3–8 sides, generated via SVG `points`)
- Size: `15px–60px` (variety)
- Fill: `rgba(20, 10, 40, 0.9)` (dark glass)
- Stroke: `rgba(200, 180, 255, 0.4)` (silver edge), 1px
- Internal glint: a single bright pixel or tiny highlight line

### Shard Motion
Each shard has a unique:
- Starting position (random across full screen)
- Drift speed (upward, `0.2px–0.8px/frame equivalent`)
- Horizontal wobble (`±10px` oscillation over `8–15s`)
- Slow rotation (`±180deg` over `15–30s`)
- Opacity: `0.3–0.7`

When shard exits top of screen, it teleports to bottom (infinite loop).

### Reflection Glint
On each shard, a tiny animated highlight sweeps across once every `10–20s`:  
A 1px white `linear-gradient` sweeps from one corner to the opposite corner.

```css
.mirror-shard {
  position: absolute;
  clip-path: polygon(/* random polygon */);
  background: rgba(20, 10, 40, 0.9);
  outline: 1px solid rgba(200, 180, 255, 0.35);
  filter: drop-shadow(0 0 4px rgba(140, 100, 200, 0.4));
  animation: shard-float var(--duration) ease-in-out infinite;
}

@keyframes shard-float {
  0%   { transform: translateY(0) rotate(0deg) translateX(0); }
  50%  { transform: translateY(calc(var(--rise) * -0.5)) rotate(calc(var(--spin) * 0.5)) translateX(var(--wobble)); }
  100% { transform: translateY(var(--rise)) rotate(var(--spin)) translateX(0); }
}
```

---

## LAYER 7: ECLIPSE OVERHEAD

The same eclipse from the loading screen persists during battle.  
It is positioned at the **very top center** of the battle screen.

### Size
- Smaller than loading screen version: `60px × 60px`
- Slightly dimmed: `opacity: 0.7`

### Behavior
- Continues slow rotation from loading screen (no reset)
- Glow intensifies when Shadow attacks: `filter: brightness(1.5)` for `0.3s`
- On player victory: eclipse becomes a full circle (no longer occluded) — a moment of wholeness
- On player defeat: eclipse goes dark (no glow) — a moment of loss

---

## DYNAMIC EVENTS (BATTLE-TRIGGERED)

### Event: SHADOW ATTACKS
1. All fog layers darken momentarily: `brightness(0.6)` for `0.4s`
2. Mirror panels flash with brief reflected light
3. Eclipse flares

### Event: PLAYER TAKES LETHAL DAMAGE
1. Background flashes dark red-purple for `0.5s`
2. All mirror shards freeze, then slowly sink downward
3. Ground fog surges upward

### Event: PLAYER WINS
1. All fog layers disperse: `opacity: 0` over `3s`
2. Mirror shards drift away faster, off-screen
3. Background lightens to `#1A1030` (still dark, but warmer)
4. Eclipse becomes full circle, glows gold-white

### Event: PLAYER LOSES
1. Background collapses to pure black
2. Ground fog surges to full-screen
3. Eclipse goes dark
4. Slow fade to black before ending screen

---

## PERFORMANCE BUDGET

| Element | Technique | Target |
|---|---|---|
| Void gradient | CSS gradient | 0ms |
| Ground fog | CSS gradient + blur | < 1ms |
| Mirror panels | CSS + mild blur | < 2ms |
| Purple fog clouds | CSS radial + blur | < 3ms |
| Mirror shards (16) | CSS clip-path + animation | < 5ms |
| Eclipse | SVG + CSS | < 1ms |
| **Total** | | **< 12ms GPU** |

Use `will-change: transform` on animated elements.  
Prefer `transform` and `opacity` for animations (GPU composited).  
Never animate `width`, `height`, `top`, `left`, `background`.

---

## COLOR PALETTE

```css
/* Battle Background */
--void-black:       #000000;
--void-deep:        #07040F;
--void-mid:         #130B1E;
--fog-purple:       rgba(80, 20, 140, 0.25);
--fog-violet:       rgba(100, 30, 180, 0.20);
--mirror-panel-bg:  rgba(20, 10, 40, 0.85);
--mirror-panel-edge: rgba(200, 180, 255, 0.15);
--shard-bg:         rgba(20, 10, 40, 0.90);
--shard-edge:       rgba(200, 180, 255, 0.4);
--ground-fog:       rgba(60, 20, 100, 0.35);
```
