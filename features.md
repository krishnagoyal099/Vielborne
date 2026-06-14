
I need you to implement three visual enhancements for the SHADOWSELF battle system:

## FEATURE 1: SHADOW DECK VISIBILITY
Add a deck indicator for the Shadow's draw pile, similar to the player's deck indicator already in the battle screen.

**Requirements:**
- Show the number of cards remaining in Shadow's draw pile
- Display it in the battle HUD or near the Shadow's portrait area
- Show discard pile count as well
- Use the same visual style as the player's deck indicator (already implemented in `battle_screen_html` function)
- Position it on the Shadow's side of the screen (left side typically)

**Implementation:**
In `src/ui/html_screens.py`, modify the `battle_screen_html` function to:
1. Extract Shadow deck data from `state.shadow_deck_data`
2. Calculate `shadow_draw_count = len(state.shadow_deck_data.get("draw_pile", []))`
3. Calculate `shadow_discard_count = len(state.shadow_deck_data.get("discard_pile", []))`
4. Add a deck indicator HTML similar to the player's (around line 780-800 in the current code)

## FEATURE 2: SHADOW CARD BACKS
When Shadow cards are in hand or being held, show their back side (face-down). Only flip them face-up when they're played to the table.

**Card Back Design (from asset spec):**
- Background: `#020108` (near-black with slight purple)
- Pattern: Inverse eclipse symbol tiled at 20px, opacity 0.05
- Central image: Shadow's eye (glowing white slits), opacity 0.25
- Border: `1px solid rgba(120, 40, 180, 0.25)`
- Subtle animation: Eye glow pulses slowly (2.5s cycle)

**Implementation:**
In `src/ui/html_screens.py`:
1. Add a new function `_shadow_card_back_html()` that generates the card back HTML
2. Modify `_card_html()` to accept a `face_down` parameter
3. When rendering Shadow's hand/field cards, check if they've been played:
   - If NOT played yet: show card back
   - If played: show card face
4. Add CSS for `.card-back-shadow` class in `src/ui/styles.py`

**CSS Example:**
```css
.card-back-shadow {
width: 68px; height: 95px;
background: #020108;
border: 1px solid rgba(120, 40, 180, 0.25);
border-radius: 8px;
position: relative;
overflow: hidden;
}

.card-back-shadow::before {
/* Eclipse pattern */
content: '';
position: absolute;
inset: 0;
background-image: url("data:image/svg+xml,..."); /* inverse eclipse */
background-size: 20px 20px;
opacity: 0.05;
}

.card-back-shadow::after {
/* Shadow eye */
content: '';
position: absolute;
top: 50%; left: 50%;
transform: translate(-50%, -50%);
width: 24px; height: 6px;
background: rgba(255, 255, 255, 0.25);
border-radius: 50%;
box-shadow: 0 0 8px rgba(200, 180, 255, 0.4);
animation: shadow-eye-pulse 2.5s ease-in-out infinite;
}

@keyframes shadow-eye-pulse {
0%, 100% { opacity: 0.25; box-shadow: 0 0 8px rgba(200, 180, 255, 0.4); }
50% { opacity: 0.4; box-shadow: 0 0 14px rgba(200, 180, 255, 0.7); }
}
```

## FEATURE 3: CARD PLAY ANIMATION
When the player clicks a card to play it, animate the card moving from their hand to the table field BEFORE executing the effects.

**Animation Sequence:**
1. Player clicks card in hand
2. Card lifts up (scale 1.1, translateY -20px, z-index 100)
3. Card travels from hand position to the table slot (0.4s ease-in-out)
4. Card lands in slot (brief scale bounce 0.95 → 1.0)
5. Card settles (0.1s)
6. Effects execute (damage numbers, HP changes, etc.)

**Implementation:**

**A. CSS Animation (add to `src/ui/styles.py`):**
```css
.card-playing {
position: fixed !important;
z-index: 1000 !important;
transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
pointer-events: none !important;
}

.card-playing.landing {
animation: card-land 0.3s ease-out forwards;
}

@keyframes card-land {
0% { transform: scale(1.1); }
50% { transform: scale(0.95); }
100% { transform: scale(1.0); }
}
```

**B. JavaScript (add to `src/ui/js_bridge.py`):**
Add a new function `playCardAnimation(cardId, targetSlotSelector)` that:
1. Finds the card element by ID
2. Gets its current position (getBoundingClientRect)
3. Creates a fixed-position clone of the card
4. Calculates target position (the table slot)
5. Animates the clone to the target position
6. Returns a Promise that resolves when animation completes

**C. Modify `app.py` - `on_play_card` function:**
1. Before executing card effects, trigger the animation
2. Wait for animation to complete (use gr.HTML to inject JS and wait)
3. Then execute the card effects as normal
4. Remove the card from hand (it's now on the table)

**Example flow:**
```python
def on_play_card(card_id: str, state: dict):
    # 1. Generate animation JS
    anim_js = f"""
    <script>
    (async () => {{
        const cardEl = document.querySelector(`[data-card-id="{card_id}"]`);
        const targetSlot = document.querySelector('#player-field .card-slot:first-child');
        await window.ShadowSelf.animateCardToSlot(cardEl, targetSlot);
        // Trigger Gradio button click to continue
        document.getElementById('btn-play-card-continue').click();
    }})();
    </script>
    """
    
    # 2. Return animation first
    return battle_screen_html(...), anim_js, state
    
    # 3. Hidden button triggers actual effect resolution
    # (wire this in Gradio event handlers)
```

**D. Update `battle_screen_html`:**
- Add card slot placeholders in the player field zone
- When a card is played, it moves from hand to the first available slot
- Show played cards in the slot (not in hand anymore)

## FILES TO MODIFY:
1. `src/ui/html_screens.py` - Add deck indicators, card back rendering
2. `src/ui/styles.py` - Add card back CSS, animation CSS
3. `src/ui/js_bridge.py` - Add card animation JavaScript
4. `app.py` - Modify play card flow to include animation step
5. `src/game/battle.py` - Track which shadow cards have been played vs in hand

## PRIORITY ORDER:
1. Shadow deck visibility (easiest)
2. Shadow card backs (medium)
3. Card play animation (hardest - requires state machine changes)

Please implement these features one at a time, starting with the Shadow deck visibility. Test each feature before moving to the next.
```

