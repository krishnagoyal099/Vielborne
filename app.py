"""
app.py — SHADOWSELF · Gradio entry point.

Architecture:
- gr.State() holds all game state as a serialisable dict
- gr.HTML() renders all visual screens (no default Gradio widgets for visuals)
- gr.Button() / gr.Image() handle interactions
- All screen transitions are pure HTML re-renders

Run locally:
    python app.py

Deploy to HuggingFace Spaces:
    Push as-is. Set HF_TOKEN as a Space secret.
"""

from __future__ import annotations
import os
import sys
import logging
import copy
from typing import Optional

import gradio as gr
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy imports (so app boots fast even if deps aren't installed yet)
# ---------------------------------------------------------------------------

def _import_game():
    from src.game.card import Card
    from src.game.deck import Deck
    from src.game.battle import BattleState, BattleEngine, PLAYER_MAX_HP, SHADOW_MAX_HP, ENERGY_PER_TURN
    return Card, Deck, BattleState, BattleEngine, PLAYER_MAX_HP, SHADOW_MAX_HP, ENERGY_PER_TURN

def _import_ai():
    from src.ai.card_generator import CardGenerator
    from src.ai.shadow_engine import ShadowEngine
    from src.ai.ending_generator import EndingGenerator
    return CardGenerator, ShadowEngine, EndingGenerator

def _import_vision():
    from src.vision.silhouette import get_silhouette_display
    return get_silhouette_display

def _import_ui():
    from src.ui.styles import CSS
    from src.ui.html_screens import (
        loading_screen_html, camera_invitation_html,
        silhouette_transform_html, prologue_screen_html,
        battle_screen_html, ending_screen_html,
    )
    from src.ui.js_bridge import MAIN_JS, damage_popup_js, heal_popup_js, corrupt_popup_js, shadow_hit_js, player_hit_js
    return (CSS, loading_screen_html, camera_invitation_html,
            silhouette_transform_html, prologue_screen_html,
            battle_screen_html, ending_screen_html,
            MAIN_JS, damage_popup_js, heal_popup_js, corrupt_popup_js, shadow_hit_js, player_hit_js)

# Pre-load UI module
(CSS, loading_screen_html, camera_invitation_html,
 silhouette_transform_html, prologue_screen_html,
 battle_screen_html, ending_screen_html,
 MAIN_JS, damage_popup_js, heal_popup_js, corrupt_popup_js, shadow_hit_js, player_hit_js) = _import_ui()

# ---------------------------------------------------------------------------
# Pre-battle dialogue choices (shown in prologue)
# ---------------------------------------------------------------------------

PROLOGUE_QUESTIONS = [
    {
        "question": "When you fail at something important, your first instinct is to:",
        "choices": [
            "Blame someone or something else",
            "Go quiet and disappear for a while",
            "Try again immediately",
            "Replay it endlessly in my mind",
        ]
    },
    {
        "question": "The emotion you're most likely to suppress is:",
        "choices": [
            "Anger — it frightens me",
            "Sadness — it feels indulgent",
            "Fear — I can't afford it",
            "Jealousy — it makes me feel small",
        ]
    },
    {
        "question": "You tend to trust people:",
        "choices": [
            "Too easily, and regret it",
            "Too slowly, and regret that too",
            "Rarely. It's safer.",
            "Completely or not at all",
        ]
    },
]

# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _initial_state() -> dict:
    return {
        "screen": "loading",
        "silhouette_html": "",
        "player_deck_data": {},
        "shadow_deck_data": {},
        "battle": {},
        "shadow_personality": "The Watcher",
        "shadow_intro_lines": [],
        "prologue_step": 0,
        "dialogue_choices": [],
        "last_dialogue": "",
        "last_log": "",
        "shadow_played": [],
        "reflection_text": "",
        "player_deck_stats": {},
        "hf_token": os.getenv("HF_TOKEN", ""),
    }


def _get_battle(state: dict):
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()
    bs = BattleState.from_dict(state["battle"])
    return bs


def _save_battle(state: dict, bs) -> dict:
    state["battle"] = bs.to_dict()
    return state


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------



def on_start_game(state: dict) -> tuple[str, str, dict]:
    """
    User clicked 'Begin' on loading screen.
    Generate all cards in background (or use fallbacks) and show camera screen.
    Returns: (main_html, btn_row_html, new_state)
    """
    hf_token = state.get("hf_token", "")
    CardGenerator, ShadowEngine, EndingGenerator = _import_ai()
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()

    gen = CardGenerator(hf_token)
    logger.info("Generating cards…")
    player_cards, shadow_cards = gen.generate_all()
    logger.info("Generated %d player cards, %d shadow cards.", len(player_cards), len(shadow_cards))

    # Store serialized decks
    state["player_deck_data"] = Deck(player_cards).to_dict()
    state["shadow_deck_data"] = Deck(shadow_cards).to_dict()
    state["screen"] = "camera"

    html_out = camera_invitation_html()
    btn_html = """
    <div style="text-align:center;margin-top:16px;">
      <p style="font-family:'Cormorant Garamond',serif;font-style:italic;
                font-size:0.88rem;color:rgba(160,145,200,0.5);margin-bottom:12px;">
        Allow camera access when prompted, or skip to use a generated silhouette.
      </p>
    </div>"""
    return html_out, btn_html, state



def on_begin_prologue(state: dict) -> tuple[str, dict]:
    """
    Transition from transform screen to prologue (Shadow speaks + dialogue choices).
    Shadow personality is assigned here.
    """
    CardGenerator, ShadowEngine, EndingGenerator = _import_ai()
    hf_token = state.get("hf_token", "")
    engine = ShadowEngine(hf_token)

    # Assign personality based on empty choices for now (will refine after prologue)
    personality, intro_lines = engine.assign_personality(state.get("dialogue_choices", []))
    state["shadow_personality"] = personality
    state["shadow_intro_lines"] = intro_lines
    state["screen"] = "prologue"
    state["prologue_step"] = 0

    q = PROLOGUE_QUESTIONS[0]
    html_out = prologue_screen_html(
        intro_lines, personality,
        question=q["question"],
        choices=q["choices"],
        question_index=0,
    )
    return html_out, state


def on_dialogue_choice(choice_text: str, state: dict) -> tuple[str, dict]:
    """Player chose a dialogue option. Advance prologue or start battle."""
    state["dialogue_choices"].append(choice_text)
    step = state["prologue_step"] + 1
    state["prologue_step"] = step

    if step >= len(PROLOGUE_QUESTIONS):
        # All questions answered — re-assign personality with full context, start battle
        return _start_battle(state)

    # Show next question (represented in the choice buttons area — handled in UI)
    return _render_prologue_current(state)


def _render_prologue_current(state: dict) -> tuple[str, dict]:
    """Re-render prologue for current question step."""
    step = state.get("prologue_step", 0)
    q = PROLOGUE_QUESTIONS[step] if step < len(PROLOGUE_QUESTIONS) else None
    html_out = prologue_screen_html(
        state["shadow_intro_lines"],
        state["shadow_personality"],
        question=q["question"] if q else "",
        choices=q["choices"] if q else [],
        question_index=step,
    )
    return html_out, state


def _start_battle(state: dict) -> tuple[str, dict]:
    """Initialize battle state and show battle screen."""
    CardGenerator, ShadowEngine, EndingGenerator = _import_ai()
    Card, Deck, BattleState, BattleEngine, PLAYER_MAX_HP, SHADOW_MAX_HP, ENERGY_PER_TURN = _import_game()
    hf_token = state.get("hf_token", "")

    # Use the personality determined during the prologue
    engine = ShadowEngine(hf_token)
    personality = state.get("shadow_personality", "The Watcher")

    # Initialize battle state
    bs = BattleState(
        shadow_personality=personality,
        dialogue_choices=state["dialogue_choices"],
        player_deck_data=state["player_deck_data"],
        shadow_deck_data=state["shadow_deck_data"],
        shadow_hand=[],
    )
    eng = BattleEngine(bs)
    eng.draw_to_hand()   # deal opening hand
    eng.draw_shadow_hand() # deal shadow opening hand
    state = _save_battle(state, bs)
    state["screen"] = "battle"
    state["shadow_played"] = []

    # Get opening battle dialogue
    dialogue = engine.get_battle_line(
        personality=personality, turn=1,
        player_hp=bs.player_hp, shadow_hp=bs.shadow_hp,
        last_player_card="", battle_outcome="",
    )
    state["last_dialogue"] = dialogue

    html_out = battle_screen_html(bs, dialogue_line=dialogue, log_message="The confrontation begins.")
    return html_out, state


def on_play_card_init(card_id: str, state: dict) -> tuple[str, str, dict]:
    """
    Player clicks a card. Validates and returns animation JS.
    """
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()
    bs = _get_battle(state)

    if not bs.is_player_turn or bs.game_over:
        return battle_screen_html(bs, state["last_dialogue"]), "", state

    # Find card in hand
    card_dict = next((c for c in bs.hand if c["id"] == card_id), None)
    if not card_dict:
        return battle_screen_html(bs, state["last_dialogue"], log_message="Card not found."), "", state

    # Check energy
    if bs.player_energy < card_dict.get("cost", 0):
        return battle_screen_html(bs, state["last_dialogue"], log_message="Not enough energy."), "", state

    # Set pending state
    state["pending_play_card_id"] = card_id

    anim_js = f"""
    <script>
    (async () => {{
        const cardEl = document.querySelector(`[data-card-id="{card_id}"]`);
        const targetSlot = document.querySelector('#player-field .card-slot:first-child');
        if (window.ShadowSelf && window.ShadowSelf.animateCardToSlot) {{
            await window.ShadowSelf.animateCardToSlot(cardEl, targetSlot);
        }}
        const btn = document.getElementById('btn-play-card-continue');
        if (btn) btn.click();
    }})();
    </script>
    """
    
    html_out = battle_screen_html(bs, state["last_dialogue"],
                                   shadow_played_cards=state.get("shadow_played", []))
    return html_out, anim_js, state

def on_play_card_execute(state: dict) -> tuple[str, str, dict]:
    """
    Resolves the actual card play after animation.
    """
    card_id = state.get("pending_play_card_id")
    if not card_id:
        return "", "", state
        
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()
    bs = _get_battle(state)

    card_dict = next((c for c in bs.hand if c["id"] == card_id), None)
    if not card_dict:
        return battle_screen_html(bs, state["last_dialogue"]), "", state

    # Play card
    eng = BattleEngine(bs)
    events, bs = eng.play_card(card_dict)
    state = _save_battle(state, bs)
    state["pending_play_card_id"] = None

    # Compose log message
    log_msg = " · ".join(e.message for e in events) if events else f"Played {card_dict['name']}."

    # Compose JS effects
    js_parts = []
    for e in events:
        if e.effect_type == "attack" and e.target == "shadow" and e.value > 0:
            js_parts.append(damage_popup_js(e.value, "shadow"))
            js_parts.append(shadow_hit_js())
        elif e.effect_type == "attack" and e.target == "player" and e.value > 0:
            js_parts.append(damage_popup_js(e.value, "player"))
            js_parts.append(player_hit_js())
        elif e.effect_type == "heal" and e.target == "player" and e.value > 0:
            js_parts.append(heal_popup_js(e.value, "player"))
        elif e.effect_type == "heal" and e.target == "shadow" and e.value > 0:
            js_parts.append(heal_popup_js(e.value, "shadow"))
        elif e.effect_type == "corrupt":
            js_parts.append(corrupt_popup_js())

    js_out = "".join(js_parts)

    if bs.game_over:
        return _trigger_ending(state)

    html_out = battle_screen_html(bs, state["last_dialogue"],
                                   shadow_played_cards=state.get("shadow_played", []),
                                   log_message=log_msg)
    return html_out, js_out, state


def on_end_turn(state: dict) -> tuple[str, str, dict]:
    """
    Player ends their turn. Shadow plays cards then player's new turn begins.
    Returns: (main_html, js_effects, new_state)
    """
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()
    CardGenerator, ShadowEngine, EndingGenerator = _import_ai()
    hf_token = state.get("hf_token", "")

    bs = _get_battle(state)
    if not bs.is_player_turn or bs.game_over:
        return battle_screen_html(bs, state["last_dialogue"]), "", state

    eng = BattleEngine(bs)
    shadow_events, bs = eng.end_turn()
    state = _save_battle(state, bs)

    # Shadow played cards are now tracked directly in battle state
    state["shadow_played"] = bs.shadow_played_cards

    # Log message
    log_msg = " · ".join(e.message for e in shadow_events) if shadow_events else "The Shadow watches in silence."

    # Get new dialogue line
    last_card = bs.player_deck_data.get("played_names", [""])[-1] if bs.player_deck_data.get("played_names") else ""
    engine = ShadowEngine(hf_token)
    outcome_str = bs.outcome if bs.game_over else ""
    dialogue = engine.get_battle_line(
        personality=bs.shadow_personality,
        turn=bs.turn_number,
        player_hp=bs.player_hp,
        shadow_hp=bs.shadow_hp,
        last_player_card=last_card,
        battle_outcome=outcome_str,
    )
    state["last_dialogue"] = dialogue

    # JS effects
    js_parts = []
    for e in shadow_events:
        if e.effect_type == "attack" and e.target == "player" and e.value > 0:
            js_parts.append(damage_popup_js(e.value, "player"))
            js_parts.append(player_hit_js())
        elif e.effect_type == "corrupt":
            js_parts.append(corrupt_popup_js())
    js_out = "".join(js_parts)

    if bs.game_over:
        return _trigger_ending(state)

    html_out = battle_screen_html(bs, dialogue_line=dialogue, 
                                   shadow_played_cards=state.get("shadow_played", []),
                                   log_message=log_msg)
    return html_out, js_out, state


def _trigger_ending(state: dict) -> tuple[str, str, dict]:
    """Generate and display the ending screen."""
    Card, Deck, BattleState, BattleEngine, *_ = _import_game()
    CardGenerator, ShadowEngine, EndingGenerator = _import_ai()
    hf_token = state.get("hf_token", "")

    bs = BattleState.from_dict(state["battle"])
    player_deck = Deck.from_dict(state["player_deck_data"])

    gen = EndingGenerator(hf_token)
    reflection = gen.generate(
        shadow_personality=bs.shadow_personality,
        battle_outcome=bs.outcome,
        turns_taken=bs.turn_number,
        cards_played=player_deck.played_names,
        cards_avoided=player_deck.never_played_archetypes,
        corruptions_triggered=bs.corruptions_triggered,
        most_used_archetype=player_deck.most_used_archetype,
        least_used_archetype=player_deck.least_used_archetype,
        dialogue_choices=bs.dialogue_choices,
    )

    deck_stats = {
        "never_played_archetypes": player_deck.never_played_archetypes,
        "most_used_archetype": player_deck.most_used_archetype,
        "total_played": player_deck.total_played,
    }

    state["reflection_text"] = reflection
    state["player_deck_stats"] = deck_stats
    state["screen"] = "ending"

    html_out = ending_screen_html(bs, reflection, deck_stats)
    return html_out, "", state


def on_new_game(state: dict) -> tuple[str, str, dict]:
    """Reset all state and start fresh."""
    new_state = _initial_state()
    html_out = loading_screen_html()
    return html_out, "", new_state


# ---------------------------------------------------------------------------
# Gradio App
# ---------------------------------------------------------------------------

PROLOGUE_CHOICE_BUTTONS = []
for qi, q_data in enumerate(PROLOGUE_QUESTIONS):
    for choice in q_data["choices"]:
        PROLOGUE_CHOICE_BUTTONS.append((qi, choice))

with gr.Blocks(
    title="SHADOWSELF",
) as demo:

    # Global state
    game_state = gr.State(_initial_state())

    # Main display area wrapper
    with gr.Column(elem_id="shadowself-app"):
        main_display = gr.HTML(loading_screen_html(), elem_id="main-display")

        # JS effects output (hidden, triggers side effects)
        js_effects = gr.HTML("", visible=False, elem_id="js-effects-out")

        # -----------------------------------------------------------------------
        # Control panel (hidden by default, shown contextually)
        # -----------------------------------------------------------------------
        with gr.Row(visible=True, elem_id="control-panel"):

            # --- LOADING / START ---
            with gr.Column(scale=1, elem_id="col-start", visible=True) as start_col:
                start_btn = gr.Button(
                    "✦ Begin ✦",
                    elem_id="btn-start",
                    variant="primary",
                )
                start_info = gr.HTML("")
    
            # --- CAMERA ---
            with gr.Column(scale=1, elem_id="col-camera", visible=False) as camera_col:
                camera_info = gr.HTML("")
                webcam = gr.Image(
                    sources=["webcam"],
                    type="numpy",
                    label="Look into the mirror",
                    elem_id="webcam-input",
                    height=300,
                )
                with gr.Row():
                    capture_btn = gr.Button("◉ Capture", variant="primary", elem_id="btn-capture")
                    skip_cam_btn = gr.Button("Skip Camera", variant="secondary", elem_id="btn-skip-cam")
    
            # --- PROLOGUE CHOICES ---
            with gr.Column(scale=1, elem_id="col-prologue", visible=False) as prologue_col:
                prologue_q_display = gr.HTML("")
                # Generate all choice buttons (hidden via CSS but always in DOM so JS can click them)
                choice_btns = []
                for qi, choice in PROLOGUE_CHOICE_BUTTONS:
                    btn = gr.Button(choice, elem_id=f"choice-{qi}-{choice[:10]}", elem_classes=["sr-only"])
                    choice_btns.append((qi, choice, btn))
    
            # --- BATTLE CONTROLS ---
            with gr.Column(scale=1, elem_id="col-battle", visible=False) as battle_col:
                # Card play: player types card ID or we use hidden inputs
                card_id_input = gr.Textbox(
                    label="Card ID to play",
                    placeholder="Click a card to play it…",
                    elem_id="card-id-input",
                    elem_classes=["sr-only"],   # hidden via CSS, but stays in DOM
                )
                play_card_btn = gr.Button("Play Selected Card", elem_id="btn-play-card", elem_classes=["sr-only"])
                play_card_continue_btn = gr.Button("Continue Play", elem_id="btn-play-card-continue", elem_classes=["sr-only"])
                end_turn_btn = gr.Button("⟳ End Turn", elem_id="btn-end-turn", variant="primary", elem_classes=["sr-only"])
    
            # --- ENDING / NEW GAME ---
            with gr.Column(scale=1, elem_id="col-ending", visible=False) as ending_col:
                new_game_btn = gr.Button("◈ Play Again", elem_id="btn-new-game", variant="primary")
    
            # Transform → prologue
            with gr.Column(elem_id="col-face-shadow", visible=False) as face_shadow_col:
                face_shadow_btn = gr.Button("⟶ Face Your Shadow", elem_id="btn-face-shadow", elem_classes=["sr-only"])


    # -----------------------------------------------------------------------
    # Event wiring
    # -----------------------------------------------------------------------

    # Loading → game start (generates cards)
    def _on_start(state):
        main_html, btn_html, new_state = on_start_game(state)
        logger.info("_on_start: player_deck_data keys=%s cards=%d",
                    list(new_state.get('player_deck_data', {}).keys()),
                    len(new_state.get('player_deck_data', {}).get('draw_pile', [])))
        return (main_html, btn_html, new_state,
                gr.update(visible=True),    # camera_col
                gr.update(visible=False),   # prologue_col
                gr.update(visible=False),   # battle_col
                gr.update(visible=False),   # ending_col
                gr.update(visible=False),   # start_col
                gr.update(visible=False),   # face_shadow_col
                )

    start_btn.click(
        fn=_on_start,
        inputs=[game_state],
        outputs=[main_display, camera_info, game_state,
                 camera_col, prologue_col, battle_col, ending_col,
                 start_col, face_shadow_col],
    )

    # Camera capture → go directly to prologue (show silhouette briefly in main_display)
    def _on_capture(image, state):
        get_silhouette_display = _import_vision()
        sil_html, is_real = get_silhouette_display(image)
        state = copy.deepcopy(state)
        state["screen"] = "transform"
        html_out = silhouette_transform_html(sil_html, is_real)
        return [html_out, state,
                 gr.update(visible=False),   # prologue_col
                 gr.update(visible=False),   # camera_col
                 gr.update(visible=False),   # battle_col
                 gr.update(visible=False),   # ending_col
                 gr.update(visible=False),   # start_col
                 gr.update(visible=True),    # face_shadow_col
                 ""]

    capture_btn.click(
        fn=_on_capture,
        inputs=[webcam, game_state],
        outputs=[main_display, game_state,
                 prologue_col, camera_col, battle_col, ending_col,
                 start_col, face_shadow_col,
                 prologue_q_display],
    )


    def _on_skip_cam(state):
        """Skip camera → go directly to prologue (no intermediate transform screen)."""
        get_silhouette_display = _import_vision()
        sil_html, _ = get_silhouette_display(None)
        state = copy.deepcopy(state)
        state["screen"] = "transform"
        html_out = silhouette_transform_html(sil_html, False)
        return [html_out, state,
                 gr.update(visible=False),   # prologue_col
                 gr.update(visible=False),   # camera_col
                 gr.update(visible=False),   # battle_col
                 gr.update(visible=False),   # ending_col
                 gr.update(visible=False),   # start_col
                 gr.update(visible=True),    # face_shadow_col
                 ""]

    skip_cam_btn.click(
        fn=_on_skip_cam,
        inputs=[game_state],
        outputs=[main_display, game_state,
                 prologue_col, camera_col, battle_col, ending_col,
                 start_col, face_shadow_col,
                 prologue_q_display],
    )

    def _on_face_shadow(state):
        main_html, new_state = on_begin_prologue(state)
        logger.info("_on_face_shadow: player_deck_data cards=%d",
                    len(new_state.get('player_deck_data', {}).get('draw_pile', [])))
        step = 0
        q = PROLOGUE_QUESTIONS[step]
        q_html = ""
        return [main_html, new_state,
                 gr.update(visible=True),   # prologue_col
                 gr.update(visible=False),  # camera_col
                 gr.update(visible=False),  # battle_col
                 gr.update(visible=False),  # ending_col
                 gr.update(visible=False),  # start_col
                 gr.update(visible=False),  # face_shadow_col — hide now
                 q_html]

    face_shadow_btn.click(
        fn=_on_face_shadow,
        inputs=[game_state],
        outputs=[main_display, game_state,
                 prologue_col, camera_col, battle_col, ending_col,
                 start_col, face_shadow_col,
                 prologue_q_display],
    )

    # Dialogue choices
    def _make_choice_handler(choice_text_static: str):
        def handler(state):
            new_state = copy.deepcopy(state)
            new_state["dialogue_choices"] = list(state.get("dialogue_choices", []))
            new_state["dialogue_choices"].append(choice_text_static)
            step = state.get("prologue_step", 0) + 1
            new_state["prologue_step"] = step

            if step >= len(PROLOGUE_QUESTIONS):
                # outputs: [main_display, js_effects, game_state, prologue_col, battle_col, ending_col,
                #           start_col, face_shadow_col, prologue_q_display]
                logger.info("_make_choice_handler battle start: player_deck cards=%d",
                            len(new_state.get('player_deck_data', {}).get('draw_pile', [])))
                main_html, final_state = _start_battle(new_state)
                logger.info("After _start_battle: hand=%d draw=%d",
                            len(final_state.get('battle', {}).get('hand', [])),
                            len(final_state.get('battle', {}).get('player_deck_data', {}).get('draw_pile', [])))
                return [main_html, "", final_state,
                         gr.update(visible=False),   # prologue_col
                         gr.update(visible=True),    # battle_col
                         gr.update(visible=False),   # ending_col
                         gr.update(visible=False),   # start_col
                         gr.update(visible=False),   # face_shadow_col
                         ""]
            else:
                q = PROLOGUE_QUESTIONS[step]
                q_html = ""
                main_html, _ = _render_prologue_current(new_state)
                return [main_html, "", new_state,
                         gr.update(visible=True),    # prologue_col
                         gr.update(visible=False),   # battle_col
                         gr.update(visible=False),   # ending_col
                         gr.update(visible=False),   # start_col
                         gr.update(visible=False),   # face_shadow_col
                         q_html]

        return handler

    for qi_val, choice_val, btn_obj in choice_btns:
        handler = _make_choice_handler(choice_val)
        btn_obj.click(
            fn=handler,
            inputs=[game_state],
            outputs=[main_display, js_effects, game_state,
                     prologue_col, battle_col, ending_col,
                     start_col, face_shadow_col,
                     prologue_q_display],
        )

    # Play card (initiate animation)
    def _on_play_card(card_id, state):
        if not card_id or not str(card_id).strip():
            bs_dict = state.get("battle", {})
            from src.game.battle import BattleState
            bs = BattleState.from_dict(bs_dict)
            return battle_screen_html(bs, state.get("last_dialogue", "")), "", state
        main_html, js_out, new_state = on_play_card_init(str(card_id).strip(), state)
        return main_html, js_out, new_state

    play_card_btn.click(
        fn=_on_play_card,
        inputs=[card_id_input, game_state],
        outputs=[main_display, js_effects, game_state],
    )

    # Also trigger on card_id_input submit (Enter key)
    card_id_input.submit(
        fn=_on_play_card,
        inputs=[card_id_input, game_state],
        outputs=[main_display, js_effects, game_state],
    )

    # Play card (execute logic after animation)
    def _on_play_card_execute_handler(state):
        main_html, js_out, new_state = on_play_card_execute(state)
        # Check if game over to transition screens
        screen = new_state.get("screen", "battle")
        ending_visible = screen == "ending"
        return (main_html, js_out, new_state,
                gr.update(visible=False),               # start_col
                gr.update(visible=False),               # camera_col
                gr.update(visible=False),               # prologue_col
                gr.update(visible=not ending_visible),  # battle_col
                gr.update(visible=ending_visible),      # ending_col
                gr.update(visible=False))               # face_shadow_col

    play_card_continue_btn.click(
        fn=_on_play_card_execute_handler,
        inputs=[game_state],
        outputs=[main_display, js_effects, game_state,
                 start_col, camera_col, prologue_col, battle_col, ending_col, face_shadow_col],
    )

    # End turn
    def _on_end_turn(state):
        main_html, js_out, new_state = on_end_turn(state)
        screen = new_state.get("screen", "battle")
        ending_visible = screen == "ending"
        return (main_html, js_out, new_state,
                gr.update(visible=False),               # start_col
                gr.update(visible=False),               # camera_col
                gr.update(visible=False),               # prologue_col
                gr.update(visible=not ending_visible),  # battle_col
                gr.update(visible=ending_visible),      # ending_col
                gr.update(visible=False))               # face_shadow_col

    end_turn_btn.click(
        fn=_on_end_turn,
        inputs=[game_state],
        outputs=[main_display, js_effects, game_state,
                 start_col, camera_col, prologue_col, battle_col, ending_col,
                 face_shadow_col],
    )

    # New game
    def _on_new_game(state):
        main_html, _, new_state = on_new_game(state)
        return (main_html, new_state,
                gr.update(visible=True),    # start_col — show Begin button again
                gr.update(visible=False),   # camera_col
                gr.update(visible=False),   # prologue_col
                gr.update(visible=False),   # battle_col
                gr.update(visible=False),   # ending_col
                gr.update(visible=False),   # face_shadow_col
                )

    new_game_btn.click(
        fn=_on_new_game,
        inputs=[game_state],
        outputs=[main_display, game_state,
                 start_col, camera_col, prologue_col, battle_col, ending_col,
                 face_shadow_col],
    )

    # (Inline JS moved to js_bridge.py MAIN_JS)




# ---------------------------------------------------------------------------
# Launch
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        css=CSS,
        head=f"""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cinzel+Decorative:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
{MAIN_JS}
        """,
        theme=gr.themes.Base(
            primary_hue="purple",
            neutral_hue="slate",
        ).set(
            body_background_fill="#000000",
            block_background_fill="transparent",
            panel_background_fill="transparent",
        ),
    )
