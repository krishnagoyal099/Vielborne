"""
card_generator.py — LLM → structured Card JSON with curated fallbacks.

Three-layer reliability system:
  1. HuggingFace Inference API (primary)
  2. JSON extraction from freeform text (if structured output fails)
  3. Curated hand-authored card templates (if API fails entirely)
"""

from __future__ import annotations
import json
import os
import re
import logging
import random
from typing import List, Optional

from src.game.card import Card, CardEffect, CorruptedEffect, PLAYER_ARCHETYPES, SHADOW_ARCHETYPES
from src.ai.prompt_templates import card_generation_prompt

logger = logging.getLogger(__name__)

HF_MODEL = os.getenv("HF_MODEL", "google/gemini-2.5-flash")


# ---------------------------------------------------------------------------
# Curated fallback card templates
# ---------------------------------------------------------------------------

FALLBACK_CARDS: dict[str, List[dict]] = {
    "Courage": [
        {"name": "Defiance",    "archetype": "Courage", "cost": 2, "rarity": "rare",
         "flavor_text": "The loudest voice in the room is the one that refused to stay silent.",
         "effects": {"attack": 7, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 7 damage.",
         "corrupted_description": "Deal 7 damage to yourself.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 7, "enemy_heal": 0}},
        {"name": "Bravery",     "archetype": "Courage", "cost": 1, "rarity": "common",
         "flavor_text": "It costs something to stand up. It costs more to stay down.",
         "effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 1},
         "pure_description": "Deal 5 damage. Draw 1 card.",
         "corrupted_description": "Take 5 damage. Discard 1 card.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 5, "enemy_heal": 0}},
        {"name": "Conviction",  "archetype": "Courage", "cost": 3, "rarity": "mythic",
         "flavor_text": "You cannot be broken if you never finish breaking.",
         "effects": {"attack": 10, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 10 damage.",
         "corrupted_description": "Deal 10 damage to yourself.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 10, "enemy_heal": 0}},
    ],
    "Hope": [
        {"name": "Dawn",        "archetype": "Hope", "cost": 1, "rarity": "common",
         "flavor_text": "Something always follows the dark. You just have to stay long enough to see it.",
         "effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 2},
         "pure_description": "Draw 2 cards.",
         "corrupted_description": "Discard 2 cards.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Renewal",     "archetype": "Hope", "cost": 2, "rarity": "rare",
         "flavor_text": "The wound heals whether you believe it will or not.",
         "effects": {"attack": 0, "heal": 6, "armor": 0, "draw": 1},
         "pure_description": "Heal 6 HP. Draw 1 card.",
         "corrupted_description": "Lose 6 HP. Discard 1 card.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 6, "enemy_heal": 0}},
        {"name": "Promise",     "archetype": "Hope", "cost": 0, "rarity": "common",
         "flavor_text": "You told yourself tomorrow. Tomorrow believed you.",
         "effects": {"attack": 0, "heal": 4, "armor": 0, "draw": 0},
         "pure_description": "Heal 4 HP.",
         "corrupted_description": "Heal the Shadow for 4 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 4}},
    ],
    "Kindness": [
        {"name": "Mercy",       "archetype": "Kindness", "cost": 2, "rarity": "common",
         "flavor_text": "You gave before you were asked. That's the part they never mention.",
         "effects": {"attack": 0, "heal": 8, "armor": 0, "draw": 0},
         "pure_description": "Heal 8 HP.",
         "corrupted_description": "Heal the Shadow 8 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 8}},
        {"name": "Compassion",  "archetype": "Kindness", "cost": 2, "rarity": "rare",
         "flavor_text": "To feel what another feels is to carry twice the weight.",
         "effects": {"attack": 0, "heal": 5, "armor": 3, "draw": 0},
         "pure_description": "Heal 5 HP. Gain 3 armor.",
         "corrupted_description": "Lose 5 HP. Lose 3 armor.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 5, "enemy_heal": 0}},
        {"name": "Shelter",     "archetype": "Kindness", "cost": 1, "rarity": "common",
         "flavor_text": "You made room when there was none. Where is your room?",
         "effects": {"attack": 0, "heal": 0, "armor": 6, "draw": 0},
         "pure_description": "Gain 6 armor.",
         "corrupted_description": "Lose 6 armor.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 6, "enemy_heal": 0}},
    ],
    "Resolve": [
        {"name": "Fortitude",   "archetype": "Resolve", "cost": 1, "rarity": "common",
         "flavor_text": "The spine bends. It does not break. Not yet.",
         "effects": {"attack": 0, "heal": 0, "armor": 7, "draw": 0},
         "pure_description": "Gain 7 armor.",
         "corrupted_description": "Lose all armor.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 4, "enemy_heal": 0}},
        {"name": "Grit",        "archetype": "Resolve", "cost": 2, "rarity": "rare",
         "flavor_text": "You are still here. That is not nothing.",
         "effects": {"attack": 4, "heal": 0, "armor": 4, "draw": 0},
         "pure_description": "Deal 4 damage. Gain 4 armor.",
         "corrupted_description": "Take 4 damage. Lose 4 armor.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 4, "enemy_heal": 0}},
        {"name": "Steadfast",   "archetype": "Resolve", "cost": 2, "rarity": "common",
         "flavor_text": "Staying is its own kind of bravery.",
         "effects": {"attack": 0, "heal": 3, "armor": 5, "draw": 0},
         "pure_description": "Heal 3 HP. Gain 5 armor.",
         "corrupted_description": "Lose 3 HP. Lose 5 armor.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 3, "enemy_heal": 0}},
    ],
    "Trust": [
        {"name": "Belief",      "archetype": "Trust", "cost": 1, "rarity": "common",
         "flavor_text": "You opened your hands. It was the hardest thing you have ever done.",
         "effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 3},
         "pure_description": "Draw 3 cards.",
         "corrupted_description": "Discard 3 cards.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Faith",       "archetype": "Trust", "cost": 2, "rarity": "rare",
         "flavor_text": "Faith is not certainty. It is choosing to move anyway.",
         "effects": {"attack": 0, "heal": 10, "armor": 0, "draw": 0},
         "pure_description": "Heal 10 HP.",
         "corrupted_description": "Heal the Shadow 10 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 10}},
        {"name": "Bond",        "archetype": "Trust", "cost": 2, "rarity": "common",
         "flavor_text": "You gave someone the blade and asked them not to use it.",
         "effects": {"attack": 4, "heal": 4, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage. Heal 4 HP.",
         "corrupted_description": "Take 4 damage. Heal the Shadow 4 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 4, "enemy_heal": 4}},
    ],
    "Acceptance": [
        {"name": "Stillness",   "archetype": "Acceptance", "cost": 0, "rarity": "common",
         "flavor_text": "Some things cannot be undone. That is not the same as wrong.",
         "effects": {"attack": 0, "heal": 0, "armor": 3, "draw": 0},
         "pure_description": "Gain 3 armor. (Free)",
         "corrupted_description": "Lose 3 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 3, "enemy_heal": 0}},
        {"name": "Release",     "archetype": "Acceptance", "cost": 0, "rarity": "common",
         "flavor_text": "You put it down. You do not know if you will pick it up again.",
         "effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 1},
         "pure_description": "Draw 1 card. (Free)",
         "corrupted_description": "Discard 1 card.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Peace",       "archetype": "Acceptance", "cost": 0, "rarity": "rare",
         "flavor_text": "Not the absence of pain. The decision to stop feeding it.",
         "effects": {"attack": 0, "heal": 5, "armor": 0, "draw": 0},
         "pure_description": "Heal 5 HP. (Free)",
         "corrupted_description": "Heal the Shadow 5 HP.",
         "corrupted_effects": {"attack": 0, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 5}},
    ],
    "Fear": [
        {"name": "Paralysis",   "archetype": "Fear", "cost": 1, "rarity": "common",
         "flavor_text": "I have lived in your chest for years. You never introduced me.",
         "effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage.",
         "corrupted_description": "Deal 4 damage.",
         "corrupted_effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Dread",       "archetype": "Fear", "cost": 2, "rarity": "rare",
         "flavor_text": "What you feared most was never the dark. It was what might be in it.",
         "effects": {"attack": 6, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 6 damage.",
         "corrupted_description": "Deal 6 damage.",
         "corrupted_effects": {"attack": 6, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Exposure",    "archetype": "Fear", "cost": 2, "rarity": "common",
         "flavor_text": "You were seen. That was always what you could not survive.",
         "effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 2},
         "pure_description": "Deal 3 damage. Player discards 2 cards.",
         "corrupted_description": "Deal 3 damage. Player discards 2 cards.",
         "corrupted_effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 2, "self_damage": 0, "enemy_heal": 0}},
    ],
    "Rage": [
        {"name": "Outburst",    "archetype": "Rage", "cost": 2, "rarity": "rare",
         "flavor_text": "I held your anger for you. I held it until it became me.",
         "effects": {"attack": 9, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 9 damage.",
         "corrupted_description": "Deal 9 damage.",
         "corrupted_effects": {"attack": 9, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Resentment",  "archetype": "Rage", "cost": 1, "rarity": "common",
         "flavor_text": "You said it was fine. I kept score.",
         "effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 5 damage.",
         "corrupted_description": "Deal 5 damage.",
         "corrupted_effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Breaking Point", "archetype": "Rage", "cost": 3, "rarity": "mythic",
         "flavor_text": "You called it losing control. I call it the first honest thing you ever did.",
         "effects": {"attack": 10, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 10 damage.",
         "corrupted_description": "Deal 10 damage.",
         "corrupted_effects": {"attack": 10, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
    ],
    "Doubt": [
        {"name": "Hesitation",  "archetype": "Doubt", "cost": 1, "rarity": "common",
         "flavor_text": "For every step you took, I asked: but what if you're wrong?",
         "effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 3 damage. Player loses 1 energy next turn.",
         "corrupted_description": "Deal 3 damage. Player loses 1 energy next turn.",
         "corrupted_effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 1, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Unraveling",  "archetype": "Doubt", "cost": 2, "rarity": "rare",
         "flavor_text": "Nothing is as fragile as certainty.",
         "effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 5 damage.",
         "corrupted_description": "Deal 5 damage.",
         "corrupted_effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "The Voice",   "archetype": "Doubt", "cost": 2, "rarity": "rare",
         "flavor_text": "What if everything you are sure of is wrong?",
         "effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage.",
         "corrupted_description": "Deal 4 damage.",
         "corrupted_effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
    ],
    "Jealousy": [
        {"name": "Comparison",  "archetype": "Jealousy", "cost": 2, "rarity": "common",
         "flavor_text": "You gave them so much. Did you ever wonder what you took from me?",
         "effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 5 damage.",
         "corrupted_description": "Deal 5 damage.",
         "corrupted_effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Coveting",    "archetype": "Jealousy", "cost": 2, "rarity": "rare",
         "flavor_text": "I watched you hold it. I have always watched you hold things.",
         "effects": {"attack": 4, "heal": 3, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage. Shadow heals 3.",
         "corrupted_description": "Deal 4 damage. Shadow heals 3.",
         "corrupted_effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 3}},
        {"name": "The Green Wound", "archetype": "Jealousy", "cost": 1, "rarity": "common",
         "flavor_text": "You had so much and didn't notice me watching.",
         "effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 3 damage.",
         "corrupted_description": "Deal 3 damage.",
         "corrupted_effects": {"attack": 3, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
    ],
    "Despair": [
        {"name": "The Long Dark", "archetype": "Despair", "cost": 2, "rarity": "rare",
         "flavor_text": "Every time you hoped, I endured the falling.",
         "effects": {"attack": 6, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 6 damage.",
         "corrupted_description": "Deal 6 damage.",
         "corrupted_effects": {"attack": 6, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Hollow",      "archetype": "Despair", "cost": 1, "rarity": "common",
         "flavor_text": "I know what happens next. I have always known.",
         "effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage.",
         "corrupted_description": "Deal 4 damage.",
         "corrupted_effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Collapse",    "archetype": "Despair", "cost": 2, "rarity": "common",
         "flavor_text": "You kept looking up. I kept counting the distance.",
         "effects": {"attack": 5, "heal": 2, "armor": 0, "draw": 0},
         "pure_description": "Deal 5 damage. Shadow heals 2.",
         "corrupted_description": "Deal 5 damage. Shadow heals 2.",
         "corrupted_effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 2}},
    ],
    "Obsession": [
        {"name": "Return",      "archetype": "Obsession", "cost": 1, "rarity": "common",
         "flavor_text": "You let go. I never could. I became the thing you released.",
         "effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 4 damage.",
         "corrupted_description": "Deal 4 damage.",
         "corrupted_effects": {"attack": 4, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "The Loop",    "archetype": "Obsession", "cost": 2, "rarity": "rare",
         "flavor_text": "I thought about you constantly. Every single day.",
         "effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 5 damage.",
         "corrupted_description": "Deal 5 damage.",
         "corrupted_effects": {"attack": 5, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
        {"name": "Possession",  "archetype": "Obsession", "cost": 3, "rarity": "mythic",
         "flavor_text": "You are mine in a way you will never fully understand.",
         "effects": {"attack": 7, "heal": 0, "armor": 0, "draw": 0},
         "pure_description": "Deal 7 damage. Corrupt 1 player card.",
         "corrupted_description": "Deal 7 damage. Corrupt 1 player card.",
         "corrupted_effects": {"attack": 7, "heal": 0, "armor": 0, "draw": 0, "self_damage": 0, "enemy_heal": 0}},
    ],
}


# ---------------------------------------------------------------------------
# Card generator
# ---------------------------------------------------------------------------

class CardGenerator:
    """
    Generates all 36 cards (18 player + 18 shadow) for a SHADOWSELF run.

    Primary:  HuggingFace Inference API with zephyr-7b-beta
    Fallback: Curated templates (always unique via name shuffling)
    """

    def __init__(self, hf_token: Optional[str] = None) -> None:
        self.hf_token = hf_token or os.getenv("HF_TOKEN", "")
        self._client = None
        if self.hf_token:
            try:
                from huggingface_hub import InferenceClient
                self._client = InferenceClient(
                    model=HF_MODEL,
                    token=self.hf_token,
                )
                logger.info("HF InferenceClient initialized with model: %s", HF_MODEL)
            except Exception as e:
                logger.warning("Failed to initialize HF client: %s", e)

    def generate_all(self) -> tuple[List[Card], List[Card]]:
        """
        Generate all player and shadow cards.

        Returns:
            (player_cards, shadow_cards) — each a list of 18 Card objects.
        """
        player_cards: List[Card] = []
        shadow_cards: List[Card] = []

        for archetype in PLAYER_ARCHETYPES:
            cards = self._generate_archetype(archetype, is_shadow=False)
            player_cards.extend(cards)

        for archetype in SHADOW_ARCHETYPES:
            cards = self._generate_archetype(archetype, is_shadow=True)
            shadow_cards.extend(cards)

        return player_cards, shadow_cards

    def _generate_archetype(self, archetype: str, is_shadow: bool) -> List[Card]:
        """Generate 3 cards for one archetype, with fallback."""
        if self._client:
            try:
                return self._generate_via_api(archetype, is_shadow)
            except Exception as e:
                logger.warning("API card generation failed for %s: %s — using fallback.", archetype, e)

        return self._fallback_cards(archetype)

    def _generate_via_api(self, archetype: str, is_shadow: bool) -> List[Card]:
        """Call HF API using chat_completion, parse JSON response, validate cards."""
        prompt = card_generation_prompt(archetype, is_shadow, count=3)

        response = self._client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a game designer for SHADOWSELF, a psychological card game. "
                        "You output ONLY valid JSON arrays. No explanation. No markdown. No extra text."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.85,
        )

        raw = response.choices[0].message.content or ""
        card_dicts = self._extract_json_array(raw)

        if not card_dicts:
            raise ValueError(f"No valid JSON array found in response for {archetype}")

        cards = []
        for d in card_dicts[:3]:
            try:
                card = self._dict_to_card(d)
                cards.append(card)
            except Exception as ce:
                logger.warning("Invalid card dict for %s: %s", archetype, ce)

        if not cards:
            raise ValueError(f"All cards invalid for archetype {archetype}")

        # Pad to 3 if fewer parsed
        while len(cards) < 3:
            fallback = self._fallback_cards(archetype)
            cards.append(random.choice(fallback))

        return cards[:3]

    def _dict_to_card(self, d: dict) -> Card:
        """Convert raw dict from LLM to validated Card object."""
        eff_raw = d.get("effects", {})
        ceff_raw = d.get("corrupted_effects", {})
        return Card(
            name=str(d.get("name", "Unknown")),
            archetype=str(d.get("archetype", "Courage")),
            flavor_text=str(d.get("flavor_text", "")),
            cost=int(d.get("cost", 1)),
            effects=CardEffect(
                attack=int(eff_raw.get("attack", 0)),
                heal=int(eff_raw.get("heal", 0)),
                armor=int(eff_raw.get("armor", 0)),
                draw=int(eff_raw.get("draw", 0)),
            ),
            pure_description=str(d.get("pure_description", "")),
            corrupted_description=str(d.get("corrupted_description", "")),
            corrupted_effects=CorruptedEffect(
                attack=int(ceff_raw.get("attack", 0)),
                heal=int(ceff_raw.get("heal", 0)),
                armor=int(ceff_raw.get("armor", 0)),
                draw=int(ceff_raw.get("draw", 0)),
                self_damage=int(ceff_raw.get("self_damage", 0)),
                enemy_heal=int(ceff_raw.get("enemy_heal", 0)),
            ),
            rarity=str(d.get("rarity", "common")),
        )

    def _extract_json_array(self, text: str) -> List[dict]:
        """Extract a JSON array from potentially messy LLM output."""
        # Try direct parse first
        text = text.strip()
        try:
            result = json.loads(text)
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

        # Find first [...] block that actually contains objects
        match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return []

    def _fallback_cards(self, archetype: str) -> List[Card]:
        """Return shuffled curated fallback cards for the given archetype."""
        templates = list(FALLBACK_CARDS.get(archetype, []))
        random.shuffle(templates)
        return [self._dict_to_card(t) for t in templates[:3]]
