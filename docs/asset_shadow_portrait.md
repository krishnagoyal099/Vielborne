# ASSET SPEC: SHADOW PORTRAIT
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The Shadow portrait is the visual and emotional anchor of the entire game.  
It is always visible during battle. It is always watching.  
The player must feel that the Shadow is a genuine presence — not a sprite, not a character — a reflection of something real.

---

## CORE DESIGN PRINCIPLES

1. **The Shadow has no face.** Its expression is implied by posture and light.
2. **It is the player.** Proportions are humanoid and relatable.
3. **It is not evil.** It is sorrowful, wounded, and ancient.
4. **Its eyes are the only constant feature.** Everything else shifts.

---

## BASE SILHOUETTE CONSTRUCTION

### Body

```
         ●●●      ← head (perfect oval, featureless)
        ●   ●     ← neck
      ●●●●●●●●●   ← shoulders (slightly broader than human norm)
      ●         ●
     ●           ●  ← arms (long, slightly elongated)
     ●           ●
      ●●●●●●●●●   ← torso
         ●●●       ← waist
        ●   ●      ← hips
       ●     ●     ← upper legs
      ●       ●    ← lower legs (fade into smoke at knee)
     ░░░░░░░░░░    ← smoke/fog base (no feet visible)
```

### Key Proportions
- Head: slightly larger than human norm (~7.5 heads tall vs 7)
- Arms: fingertips reach mid-thigh (uncanny valley length)
- Body: rigid upright posture — no casual slouch
- Lower body: dissolves into layered smoke ~25% from bottom

---

## GLOWING EYES

### Shape
- Two narrow horizontal slits (almond-shaped, horizontal)
- Width: ~30% of face width
- Color: Pure white inner core → pale violet fade → transparent
- No iris visible. No pupil visible.

### Glow Layers
```
Layer 1: Core white      — opacity 1.0,   blur 2px
Layer 2: Pale violet     — opacity 0.7,   blur 8px   (#C084FC)
Layer 3: Deep violet     — opacity 0.4,   blur 20px  (#7C3AED)
Layer 4: Wide outer halo — opacity 0.15,  blur 40px  (#4C1D95)
```

### Eye Animation
- **Default idle**: Subtle breathing glow pulse (1.0 → 1.4 → 1.0 scale on glow layers over 3s)
- **When speaking**: Eyes brighten +40% opacity, glow radius expands
- **When attacking**: Eyes flash pure white for 0.15s, then return
- **On player victory**: Eyes dim and slowly close (opacity 1.0 → 0 over 3s)
- **On player defeat**: Eyes flare brilliant white, then the portrait shatters

---

## SMOKE-LIKE BODY TEXTURE

### Layer System (3 smoke layers, independently animated)

**Layer 1 — Body Core**
- Solid dark silhouette: `#0a0005`
- Sharp edges on upper body, increasingly soft on lower body
- CSS: `clip-path` humanoid path, `mask-image` gradient fade at 60% height

**Layer 2 — Smoke Tendrils**
- Multiple thin wisps extending from shoulders, arms, edges
- Color: `rgba(80, 20, 120, 0.5)` → transparent
- Animation: Slow upward drift, `rotate(±5deg)` over 6–10s (each tendril different speed)
- Created via `border-radius` distortion and `filter: blur(8px)`

**Layer 3 — Outer Aura**
- Very wide, very soft dark haze surrounding entire figure
- Color: `rgba(30, 0, 60, 0.35)`
- `filter: blur(30px)`
- Pulses slowly: opacity `0.35 → 0.55 → 0.35` over 5s

---

## EMOTIONAL VARIANTS

The Shadow portrait adjusts based on its **personality type**. All variants use the same base silhouette — only glow color, posture offset, and aura change.

### THE ACCUSER
- **Posture**: Leans forward ~5° (aggressive, predatory)
- **Eye color**: Harsh white → cold blue (`#BFDBFE`)
- **Aura**: Sharper edges, less smoke
- **Tendrils**: Point forward like fingers
- **CSS modifier class**: `.shadow--accuser`

### THE WATCHER
- **Posture**: Perfectly still, centered
- **Eye color**: Silver-white, very wide open
- **Aura**: Perfect symmetry, slow pulse
- **Tendrils**: None. The Watcher is unnervingly still.
- **CSS modifier class**: `.shadow--watcher`

### THE MOURNER
- **Posture**: Head bowed ~10° (grief)
- **Eye color**: Pale blue → soft violet (`#A5B4FC`)
- **Aura**: Dripping downward tendrils (tears effect)
- **Tendrils**: Hang downward rather than drift upward
- **CSS modifier class**: `.shadow--mourner`

### THE TYRANT
- **Posture**: Towering — scale `1.0 → 1.08` (larger than others)
- **Eye color**: Deep red-violet (`#C026D3`)
- **Aura**: Heavy, dense, very dark
- **Tendrils**: Thick, rigid, not wispy
- **CSS modifier class**: `.shadow--tyrant`

### THE FORGOTTEN ONE
- **Posture**: Slightly tilted, asymmetric (~3° lean)
- **Eye color**: Flickering — alternates between white and dark (glitch effect)
- **Aura**: Fragmented — broken into patches with gaps
- **Tendrils**: Erratic, move in non-smooth paths
- **CSS modifier class**: `.shadow--forgotten`

---

## ANIMATION STATES

### State: IDLE
```css
@keyframes shadow-idle-breathe {
  0%, 100% { transform: scaleY(1.0); }
  50% { transform: scaleY(1.012); }
}
/* Duration: 5s, ease-in-out, infinite */
```

### State: SPEAKING (dialogue box active)
- Portrait shifts slightly left (makes room for dialogue bubble)
- Eyes intensify
- A subtle ripple emanates from the figure outward

### State: ATTACKING
1. Figure lurches forward (`translateX(+20px)`) over `0.15s`
2. Eyes flash
3. A shadow-tendril visual shoots from figure toward player's card zone
4. Figure snaps back over `0.3s`

### State: HIT (player attacks Shadow)
1. Figure momentarily brightens (highlight flash)
2. Cracks appear in the background mirror behind it
3. Figure shudders (`rotate ±2deg` over `0.3s`)
4. HP bar in header decreases

### State: DEFEAT
1. Eyes close slowly (2s)
2. Figure dissolves bottom-to-top: `mask-image` shrinks upward over `3s`
3. Final flash of white light
4. Silence — 2 second pause — then transition to ending

---

## CSS IMPLEMENTATION

```css
.shadow-portrait {
  position: relative;
  width: 220px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shadow-body {
  width: 100%;
  height: 100%;
  background: #0a0005;
  clip-path: polygon(/* humanoid SVG path data */);
  mask-image: linear-gradient(
    to bottom,
    black 0%,
    black 55%,
    rgba(0,0,0,0.3) 75%,
    transparent 100%
  );
  animation: shadow-idle-breathe 5s ease-in-out infinite;
  filter: drop-shadow(0 0 40px rgba(100, 20, 180, 0.5));
}

.shadow-eyes {
  position: absolute;
  top: 12%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 18px;
}

.shadow-eye {
  width: 28px;
  height: 8px;
  border-radius: 50%;
  background: white;
  box-shadow:
    0 0 6px 2px rgba(255,255,255,0.9),
    0 0 16px 6px rgba(192, 132, 252, 0.7),
    0 0 40px 16px rgba(124, 58, 237, 0.4),
    0 0 80px 32px rgba(76, 29, 149, 0.2);
  animation: eye-pulse 3s ease-in-out infinite;
}

.shadow-aura {
  position: absolute;
  inset: -40px;
  background: radial-gradient(
    ellipse at 50% 40%,
    rgba(30, 0, 60, 0.4) 0%,
    transparent 70%
  );
  animation: aura-pulse 5s ease-in-out infinite;
  pointer-events: none;
}
```

---

## PORTRAIT SIZING IN LAYOUT

| Context | Width | Notes |
|---|---|---|
| Battle screen (desktop) | `220px` | Fixed left panel |
| Battle screen (mobile) | `140px` | Top of screen |
| Loading screen silhouette | `180px` | Centered, rising animation |
| Ending card | `80px` thumbnail | Grayscale, faded |
