# ASSET SPEC: UI SYSTEM
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The UI system is the complete design language for SHADOWSELF.  
Every element inherits from this specification.  
Implementing this document correctly means the game looks polished by default.

---

## DESIGN LANGUAGE PRINCIPLES

1. **Dark as the void.** UI disappears into the background. The game is the foreground.
2. **Silver and violet.** The only palette that feels both ancient and alien.
3. **Typography is ceremony.** Every word placement should feel intentional.
4. **Interactions are rituals.** Hover = recognition. Click = commitment. Transition = consequence.
5. **Never flat.** Every element has depth through shadow, glow, or gradient.

---

## CSS CUSTOM PROPERTIES (DESIGN TOKENS)

```css
:root {
  /* === COLORS === */

  /* Backgrounds */
  --bg-void:          #000000;
  --bg-deep:          #06050D;
  --bg-base:          #09070F;
  --bg-surface:       #0E0B18;
  --bg-elevated:      #141020;
  --bg-hover:         #1A1530;

  /* Borders */
  --border-subtle:    rgba(180, 160, 220, 0.12);
  --border-default:   rgba(180, 160, 220, 0.25);
  --border-strong:    rgba(180, 160, 220, 0.5);
  --border-focus:     rgba(180, 160, 220, 0.8);

  /* Text */
  --text-primary:     rgba(230, 220, 255, 0.95);
  --text-secondary:   rgba(200, 185, 240, 0.75);
  --text-muted:       rgba(160, 145, 200, 0.45);
  --text-disabled:    rgba(120, 110, 160, 0.3);
  --text-inverse:     rgba(8, 6, 14, 0.9);

  /* Accents */
  --accent-primary:   #A855F7;          /* purple */
  --accent-light:     #C084FC;          /* light purple */
  --accent-dark:      #7C3AED;          /* deep purple */
  --accent-silver:    rgba(200, 190, 230, 0.8);
  --accent-gold:      rgba(250, 200, 80, 0.8);

  /* Shadow archetypes */
  --fear-color:       rgba(160, 40, 40, 0.9);
  --rage-color:       rgba(220, 60, 20, 0.9);
  --doubt-color:      rgba(80, 80, 120, 0.9);
  --jealousy-color:   rgba(40, 140, 80, 0.9);
  --despair-color:    rgba(60, 40, 100, 0.9);
  --obsession-color:  rgba(160, 80, 180, 0.9);

  /* Player archetypes */
  --courage-color:    rgba(255, 140, 50, 0.9);
  --hope-color:       rgba(100, 200, 255, 0.9);
  --kindness-color:   rgba(120, 220, 160, 0.9);
  --resolve-color:    rgba(220, 180, 255, 0.9);
  --trust-color:      rgba(255, 220, 100, 0.9);
  --acceptance-color: rgba(200, 200, 200, 0.9);

  /* === TYPOGRAPHY === */
  --font-display:     'Cinzel Decorative', serif;
  --font-heading:     'Cinzel', serif;
  --font-body:        'Cormorant Garamond', serif;
  --font-ui:          'Cinzel', serif;

  /* === SPACING === */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* === BORDERS === */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   20px;
  --radius-pill: 9999px;
  --radius-circle: 50%;

  /* === TRANSITIONS === */
  --transition-fast:   0.15s ease;
  --transition-base:   0.25s ease;
  --transition-slow:   0.4s ease;
  --transition-ritual: 0.6s cubic-bezier(0.22, 1, 0.36, 1);

  /* === Z-INDEX === */
  --z-background: 0;
  --z-base:       1;
  --z-elevated:   10;
  --z-overlay:    50;
  --z-modal:      100;
  --z-top:        200;
}
```

---

## TYPOGRAPHY SYSTEM

### Importing Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cinzel+Decorative:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
```

### Type Scale

| Role | Font | Size | Weight | Letter-spacing | Color |
|---|---|---|---|---|---|
| Game Logo | Cinzel Decorative | clamp(2.5rem, 6vw, 5rem) | 700 | 0.35em | White |
| Screen Title | Cinzel | 1.5rem | 600 | 0.15em | --text-primary |
| Section Header | Cinzel | 0.75rem | 400 | 0.3em | --text-muted |
| Card Name | Cinzel | 0.85rem | 600 | 0.1em | --text-primary |
| Body / Flavor | Cormorant Garamond | 1rem | 400 | normal | --text-secondary |
| UI Label | Cinzel | 0.7rem | 400 | 0.2em | --text-muted |
| Dialogue | Cormorant Garamond Italic | 1.05rem | 400 | 0.01em | --text-secondary |
| Stat Number | Cinzel | 0.9rem | 600 | 0 | --text-primary |
| Button Text | Cinzel | 0.75rem | 400 | 0.25em | varies |

---

## BUTTON SYSTEM

### Base Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  font-family: var(--font-ui);
  font-size: 0.75rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-default);
  background: rgba(180, 160, 220, 0.06);
  color: var(--text-secondary);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all var(--transition-base);
  user-select: none;
}

/* Shimmer on hover */
.btn::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.04),
    transparent
  );
  transition: left var(--transition-slow);
}

.btn:hover {
  border-color: var(--border-strong);
  color: var(--text-primary);
  box-shadow: 0 0 16px rgba(168, 85, 247, 0.25);
  transform: translateY(-1px);
}

.btn:hover::after {
  left: 100%;
}

.btn:active {
  transform: translateY(0);
  box-shadow: none;
}
```

### Button Variants

```css
/* Primary — glowing purple */
.btn-primary {
  background: rgba(124, 58, 237, 0.2);
  border-color: rgba(168, 85, 247, 0.6);
  color: rgba(220, 200, 255, 0.95);
  box-shadow: 0 0 20px rgba(124, 58, 237, 0.2);
}
.btn-primary:hover {
  background: rgba(124, 58, 237, 0.35);
  box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
}

/* Ghost — minimal, text only */
.btn-ghost {
  background: transparent;
  border-color: transparent;
  color: var(--text-muted);
  box-shadow: none;
}
.btn-ghost:hover {
  color: var(--text-secondary);
  border-color: var(--border-subtle);
}

/* Danger — for ominous actions */
.btn-danger {
  background: rgba(150, 20, 60, 0.15);
  border-color: rgba(180, 40, 80, 0.4);
  color: rgba(240, 160, 180, 0.9);
}
.btn-danger:hover {
  background: rgba(150, 20, 60, 0.3);
  box-shadow: 0 0 20px rgba(150, 20, 60, 0.35);
}
```

---

## PANEL / CARD SYSTEM

```css
.panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

/* Subtle top-edge glow */
.panel::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--border-default) 40%,
    var(--border-default) 60%,
    transparent
  );
}

.panel-elevated {
  background: var(--bg-elevated);
  border-color: var(--border-default);
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(180, 160, 220, 0.05);
}
```

---

## HEALTH BAR SYSTEM

### Player HP Bar

```css
.health-bar-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.health-bar-track {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-pill);
  overflow: hidden;
  position: relative;
}

.health-bar-fill {
  height: 100%;
  border-radius: var(--radius-pill);
  background: linear-gradient(
    90deg,
    #6B21A8,
    #A855F7,
    #C084FC
  );
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.6);
  transition: width 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
}

/* Shine effect on bar */
.health-bar-fill::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 50%;
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-pill) var(--radius-pill) 0 0;
}

/* Low HP state */
.health-bar-fill.danger {
  background: linear-gradient(90deg, #7F1D1D, #DC2626, #EF4444);
  box-shadow: 0 0 12px rgba(220, 38, 38, 0.7);
  animation: health-pulse 1.5s ease-in-out infinite;
}

@keyframes health-pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(220, 38, 38, 0.7); }
  50% { box-shadow: 0 0 20px rgba(220, 38, 38, 1.0); }
}
```

### Shadow HP Bar

```css
.health-bar-fill.shadow {
  background: linear-gradient(
    90deg,
    #3B0764,
    #6B21A8,
    #8B5CF6
  );
  box-shadow: 0 0 8px rgba(107, 33, 168, 0.6);
}
```

### HP Display Format
```
HP  [███████░░░]  35 / 50
```
- Number: Cinzel, 0.85rem, right of bar
- Format: `current / max`

---

## ENERGY COUNTER

3 energy diamonds per turn. Spent on card plays.

```css
.energy-container {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.energy-pip {
  width: 12px;
  height: 12px;
  background: rgba(168, 85, 247, 0.8);
  transform: rotate(45deg);  /* Diamond shape */
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.6);
  transition: all var(--transition-base);
}

.energy-pip.spent {
  background: rgba(60, 40, 90, 0.4);
  box-shadow: none;
}

/* Refill animation on new turn */
.energy-pip.refilling {
  animation: pip-refill 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes pip-refill {
  0%   { transform: rotate(45deg) scale(0); opacity: 0; }
  60%  { transform: rotate(45deg) scale(1.2); }
  100% { transform: rotate(45deg) scale(1.0); opacity: 1; }
}
```

---

## DIALOGUE BOX SYSTEM

The Shadow speaks throughout the battle.

### Visual Design

```css
.dialogue-box {
  position: relative;
  background: rgba(10, 6, 20, 0.92);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-6);
  max-width: 520px;
  backdrop-filter: blur(8px);
}

/* Left accent bar */
.dialogue-box::before {
  content: '';
  position: absolute;
  left: 0; top: 10%; bottom: 10%;
  width: 2px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(168, 85, 247, 0.8),
    transparent
  );
  border-radius: 2px;
}

.dialogue-speaker {
  font-family: var(--font-heading);
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

.dialogue-text {
  font-family: var(--font-body);
  font-style: italic;
  font-size: 1.0rem;
  line-height: 1.7;
  color: var(--text-secondary);
}

/* Typewriter cursor */
.dialogue-text::after {
  content: '▌';
  animation: cursor-blink 0.8s step-end infinite;
  color: rgba(168, 85, 247, 0.7);
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

### Dialogue Entry Animation
```css
@keyframes dialogue-appear {
  from {
    opacity: 0;
    transform: translateY(6px);
    clip-path: inset(0 100% 0 0);  /* Wipe in from left */
  }
  to {
    opacity: 1;
    transform: translateY(0);
    clip-path: inset(0 0% 0 0);
  }
}

.dialogue-box.entering {
  animation: dialogue-appear 0.5s ease-out forwards;
}
```

---

## CARD HOVER TOOLTIP

When hovering a card in hand (desktop only):

- Large card preview appears above hand (1.5× size)
- Full card details visible: name, archetype, all effect stats, flavor text
- Background: blurred overlay behind preview card

```css
.card-tooltip {
  position: absolute;
  bottom: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 288px;
  z-index: var(--z-overlay);
  pointer-events: none;

  /* Entry animation */
  animation: tooltip-rise 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes tooltip-rise {
  from { opacity: 0; transform: translateX(-50%) translateY(8px) scale(0.95); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0)  scale(1.0); }
}
```

---

## SCREEN TRANSITIONS

All screen-to-screen transitions use the same base system:

```css
/* PHASE OUT */
@keyframes screen-exit {
  0%   { opacity: 1; transform: scale(1.0); }
  100% { opacity: 0; transform: scale(0.97); filter: blur(4px); }
}

/* PHASE IN */
@keyframes screen-enter {
  0%   { opacity: 0; transform: scale(1.03); filter: blur(4px); }
  100% { opacity: 1; transform: scale(1.0);  filter: blur(0px); }
}

.screen-exiting {
  animation: screen-exit 0.5s ease-in forwards;
}

.screen-entering {
  animation: screen-enter 0.5s ease-out forwards;
}
```

**Duration**: 0.5s exit + 0.1s pause + 0.5s enter = 1.1s total.

---

## TURN INDICATOR

Displays whose turn it is.

```css
.turn-indicator {
  font-family: var(--font-heading);
  font-size: 0.7rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-pill);
  transition: all var(--transition-slow);
}

.turn-indicator.player-turn {
  color: rgba(200, 185, 255, 0.9);
  background: rgba(124, 58, 237, 0.15);
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.turn-indicator.shadow-turn {
  color: rgba(200, 160, 220, 0.9);
  background: rgba(80, 20, 120, 0.2);
  border: 1px solid rgba(120, 40, 180, 0.4);
  animation: shadow-turn-pulse 1s ease-in-out infinite;
}

@keyframes shadow-turn-pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(120, 40, 180, 0.3); }
  50% { box-shadow: 0 0 16px rgba(120, 40, 180, 0.6); }
}
```

---

## END TURN BUTTON

Large, prominent, cannot be missed.

```css
.btn-end-turn {
  padding: var(--space-4) var(--space-10);
  font-size: 0.8rem;
  letter-spacing: 0.3em;
  background: rgba(124, 58, 237, 0.12);
  border: 1px solid rgba(168, 85, 247, 0.4);
  color: rgba(200, 185, 255, 0.85);
  box-shadow: 0 0 20px rgba(124, 58, 237, 0.15);
}

.btn-end-turn:hover {
  background: rgba(124, 58, 237, 0.25);
  border-color: rgba(168, 85, 247, 0.7);
  box-shadow: 0 0 30px rgba(124, 58, 237, 0.35);
  transform: translateY(-2px);
}

.btn-end-turn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

---

## NOTIFICATION / EFFECT POPUPS

Floating damage numbers and effect labels.

```css
.effect-popup {
  position: absolute;
  font-family: var(--font-heading);
  font-size: 1.2rem;
  font-weight: 600;
  pointer-events: none;
  animation: popup-float 1.2s ease-out forwards;
  z-index: var(--z-top);
}

.effect-popup.damage    { color: rgba(240, 100, 100, 0.95); }
.effect-popup.heal      { color: rgba(100, 220, 140, 0.95); }
.effect-popup.armor     { color: rgba(180, 180, 220, 0.95); }
.effect-popup.corrupt   { color: rgba(180, 40, 100, 0.95); }
.effect-popup.energy    { color: rgba(200, 150, 255, 0.95); }

@keyframes popup-float {
  0%   { opacity: 1; transform: translateY(0) scale(1.0); }
  20%  { transform: translateY(-10px) scale(1.15); }
  100% { opacity: 0; transform: translateY(-50px) scale(0.9); }
}
```

---

## SCROLLBAR STYLING

```css
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: var(--bg-deep);
}

::-webkit-scrollbar-thumb {
  background: rgba(168, 85, 247, 0.3);
  border-radius: var(--radius-pill);
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(168, 85, 247, 0.6);
}
```

---

## GLOBAL BASE STYLES

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

/* Selection styling */
::selection {
  background: rgba(168, 85, 247, 0.3);
  color: var(--text-primary);
}

/* Focus ring */
:focus-visible {
  outline: 1px solid rgba(168, 85, 247, 0.6);
  outline-offset: 2px;
}
```

---

## GRADIO CUSTOMIZATION NOTES

When using Gradio, override default styles via custom CSS injected into `gr.Blocks(css=...)`:

```python
CUSTOM_CSS = """
/* Hide Gradio default elements */
.gradio-container { background: transparent !important; }
footer { display: none !important; }
.svelte-1gfkn6j { display: none !important; }  /* Gradio branding */

/* Override Gradio button defaults */
.gr-button {
  font-family: 'Cinzel', serif !important;
  letter-spacing: 0.2em !important;
}
"""
```

All visual design is implemented via Gradio's `css` parameter and HTML injection through `gr.HTML()` components.
