# ASSET SPEC: MIRROR TABLE
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The mirror table is the ritual space.  
It is not a "game board." It is a **sacred object** — a surface where memory and reality intersect.  
Every card placement must feel like a gesture in a ritual.

---

## OVERVIEW COMPOSITION

```
╔═══════════════════════════════════════════════════════════════╗
║  [SHADOW PORTRAIT]     SHADOW HP ████████░░   ENERGY: ◆◆◆    ║
║                                                               ║
║  ┌─────────────────────────────────────────┐                  ║
║  │         SHADOW CARD ZONE  [3 slots]     │   ← Shadow side  ║
║  │    ┌───┐  ┌───┐  ┌───┐                 │                  ║
║  │    │   │  │   │  │   │                 │                  ║
║  │    └───┘  └───┘  └───┘                 │                  ║
║  │─────────────────────────────────────────│                  ║
║  │         [MIRROR TABLE SURFACE]          │   ← center       ║
║  │─────────────────────────────────────────│                  ║
║  │    ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  │                  ║
║  │    │   │  │   │  │   │  │   │  │   │  │                  ║
║  │    └───┘  └───┘  └───┘  └───┘  └───┘  │                  ║
║  │         PLAYER CARD ZONE  [5 slots]    │   ← Player side  ║
║  └─────────────────────────────────────────┘                  ║
║                                                               ║
║  [Player HAND — 5 cards, bottom]     ENERGY: ◆◆◆  HP: ████   ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## TABLE SURFACE DESIGN

### Shape
- Elliptical / circular — appears round from a slightly overhead perspective (15° tilt)
- CSS `border-radius: 50%` with `perspective` and `rotateX(15deg)` to create 3D illusion
- Width: `90%` of available battle area
- The table edge has a subtle silver border: `border: 2px solid rgba(192, 180, 220, 0.4)`

### Surface Material: Reflective Black Glass

```css
.mirror-table {
  background:
    radial-gradient(ellipse at 50% 20%, rgba(80, 40, 120, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 50% 80%, rgba(40, 20, 80, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, #0D0A14 0%, #08060F 40%, #0D0A14 100%);
  border: 2px solid rgba(192, 180, 220, 0.35);
  box-shadow:
    inset 0 0 60px rgba(120, 60, 200, 0.08),
    0 0 80px rgba(60, 20, 120, 0.4),
    0 4px 40px rgba(0,0,0,0.8);
  position: relative;
  overflow: hidden;
}
```

### Reflection Layer
A faint, inverted duplicate of the card zone (CSS `scaleY(-1)`, `opacity: 0.08`) gives the illusion of the table being a reflective surface.

---

## CRACK SYSTEM: MEMORIES REVEALED

### Crack Behavior
- Cracks appear when Shadow takes damage
- Each crack is a unique SVG path (pre-generated set of 8 crack patterns, randomly selected)
- Cracks do NOT disappear — they accumulate across the battle
- At the final blow, ALL cracks flash simultaneously

### Crack Anatomy

```
       ╲      /
        ╲    /
    ─────╲──/──────
          \/
          /╲
         /  ╲
```

Each crack:
1. Appears instantly at a random table position
2. A faint **memory flash** appears inside the crack (brief white flash with a faint image beneath)
3. The crack itself glows faintly purple from within

### Memory Flashes
The "memory" appearing in cracks is a visual artifact — not real player photos.  
Render as: a white rectangular flash, `opacity: 0 → 0.4 → 0` over `0.8s`, `filter: blur(3px)`.  
This implies memory without displaying actual images (privacy/simplicity).

### CSS
```css
.table-crack {
  position: absolute;
  pointer-events: none;
  z-index: 5;
  stroke: rgba(192, 180, 255, 0.6);
  stroke-width: 1.5px;
  filter: drop-shadow(0 0 4px rgba(140, 100, 255, 0.8));
  animation: crack-appear 0.2s ease-out forwards;
}

@keyframes crack-appear {
  from { opacity: 0; stroke-dashoffset: 100%; }
  to   { opacity: 1; stroke-dashoffset: 0%; }
}
```

---

## CARD PLACEMENT SLOTS

### Player Side (5 slots)

```
[  S1  ]  [  S2  ]  [  S3  ]  [  S4  ]  [  S5  ]
   ↑           ↑           ↑          ↑           ↑
  52×80px   active slot zones — cards dragged here
```

- Slot inactive state: faint border `rgba(192, 180, 255, 0.15)`, dashed
- Slot hover state: border brightens to `rgba(192, 180, 255, 0.5)`, soft glow
- Slot occupied state: card renders in slot, slot border solid

### Shadow Side (3 slots)

- 3 slots, centered on Shadow's side of the table
- Shadow cards animate INTO slots automatically (no drag — shadow plays autonomously)
- Shadow card placement animation: card sweeps from off-screen top, lands in slot with a thud effect (shake `±2px` over `0.1s`)

---

## SHADOW RIPPLE EFFECTS

### When a Card is Played

1. Card slides from player hand to the chosen slot (CSS `translate` transition, `0.3s`)
2. On landing: ripple emanates from the slot outward on the table surface
3. Ripple: SVG circle expanding from 0 → 120px radius, `opacity: 0.5 → 0`, `stroke: rgba(192, 180, 255, 0.6)`

```css
@keyframes table-ripple {
  0%   { r: 0;   opacity: 0.5; }
  100% { r: 60px; opacity: 0; }
}
```

### When Effects Resolve

- Attack: A slash graphic in dark purple sweeps from player side to shadow side (or vice versa)
- Heal: A soft white glow pulses on the healed entity
- Corruption: Slot turns dark red momentarily; card flips to corrupted face

---

## CENTER DIVIDER LINE

### Visual
- A thin, glowing horizontal line divides player and shadow zones on the table
- This represents the "mirror line" — the boundary between self and shadow

```css
.table-divider {
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(192, 180, 255, 0.5) 20%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(192, 180, 255, 0.5) 80%,
    transparent 100%
  );
  box-shadow: 0 0 8px rgba(192, 180, 255, 0.6);
  animation: divider-pulse 4s ease-in-out infinite;
}

@keyframes divider-pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1.0; }
}
```

---

## PERSPECTIVE & 3D EFFECT

The table uses CSS `perspective` to create a mild 3D tilt — making it feel like looking down at a ritual table.

```css
.battle-arena {
  perspective: 1200px;
}

.mirror-table {
  transform: rotateX(12deg);
  transform-style: preserve-3d;
}

/* Cards on the table are at z=1, slightly elevated above surface */
.card-on-table {
  transform: rotateX(-12deg) translateZ(4px);
}
```

---

## IDLE SURFACE ANIMATIONS

These animations play continuously during battle to keep the table feeling alive.

### 1. Slow Shimmer
A very subtle traveling highlight across the table surface — like light reflecting off glass.  
Linear gradient swept left-to-right over `8s` infinite.

### 2. Fog Wisps
3 SVG blur-filtered shapes drift slowly across the table surface in different directions.  
`opacity: 0.06`. They represent memories drifting beneath the glass.

### 3. Depth Pulse
The inner glow of the table (purple radial gradient) pulses gently:  
`opacity: 0.08 → 0.16 → 0.08` over `6s`.

---

## Z-INDEX LAYER ORDER

```
z=100  Dialogue box
z=50   Card in hand (being dragged)
z=20   Crack SVGs
z=15   Cards on table (placed)
z=10   Ripple effects
z=5    Table surface effects (shimmer, fog)
z=1    Mirror table base
z=0    Battle background (behind table)
```

---

## COLOR TOKENS (TABLE-SPECIFIC)

```css
--table-surface:      #09070F;
--table-edge:         rgba(192, 180, 220, 0.35);
--table-glow:         rgba(120, 60, 200, 0.08);
--slot-inactive:      rgba(192, 180, 255, 0.12);
--slot-hover:         rgba(192, 180, 255, 0.45);
--divider-line:       rgba(255, 255, 255, 0.7);
--crack-glow:         rgba(140, 100, 255, 0.8);
--ripple-color:       rgba(192, 180, 255, 0.6);
```
