"""
card.py — Card dataclass with full validation.

Implements the JSON schema defined in GAME_BIBLE §4.1.
All numeric fields are clamped to their valid ranges on construction.
"""

from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Archetype constants
# ---------------------------------------------------------------------------

PLAYER_ARCHETYPES = ["Courage", "Hope", "Kindness", "Resolve", "Trust", "Acceptance"]
SHADOW_ARCHETYPES = ["Fear", "Rage", "Doubt", "Jealousy", "Despair", "Obsession"]

ARCHETYPE_COLORS = {
    # Player
    "Courage":    {"rgb": "255,140,50",  "icon": "⚔",  "label": "courage"},
    "Hope":       {"rgb": "100,200,255", "icon": "✦",  "label": "hope"},
    "Kindness":   {"rgb": "120,220,160", "icon": "❤",  "label": "kindness"},
    "Resolve":    {"rgb": "220,180,255", "icon": "◈",  "label": "resolve"},
    "Trust":      {"rgb": "255,220,100", "icon": "∞",  "label": "trust"},
    "Acceptance": {"rgb": "200,200,200", "icon": "⊙",  "label": "acceptance"},
    # Shadow
    "Fear":       {"rgb": "160,40,40",   "icon": "👁",  "label": "fear"},
    "Rage":       {"rgb": "220,60,20",   "icon": "✖",  "label": "rage"},
    "Doubt":      {"rgb": "80,80,120",   "icon": "?",  "label": "doubt"},
    "Jealousy":   {"rgb": "40,140,80",   "icon": "⊗",  "label": "jealousy"},
    "Despair":    {"rgb": "60,40,100",   "icon": "↓",  "label": "despair"},
    "Obsession":  {"rgb": "160,80,180",  "icon": "∞",  "label": "obsession"},
}


# ---------------------------------------------------------------------------
# Effect dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CardEffect:
    """Pure effects of a card when played in normal state."""
    attack: int = 0
    heal: int = 0
    armor: int = 0
    draw: int = 0

    def __post_init__(self) -> None:
        self.attack = max(0, min(10, int(self.attack)))
        self.heal   = max(0, min(10, int(self.heal)))
        self.armor  = max(0, min(10, int(self.armor)))
        self.draw   = max(0, min(3,  int(self.draw)))

    def is_empty(self) -> bool:
        return self.attack == 0 and self.heal == 0 and self.armor == 0 and self.draw == 0


@dataclass
class CorruptedEffect:
    """Corrupted (psychologically inverted) effects of a card."""
    attack: int = 0
    heal: int = 0
    armor: int = 0
    draw: int = 0
    self_damage: int = 0
    enemy_heal: int = 0

    def __post_init__(self) -> None:
        self.attack      = max(0, min(10, int(self.attack)))
        self.heal        = max(0, min(10, int(self.heal)))
        self.armor       = max(0, min(10, int(self.armor)))
        self.draw        = max(0, min(3,  int(self.draw)))
        self.self_damage = max(0, min(10, int(self.self_damage)))
        self.enemy_heal  = max(0, min(10, int(self.enemy_heal)))


# ---------------------------------------------------------------------------
# Card dataclass
# ---------------------------------------------------------------------------

@dataclass
class Card:
    """
    A single SHADOWSELF card.

    Matches the JSON schema from GAME_BIBLE §4.1.
    Numeric fields are clamped to valid ranges automatically.
    """
    name: str
    archetype: str
    flavor_text: str
    cost: int
    effects: CardEffect
    pure_description: str
    corrupted_description: str
    corrupted_effects: CorruptedEffect
    rarity: str = "common"
    is_corrupted: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def __post_init__(self) -> None:
        # Clamp cost
        self.cost = max(0, min(3, int(self.cost)))
        # Validate rarity
        if self.rarity not in ("common", "rare", "mythic"):
            self.rarity = "common"
        # Validate archetype
        all_archetypes = PLAYER_ARCHETYPES + SHADOW_ARCHETYPES
        if self.archetype not in all_archetypes:
            self.archetype = "Courage"

    @property
    def is_player_card(self) -> bool:
        return self.archetype in PLAYER_ARCHETYPES

    @property
    def is_shadow_card(self) -> bool:
        return self.archetype in SHADOW_ARCHETYPES

    @property
    def active_effects(self) -> CardEffect | CorruptedEffect:
        """Return whichever effect set is currently active."""
        return self.corrupted_effects if self.is_corrupted else self.effects

    @property
    def archetype_color_rgb(self) -> str:
        return ARCHETYPE_COLORS.get(self.archetype, {}).get("rgb", "200,200,200")

    @property
    def archetype_icon(self) -> str:
        return ARCHETYPE_COLORS.get(self.archetype, {}).get("icon", "◆")

    @property
    def archetype_label(self) -> str:
        return ARCHETYPE_COLORS.get(self.archetype, {}).get("label", "unknown")

    def corrupt(self) -> None:
        """Apply corruption to this card."""
        self.is_corrupted = True

    def uncorrupt(self) -> None:
        """Remove corruption from this card."""
        self.is_corrupted = False

    def to_dict(self) -> dict:
        """Serialize to dict for Gradio state passing."""
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "flavor_text": self.flavor_text,
            "cost": self.cost,
            "effects": {
                "attack": self.effects.attack,
                "heal":   self.effects.heal,
                "armor":  self.effects.armor,
                "draw":   self.effects.draw,
            },
            "pure_description": self.pure_description,
            "corrupted_description": self.corrupted_description,
            "corrupted_effects": {
                "attack":      self.corrupted_effects.attack,
                "heal":        self.corrupted_effects.heal,
                "armor":       self.corrupted_effects.armor,
                "draw":        self.corrupted_effects.draw,
                "self_damage": self.corrupted_effects.self_damage,
                "enemy_heal":  self.corrupted_effects.enemy_heal,
            },
            "rarity": self.rarity,
            "is_corrupted": self.is_corrupted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """Deserialize from dict (Gradio state → Card)."""
        eff = data.get("effects", {})
        ceff = data.get("corrupted_effects", {})
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            name=data.get("name", "Unknown"),
            archetype=data.get("archetype", "Courage"),
            flavor_text=data.get("flavor_text", ""),
            cost=data.get("cost", 1),
            effects=CardEffect(
                attack=eff.get("attack", 0),
                heal=eff.get("heal", 0),
                armor=eff.get("armor", 0),
                draw=eff.get("draw", 0),
            ),
            pure_description=data.get("pure_description", ""),
            corrupted_description=data.get("corrupted_description", ""),
            corrupted_effects=CorruptedEffect(
                attack=ceff.get("attack", 0),
                heal=ceff.get("heal", 0),
                armor=ceff.get("armor", 0),
                draw=ceff.get("draw", 0),
                self_damage=ceff.get("self_damage", 0),
                enemy_heal=ceff.get("enemy_heal", 0),
            ),
            rarity=data.get("rarity", "common"),
            is_corrupted=data.get("is_corrupted", False),
        )
