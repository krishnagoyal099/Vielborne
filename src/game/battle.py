"""
battle.py — Turn state machine for SHADOWSELF.

Implements GAME_BIBLE §5 (Battle Rules) and §5.4 (Shadow AI Behavior).
The Shadow AI is fully deterministic — no LLM needed per turn.
LLM is only called for dialogue lines (handled by shadow_engine.py).
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import copy

from src.game.card import Card, CardEffect, CorruptedEffect
from src.game.deck import Deck


# ---------------------------------------------------------------------------
# Battle constants
# ---------------------------------------------------------------------------

PLAYER_MAX_HP    = 50
SHADOW_MAX_HP    = 50
ENERGY_PER_TURN  = 3
HAND_SIZE        = 5
CORRUPTION_HP_THRESHOLD = 0.30   # below 30% HP → corruption risk


# ---------------------------------------------------------------------------
# Battle event log (for UI feedback and ending analysis)
# ---------------------------------------------------------------------------

@dataclass
class BattleEvent:
    """A single resolved event in the battle log."""
    source: str              # "player" | "shadow"
    card_name: str
    effect_type: str         # "attack" | "heal" | "armor" | "draw" | "corrupt" | "drain"
    value: int
    target: str              # "player" | "shadow"
    message: str = ""


# ---------------------------------------------------------------------------
# Battle state
# ---------------------------------------------------------------------------

@dataclass
class BattleState:
    """
    Full serialisable snapshot of one battle.

    All values passed through Gradio state as a plain dict via to_dict/from_dict.
    """
    # HP
    player_hp:  int = PLAYER_MAX_HP
    shadow_hp:  int = SHADOW_MAX_HP

    # Energy
    player_energy: int = ENERGY_PER_TURN

    # Turn tracking
    turn_number: int = 1
    is_player_turn: bool = True
    game_over: bool = False
    outcome: str = ""            # "win" | "loss"

    # Decks (stored as dicts for serialization)
    player_deck_data: dict = field(default_factory=dict)
    shadow_deck_data: dict = field(default_factory=dict)

    # Player hand (list of card dicts)
    hand: List[dict] = field(default_factory=list)
    
    # Cards played by player this turn
    player_played_cards: List[dict] = field(default_factory=list)

    # Cards played by shadow this turn (for UI display)
    shadow_played_cards: List[dict] = field(default_factory=list)

    # Shadow hand (drawn at start of player's turn)
    shadow_hand: List[dict] = field(default_factory=list)

    # Shadow personality (set by ShadowEngine)
    shadow_personality: str = "The Watcher"

    # Corruption tracking
    corruptions_triggered: int = 0

    # Battle log (for ending analysis)
    events: List[dict] = field(default_factory=list)

    # Dialogue choices made by player (pre-battle)
    dialogue_choices: List[str] = field(default_factory=list)

    # Armor buffers (reset each turn)
    player_armor: int = 0
    shadow_armor: int = 0

    # Drain buffer
    player_energy_drain: int = 0

    def to_dict(self) -> dict:
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict) -> "BattleState":
        obj = cls()
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, copy.deepcopy(v))
        return obj

    # Convenience queries
    @property
    def player_hp_pct(self) -> float:
        return self.player_hp / PLAYER_MAX_HP

    @property
    def shadow_hp_pct(self) -> float:
        return self.shadow_hp / SHADOW_MAX_HP


# ---------------------------------------------------------------------------
# Battle engine
# ---------------------------------------------------------------------------

class BattleEngine:
    """
    Resolves card effects, manages turns, and implements Shadow AI.

    Usage:
        engine = BattleEngine(state)
        events, new_state = engine.play_card(card_dict)
        events, new_state = engine.end_turn()
    """

    def __init__(self, state: BattleState) -> None:
        self.state = state

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------

    def play_card(self, card_dict: dict) -> Tuple[List[BattleEvent], BattleState]:
        """
        Player plays a card from hand.

        Args:
            card_dict: Serialized Card dict from Gradio state.

        Returns:
            (events, updated_state)
        """
        card = Card.from_dict(card_dict)
        events: List[BattleEvent] = []

        # Check energy
        if self.state.player_energy < card.cost:
            return [], self.state   # silently reject — UI should disable

        # Spend energy
        self.state.player_energy -= card.cost

        # Check corruption (below threshold → random chance of corruption)
        if (
            not card.is_corrupted
            and card.is_player_card
            and self.state.player_hp_pct < CORRUPTION_HP_THRESHOLD
            and random.random() < 0.35
        ):
            card.corrupt()
            self.state.corruptions_triggered += 1
            events.append(BattleEvent(
                source="shadow", card_name=card.name,
                effect_type="corrupt", value=1, target="player",
                message=f"Your {card.name} fractures — the darkness seeps in."
            ))

        # Resolve active effects
        active = card.active_effects
        if isinstance(active, CardEffect):
            events.extend(self._resolve_player_effects(card, active))
        elif isinstance(active, CorruptedEffect):
            events.extend(self._resolve_corrupted_effects(card, active))

        # Record in player deck
        player_deck = Deck.from_dict(self.state.player_deck_data)
        player_deck.record_played(card)
        self.state.player_deck_data = player_deck.to_dict()

        # Remove from hand
        self.state.hand = [c for c in self.state.hand if c["id"] != card.id]
        # Store updated card state (in case it was corrupted during play)
        self.state.player_played_cards.append(card.to_dict())

        # Log events
        self.state.events.extend([e.__dict__ for e in events])

        # Check win/loss
        self._check_game_over()

        return events, self.state

    def end_turn(self) -> Tuple[List[BattleEvent], BattleState]:
        """
        Player ends their turn. Shadow plays cards automatically.

        Returns:
            (shadow_events, updated_state)
        """
        self.state.is_player_turn = False
        self.state.player_armor = 0   # armor doesn't persist between turns

        # Shadow plays 1-3 cards based on personality
        shadow_deck = Deck.from_dict(self.state.shadow_deck_data)
        events = self._shadow_turn(shadow_deck)
        self.state.shadow_deck_data = shadow_deck.to_dict()

        # Log
        self.state.events.extend([e.__dict__ for e in events])

        # Check win/loss
        self._check_game_over()

        if not self.state.game_over:
            self._start_player_turn()

        return events, self.state

    def draw_to_hand(self) -> List[dict]:
        """Draw cards until hand is full. Called at start of player turn."""
        player_deck = Deck.from_dict(self.state.player_deck_data)
        needed = HAND_SIZE - len(self.state.hand)
        new_cards = player_deck.draw(needed)
        self.state.player_deck_data = player_deck.to_dict()
        self.state.hand.extend([c.to_dict() for c in new_cards])
        return [c.to_dict() for c in new_cards]

    def draw_shadow_hand(self) -> None:
        """Draw cards until Shadow hand has 4 cards."""
        shadow_deck = Deck.from_dict(self.state.shadow_deck_data)
        needed = 4 - len(self.state.shadow_hand)
        if needed > 0:
            new_cards = shadow_deck.draw(needed)
            self.state.shadow_deck_data = shadow_deck.to_dict()
            self.state.shadow_hand.extend([c.to_dict() for c in new_cards])

    # ------------------------------------------------------------------
    # Shadow AI
    # ------------------------------------------------------------------

    def _shadow_turn(self, shadow_deck: Deck) -> List[BattleEvent]:
        """Shadow draws to hand, then plays cards."""
        personality = self.state.shadow_personality
        events: List[BattleEvent] = []
        
        # Clear shadow played cards from previous turn
        self.state.shadow_played_cards = []
        
        # Draw 4 cards to Shadow hand at start of turn
        while len(self.state.shadow_hand) < 4:
            drawn = shadow_deck.draw(1)
            if drawn:
                self.state.shadow_hand.append(drawn[0].to_dict())
            else:
                break  # Deck empty
        
        # Determine how many cards to play (1-3 based on personality)
        num_to_play = self._shadow_cards_per_turn(personality)
        num_to_play = min(num_to_play, len(self.state.shadow_hand))
        
        # Play cards from hand
        for _ in range(num_to_play):
            if self.state.game_over or not self.state.shadow_hand:
                break
                
            # Select card from hand (simple: first card, or AI logic)
            card_idx = 0  # Could be smarter based on personality
            card_dict = self.state.shadow_hand.pop(card_idx)
            
            # Reconstruct the Card object
            card = Card.from_dict(card_dict)
            
            # Track card as played (for UI display)
            self.state.shadow_played_cards.append(card_dict)
            
            # Record explicit play event for the UI
            events.append(BattleEvent(
                source="shadow", card_name=card.name,
                effect_type="play", value=0, target="shadow",
                message=f"The Shadow plays {card.name}."
            ))
            
            # Resolve card effects
            card_events = self._resolve_shadow_card(card, personality)
            events.extend(card_events)
            
            # Card goes to discard (NOT back to hand, NOT staying on table)
            shadow_deck.discard(card)

        self.state.shadow_armor = 0   # shadow armor resets each turn
        return events

    def _shadow_cards_per_turn(self, personality: str) -> int:
        """Number of cards shadow plays per turn, by personality."""
        return {
            "The Accuser":      2,
            "The Watcher":      1,
            "The Mourner":      2,
            "The Tyrant":       3,
            "The Forgotten One": random.randint(1, 3),
        }.get(personality, 2)

    def _resolve_shadow_card(self, card: Card, personality: str) -> List[BattleEvent]:
        """Apply one shadow card's effects to the player."""
        events: List[BattleEvent] = []
        eff = card.active_effects

        attack = getattr(eff, "attack", 0)
        self_dmg = getattr(eff, "self_damage", 0)
        enemy_heal = getattr(eff, "enemy_heal", 0)
        drain = getattr(eff, "draw", 0)   # shadow 'draw' interpreted as drain

        # Shadow personaliy modifiers
        if personality == "The Tyrant":
            attack = min(10, attack + 2)
        elif personality == "The Mourner":
            attack = max(0, attack - 1)
            drain = max(drain, 1)   # Mourner always drains
        elif personality == "The Forgotten One" and random.random() < 0.3:
            # Corrupts a random player card in hand
            if self.state.hand:
                target_idx = random.randint(0, len(self.state.hand) - 1)
                self.state.hand[target_idx]["is_corrupted"] = True
                self.state.corruptions_triggered += 1
                events.append(BattleEvent(
                    source="shadow", card_name=card.name,
                    effect_type="corrupt", value=1, target="player",
                    message=f"The Forgotten One taints your {self.state.hand[target_idx]['name']}."
                ))

        # Watcher mirrors: boost attack if player is low on HP (retaliatory)
        if personality == "The Watcher":
            player_hp_low = self.state.player_hp < (PLAYER_MAX_HP * 0.5)
            if player_hp_low:
                attack = min(10, attack + 1)

        # Resolve attack (reduced by player armor)
        if attack > 0:
            effective = max(0, attack - self.state.player_armor)
            self.state.player_armor = max(0, self.state.player_armor - attack)
            self.state.player_hp = max(0, self.state.player_hp - effective)
            if effective > 0:
                events.append(BattleEvent(
                    source="shadow", card_name=card.name,
                    effect_type="attack", value=effective, target="player",
                    message=f"Shadow plays {card.name}: deals {effective} damage."
                ))

        # Enemy heal (heals shadow)
        if enemy_heal > 0:
            healed = min(enemy_heal, SHADOW_MAX_HP - self.state.shadow_hp)
            self.state.shadow_hp += healed
            if healed > 0:
                events.append(BattleEvent(
                    source="shadow", card_name=card.name,
                    effect_type="heal", value=healed, target="shadow",
                    message=f"Shadow recovers {healed} HP."
                ))

        # Drain player energy next turn
        if drain > 0:
            events.append(BattleEvent(
                source="shadow", card_name=card.name,
                effect_type="drain", value=drain, target="player",
                message=f"Shadow drains {drain} energy from your next turn."
            ))
            # Apply drain to current player energy (for next turn, stored temporarily)
            self.state.player_energy_drain += drain

        return events

    # ------------------------------------------------------------------
    # Player effect resolution
    # ------------------------------------------------------------------

    def _resolve_player_effects(self, card: Card, eff: CardEffect) -> List[BattleEvent]:
        events: List[BattleEvent] = []

        if eff.attack > 0:
            effective = max(0, eff.attack - self.state.shadow_armor)
            self.state.shadow_armor = max(0, self.state.shadow_armor - eff.attack)
            self.state.shadow_hp = max(0, self.state.shadow_hp - effective)
            if effective > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="attack", value=effective, target="shadow",
                    message=f"You play {card.name}: deals {effective} damage."
                ))

        if eff.heal > 0:
            healed = min(eff.heal, PLAYER_MAX_HP - self.state.player_hp)
            self.state.player_hp += healed
            if healed > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="heal", value=healed, target="player",
                    message=f"{card.name}: you recover {healed} HP."
                ))

        if eff.armor > 0:
            self.state.player_armor += eff.armor
            events.append(BattleEvent(
                source="player", card_name=card.name,
                effect_type="armor", value=eff.armor, target="player",
                message=f"{card.name}: gained {eff.armor} armor."
            ))

        if eff.draw > 0:
            player_deck = Deck.from_dict(self.state.player_deck_data)
            drawn = player_deck.draw(eff.draw)
            self.state.player_deck_data = player_deck.to_dict()
            # Enforce max hand size to prevent overflow
            max_hand_size = HAND_SIZE + 1
            added_count = 0
            for c in drawn:
                if len(self.state.hand) < max_hand_size:
                    self.state.hand.append(c.to_dict())
                    added_count += 1
            if added_count > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="draw", value=added_count, target="player",
                    message=f"{card.name}: drew {added_count} card(s)."
                ))

        return events

    def _resolve_corrupted_effects(self, card: Card, eff: CorruptedEffect) -> List[BattleEvent]:
        events: List[BattleEvent] = []

        if eff.self_damage > 0:
            actual_damage = min(eff.self_damage, self.state.player_hp)
            self.state.player_hp = max(0, self.state.player_hp - actual_damage)
            if actual_damage > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="attack", value=actual_damage, target="player",
                    message=f"Corrupted {card.name} turns against you: {actual_damage} self-damage."
                ))

        if eff.enemy_heal > 0:
            healed = min(eff.enemy_heal, SHADOW_MAX_HP - self.state.shadow_hp)
            self.state.shadow_hp += healed
            if healed > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="heal", value=healed, target="shadow",
                    message=f"Corrupted {card.name}: heals the Shadow for {healed}."
                ))

        # Corrupted draw = discard instead
        if card.effects.draw > 0:
            discard_count = min(card.effects.draw, len(self.state.hand))
            to_discard = self.state.hand[:discard_count]
            self.state.hand = self.state.hand[discard_count:]
            
            # Send to discard pile
            player_deck = Deck.from_dict(self.state.player_deck_data)
            for c_dict in to_discard:
                player_deck.discard(Card.from_dict(c_dict))
            self.state.player_deck_data = player_deck.to_dict()
            
            if discard_count > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="drain", value=discard_count, target="player",
                    message=f"Corrupted {card.name}: forced to discard {discard_count} card(s)."
                ))

        # Corrupted armor = lose armor
        if card.effects.armor > 0:
            armor_loss = min(card.effects.armor, self.state.player_armor)
            self.state.player_armor = max(0, self.state.player_armor - armor_loss)
            if armor_loss > 0:
                events.append(BattleEvent(
                    source="player", card_name=card.name,
                    effect_type="armor", value=-armor_loss, target="player",
                    message=f"Corrupted {card.name}: lost {armor_loss} armor."
                ))

        return events

    # ------------------------------------------------------------------
    # Turn management
    # ------------------------------------------------------------------

    def _start_player_turn(self) -> None:
        self.state.player_played_cards = []
        # NOTE: Do NOT clear shadow_played_cards here.
        # shadow_played_cards is cleared at the start of _shadow_turn() (line 260).
        # Clearing here would wipe the data before the HTML renderer can display it.
        self.state.is_player_turn = True
        self.state.turn_number += 1
        # Apply energy drain (cap it to not exceed ENERGY_PER_TURN)
        drain = min(self.state.player_energy_drain, ENERGY_PER_TURN)
        drain = max(0, drain)  # Ensure drain is non-negative
        self.state.player_energy = max(0, ENERGY_PER_TURN - drain)
        self.state.player_energy_drain = 0
        # Reset armor at start of turn
        self.state.player_armor = 0
        self.draw_to_hand()
        self.draw_shadow_hand()

    def _check_game_over(self) -> None:
        if self.state.shadow_hp <= 0:
            self.state.game_over = True
            self.state.outcome = "win"
        elif self.state.player_hp <= 0:
            self.state.game_over = True
            self.state.outcome = "loss"
