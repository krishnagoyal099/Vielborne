# ASSET SPEC: FINAL SUMMARY CARD
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The final summary is the most important moment in the game.  
It is what players will screenshot and share.  
It must feel like **receiving a personal letter from your own subconscious**.

The design should evoke: an ancient document, a psychological evaluation, a confession.  
It should never feel like a game over screen.

---

## CONCEPTUAL REFERENCE

Imagine receiving a sealed letter in parchment, written in old ink.  
It has your name on it. It knows things about you.  
You don't know how it knows.  
You fold it and put it in your pocket.  
You think about it for days.

That is the target feeling.

---

## OVERALL LAYOUT

```
┌────────────────────────────────────────────────────────────┐
│  [SHADOWSELF SIGIL — top center, small]                    │
│                                                            │
│  ═══════════════════════════════════════════════════════   │
│                                                            │
│  PSYCHOLOGICAL REFLECTION                                  │
│  Observation Record · [Date] · Run #[N]                    │
│                                                            │
│  ─────────────────────────────────────────────────────     │
│                                                            │
│  SUBJECT OBSERVED                                          │
│  Shadow Personality: [ THE ACCUSER ]                       │
│  Battle Outcome:     [ VICTORY / DEFEAT ]                  │
│  Turns Endured:      [ 12 ]                                │
│  Cards Played:       [ 14 / 18 ]                           │
│  Cards Avoided:      [ 4 ]  — [archetype names]            │
│  Corruptions:        [ 3 triggered ]                       │
│                                                            │
│  ─────────────────────────────────────────────────────     │
│                                                            │
│  [REFLECTION TEXT — 3-5 paragraphs, AI-generated]         │
│                                                            │
│  Paragraph 1: What the Shadow saw in the player            │
│  Paragraph 2: What the avoided cards reveal               │
│  Paragraph 3: What the outcome means                      │
│  Paragraph 4: A final haunting observation                 │
│  Paragraph 5 (optional): A question left unanswered       │
│                                                            │
│  ─────────────────────────────────────────────────────     │
│                                                            │
│  [SHADOW ARCHETYPE SIGIL — small, centered]                │
│  "The mirror has been put away."                           │
│                                                            │
│  ─────────────────────────────────────────────────────     │
│                                                            │
│  [SHADOWSELF LOGO — small, bottom center]                  │
│                                            shadowself.ai   │
└────────────────────────────────────────────────────────────┘
```

---

## VISUAL DESIGN: PARCHMENT STYLE

### Card Dimensions
- Width: `680px` (desktop) / `95vw` (mobile)
- Height: Dynamic (content-driven, approximately `900px`)
- Border-radius: `6px` (slight, not rounded — parchment is stiff)

### Background Texture
The parchment effect uses layered CSS gradients — no image files needed:

```css
.final-summary-card {
  background:
    /* Subtle noise/grain texture via SVG filter */
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.04'/></svg>"),
    /* Aged parchment gradient */
    linear-gradient(
      170deg,
      #1A1428 0%,
      #150F22 30%,
      #110D1E 60%,
      #0E0B1A 100%
    );
  border: 1px solid rgba(180, 160, 220, 0.25);
  box-shadow:
    0 0 0 4px rgba(10, 8, 18, 0.8),
    0 0 60px rgba(80, 40, 140, 0.3),
    0 20px 80px rgba(0, 0, 0, 0.7);
  position: relative;
}
```

### Corner Decorations
Ornate corner decorations at all four corners using CSS:
- Thin `L`-shaped lines in silver-purple: `rgba(180, 160, 220, 0.4)`
- Each corner decoration: `20px × 20px`
- Generated with CSS `::before` / `::after` on corner elements

```css
.summary-corner {
  position: absolute;
  width: 20px;
  height: 20px;
}
.summary-corner::before,
.summary-corner::after {
  content: '';
  position: absolute;
  background: rgba(180, 160, 220, 0.4);
}
.summary-corner::before { width: 100%; height: 1px; top: 0; left: 0; }
.summary-corner::after  { width: 1px; height: 100%; top: 0; left: 0; }
/* Rotate for each corner position */
```

---

## TYPOGRAPHY SYSTEM

### Section Headers
- Font: **Cinzel** (Google Fonts)
- Size: `0.75rem`
- Letter-spacing: `0.25em`
- Color: `rgba(180, 160, 220, 0.5)`
- All caps
- Text: `PSYCHOLOGICAL REFLECTION`, `SUBJECT OBSERVED`, etc.

### Data Labels
- Font: **Cormorant Garamond** Regular
- Size: `0.85rem`
- Color: `rgba(180, 160, 220, 0.6)`
- Left-aligned

### Data Values
- Font: **Cormorant Garamond** SemiBold
- Size: `0.95rem`
- Color: `rgba(230, 220, 255, 0.9)`

### Reflection Body Text
- Font: **Cormorant Garamond** Regular
- Size: `1rem`
- Line-height: `1.8`
- Color: `rgba(210, 200, 240, 0.85)`
- First letter of Paragraph 1: Drop cap — Cinzel, `3rem`, color `rgba(180, 160, 220, 0.9)`

### Final Inscription
- Font: Cinzel Decorative
- Size: `0.7rem`
- Color: `rgba(180, 160, 220, 0.35)`
- Centered
- Letter-spacing: `0.4em`

---

## DIVIDER LINE DESIGN

Ornate horizontal dividers between sections:

```css
.summary-divider {
  position: relative;
  height: 1px;
  background: transparent;
  margin: 24px 0;
}

.summary-divider::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(180, 160, 220, 0.5) 25%,
    rgba(180, 160, 220, 0.8) 50%,
    rgba(180, 160, 220, 0.5) 75%,
    transparent
  );
}

/* Optional center diamond ornament */
.summary-divider::after {
  content: '◆';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.4rem;
  color: rgba(180, 160, 220, 0.6);
  background: #110D1E;
  padding: 0 4px;
}
```

---

## SHADOW ARCHETYPE SIGIL

A small decorative sigil representing the Shadow's personality type.  
Rendered as SVG inline, approximately `48px × 48px`:

| Personality | Sigil Design |
|---|---|
| The Accuser | Pointing finger, fractured |
| The Watcher | Open eye, no pupil |
| The Mourner | Tear-drop shape, inverted |
| The Tyrant | Crown with cracks |
| The Forgotten One | Scattered dots, dispersing |

The sigil is `opacity: 0.4` in the final card — present but not dominant.

---

## AI-GENERATED REFLECTION TEXT SPECIFICATION

The AI receives this data and generates the reflection:

```python
prompt_context = {
    "shadow_personality": "The Accuser",
    "battle_outcome": "victory",
    "turns_taken": 12,
    "cards_played": ["Defiance", "Mercy", "Stillness", "Dawn", ...],
    "cards_avoided": ["Conviction", "Surrender"],  # cards never played
    "corruptions_triggered": 3,
    "most_used_archetype": "Kindness",
    "least_used_archetype": "Trust",
    "dialogue_choices": ["I am not afraid", "I don't know", "Please stop"]
}
```

### Tone Guidelines for AI Prompt
- Write as the Shadow speaking its final words to the player
- Voice: Ancient, weary, sorrowful — not hostile
- Do NOT say "Congratulations" or "You won" or "You lost"
- Do NOT use generic self-help language
- Reference specific cards by name when meaningful
- Reference the Shadow's personality in its own voice
- Each paragraph should feel true — not invented

### Example Reflection (Target Quality)

> *You reached for Mercy when you needed it. You reached for Defiance when fear would have been honest. Three times you let the darkness shape your hand — and three times you chose not to examine why.*
>
> *The cards you never played tell me more than the ones you did. Conviction waited in your deck, untouched. Surrender was always available. You knew what they cost.*
>
> *I am not gone. I don't know why you expected that. You silenced me today, yes. But silence is not the same as peace. I will be here the next time something frightens you, the next time something reminds you of what you haven't let yourself want.*
>
> *I carry what you refuse to name. I always have. Perhaps someday you'll ask me what that's been like.*
>
> *— Your Shadow*

---

## SCREENSHOT OPTIMIZATION

The final summary must be visually clean at common screenshot resolutions:

| Platform | Optimal Width |
|---|---|
| Twitter/X | 680px |
| Instagram | 680px (square crop will show top 680px) |
| Discord | 680px |
| Mobile screenshot | 95vw, dynamic height |

**The first visible fold (top ~450px) must contain:**
- SHADOWSELF logo/sigil
- Shadow personality + outcome
- At least the first paragraph of reflection

This ensures even a cropped screenshot tells the story.

---

## ENTRY ANIMATION

The summary card appears after a `2s` black pause:

1. Card fades in from `opacity: 0` over `1.5s`
2. Background particles appear (very faint, slow drift)
3. Sections appear with `0.3s` stagger:
   - Header → Stats → Divider → Body text (word by word: typewriter effect at 30ms/word)
4. Final inscription fades in last, `opacity: 0.35`
5. Share buttons appear after text completes

### Typewriter Effect for Reflection Text
```css
/* Use CSS animation-delay stagger per word span */
.reflection-word {
  display: inline;
  opacity: 0;
  animation: word-appear 0.08s ease forwards;
}

@keyframes word-appear {
  from { opacity: 0; transform: translateY(2px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## SHARE BUTTON DESIGN

```
[ ⬡ Play Again ]    [ ↗ Share to X ]    [ ⬇ Download Image ]
```

- Font: Cinzel, `0.75rem`, letter-spacing `0.2em`
- Background: `rgba(180, 160, 220, 0.08)`, border `rgba(180, 160, 220, 0.3)`
- Hover: border brightens, subtle lift `translateY(-2px)`
- Download: Exports the summary card as a PNG via `html2canvas` or Gradio download

---

## COLOR PALETTE (SUMMARY-SPECIFIC)

```css
--summary-bg:           #110D1E;
--summary-bg-light:     #1A1428;
--summary-border:       rgba(180, 160, 220, 0.25);
--summary-divider:      rgba(180, 160, 220, 0.5);
--summary-corner:       rgba(180, 160, 220, 0.4);
--text-heading:         rgba(180, 160, 220, 0.5);
--text-label:           rgba(180, 160, 220, 0.6);
--text-value:           rgba(230, 220, 255, 0.9);
--text-body:            rgba(210, 200, 240, 0.85);
--text-inscription:     rgba(180, 160, 220, 0.35);
--dropcap-color:        rgba(180, 160, 220, 0.9);
```
