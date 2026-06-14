# ASSET SPEC: SHADOW CARDS
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

Shadow cards are the player's own darkness turned outward.  
They must feel **familiar yet wrong** — like recognizing something about yourself you don't want to admit.  
Every Shadow card is a dark mirror of a player archetype.

---

## DESIGN PHILOSOPHY

Shadow cards are NOT randomly evil.  
Each shadow archetype is the **repressed inverse** of a player archetype:

| Player Archetype | Shadow Archetype | Psychological Mirror |
|---|---|---|
| Courage | Fear | What courage suppresses |
| Hope | Despair | What hope fights against |
| Kindness | Rage | What kindness buries |
| Resolve | Doubt | What resolve masks |
| Trust | Jealousy | The wound inside trust |
| Acceptance | Obsession | The failure of acceptance |

The player should recognize this. It should sting.

---

## SHADOW CARD DIMENSIONS

Identical to player cards:
```
Width:  140px  (in-hand / on-table for Shadow)
Height: 200px
Border-radius: 10px
```

Shadow cards are shown face-down in Shadow's hand.  
They flip face-up only when played.

---

## SHADOW CARD FRAME ANATOMY

```
┌─────────────────────────────┐
│  [COST]  [SHADOW MARK]      │  ← Dark header (24px)
├──────────────────────╌╌╌╌╌╌┤
│                             │
│      [SHADOW ICON]          │  ← Inverted/corrupted icon (60px)
│       dark + bleeding       │
│                             │
├──╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│  CARD NAME  [distorted]     │  ← Name bar
├─────────────────────────────┤
│  [EFFECT — always harmful   │  ← Effect text
│   to player]                │
├─────────────────────────────┤
│  ❝ haunting flavor text ❞   │  ← Flavor (always 1st person)
├─────────────────────────────┤
│  [ATK] [DRAIN] [CORRUPT]    │  ← Stat strip
└─────────────────────────────┘
```

---

## SHADOW CARD FRAME DESIGN

Shadow cards use a distinct visual language from player cards:

```css
.card-shadow {
  background: linear-gradient(
    160deg,
    rgba(var(--shadow-archetype-rgb), 0.18) 0%,
    #060310 50%,
    #030108 100%
  );
  border: 1.5px solid rgba(var(--shadow-archetype-rgb), 0.6);
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.4),
    0 0 24px rgba(var(--shadow-archetype-rgb), 0.35),
    inset 0 0 40px rgba(var(--shadow-archetype-rgb), 0.06);
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

/* Bleeding effect — color drips down the card */
.card-shadow::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 40%;
  background: linear-gradient(
    to bottom,
    rgba(var(--shadow-archetype-rgb), 0.15) 0%,
    transparent 100%
  );
  pointer-events: none;
}

/* Distortion overlay — very subtle noise/grain */
.card-shadow::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,/* SVG noise texture */");
  opacity: 0.05;
  mix-blend-mode: overlay;
}
```

---

## SHADOW ARCHETYPE COLOR TOKENS

| Archetype | Primary RGB | Glow Color | Icon Symbol |
|---|---|---|---|
| Fear | `160, 40, 40` | Dark crimson | ⚠ Eye with cracks |
| Rage | `220, 60, 20` | Burning orange-red | ✖ Jagged fist |
| Doubt | `80, 80, 120` | Cold steel blue | ? Fractured mirror |
| Jealousy | `40, 140, 80` | Poisoned green | ⊗ Serpent eye |
| Despair | `60, 40, 100` | Deepest violet | ↓ Falling teardrop |
| Obsession | `160, 80, 180` | Invasive purple | ∞ Broken loop |

---

## SHADOW CARD FAMILIES

---

### FEAR FAMILY
**Shadow of Courage**  
*"You called it bravery. I called it not knowing what could go wrong."*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| Paralysis | Attack + Disable | Deal 4. Player skips card draw next turn. |
| The Worst Outcome | Attack | Deal 8. |
| Anticipation | Drain | Player loses 2 energy next turn. |
| Dread | Attack + Corrupt | Deal 3. Corrupt 1 random player card. |
| Exposure | Forced Discard | Player discards 2 cards. |
| Creeping Certainty | DoT | Player takes 3 damage at start of their next 2 turns. |

**Icon**: Eye with cracks radiating outward  
**Flavor text style**: *"It wasn't possible to look away."*  
**Color**: Dark crimson bleeds from top

---

### RAGE FAMILY
**Shadow of Kindness**  
*"I held your anger for you. I held it until it became me."*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| Outburst | Heavy Attack | Deal 10 damage. |
| Resentment | Attack + Drain | Deal 5. Player loses 1 energy. |
| The Breaking Point | Attack | Deal 12. Cost 3. |
| Smothered | Corrupt | Corrupt 2 random player cards. |
| Blind Fury | Attack (self-damage) | Deal 8 to player. Shadow takes 3. |
| Long Memory | Escalating | Deal 2 more damage for each turn taken (max 12). |

**Icon**: Jagged fist, fractured knuckles  
**Flavor text style**: *"I never asked to carry this."*  
**Color**: Orange-red burning from edges

---

### DOUBT FAMILY
**Shadow of Resolve**  
*"For every step you took, I asked: but what if you're wrong?"*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| Second-Guessing | Forced Discard | Player discards 1 card they just played. (Undo) |
| Hesitation | Energy Drain | Player loses 2 energy. |
| The Long Night | DoT | Player takes 2 damage for 3 turns. |
| Unraveling | Armor Remove | Remove all player armor. |
| Imposter | Corrupt | Corrupt player's highest-cost card. |
| The Voice | Psychic | Player's next card costs +2 more to play. |

**Icon**: Fractured mirror — two halves misaligned  
**Flavor text style**: *"What if you were wrong about me?"*  
**Color**: Cold steel-blue, desaturated

---

### JEALOUSY FAMILY
**Shadow of Trust**  
*"You gave them so much. Did you ever wonder what you took from me?"*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| Comparison | Attack | Deal 5. If player has more HP, deal 8 instead. |
| Coveting | Card Steal | Copy the last card player played. Play it against them. |
| The Green Wound | Drain | Player loses 3 HP at start of each turn for 2 turns. |
| Withholding | Energy Block | Player gains 1 less energy next turn. |
| Envy's Eye | Attack + Corrupt | Deal 4. Corrupt 1 player card. |
| What You Have | Invert | Swap player and shadow current HP values. (Rare/Mythic) |

**Icon**: Serpent eye — poisoned green pupil  
**Flavor text style**: *"You had so much and didn't notice me watching."*  
**Color**: Poisoned green-gray at edges

---

### DESPAIR FAMILY
**Shadow of Hope**  
*"Every time you hoped, I endured the falling. I know what happens next."*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| The Long Dark | Heavy Drain | Player loses 12 HP over 3 turns (4/turn). |
| Giving Up | Card Suppress | Player's hand size reduced by 2 next turn. |
| Hollow | Heal Negate | Player's next healing card heals 0. |
| The Weight | Attack | Deal 7. Player cannot draw cards next turn. |
| Pointlessness | Energy Drain | Player begins next turn with 0 energy. |
| Collapse | Attack + Drain | Deal 5. Player loses 2 HP at start of next 3 turns. |

**Icon**: Falling teardrop, trailing light  
**Flavor text style**: *"You kept looking up. I kept counting the distance."*  
**Color**: Deep violet, dripping downward

---

### OBSESSION FAMILY
**Shadow of Acceptance**  
*"You let go. I never could. I became the thing you released."*

| Variant Name | Effect Type | Example Effects |
|---|---|---|
| Return | Replay | Shadow replays its last card immediately. |
| The Loop | Persistent | This card is not discarded; Shadow plays it again next turn. |
| Fixation | Targeted | Shadow targets whichever player card is played most often. |
| Possession | Corrupt | Corrupt 2 player cards. |
| Cannot Let Go | Drain | Player loses 3 energy over 3 turns (1/turn). |
| The Final Thought | Win-condition | If Shadow plays this 3 times, player's deck is corrupted. |

**Icon**: Infinity loop, broken in the middle  
**Flavor text style**: *"I thought about you constantly. Every single day."*  
**Color**: Invasive purple bleeding inward from all edges

---

## SHADOW CARD — FLIP ANIMATION

When Shadow plays a card, it animates from face-down to face-up:

```css
@keyframes shadow-card-flip {
  0%   { transform: rotateY(0deg);    filter: brightness(0.3); }
  40%  { transform: rotateY(90deg);   filter: brightness(0.1); }
  60%  { transform: rotateY(-90deg);  filter: brightness(0.1); }
  100% { transform: rotateY(0deg);    filter: brightness(1.0); }
}

.shadow-card-playing {
  animation: shadow-card-flip 0.5s ease-in-out forwards;
  /* Card back shows first 40%, then switches to face side at midpoint */
}
```

A dark energy effect (radial pulse) accompanies the card landing on the table.

---

## SHADOW CARD — HOVER PREVIEW

Player can hover shadow cards ON the table to see full card details.  
A tooltip appears above the table showing the full card face (at `1.3×` scale).  
Shadow cards cannot be hovered in Shadow's hand (face-down).

---

## SHADOW MARK (HEADER ELEMENT)

Instead of rarity gems, shadow cards have a **Shadow Mark** — a small glyph:

- **Dark Mark** (common): `⬟` hollow dark pentagon
- **Cursed Mark** (rare): `⬟` filled, glowing
- **Abyssal Mark** (mythic): `⬟` with rotating ring and constant glow

---

## SHADOW CARD BACK

Shadow's hand is always face-down to player.  
Shadow card back design:

- Background: `#020108` (near-absolute black, slightly purple)
- Pattern: Inverse eclipse — solid black sun, revealed white ring around it
- Tiled at `20px`, `opacity: 0.05`
- Central image: The Shadow's eye (glowing white slits), `opacity: 0.25`
- Border: `1px solid rgba(120, 40, 180, 0.25)`
- Subtle animation: Eye glow pulses slowly (2.5s cycle)

Psychologically, the face-down card backs feel like the Shadow is watching.
