Act as a Senior Python/Gradio Game Developer and Frontend Engineer. I need you to perform a comprehensive, deep-dive code review of the battle system and card mechanics for my game "SHADOWSELF". 

The game is built using Gradio for the UI, with pure HTML/CSS/JS injected via `gr.HTML()`, and Python dataclasses for game logic. State is managed via `gr.State()` as a serializable dictionary.

### CONTEXT & KEY FILES
- `app.py`: Gradio entry point, event handlers (`on_play_card`, `on_end_turn`), UI wiring.
- `src/game/battle.py`: `BattleState` and `BattleEngine`. Handles turn logic, card effect resolution, Shadow AI, and game over checks.
- `src/game/card.py`: `Card`, `CardEffect`, `CorruptedEffect` dataclasses.
- `src/game/deck.py`: `Deck` management (draw, discard, reshuffle, tracking).
- `src/ui/html_screens.py`: HTML string generators for the Battle Screen, Cards, and HUD.
- `src/ui/js_bridge.py`: Client-side JS for card clicks, popups, and triggering hidden Gradio buttons.
- `src/ui/styles.py`: CSS for cards, arena, and animations.

### YOUR TASK
Audit the following systems for logical bugs, UI/UX flaws, state synchronization issues, and edge cases. Be extremely critical.

#### 1. Card Rendering & UI (src/ui/html_screens.py & src/ui/styles.py)
- Check `_card_html()`: Are all card attributes (cost, rarity, archetype color, corrupted state) correctly mapped to HTML/CSS? 
- Verify `data-card-id="{_esc(card.id)}"` is correctly formatted and accessible via JS.
- Check if the visual distinction between "Pure" and "Corrupted" cards is clear in the generated HTML.
- Ensure the "Shadow field" and "Player hand" HTML structures correctly iterate through card dictionaries.

#### 2. Card Interaction & JS Bridge (src/ui/js_bridge.py & app.py)
- Analyze the `triggerCardPlay(cardId)` function in `app.py`'s injected JS. 
- **CRITICAL**: Gradio often fails to detect programmatic value changes. Verify if `ta.dispatchEvent(new Event('input', {bubbles: true}))` and `change` events are sufficient to update the Gradio `card_id_input` Textbox state before `btn-play-card` is clicked. Suggest fixes if Gradio might miss the event.
- Check if the `150ms` timeout for clicking the play button is robust enough, or if it should use a callback/MutationObserver.
- Verify that `on_play_card` in `app.py` correctly validates the `card_id` and prevents duplicate plays or playing cards not in hand.

#### 3. Battle Logic & State Machine (src/game/battle.py)
- **Energy System**: Verify `player_energy` is correctly deducted. What happens if a card costs 0? What if energy is negative?
- **Effect Resolution**: Check `_resolve_player_effects` and `_resolve_corrupted_effects`. 
  - Are armor calculations correct? (e.g., `effective = max(0, attack - armor)`).
  - Does healing cap at `PLAYER_MAX_HP`?
  - Do draw effects correctly handle an empty draw pile?
- **Corruption Logic**: In `play_card`, corruption is checked if `player_hp_pct < 0.30`. Verify the random chance (35%) and ensure `card.corrupt()` correctly swaps `active_effects` to `corrupted_effects`.
- **Hand & Deck Management**: 
  - When a card is played, is it correctly removed from `state.hand`?
  - In `draw_to_hand`, does it correctly draw up to `HAND_SIZE` (5)?
  - Check `Deck._reshuffle()`: If the draw pile is empty, does it correctly move the discard pile back to the draw pile and shuffle?

#### 4. Shadow AI & Turn Management (src/game/battle.py)
- Analyze `_shadow_turn` and `_resolve_shadow_card`.
- Do different personalities (Accuser, Watcher, Mourner, Tyrant, Forgotten One) correctly modify attack/drain values?
- Verify that Shadow armor resets at the start of its turn (`self.state.shadow_armor = 0`).
- Check if the Shadow can play more cards than it has in its deck (does `shadow_deck.draw()` handle empty decks gracefully?).

#### 5. State Serialization & Gradio Sync (src/game/*.py & app.py)
- The game relies on `BattleState.to_dict()` and `from_dict()`. 
- Check if all nested objects (like `hand`, `events`, `player_deck_data`) are correctly serialized and deserialized. 
- **CRITICAL**: In `app.py`, `on_play_card` calls `_get_battle(state)` which uses `BattleState.from_dict()`. After modifications, it calls `_save_battle(state, bs)`. Verify that `state["battle"]` is fully updated and no references to the old dictionary are kept, which could cause state desync in Gradio.

#### 6. Edge Cases & Game Over
- What happens if the player plays a card that kills the Shadow? Does `_check_game_over` trigger immediately, preventing the player from playing more cards that turn?
- What happens if the Shadow kills the player during `_shadow_turn`? Does the UI correctly transition to the ending screen without allowing the player to end their turn?
- Check `on_end_turn` in `app.py`: If the game is already over, does it block the action?

### OUTPUT FORMAT
Please provide your review in the following structured format:
1. **Critical Bugs**: Issues that will break the game or cause state desync. Provide exact code fixes.
2. **Logic Flaws**: Edge cases in battle math, deck management, or AI behavior.
3. **JS/Gradio Integration Risks**: Specific warnings about the JS bridge and Gradio event listeners.
4. **UI/UX Improvements**: Suggestions for better visual feedback or CSS tweaks.
5. **Refactoring Suggestions**: Code cleanup or architectural improvements for maintainability.

Be extremely detailed. Quote the specific lines or functions where issues are found.