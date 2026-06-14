# SHADOWSELF — MASTER GAME BIBLE
### Build Small Hackathon Edition · Single Source of Truth

> Feed this file into any coding agent (Cursor, Claude Code, Codex, Gemini) to reproduce consistent results.

---

## 0. NORTH STAR

SHADOWSELF is a **short, highly-polished AI-native psychological card duel**.  
Duration: **5–10 minutes per run**.  
Platform: **Gradio app hosted on Hugging Face Spaces**.  
The AI is not an assistant. The AI **is** the game.

---

## 1. HACKATHON CONSTRAINTS

| Constraint | Requirement |
|---|---|
| Framework | Gradio |
| Host | Hugging Face Space |
| Models | Small models only (≤ 7B params, or API-accessible free tier) |
| AI centrality | AI generates: cards, shadow, dialogue, endings — nothing is hand-authored |
| Completability | One sitting, under 10 minutes |
| Shareability | Final summary card must be screenshot-worthy |

---

## 2. EXPERIENCE FLOW

```
LOADING SCREEN
    ↓
CAMERA CAPTURE
    ↓  (player takes webcam photo)
SILHOUETTE TRANSFORM
    ↓  (photo → shadow silhouette with animation)
DIALOGUE PROLOGUE  [AI-generated, 3 lines from Shadow]
    ↓
MIRROR TABLE BATTLE  [18 player cards vs 18 shadow cards]
    ↓
AI ENDING SUMMARY  [personalized psychological reflection]
    ↓
SHARE SCREEN
```

---

## 3. PLAYER EMOTION ARC

```
CURIOSITY → UNEASE → RECOGNITION → CONFLICT → REFLECTION
```

This arc supersedes mechanical complexity. Winning is secondary to feeling.

---

## 4. CARD SYSTEM SPECIFICATION

### 4.1 Card Structure (JSON Schema)

```json
{
  "id": "string (uuid)",
  "name": "string",
  "archetype": "Courage|Hope|Kindness|Resolve|Trust|Acceptance|Fear|Rage|Doubt|Jealousy|Despair|Obsession",
  "flavor_text": "string (1 sentence, psychologically resonant)",
  "cost": "integer 0–3",
  "effects": {
    "attack": "integer 0–10",
    "heal": "integer 0–10",
    "armor": "integer 0–10",
    "draw": "integer 0–3"
  },
  "pure_description": "string",
  "corrupted_description": "string",
  "corrupted_effects": {
    "attack": "integer 0–10",
    "heal": "integer 0–10",
    "armor": "integer 0–10",
    "draw": "integer 0–3",
    "self_damage": "integer 0–10",
    "enemy_heal": "integer 0–10"
  },
  "is_corrupted": "boolean",
  "rarity": "common|rare|mythic",
  "visual_variant": "string (CSS class or asset key)"
}
```

### 4.2 Generation Rules

- **18 Player Cards** per run, across 6 archetypes (3 per archetype)
- **18 Shadow Cards** per run, across 6 shadow archetypes (3 per archetype)
- AI generates `name`, `flavor_text`, `effects`, `descriptions` — never raw code
- AI output is **structured JSON only** — no freeform, no executable
- Values MUST stay within ranges above; AI must be prompted with explicit constraints
- Same archetype must feel different between runs (variant naming required)

### 4.3 Corruption Logic

Every player card has a corrupted state. Corrupted effects must be **psychologically inverse**:

| Pure Effect | Corrupted Effect |
|---|---|
| Heal self | Heal enemy |
| Draw cards | Discard cards |
| Gain armor | Lose armor |
| Deal damage | Take self-damage |
| Gain energy | Lose energy |

Corruption trigger: Shadow plays `Corrupt` mechanic card, or player's HP drops below 30%.

---

## 5. BATTLE RULES

### 5.1 Stats

| Stat | Player | Shadow |
|---|---|---|
| HP | 50 | 50 |
| Energy/turn | 3 | 3 |
| Hand size | 5 | — (Shadow auto-plays) |
| Deck size | 18 | 18 |

### 5.2 Turn Structure

1. Player draws to hand size (5)
2. Player plays cards (spend energy)
3. Player ends turn
4. Shadow draws + plays 1–3 cards (AI-selected, personality-driven)
5. Effects resolve
6. Next turn begins

### 5.3 Win/Lose Conditions

- **Player wins**: Shadow HP ≤ 0
- **Player loses**: Player HP ≤ 0
- Both outcomes lead to the **AI Ending Summary** — wording changes, game always completes

### 5.4 Shadow AI Behavior

Shadow card selection is governed by its personality type:

| Personality | Card Preference |
|---|---|
| The Accuser | High attack, targets player's strongest card |
| The Watcher | Mirrors player's last move |
| The Mourner | Despair/Obsession cards, low attack, high drain |
| The Tyrant | Always plays max-cost cards, brute force |
| The Forgotten One | Erratic, corrupts player cards |

---

## 6. SHADOW PERSONALITY SYSTEM

Shadow personality is determined by:
1. Player dialogue responses (pre-battle prompts)
2. First 5 cards player chooses to play
3. Whether player uses Kindness vs Rage archetypes

The AI must assign ONE of the 5 personality types and maintain it throughout the battle.  
All Shadow dialogue must be consistent with the assigned personality.

---

## 7. ENDING SYSTEM

The AI analyzes post-battle data:

```json
{
  "cards_played": ["list of card names/archetypes"],
  "cards_avoided": ["list of cards never played"],
  "corruptions_triggered": "integer",
  "dialogue_choices": ["list of player choices"],
  "battle_outcome": "win|loss",
  "turns_taken": "integer",
  "shadow_personality": "string"
}
```

The ending is a **3–5 paragraph personal reflection**, written as if the Shadow is speaking its final words.  
Tone: elegiac, not congratulatory. Memorable, screenshot-worthy.  
Never use generic phrases like "You have won" or "You have lost."

---

## 8. TECHNICAL ARCHITECTURE

```
shadowself/
├── app.py                    # Gradio entry point
├── requirements.txt
├── .env.example
├── docs/                     # Asset specifications (this folder)
├── src/
│   ├── ai/
│   │   ├── card_generator.py     # LLM → structured card JSON
│   │   ├── shadow_engine.py      # Shadow personality + dialogue
│   │   ├── ending_generator.py   # Post-battle reflection
│   │   └── prompt_templates.py   # All LLM prompts
│   ├── game/
│   │   ├── battle.py             # Turn logic, state machine
│   │   ├── card.py               # Card dataclass + validation
│   │   └── deck.py               # Deck management
│   ├── vision/
│   │   └── silhouette.py         # Webcam → silhouette transform
│   └── ui/
│       ├── html_screens.py       # HTML string generators for all screens
│       ├── styles.py             # Custom CSS injection
│       └── js_bridge.py          # JavaScript for animations and Gradio events
└── assets/
    ├── fonts/
    ├── icons/
    └── sounds/                  # Optional ambient audio
```

---

## 9. MODEL SELECTION

| Task | Model | Rationale |
|---|---|---|
| Card generation | `mistralai/Mistral-7B-Instruct-v0.3` or `HuggingFaceH4/zephyr-7b-beta` | JSON structured output, fast |
| Shadow dialogue | Same as above | Consistent tone |
| Ending summary | `meta-llama/Meta-Llama-3-8B-Instruct` | Better prose quality |
| Silhouette | `rembg` (library, no model download) | Background removal |

Use `InferenceClient` from `huggingface_hub` for all model calls.  
Use `response_format={"type": "json_object"}` where supported.  
Fallback: parse JSON from freeform response with regex extraction.

---

## 10. DESIGN PRINCIPLES (NON-NEGOTIABLE)

1. **Never feel like a card game.** It must feel like a ritual.
2. **Every AI output is unique.** No two runs produce the same cards, dialogue, or endings.
3. **Emotion before mechanics.** If a feature doesn't serve the emotional arc, cut it.
4. **The Shadow is always the focal point.** All visual hierarchy serves the Shadow.
5. **The ending must be shareable.** Design every run around this moment.

---

## 11. ASSET FILE INDEX

| File | Purpose |
|---|---|
| `docs/asset_loading_screen.md` | Loading screen visual specification |
| `docs/asset_shadow_portrait.md` | Shadow boss visual specification |
| `docs/asset_mirror_table.md` | Battle arena specification |
| `docs/asset_player_cards.md` | Player card design specification |
| `docs/asset_shadow_cards.md` | Shadow card design specification |
| `docs/asset_battle_background.md` | Background environment specification |
| `docs/asset_final_summary.md` | Ending card visual specification |
| `docs/asset_camera_capture.md` | Webcam UI specification |
| `docs/asset_ui_system.md` | Full UI kit specification |

---

*This document is the single source of truth. Any conflict between this file and other files should resolve in favor of this file.*
