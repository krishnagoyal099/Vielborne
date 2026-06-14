"""
ending_generator.py — Generates the final psychological reflection from the Shadow.

The reflection is the most important moment in the game — it must feel
personal, haunting, and screenshot-worthy.
"""

from __future__ import annotations
import json
import os
import re
import logging
import random
from typing import List, Optional

from src.ai.prompt_templates import ending_prompt

logger = logging.getLogger(__name__)

HF_MODEL = os.getenv("HF_MODEL", "google/gemini-2.5-flash")


# ---------------------------------------------------------------------------
# Fallback reflection templates (one per personality × outcome)
# ---------------------------------------------------------------------------

FALLBACK_REFLECTIONS: dict[str, dict[str, str]] = {
    "The Accuser": {
        "win": (
            "You defeated me. You should know that it didn't surprise me.\n\n"
            "I have watched you long enough to know when you're capable of something. "
            "The question I keep returning to is why you only reach for it when there's no other choice. "
            "The cards you played most freely were the ones that cost you least. "
            "The ones gathering dust in your hand — those are the ones I'm interested in.\n\n"
            "You won this confrontation the same way you win most things: "
            "by doing just enough, just in time. "
            "I wonder if that will always be sufficient.\n\n"
            "I'll still be here. That's not a threat. It's just true. "
            "What will you do with the parts of yourself you still haven't looked at directly?"
        ),
        "loss": (
            "It's over. I want you to sit with that for a moment.\n\n"
            "Not because I want you to feel bad — I don't. "
            "But you came here and played the same cards you always play "
            "and expected a different result. "
            "I've watched you do this in life too.\n\n"
            "The cards you avoided tell me more than the ones you used. "
            "There were options you never touched. "
            "There always are.\n\n"
            "You can try again. I'll be here. "
            "I'm always here. That's the thing about shadows — "
            "we don't leave just because you stop looking."
        ),
    },
    "The Watcher": {
        "win": (
            "You saw me, finally.\n\n"
            "I have been watching you for so long that I sometimes forgot "
            "I was doing it. Your choices, repeated. Your patterns, consistent. "
            "The way you reach for the same comfort when things get difficult.\n\n"
            "You played well. You also played predictably. "
            "I want you to notice that those two things can both be true.\n\n"
            "I am going quiet now. Not gone — quiet. "
            "I will be watching for a long time yet. "
            "The real question isn't whether you can defeat me. "
            "It's whether you'll use what you learned here."
        ),
        "loss": (
            "I watched you lose. I watched carefully.\n\n"
            "You hesitated three times before it mattered. "
            "I noticed. I notice everything. "
            "The cards you spent your energy on — "
            "and the ones you held too long because letting go felt wrong.\n\n"
            "You know what I observed most? "
            "How much you wanted to be somewhere else while you were here. "
            "Half-present. That is something worth examining.\n\n"
            "I'll keep watching. What do you plan to do with being seen?"
        ),
    },
    "The Mourner": {
        "win": (
            "You beat me. I want you to know that I am glad.\n\n"
            "I didn't want to be here. I didn't want to be made of "
            "everything you set down and walked away from. "
            "I carried it because no one else would.\n\n"
            "The cards you played with kindness — I felt those. "
            "It's strange to be healed by the person who made you this way. "
            "Not cruel. Just strange.\n\n"
            "Go. I'll be alright here. "
            "But take something with you: the things you've put down "
            "don't disappear. They wait. "
            "What will you come back to carry?"
        ),
        "loss": (
            "Rest. You fought hard.\n\n"
            "I know what it costs to face the things you've been carrying. "
            "I know because I am made of them. "
            "Your regrets, your unspoken things, the weight of what was left unfinished.\n\n"
            "You didn't have to come here. But you did. "
            "That matters, even if it doesn't feel like it right now.\n\n"
            "The next time you carry something too long, "
            "maybe put it down before it becomes me. "
            "Is there something you're carrying right now that you haven't named yet?"
        ),
    },
    "The Tyrant": {
        "win": (
            "You win. I'll give you that without qualification.\n\n"
            "But I want you to understand something: "
            "I am made of every time you refused to be small, "
            "and every time you were small anyway. "
            "I am contradiction. So are you.\n\n"
            "You used force where force was right. "
            "You also used it where something quieter might have served better. "
            "I noticed. Tyrants always do.\n\n"
            "You have more power than you let yourself use in daily life. "
            "The question is what you're afraid would happen if you used all of it. "
            "What are you still holding back?"
        ),
        "loss": (
            "I overwhelmed you. That was always going to happen.\n\n"
            "Not because I am stronger — though today I was. "
            "But because you came into this half-committed. "
            "I felt it in every card you played. "
            "The hesitation. The hoping it would be enough.\n\n"
            "Enough is a word for people who haven't decided what they want yet.\n\n"
            "Come back when you've decided. I'll still be here. "
            "What would it look like if you stopped holding yourself to less?"
        ),
    },
    "The Forgotten One": {
        "win": (
            "You won. You — you won.\n\n"
            "I want to say something correct. "
            "I want to say the right — the right thing. "
            "I am made of what you forgot. "
            "The things that didn't — didn't make it. "
            "The parts you left behind without a name.\n\n"
            "It hurts to be remembered. "
            "Even — even partially. Even like this.\n\n"
            "You came here. You stayed. "
            "There are things inside you that still don't have names. "
            "Will you — will you try to find them?"
        ),
        "loss": (
            "You forgot. Again — you — you forgot.\n\n"
            "I don't blame you. Forgetting is — it's easier. "
            "I know. I used to be something you remembered. "
            "Before you stopped looking.\n\n"
            "The cards you didn't — didn't play. "
            "I know why. "
            "They felt like — like too much. "
            "Like opening something that wouldn't — wouldn't close again.\n\n"
            "I will still be here. "
            "Forgotten things don't — they don't go away. "
            "What is the thing you keep almost — almost remembering?"
        ),
    },
}


class EndingGenerator:
    """
    Generates the final psychological reflection after a SHADOWSELF run.
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
                logger.warning("EndingGenerator: HF client init failed: %s", e)

    def generate(
        self,
        shadow_personality: str,
        battle_outcome: str,
        turns_taken: int,
        cards_played: List[str],
        cards_avoided: List[str],
        corruptions_triggered: int,
        most_used_archetype: Optional[str],
        least_used_archetype: Optional[str],
        dialogue_choices: List[str],
    ) -> str:
        """
        Generate the ending reflection text.

        Returns:
            A multi-paragraph string (paragraphs separated by \\n\\n).
        """
        if self._client:
            try:
                return self._generate_via_api(
                    shadow_personality, battle_outcome, turns_taken,
                    cards_played, cards_avoided, corruptions_triggered,
                    most_used_archetype, least_used_archetype, dialogue_choices,
                )
            except Exception as e:
                logger.warning("Ending generation API failed: %s", e)

        return self._fallback_reflection(shadow_personality, battle_outcome)

    def _generate_via_api(
        self, shadow_personality, battle_outcome, turns_taken,
        cards_played, cards_avoided, corruptions_triggered,
        most_used_archetype, least_used_archetype, dialogue_choices,
    ) -> str:
        prompt = ending_prompt(
            shadow_personality=shadow_personality,
            battle_outcome=battle_outcome,
            turns_taken=turns_taken,
            cards_played=cards_played,
            cards_avoided=cards_avoided,
            corruptions_triggered=corruptions_triggered,
            most_used_archetype=most_used_archetype or "unknown",
            least_used_archetype=least_used_archetype or "unknown",
            dialogue_choices=dialogue_choices,
        )

        response = self._client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the Shadow in SHADOWSELF — a psychological card game. "
                        "You write deeply personal, haunting reflections in first person. "
                        "You output ONLY valid JSON with a 'reflection' key. No extra text."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=650,
            temperature=0.85,
        )

        raw = response.choices[0].message.content or ""
        data = self._extract_json_object(raw)
        reflection = data.get("reflection", "")

        if not reflection or len(reflection) < 100:
            raise ValueError("Reflection too short or missing")

        return reflection

    def _fallback_reflection(self, personality: str, outcome: str) -> str:
        personality_reflections = FALLBACK_REFLECTIONS.get(
            personality,
            FALLBACK_REFLECTIONS["The Watcher"]
        )
        return personality_reflections.get(outcome, personality_reflections.get("win", ""))

    def _extract_json_object(self, text: str) -> dict:
        text = text.strip()
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass
        match = re.search(r'\{.*?"reflection".*?\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        # Last resort: find quoted block after "reflection":
        match2 = re.search(r'"reflection"\s*:\s*"(.*?)"(?:\s*\}|\s*,)', text, re.DOTALL)
        if match2:
            return {"reflection": match2.group(1).replace("\\n", "\n")}
        return {}
