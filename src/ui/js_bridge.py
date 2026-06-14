"""
js_bridge.py — JavaScript snippets injected into the Gradio app.

Handles:
- Floating damage/heal/effect number popups
- Screen transition animations
- Card play visual feedback
"""

# ---------------------------------------------------------------------------
# Main JS — injected once into the page head via gr.HTML
# ---------------------------------------------------------------------------

MAIN_JS = """
<script>
// ============================================================
// SHADOWSELF — Client-side JS
// ============================================================

window.ShadowSelf = window.ShadowSelf || {};

// Spawn a floating effect number at the given DOM element
ShadowSelf.spawnPopup = function(text, type, anchorSelector) {
  const anchor = document.querySelector(anchorSelector);
  if (!anchor) return;
  const rect = anchor.getBoundingClientRect();

  const el = document.createElement('div');
  el.className = 'effect-popup ' + type;
  el.textContent = text;
  el.style.left = (rect.left + rect.width / 2 - 20) + 'px';
  el.style.top  = (rect.top  + window.scrollY - 10) + 'px';
  document.body.appendChild(el);

  setTimeout(() => { if (el.parentNode) el.parentNode.removeChild(el); }, 1500);
};

// Flash the whole screen briefly (for captures, attacks)
ShadowSelf.flashScreen = function(color, durationMs) {
  const el = document.createElement('div');
  el.style.cssText = [
    'position:fixed','inset:0','z-index:9999',
    'background:' + (color || 'white'),
    'pointer-events:none','opacity:0.6',
    'transition:opacity ' + (durationMs || 400) + 'ms ease'
  ].join(';');
  document.body.appendChild(el);
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      el.style.opacity = '0';
      setTimeout(() => { if (el.parentNode) el.parentNode.removeChild(el); }, durationMs || 400);
    });
  });
};

// Shake an element (shadow hit)
ShadowSelf.shake = function(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  el.style.animation = 'none';
  el.style.transition = 'transform 0.1s ease';
  const steps = [4, -4, 3, -3, 2, -2, 0];
  let i = 0;
  const step = () => {
    if (i >= steps.length) { el.style.transform = ''; return; }
    el.style.transform = 'translateX(' + steps[i] + 'px)';
    i++;
    setTimeout(step, 50);
  };
  step();
};

// Auto-scroll to bottom of the game log
ShadowSelf.scrollLog = function() {
  const log = document.querySelector('.game-log');
  if (log) log.scrollIntoView({behavior:'smooth', block:'nearest'});
};

// Animate energy pip refill
ShadowSelf.refillEnergy = function() {
  const pips = document.querySelectorAll('.energy-pip');
  pips.forEach((pip, i) => {
    pip.classList.remove('spent');
    pip.style.animation = 'none';
    setTimeout(() => {
      pip.style.animation = 'pip-refill 0.4s cubic-bezier(0.34,1.56,0.64,1) forwards';
    }, i * 120);
  });
};

// Handle Prologue Choices
window.shadowselfChooseOption = function(qi, choiceText) {
    console.log("[SS] User clicked choice, qi:", qi, "text:", choiceText);
    
    // Disable all choice buttons to prevent double-clicks
    var btns = document.querySelectorAll('.prologue-choice-btn');
    btns.forEach(function(b) { b.disabled = true; b.style.opacity='0.5'; });
    
    // Find all hidden Gradio choice buttons
    var allGrBtns = document.querySelectorAll('button[id^="choice-"]');
    var clicked = false;
    
    for (var i = 0; i < allGrBtns.length; i++) {
        var btn = allGrBtns[i];
        var id = btn.id || '';
        var txt = (btn.textContent || '').trim();
        
        // Check if ID starts with 'choice-{qi}-' AND text matches exactly
        if (id.startsWith('choice-' + qi + '-') && txt === choiceText) {
            console.log("[SS] Match found! Clicking:", btn.id);
            btn.click();
            clicked = true;
            break;
        }
    }
    
    if (!clicked) {
        console.warn('[SS] Could not find Gradio button for qi:', qi, 'choice:', choiceText);
        // Re-enable so user can retry if something went wrong
        btns.forEach(function(b) { b.disabled = false; b.style.opacity=''; });
    }
};

// Feature 3: Card Play Animation
ShadowSelf.animateCardToSlot = function(cardEl, targetSlot) {
    return new Promise((resolve) => {
        if (!cardEl || !targetSlot) {
            resolve();
            return;
        }

        const startRect = cardEl.getBoundingClientRect();
        const endRect = targetSlot.getBoundingClientRect();

        // Create a clone
        const clone = cardEl.cloneNode(true);
        // Remove ID so it doesn't conflict
        clone.removeAttribute('id');
        clone.removeAttribute('data-card-id');
        clone.classList.add('card-playing');

        // Set initial position
        clone.style.left = startRect.left + 'px';
        clone.style.top = startRect.top + 'px';
        clone.style.width = startRect.width + 'px';
        clone.style.height = startRect.height + 'px';
        clone.style.margin = '0';

        document.body.appendChild(clone);

        // Hide original immediately
        cardEl.style.opacity = '0';

        // Trigger animation
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                clone.classList.add('landing');
                clone.style.left = endRect.left + 'px';
                clone.style.top = endRect.top + 'px';
                // Scale width/height to match target slot
                clone.style.width = endRect.width + 'px';
                clone.style.height = endRect.height + 'px';

                // Wait for CSS transition (0.4s) + settle (0.1s)
                setTimeout(() => {
                    if (clone.parentNode) {
                        clone.parentNode.removeChild(clone);
                    }
                    resolve();
                }, 500);
            });
        });
    });
};

// Wire card clicks to trigger play via hidden textbox + button
(function() {
  let isPlaying = false;
  function triggerCardPlay(cardId) {
    if (isPlaying) return;
    isPlaying = true;
    window._pendingCardId = cardId;

    // Find the hidden textbox wrapper and its textarea
    var taWrap = document.getElementById('card-id-input');
    if (!taWrap) { console.warn('[SS] card-id-input not found'); isPlaying = false; return; }

    var ta = taWrap.tagName === 'TEXTAREA' || taWrap.tagName === 'INPUT' ? taWrap : taWrap.querySelector('textarea, input');
    if (!ta) { console.warn('[SS] Inner textarea not found'); isPlaying = false; return; }

    // Set value via native setter (bypasses Svelte reactivity)
    var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set
        || Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
    if (nativeSetter) {
      nativeSetter.call(ta, cardId);
    } else {
      ta.value = cardId;
    }
    // Dispatch events for Svelte bind:value
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('change', { bubbles: true }));

    console.log('[SS] Set textbox value to:', cardId);

    // Click the play button after a short delay for Gradio to pick up the value
    setTimeout(function() {
      var btnWrap = document.getElementById('btn-play-card');
      if (!btnWrap) { console.warn('[SS] btn-play-card not found'); isPlaying = false; return; }
      var btn = btnWrap.tagName === 'BUTTON' ? btnWrap : btnWrap.querySelector('button');
      if (btn) {
          btn.click();
          console.log('[SS] Triggered play for:', cardId);
      } else {
          console.warn('[SS] No button found inside btn-play-card');
      }
      // release lock after a delay
      setTimeout(() => { isPlaying = false; }, 1200);
    }, 150);
  }

  // Delegate card clicks from anywhere on the page
  document.addEventListener('click', function(e) {
    var card = e.target.closest('.card[data-card-id]');
    if (!card) return;
    e.preventDefault();
    e.stopPropagation();
    triggerCardPlay(card.dataset.cardId);
  }, true);
})();

// ============================================================
// DRAG AND DROP FOR CARDS
// ============================================================

(function() {
  let draggedCardId = null;
  let draggedElement = null;
  
  // Make cards draggable
  document.addEventListener('dragstart', function(e) {
    const card = e.target.closest('.card[data-card-id]');
    if (!card) return;
    
    // Only allow dragging cards from the hand (not from played cards)
    if (!card.closest('.hand-cards')) return;
    
    draggedCardId = card.dataset.cardId;
    draggedElement = card;
    
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', draggedCardId);
    
    // Add visual feedback
    card.classList.add('dragging');
    console.log('[SS Drag] Started dragging card:', draggedCardId);
  }, true);
  
  document.addEventListener('dragend', function(e) {
    const card = e.target.closest('.card[data-card-id]');
    if (card) {
      card.classList.remove('dragging');
    }
    draggedCardId = null;
    draggedElement = null;
    
    // Clear drop zone highlights
    document.querySelectorAll('.card-zone.drop-target').forEach(function(zone) {
      zone.classList.remove('drop-target');
    });
  }, true);
  
  document.addEventListener('dragover', function(e) {
    const playerField = document.getElementById('player-field');
    if (!playerField) return;
    
    // Only allow drop over the player field
    if (playerField.contains(e.target)) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      playerField.classList.add('drop-target');
    }
  }, true);
  
  document.addEventListener('dragleave', function(e) {
    const playerField = document.getElementById('player-field');
    if (!playerField) return;
    
    // Remove highlight if leaving the field entirely
    if (e.target === playerField || !playerField.contains(e.relatedTarget)) {
      playerField.classList.remove('drop-target');
    }
  }, true);
  
  document.addEventListener('drop', function(e) {
    const playerField = document.getElementById('player-field');
    if (!playerField || !playerField.contains(e.target)) return;
    
    e.preventDefault();
    e.stopPropagation();
    
    const cardId = e.dataTransfer.getData('text/plain') || draggedCardId;
    playerField.classList.remove('drop-target');
    
    if (cardId) {
      console.log('[SS Drop] Dropped card:', cardId);
      // Trigger the card play with the dropped card
      triggerCardPlayDrop(cardId);
    }
  }, true);
  
  function triggerCardPlayDrop(cardId) {
    window._pendingCardId = cardId;

    // Find the hidden textbox wrapper and its textarea
    var taWrap = document.getElementById('card-id-input');
    if (!taWrap) { console.warn('[SS] card-id-input not found (drop)'); return; }

    var ta = taWrap.tagName === 'TEXTAREA' || taWrap.tagName === 'INPUT' ? taWrap : taWrap.querySelector('textarea, input');
    if (!ta) { console.warn('[SS] Inner textarea not found (drop)'); return; }

    var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set
        || Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
    if (nativeSetter) {
      nativeSetter.call(ta, cardId);
    } else {
      ta.value = cardId;
    }
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('change', { bubbles: true }));

    console.log('[SS] Drop set textbox value to:', cardId);

    setTimeout(function() {
      var btnWrap = document.getElementById('btn-play-card');
      if (!btnWrap) { console.warn('[SS] btn-play-card not found (drop)'); return; }
      var btn = btnWrap.tagName === 'BUTTON' ? btnWrap : btnWrap.querySelector('button');
      if (btn) {
          btn.click();
          console.log('[SS] Triggered play via drop:', cardId);
      } else {
          console.warn('[SS] No button found inside btn-play-card');
      }
    }, 150);
  }
})();

console.log('[ShadowSelf] JS bridge loaded with drag-and-drop support.');
</script>
"""


def damage_popup_js(value: int, target: str = "shadow") -> str:
    """Return inline JS to spawn a damage popup."""
    selector = ".shadow-body-wrap" if target == "shadow" else ".health-bar-track"
    return f"<script>ShadowSelf.spawnPopup('-{value}', 'damage', '{selector}');</script>"


def heal_popup_js(value: int, target: str = "player") -> str:
    selector = ".health-bar-track" if target == "player" else ".shadow-body-wrap"
    return f"<script>ShadowSelf.spawnPopup('+{value}', 'heal', '{selector}');</script>"


def corrupt_popup_js() -> str:
    return "<script>ShadowSelf.spawnPopup('CORRUPTED', 'corrupt', '.hand-cards');ShadowSelf.flashScreen('rgba(150,20,80,0.3)',500);</script>"


def shadow_hit_js() -> str:
    return "<script>ShadowSelf.shake('.shadow-body-wrap');ShadowSelf.flashScreen('rgba(168,85,247,0.15)',300);</script>"


def player_hit_js() -> str:
    return "<script>ShadowSelf.flashScreen('rgba(200,30,60,0.25)',400);</script>"
