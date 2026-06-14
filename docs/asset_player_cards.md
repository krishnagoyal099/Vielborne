# ASSET SPEC: PLAYER CARDS
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

Player cards are the player's voice in the confrontation.  
They must feel **personal, luminous, and hopeful** — even when they hurt.  
Each card is a facet of the Self: not perfect, but real.

---

## CARD DIMENSIONS

```
Width:  140px  (in-hand)    /  120px (on-table)
Height: 200px  (in-hand)    /  172px (on-table)
Border-radius: 10px
```

---

## CARD FRAME ANATOMY

```
┌─────────────────────────────┐
│  [COST]  [RARITY GEMS]      │  ← Header bar (24px tall)
├─────────────────────────────┤
│                             │
│      [ARCHETYPE ICON]       │  ← Icon zone (60px tall)
│           64×64             │
│                             │
├─────────────────────────────┤
│  CARD NAME                  │  ← Name bar (20px)
├─────────────────────────────┤
│  [EFFECT DESCRIPTION]       │  ← Effect text (48px)
│  "Deal 6 damage."           │
├─────────────────────────────┤
│  ❝ flavor text here ❞       │  ← Flavor (28px)
├─────────────────────────────┤
│  [ATK] [HEAL] [ARM] [DRAW]  │  ← Stat strip (20px)
└─────────────────────────────┘
```

---

## CARD FRAME DESIGN — PURE STATE

### Frame Material
- Background: Deep dark with archetype-tinted gradient
- Border: Silver with archetype color glow
- Corner runes: Tiny decorative marks at each corner (SVG, `4px`)

```css
.card-player {
  background: linear-gradient(
    160deg,
    rgba(var(--archetype-color-rgb), 0.12) 0%,
    #0D0A16 40%,
    #08060F 100%
  );
  border: 1.5px solid rgba(var(--archetype-color-rgb), 0.5);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.05),
    0 0 20px rgba(var(--archetype-color-rgb), 0.2),
    inset 0 0 30px rgba(var(--archetype-color-rgb), 0.04);
  border-radius: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-player:hover {
  transform: translateY(-8px) scale(1.04);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.1),
    0 12px 40px rgba(var(--archetype-color-rgb), 0.5),
    0 0 60px rgba(var(--archetype-color-rgb), 0.2);
}
```

---

## ARCHETYPE COLOR TOKENS

| Archetype | Primary RGB | Glow Color | Icon Symbol |
|---|---|---|---|
| Courage | `255, 140, 50` | Warm amber | ⚔ Upward sword |
| Hope | `100, 200, 255` | Sky blue | ✦ Rising star |
| Kindness | `120, 220, 160` | Soft green | ❤ Open hands |
| Resolve | `220, 180, 255` | Silver-violet | ◈ Diamond shield |
| Trust | `255, 220, 100` | Warm gold | ∞ Linked rings |
| Acceptance | `200, 200, 200` | Neutral silver | ⊙ Open circle |

---

## RARITY STYLING

### Common
- 1 small gem in header: `⬡` (hexagon), color: `rgba(180, 180, 200, 0.7)`
- No extra glow
- Frame: standard

### Rare
- 2 gems: `⬡⬡`, color: `rgba(140, 100, 255, 0.9)`
- Additional glow on border: `box-shadow` +10px spread
- Subtle shimmer animation on frame: a traveling `linear-gradient` highlight

### Mythic
- 3 gems: `⬡⬡⬡`, color cycling between archetype colors over `4s`
- Animated border: gradient rotates around card frame
- Name text has gradient fill matching archetype color

```css
/* Mythic animated border */
.card-mythic {
  --border-angle: 0turn;
  border-image: conic-gradient(
    from var(--border-angle),
    rgba(var(--archetype-color-rgb), 0.2),
    rgba(var(--archetype-color-rgb), 0.9),
    rgba(var(--archetype-color-rgb), 0.2)
  ) 1;
  animation: border-spin 4s linear infinite;
}

@keyframes border-spin {
  to { --border-angle: 1turn; }
}
```

---

## CARD FAMILIES — AI GENERATION VARIANTS

For each archetype, AI generates 3 cards per run using variant naming.  
The examples below show the **range of variation** — AI will generate new variants each run.

---

### COURAGE FAMILY
**Base Identity**: Action in the face of fear. Cards deal damage or empower.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Defiance | Attack | Deal 7 damage. If below 50% HP, deal 10 instead. |
| Bravery | Attack + Draw | Deal 5 damage. Draw 1. |
| Persistence | Attack + Armor | Deal 4 damage. Gain 3 armor. |
| Conviction | Attack | Deal 10 damage. Cost 3. |
| Tenacity | Self-heal + Attack | Heal 3. Deal 5 damage. |
| Valor | Attack (all) | Deal 4 damage. (No variants overlap per run) |

**Icon**: Upward-pointing sword, warm amber glow  
**Color gradient tip**: Amber → deep crimson at bottom

---

### HOPE FAMILY
**Base Identity**: Drawing cards, restoring energy, believing in the next turn.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Dawn | Draw | Draw 2 cards. |
| Promise | Draw + Heal | Draw 1. Heal 4. |
| Wish | Energy | Gain 2 energy. |
| Aspiration | Draw | Draw 3 cards. Cost 2. |
| Renewal | Heal + Draw | Heal 6. Draw 1. |
| Beacon | Armor + Draw | Gain 4 armor. Draw 1. |

**Icon**: Rising star, cool sky-blue  
**Color gradient tip**: Pale blue → deep navy

---

### KINDNESS FAMILY
**Base Identity**: Healing, protecting, occasionally at personal cost.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Mercy | Heal | Heal 8. |
| Compassion | Heal + Armor | Heal 5. Gain 3 armor. |
| Empathy | Heal | Heal 10. Cost 2. |
| Grace | Armor | Gain 8 armor. |
| Tenderness | Heal | Heal 4. Draw 1. Cost 0. |
| Shelter | Armor | Gain 5 armor. Next hit blocked. |

**Icon**: Open hands, soft green  
**Color gradient tip**: Mint green → deep forest green

---

### RESOLVE FAMILY
**Base Identity**: Endurance, armor, countering corruption.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Fortitude | Armor | Gain 6 armor. |
| Grit | Armor + Attack | Gain 4 armor. Deal 3 damage. |
| Willpower | Corruption cleanse | Remove corruption from 1 card. |
| Steadfast | Armor | Gain 10 armor. Cost 2. |
| Endurance | Armor + Heal | Gain 4 armor. Heal 3. |
| Indomitable | All armor | Gain 6 armor. Immune to corruption this turn. |

**Icon**: Diamond shield, silver-violet  
**Color gradient tip**: Silver → deep violet

---

### TRUST FAMILY
**Base Identity**: Double-edged, risky, high-reward. Trust is always a risk.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Belief | Draw | Draw 3 cards. Discard 1. |
| Faith | Heal | Heal 12. Cost 2. |
| Surrender | Heal + Vulnerable | Heal 15. Take 5 damage next turn. |
| Bond | Attack + Heal | Deal 4 damage. Heal 4. |
| Reliance | Draw | Draw 4 cards. Cost 2. |
| Hope's Edge | Attack | Deal 8. If you are below 25% HP, deal 15. |

**Icon**: Linked rings, warm gold  
**Color gradient tip**: Gold → dark amber

---

### ACCEPTANCE FAMILY
**Base Identity**: Cost 0, weaker individually but free. Peace is cheap but real.

| Variant Name Ideas | Effect Type | Example Effects |
|---|---|---|
| Stillness | Armor | Gain 3 armor. Cost 0. |
| Release | Draw | Draw 1. Cost 0. |
| Peace | Heal | Heal 4. Cost 0. |
| Letting Go | Discard + Draw | Discard 1. Draw 2. Cost 0. |
| Equanimity | Armor + Heal | Gain 2 armor. Heal 2. Cost 0. |
| The Last Word | Heal | Heal 6. Can only be played once per game. |

**Icon**: Open circle (enso-like), neutral silver  
**Color gradient tip**: White → deep cool gray

---

## CORRUPTED STATE DESIGN

When a player card becomes corrupted:

### Visual Changes
1. Border color inverts: archetype color → dark red-purple `rgb(120, 20, 60)`
2. Icon tints to dark red: `filter: sepia(1) hue-rotate(300deg)`
3. Name text gains strikethrough OR alternate name appears (AI-generated)
4. A cracked texture overlay appears on the card
5. Effect description shows corrupted text in red

### Animation on Corruption
- Card flips (rotateY 180deg, 0.5s)
- Brief flash of dark energy
- Card lands face-up with corrupted visual

```css
.card-corrupted {
  border-color: rgba(150, 30, 80, 0.8);
  background: linear-gradient(
    160deg,
    rgba(100, 10, 40, 0.2) 0%,
    #0D0A16 40%,
    #08060F 100%
  );
  box-shadow:
    0 0 20px rgba(150, 30, 80, 0.4),
    inset 0 0 30px rgba(100, 10, 40, 0.08);
}

.card-corrupted .card-icon {
  filter: sepia(1) hue-rotate(290deg) brightness(0.7);
}

.card-corrupted .card-name {
  color: rgb(200, 80, 100);
}

.card-corrupted::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,/* crack pattern SVG */");
  opacity: 0.15;
  border-radius: 10px;
  pointer-events: none;
}
```

---

## CARD HOVER ANIMATION

```css
.card-player {
  transform-origin: bottom center;
  transition:
    transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.2s ease;
}

.card-player:hover {
  transform: translateY(-10px) scale(1.05) rotateX(3deg);
  z-index: 100;
}

/* Fan layout for hand: cards spread with rotation */
.hand-card:nth-child(1) { transform-origin: bottom center; --base-rotation: -8deg; }
.hand-card:nth-child(2) { transform-origin: bottom center; --base-rotation: -4deg; }
.hand-card:nth-child(3) { transform-origin: bottom center; --base-rotation:  0deg; }
.hand-card:nth-child(4) { transform-origin: bottom center; --base-rotation:  4deg; }
.hand-card:nth-child(5) { transform-origin: bottom center; --base-rotation:  8deg; }
```

---

## CARD BACK DESIGN

Card backs are shown for unrevealed cards (deck indicator, etc.).

- Background: `#06040E`
- Pattern: Repeating sigil — the SHADOWSELF eclipse symbol, tiled at `20px`, `opacity: 0.08`
- Border: `1px solid rgba(192, 180, 255, 0.2)`
- Center: Large single eclipse symbol, `opacity: 0.3`, subtle rotation animation
