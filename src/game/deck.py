"""
deck.py — Deck management for SHADOWSELF.

Handles shuffle, draw, discard, and tracking played cards
for the post-battle ending analysis.
"""

from __future__ import annotations
import random
from typing import List, Optional
import copy
from src.game.card import Card


class Deck:
    """
    Manages a deck of 18 cards with draw, discard, and play tracking.

    Attributes:
        draw_pile:    Cards not yet drawn.
        discard_pile: Cards that have been played and discarded.
        played_names: Ordered list of card names as played (for ending analysis).
        never_played: Set of card ids never played during the run.
    """

    def __init__(self, cards: List[Card]) -> None:
        self._all_card_ids = {c.id for c in cards}
        self.draw_pile: List[Card] = list(cards)
        self.discard_pile: List[Card] = []
        self.played_names: List[str] = []
        self.played_archetypes: List[str] = []
        random.shuffle(self.draw_pile)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def draw(self, count: int = 1) -> List[Card]:
        """
        Draw up to `count` cards from the top of the draw pile.
        Automatically reshuffles discard pile if draw pile is exhausted.
        Returns a (possibly shorter) list if not enough cards remain.
        """
        drawn: List[Card] = []
        for _ in range(count):
            if not self.draw_pile:
                self._reshuffle()
            if self.draw_pile:
                drawn.append(self.draw_pile.pop(0))
        return drawn

    def discard(self, card: Card) -> None:
        """Move a card to the discard pile."""
        self.discard_pile.append(card)

    def record_played(self, card: Card) -> None:
        """Record a card as played (for ending analysis) then discard it."""
        self.played_names.append(card.name)
        self.played_archetypes.append(card.archetype)
        self.discard(card)

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    @property
    def never_played_archetypes(self) -> List[str]:
        """
        Return archetypes of cards that were never played during the run.
        Used by the ending generator to infer psychological meaning.
        """
        played_ids = set()
        # We track by name because card objects are recreated from dicts
        played_names_set = set(self.played_names)

        # Find all cards (across draw + discard) not in played set
        all_cards = self.draw_pile + self.discard_pile
        return list({
            c.archetype for c in all_cards
            if c.name not in played_names_set
        })

    @property
    def cards_remaining(self) -> int:
        return len(self.draw_pile)

    @property
    def total_played(self) -> int:
        return len(self.played_names)

    @property
    def archetype_play_counts(self) -> dict:
        """Returns {archetype: count} for all played cards."""
        counts: dict = {}
        for a in self.played_archetypes:
            counts[a] = counts.get(a, 0) + 1
        return counts

    @property
    def most_used_archetype(self) -> Optional[str]:
        counts = self.archetype_play_counts
        return max(counts, key=counts.get) if counts else None

    @property
    def least_used_archetype(self) -> Optional[str]:
        counts = self.archetype_play_counts
        return min(counts, key=counts.get) if counts else None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _reshuffle(self) -> None:
        """Reshuffle discard pile back into draw pile."""
        if self.discard_pile:
            random.shuffle(self.discard_pile)
            self.draw_pile = self.discard_pile
            self.discard_pile = []

    # ------------------------------------------------------------------
    # Serialization (Gradio state ↔ Deck)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "draw_pile":         [c.to_dict() for c in self.draw_pile],
            "discard_pile":      [c.to_dict() for c in self.discard_pile],
            "played_names":      copy.deepcopy(self.played_names),
            "played_archetypes": copy.deepcopy(self.played_archetypes),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        draw    = [Card.from_dict(d) for d in data.get("draw_pile", [])]
        discard = [Card.from_dict(d) for d in data.get("discard_pile", [])]
        deck = cls.__new__(cls)
        deck._all_card_ids      = {c.id for c in draw + discard}
        deck.draw_pile          = draw
        deck.discard_pile       = discard
        deck.played_names       = copy.deepcopy(data.get("played_names", []))
        deck.played_archetypes  = copy.deepcopy(data.get("played_archetypes", []))
        return deck
