"""
shadow_engine.py — Shadow personality assignment and dialogue generation.

The Shadow's personality is determined once per run and influences
all dialogue and battle card selection logic.
"""

from __future__ import annotations
import json
import os
import re
import logging
import random
from typing import List, Optional

from src.ai.prompt_templates import SHADOW_PERSONALITY_PROMPT, shadow_dialogue_prompt

logger = logging.getLogger(__name__)

HF_MODEL = os.getenv("HF_MODEL", "google/gemini-2.5-flash")

PERSONALITIES = [
    "The Accuser",
    "The Watcher",
    "The Mourner",
    "The Tyrant",
    "The Forgotten One",
]

# ---------------------------------------------------------------------------
# Fallback dialogue pools (one per personality)
# ---------------------------------------------------------------------------

FALLBACK_INTRO: dict[str, List[str]] = {
    "The Accuser": [
        "You came here like you come everywhere — hoping to leave before it gets real.",
        "I have watched you make the same choice a hundred times. Today is no different.",
        "Let's see what you do when you can't look away.",
    ],
    "The Watcher": [
        "I have been waiting here.",
        "I have seen everything you think no one noticed.",
        "We can begin.",
    ],
    "The Mourner": [
        "Do you know how long I have carried this?",
        "I did not ask to be made of everything you refused to feel.",
        "I am not angry. I am tired. There is a difference.",
    ],
    "The Tyrant": [
        "You thought silence was a kind of strength. It was not.",
        "Everything you avoided came to me. I made use of it.",
        "This ends when I decide it ends.",
    ],
    "The Forgotten One": [
        "You — you forgot. I remember. I remember everything.",
        "The name you had for me. Did you think — did you think that would work?",
        "I am still. Here. Still here.",
    ],
}

FALLBACK_BATTLE_LINES: dict[str, List[str]] = {
    "The Accuser": [
        "You play that card and call it strength. I call it avoidance.",
        "That's the third time you've reached for the same answer.",
        "You keep choosing the cards that don't cost you anything real.",
        "I notice you haven't touched the ones that require something of you.",
        "Convenient, the cards you leave unplayed.",
    ],
    "The Watcher": [
        "I see you.",
        "That choice tells me more than you intended.",
        "You always do this when you're afraid.",
        "Interesting.",
        "Keep going. I'm learning.",
    ],
    "The Mourner": [
        "I used to hope too. I want you to know that.",
        "Every card you play costs something. You just don't feel it yet.",
        "I carried this alone for so long.",
        "Does it hurt? It should. It should mean something.",
        "We were the same, once.",
    ],
    "The Tyrant": [
        "Is that the best you have?",
        "You hesitated. I don't.",
        "Strength is the only language I respect. Try harder.",
        "Everything you hold back makes me stronger.",
        "You cannot outlast me. You never could.",
    ],
    "The Forgotten One": [
        "You — you played that. I remember when you — when you used to.",
        "Does this feel like the right — the right card? Does it?",
        "I was there. I was always — always there.",
        "Almost. Almost right. Almost — no.",
        "You forgot. But I. I did not.",
    ],
}

FALLBACK_VICTORY_LINES: dict[str, List[str]] = {
    "The Accuser": ["You won this. You won it doing exactly what you always do. Think about that."],
    "The Watcher": ["You saw me. I wonder if you saw yourself."],
    "The Mourner": ["It's alright. You can go now. I'll be fine here."],
    "The Tyrant": ["You beat me. I will give you that. It changes nothing else."],
    "The Forgotten One": ["You — you won. I will — I will try to remember that."],
}

FALLBACK_DEFEAT_LINES: dict[str, List[str]] = {
    "The Accuser": ["You see? You always knew this was how it would go."],
    "The Watcher": ["I watched you try. That matters. It won't feel like it does, but it matters."],
    "The Mourner": ["Rest. You carried it for a long time. Rest."],
    "The Tyrant": ["You gave everything. I simply had more."],
    "The Forgotten One": ["Don't — don't go. Not yet. I haven't — I haven't finished."],
}


class ShadowEngine:
    """
    Manages the Shadow's personality and generates all its dialogue.

    Personality is assigned once and persists for the full run.
    Dialogue falls back to curated pools if the LLM is unavailable.
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
            except Exception as e:
                logger.warning("ShadowEngine: HF client init failed: %s", e)

    def assign_personality(self, player_responses: List[str]) -> tuple[str, List[str]]:
        """
        Determine the Shadow's personality from pre-battle player dialogue choices.

        Args:
            player_responses: List of strings the player chose/typed before battle.

        Returns:
            (personality_name, [intro_line_1, intro_line_2, intro_line_3])
        """
        if self._client and player_responses:
            try:
                return self._assign_via_api(player_responses)
            except Exception as e:
                logger.warning("Shadow personality API call failed: %s", e)

        return self._assign_fallback(player_responses)

    def get_battle_line(
        self,
        personality: str,
        turn: int,
        player_hp: int,
        shadow_hp: int,
        last_player_card: str,
        battle_outcome: str = "",
    ) -> str:
        """
        Get one line of Shadow dialogue for the current battle state.

        Returns a plain string (the dialogue line).
        """
        if self._client:
            try:
                prompt = shadow_dialogue_prompt(
                    personality, turn, player_hp,
                    shadow_hp, last_player_card, battle_outcome
                )
                response = self._client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are the Shadow in SHADOWSELF. "
                                "You output ONLY valid JSON with a 'line' key. No extra text."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=120,
                    temperature=0.9,
                )
                raw = response.choices[0].message.content or ""
                result = self._extract_json_field(raw, "line")
                if result:
                    return result
            except Exception as e:
                logger.warning("Shadow battle dialogue API failed: %s", e)

        # Fallback pool
        if battle_outcome == "win":
            pool = FALLBACK_VICTORY_LINES.get(personality, ["..."])
        elif battle_outcome == "loss":
            pool = FALLBACK_DEFEAT_LINES.get(personality, ["..."])
        else:
            pool = FALLBACK_BATTLE_LINES.get(personality, ["..."])

        return random.choice(pool)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _assign_via_api(self, responses: List[str]) -> tuple[str, List[str]]:
        prompt = SHADOW_PERSONALITY_PROMPT.format(responses="; ".join(responses))
        response = self._client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the Shadow in SHADOWSELF. "
                        "You output ONLY valid JSON. No explanation. No extra text."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,
            temperature=0.8,
        )
        raw = response.choices[0].message.content or ""
        data = self._extract_json_object(raw)
        personality = data.get("personality", "")
        intro_lines = data.get("intro_lines", [])

        if personality not in PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        if len(intro_lines) < 3:
            raise ValueError("Not enough intro lines")

        return personality, intro_lines[:3]

    def _assign_fallback(self, responses: List[str]) -> tuple[str, List[str]]:
        """Deterministically pick personality based on response keywords."""
        combined = " ".join(responses).lower()

        if any(w in combined for w in ["blame", "fault", "wrong", "why"]):
            p = "The Accuser"
        elif any(w in combined for w in ["watch", "see", "notice", "quiet"]):
            p = "The Watcher"
        elif any(w in combined for w in ["sad", "loss", "miss", "regret", "sorry"]):
            p = "The Mourner"
        elif any(w in combined for w in ["power", "control", "win", "strong", "force"]):
            p = "The Tyrant"
        elif any(w in combined for w in ["forget", "remember", "lost", "confused", "broken"]):
            p = "The Forgotten One"
        else:
            p = random.choice(PERSONALITIES)

        return p, list(FALLBACK_INTRO[p])

    def _extract_json_object(self, text: str) -> dict:
        text = text.strip()
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return {}

    def _extract_json_field(self, text: str, field: str) -> Optional[str]:
        data = self._extract_json_object(text)
        return data.get(field)
