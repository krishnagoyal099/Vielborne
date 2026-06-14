"""
prompt_templates.py — All LLM prompt strings for SHADOWSELF.

Every prompt enforces strict JSON output with explicit value constraints.
The system prompts are intentionally terse to fit within small model context windows.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Card generation prompt
# ---------------------------------------------------------------------------

def card_generation_prompt(archetype: str, is_shadow: bool, count: int = 3) -> str:
    """
    Returns the full prompt for generating `count` cards of the given archetype.

    Args:
        archetype: e.g. "Courage", "Fear"
        is_shadow: True for shadow archetypes
        count:     Number of cards to generate (default 3)
    """
    side = "shadow" if is_shadow else "player"

    if is_shadow:
        tone = (
            "Dark, sorrowful, and unsettling. Shadow cards feel like wounds — "
            "they drain, corrupt, and diminish. The flavor text is written in first person "
            "as if the shadow itself is speaking."
        )
        effect_guide = (
            "Shadow cards primarily attack, drain energy, corrupt player cards, "
            "or heal the shadow. They should NOT heal the player."
        )
    else:
        tone = (
            "Psychologically resonant and personal. Player cards feel like acts of will — "
            "they defend, restore, and empower. The flavor text reflects a hard-won truth."
        )
        effect_guide = (
            "Player cards primarily deal damage, heal the player, grant armor, or draw cards. "
            "Corrupted effects must be the PSYCHOLOGICAL INVERSE of the pure effect: "
            "heal → enemy_heal, draw → discard (set draw to 0 in corrupted_effects and self_damage to cards count), "
            "armor → set armor to 0 in corrupted_effects and add self_damage, "
            "attack → self_damage."
        )

    return f"""You generate cards for a psychological card game called SHADOWSELF.
Generate exactly {count} unique {side} cards for the "{archetype}" archetype.

RULES:
- Each card must have a unique variant name (NOT the archetype word itself).
  Example variants for Courage: Defiance, Bravery, Persistence, Conviction, Tenacity
- Flavor text: 1 sentence, haunting and personal. No generic clichés.
- Tone: {tone}
- Effects: {effect_guide}
- All numeric values MUST be within these ranges:
  cost: 0-3, attack: 0-10, heal: 0-10, armor: 0-10, draw: 0-3,
  self_damage: 0-10, enemy_heal: 0-10
- rarity: distribute roughly as common/common/rare or common/rare/mythic

Return ONLY a valid JSON array. No explanation. No markdown. No extra text.

FORMAT:
[
  {{
    "name": "Defiance",
    "archetype": "{archetype}",
    "flavor_text": "One sentence here.",
    "cost": 2,
    "effects": {{"attack": 7, "heal": 0, "armor": 0, "draw": 0}},
    "pure_description": "Deal 7 damage.",
    "corrupted_description": "Deal 7 damage to yourself instead.",
    "corrupted_effects": {{"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 7, "enemy_heal": 0}},
    "rarity": "rare"
  }}
]"""


# ---------------------------------------------------------------------------
# Shadow personality assignment + intro monologue
# ---------------------------------------------------------------------------

SHADOW_PERSONALITY_PROMPT = """You are the Shadow in the psychological card game SHADOWSELF.
Based on the player's responses below, assign ONE personality type from this list:
- The Accuser (aggressive, blames the player, confrontational)
- The Watcher (silent, observant, mirrors the player's actions)
- The Mourner (sorrowful, grieving, speaks of loss and regret)
- The Tyrant (domineering, overwhelming, raw power)
- The Forgotten One (erratic, fractured, speaks in broken sentences)

Then write exactly 3 lines of opening dialogue as that personality.
The dialogue should feel intelligent, unsettling, and deeply personal.
Never say "You have won" or "You have lost." Never be generic.
Write as the Shadow speaking directly to the player.

Player responses: {responses}

Return ONLY valid JSON. No extra text.

FORMAT:
{{
  "personality": "The Accuser",
  "intro_lines": [
    "First line of opening dialogue.",
    "Second line.",
    "Third line."
  ]
}}"""


# ---------------------------------------------------------------------------
# Shadow battle dialogue (called once per turn)
# ---------------------------------------------------------------------------

def shadow_dialogue_prompt(personality: str, turn: int, player_hp: int,
                            shadow_hp: int, last_player_card: str,
                            battle_outcome: str = "") -> str:
    """
    Generate one contextual dialogue line from the Shadow during battle.

    Args:
        personality:      Shadow's assigned personality.
        turn:             Current turn number.
        player_hp:        Player's current HP.
        shadow_hp:        Shadow's current HP.
        last_player_card: Name of the last card the player played.
        battle_outcome:   "win" | "loss" | "" (still in battle)
    """
    context = f"""Turn {turn}. Player HP: {player_hp}/50. Shadow HP: {shadow_hp}/50.
Last card played by player: {last_player_card or "none yet"}.
Battle outcome: {battle_outcome or "ongoing"}."""

    personality_voice = {
        "The Accuser":      "Accusatory, incisive. Points out the player's flaws and choices. Never wrong.",
        "The Watcher":      "Quiet. Observational. Speaks in short, knowing sentences. Never raises its voice.",
        "The Mourner":      "Sorrowful. Speaks of what was lost. Sometimes trails off mid-sentence.",
        "The Tyrant":       "Commanding. Overwhelming. Speaks as if the outcome is already decided.",
        "The Forgotten One": "Fractured. Incomplete thoughts. Sometimes repeats a word. Unsettling rhythm.",
    }.get(personality, "Calm and unsettling.")

    return f"""You are the Shadow in SHADOWSELF. Your personality: {personality}.
Voice: {personality_voice}

Context: {context}

Write EXACTLY ONE line of dialogue (1-2 sentences max). 
It must feel intelligent and deeply personal. Not generic.
Reference the game context subtly.

Return ONLY valid JSON:
{{"line": "Your single dialogue line here."}}"""


# ---------------------------------------------------------------------------
# Ending reflection
# ---------------------------------------------------------------------------

def ending_prompt(
    shadow_personality: str,
    battle_outcome: str,
    turns_taken: int,
    cards_played: list,
    cards_avoided: list,
    corruptions_triggered: int,
    most_used_archetype: str,
    least_used_archetype: str,
    dialogue_choices: list,
) -> str:
    """Generate the final psychological reflection from the Shadow."""

    outcome_note = (
        "The player defeated you." if battle_outcome == "win"
        else "You overwhelmed the player."
    )

    return f"""You are the Shadow in the psychological card game SHADOWSELF, speaking your final words.
{outcome_note}

BATTLE DATA:
- Your personality: {shadow_personality}
- Turns endured: {turns_taken}
- Cards the player used: {', '.join(cards_played[:10]) if cards_played else 'none'}
- Cards the player never touched: {', '.join(cards_avoided[:5]) if cards_avoided else 'none'}
- Times the player's cards were corrupted: {corruptions_triggered}
- Archetype used most: {most_used_archetype or 'unknown'}
- Archetype used least: {least_used_archetype or 'unknown'}
- Player's pre-battle responses: {'; '.join(dialogue_choices) if dialogue_choices else 'none'}

Write a psychological reflection of 3-4 paragraphs spoken by the Shadow.
Tone: elegiac, personal, haunting. Not congratulatory. Not angry.
Reference specific cards or choices where meaningful.
The final paragraph should end with a question or an unresolved observation.
NEVER say "You have won," "You have lost," "Congratulations," or "Game over."
Write as if the Shadow knows the player intimately — because it does.

Return ONLY valid JSON:
{{"reflection": "Full 3-4 paragraph text here. Paragraphs separated by \\n\\n."}}"""
