"""
html_screens.py — HTML string generators for every SHADOWSELF screen.

All screens are pure HTML/CSS — no Gradio default widgets used for visuals.
Gradio is used only for state management and event wiring (via gr.State, gr.Button etc.)
"""

from __future__ import annotations
import html
from typing import List, Optional
from src.game.card import Card, ARCHETYPE_COLORS
from src.game.battle import BattleState, PLAYER_MAX_HP, SHADOW_MAX_HP, ENERGY_PER_TURN


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """HTML-escape a string."""
    return html.escape(str(text))


def _hp_bar(current: int, maximum: int, css_class: str = "") -> str:
    pct = max(0, min(100, (current / maximum) * 100))
    danger = " danger" if pct < 30 else ""
    return f"""
    <div class="health-bar-row">
      <div class="health-bar-track">
        <div class="health-bar-fill {css_class}{danger}" style="width:{pct:.1f}%"></div>
      </div>
      <div class="hp-text">{current}/{maximum}</div>
    </div>"""


def _energy_pips(current: int, maximum: int = ENERGY_PER_TURN) -> str:
    pips = ""
    for i in range(maximum):
        spent = " spent" if i >= current else ""
        pips += f'<div class="energy-pip{spent}"></div>'
    return f'<div class="energy-row"><span class="energy-label">Energy</span>{pips}</div>'


def _shadow_card_back_html() -> str:
    return """
    <div class="card shadow-card-back" style="
        width:68px; 
        height:95px; 
        background: #020108;
        border: 1px solid rgba(120, 40, 180, 0.25);
        border-radius: 6px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 12px rgba(120, 40, 180, 0.1);
        flex-shrink: 0;
    ">
      <!-- Inverse eclipse pattern -->
      <div style="
          position: absolute;
          inset: 0;
          background-image: radial-gradient(circle at center, transparent 40%, rgba(120, 40, 180, 0.1) 80%);
          background-size: 20px 20px;
          opacity: 0.05;
      "></div>
      
      <!-- Glowing eye -->
      <div class="shadow-card-eye" style="
          width: 24px;
          height: 12px;
          background: #fff;
          border-radius: 50%;
          opacity: 0.25;
          box-shadow: 0 0 8px #fff, 0 0 16px rgba(120, 40, 180, 0.8);
          position: relative;
          animation: shadow-eye-pulse 2.5s infinite alternate ease-in-out;
      ">
        <!-- Slit -->
        <div style="
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #020108;
            transform: translateX(-50%);
        "></div>
      </div>
    </div>
    """

def _card_html(card: Card, clickable: bool = True, slot_size: bool = False, face_down: bool = False) -> str:
    """Render a single card as HTML."""
    if face_down:
        return _shadow_card_back_html()

    rgb = card.archetype_color_rgb
    icon = card.archetype_icon
    rarity_class = f"rarity-{card.rarity}"
    rarity_gems = {"common": "◆", "rare": "◆◆", "mythic": "◆◆◆"}.get(card.rarity, "◆")
    corrupted_class = " corrupted" if card.is_corrupted else ""
    desc = card.corrupted_description if card.is_corrupted else card.pure_description

    width = "68px" if slot_size else "100px"
    height = "95px" if slot_size else "140px"

    eff = card.active_effects
    stats = []
    if getattr(eff, "attack", 0) > 0:      stats.append(f'<span class="card-stat">ATK <span>{eff.attack}</span></span>')
    if getattr(eff, "heal", 0) > 0:        stats.append(f'<span class="card-stat">HP <span>+{eff.heal}</span></span>')
    if getattr(eff, "armor", 0) > 0:       stats.append(f'<span class="card-stat">ARM <span>{eff.armor}</span></span>')
    if getattr(eff, "draw", 0) > 0:        stats.append(f'<span class="card-stat">DRAW <span>{eff.draw}</span></span>')
    if getattr(eff, "self_damage", 0) > 0: stats.append(f'<span class="card-stat" style="color:rgba(240,80,100,0.9)">SELF <span>{eff.self_damage}</span></span>')
    if getattr(eff, "enemy_heal", 0) > 0:  stats.append(f'<span class="card-stat" style="color:rgba(200,80,80,0.9)">SHDHP <span>+{eff.enemy_heal}</span></span>')

    return f"""
    <div class="card{corrupted_class}" style="--card-rgb:{rgb}; width:{width}; height:{height};"
         data-card-id="{_esc(card.id)}" title="{_esc(card.flavor_text)}" draggable="true">
      <div class="card-header">
        <div class="card-cost">{card.cost}</div>
        <div class="card-rarity {rarity_class}">{rarity_gems}</div>
      </div>
      <div class="card-icon-zone">{icon}</div>
      <div class="card-name">{_esc(card.name)}</div>
      <div class="card-desc">{_esc(desc)}</div>
      <div class="card-stats">{''.join(stats)}</div>
    </div>"""


def _shadow_portrait_html(personality: str = "The Watcher") -> str:
    return f"""
    <div class="shadow-portrait">
      <div class="shadow-aura"></div>
      <div class="shadow-body-wrap">
        <div class="shadow-body-shape"></div>
        <div class="shadow-eyes">
          <div class="shadow-eye"></div>
          <div class="shadow-eye"></div>
        </div>
      </div>
      <div class="shadow-smoke"></div>
    </div>"""


def _battle_background_html() -> str:
    """Layered background elements (fixed, behind everything)."""
    shards = ""
    positions = [
        (8, 15, 40, 140, -8), (18, 10, 30, 90, 5), (72, 8, 20, 70, 12),
        (82, 20, 35, 110, -5), (5, 55, 15, 50, 20), (90, 45, 25, 80, -15),
        (45, 5, 18, 60, 3), (60, 70, 22, 75, -10), (30, 80, 16, 55, 8),
        (78, 65, 28, 95, 15),
    ]
    for left, top, w, h, rot in positions:
        shards += f'<div class="mirror-shard" style="left:{left}%;top:{top}%;width:{w}px;height:{h}px;transform:rotate({rot}deg);opacity:{0.2+abs(rot)/100:.2f};border-radius:2px;"></div>'

    fog_clouds = ""
    clouds = [(15, 25, 400, 300, 0.18), (60, 35, 350, 250, 0.15), (35, 55, 500, 200, 0.12)]
    for left, top, w, h, opacity in clouds:
        fog_clouds += f'<div class="fog-cloud" style="left:{left}%;top:{top}%;width:{w}px;height:{h}px;background:radial-gradient(ellipse,rgba(100,30,180,{opacity}) 0%,transparent 70%);"></div>'

    return f"""
    <div class="battle-bg">
      <div class="battle-bg-void"></div>
      <div class="ground-fog"></div>
      {fog_clouds}
      {shards}
      <div class="eclipse-overhead">
        <div class="eclipse-outer" style="width:100%;height:100%;border-radius:50%;border:1.5px solid rgba(192,180,220,0.4);position:relative;">
          <div class="eclipse-inner" style="position:absolute;width:78%;height:78%;background:#08080D;border-radius:50%;top:11%;left:16%;"></div>
        </div>
      </div>
    </div>"""


# ---------------------------------------------------------------------------
# SCREEN: Loading
# ---------------------------------------------------------------------------

def loading_screen_html() -> str:
    particles = ""
    for i in range(12):
        left = (i * 8 + 5) % 95
        delay = (i * 0.7) % 6
        dur = 5 + (i % 4)
        particles += f'<div class="particle" style="left:{left}%;animation-duration:{dur}s;animation-delay:{delay}s;"></div>'

    return """
    <div id="loading-screen">
      """ + particles + """
      <div class="eclipse-symbol">
        <div class="eclipse-outer">
          <div class="eclipse-inner"></div>
        </div>
      </div>
      <div class="logo-title">SHADOWSELF</div>
      <div class="logo-tagline">Every shadow has a name.</div>
      <div class="loading-bar-track">
        <div class="loading-bar-fill"></div>
      </div>
      <div class="loading-text" id="loading-msg">Summoning your shadow\u2026</div>

      <button id="inner-begin-btn"
        style="margin-top:40px;padding:12px 36px;
               font-family:'Cinzel',serif;font-size:0.78rem;
               letter-spacing:0.3em;text-transform:uppercase;
               background:rgba(124,58,237,0.2);
               border:1px solid rgba(168,85,247,0.6);
               color:rgba(220,200,255,0.9);border-radius:4px;
               cursor:pointer;box-shadow:0 0 20px rgba(124,58,237,0.3);
               opacity:0;transition:opacity 0.8s ease;pointer-events:none;">
        \u2756 Begin \u2756
      </button>
    </div>
    <script>
    (function() {
      var msgs = [
        'Summoning your shadow\u2026',
        'Polishing the mirror\u2026',
        'The darkness is listening\u2026',
        'Preparing the ritual table\u2026',
        'Your other self is waiting\u2026'
      ];
      var idx = 0;
      var el = document.getElementById('loading-msg');
      if (el) {
        setInterval(function() {
          idx = (idx + 1) % msgs.length;
          el.textContent = msgs[idx];
        }, 1500);
      }

      function doBegin() {
        // Find the hidden Gradio begin button outside the overlay
        var allBtns = document.querySelectorAll('button');
        for (var b = 0; b < allBtns.length; b++) {
          var txt = (allBtns[b].textContent || '').trim();
          if ((txt.indexOf('Begin') !== -1) && allBtns[b].id !== 'inner-begin-btn') {
            allBtns[b].click();
            return;
          }
        }
        // Fallback: direct id
        var btn = document.getElementById('btn-start');
        if (btn) btn.click();
      }

      var innerBtn = document.getElementById('inner-begin-btn');

      // Show Begin button after loading bar animation (2.8s)
      setTimeout(function() {
        if (innerBtn) {
          innerBtn.style.opacity = '1';
          innerBtn.style.pointerEvents = 'auto';
          innerBtn.onclick = doBegin;
        }
        // Auto-advance 1.5s later if user hasn't clicked
        setTimeout(doBegin, 1500);
      }, 2800);
    })();
    </script>"""


# ---------------------------------------------------------------------------
# SCREEN: Camera Capture
# ---------------------------------------------------------------------------

def camera_invitation_html() -> str:
    return """
    <div class="ss-screen screen-enter" style="background:var(--bg-base);">
      <div class="camera-screen">
        <div class="invitation-text">
          The mirror is ready.<br><br>
          Before you begin, it will need to see you.<br><br>
          Not your name.<br>
          Not your history.<br>
          Just your face.<br><br>
          What it finds there<br>
          will become your Shadow.
        </div>
      </div>
    </div>"""


def silhouette_transform_html(silhouette_html: str, is_real: bool) -> str:
    msg = (
        "Your shadow has been extracted from the light."
        if is_real else
        "No camera found — a shadow has been summoned from memory instead."
    )
    return f"""
    <div class="ss-screen screen-enter transform-screen" style="background:var(--bg-base);">
      <div class="transform-content" style="text-align:center; width: 100%;">
        {silhouette_html}
        <div class="transform-text">
          {_esc(msg)}<br><br>
          <em>It has something to say.</em>
        </div>
        <div style="margin-top: 40px;">
          <button id="inner-face-btn" class="ss-btn ss-btn-primary" onclick="document.getElementById('btn-face-shadow').click()">
            ⟶ Face Your Shadow
          </button>
        </div>
      </div>
    </div>"""


# ---------------------------------------------------------------------------
# SCREEN: Prologue (dialogue choices)
# ---------------------------------------------------------------------------

def prologue_screen_html(
    intro_lines: List[str],
    personality: str,
    question: str = "",
    choices: Optional[List[str]] = None,
    question_index: int = 0,
) -> str:
    """Render the prologue screen with inline choices that trigger hidden Gradio buttons via JS."""
    lines_html = "".join(f"<div>{_esc(line)}</div>" for line in intro_lines)

    choices_html = ""
    if question and choices:
        choice_items = ""
        for i, choice in enumerate(choices):
            # Each choice button calls a JS function that finds & clicks the hidden Gradio button
            safe_choice = _esc(choice)
            choice_items += f"""
            <button class="prologue-choice-btn"
                    onclick="shadowselfChooseOption({question_index}, '{safe_choice.replace("'", "\\'")}')"
                    id="prologue-choice-{question_index}-{i}">
              {safe_choice}
            </button>"""
        choices_html = f"""
        <div class="prologue-question-text">{_esc(question)}</div>
        <div class="prologue-choices-grid">
          {choice_items}
        </div>"""

    return f"""
    <div class="ss-screen screen-enter" style="background:var(--bg-base);">
      <div class="prologue-screen">
        <div style="margin-bottom:24px;">
          {_shadow_portrait_html(personality)}
        </div>
        <div class="prologue-shadow-quote">
          {lines_html}
        </div>
        <div class="prologue-question">Before we begin — answer honestly.</div>
        <div id="prologue-choices" class="choice-buttons">
          {choices_html}
        </div>
      </div>
    </div>
    <style>
    .prologue-question-text {{
      font-family: var(--font-heading);
      font-size: 0.72rem;
      letter-spacing: 0.2em;
      color: rgba(160,145,200,0.7);
      text-transform: uppercase;
      margin-bottom: 16px;
      text-align: center;
    }}
    .prologue-choices-grid {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      align-items: center;
      max-width: 480px;
      margin: 0 auto;
    }}
    .prologue-choice-btn {{
      width: 100%;
      padding: 12px 20px;
      background: rgba(80,40,120,0.15);
      border: 1px solid rgba(160,145,200,0.3);
      border-radius: 6px;
      color: rgba(220,200,255,0.85);
      font-family: var(--font-body);
      font-size: 0.82rem;
      line-height: 1.4;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      letter-spacing: 0.02em;
    }}
    .prologue-choice-btn:hover {{
      background: rgba(120,60,200,0.25);
      border-color: rgba(168,85,247,0.6);
      color: rgba(255,240,255,0.95);
      transform: translateX(4px);
      box-shadow: -2px 0 0 rgba(168,85,247,0.5), 0 0 12px rgba(120,60,200,0.2);
    }}
    .prologue-choice-btn:active {{
      transform: translateX(2px) scale(0.99);
      background: rgba(140,70,220,0.35);
    }}
    </style>
    """



# ---------------------------------------------------------------------------
# SCREEN: Battle
# ---------------------------------------------------------------------------

def battle_screen_html(
    state: BattleState,
    dialogue_line: str = "",
    hand_cards: Optional[List[dict]] = None,
    shadow_played_cards: Optional[List[dict]] = None,
    log_message: str = "",
) -> str:
    hand_cards = hand_cards or state.hand
    shadow_played_cards = shadow_played_cards or []

    # Turn badge
    if state.game_over:
        badge_text = "\u2756 BATTLE ENDED \u2756"
        badge_class = ""
    elif state.is_player_turn:
        badge_text = "\u25c6 Your Turn \u25c6"
        badge_class = ""
    else:
        badge_text = "\u25c8 Shadow Stirs \u25c8"
        badge_class = " shadow-turn"

    # Energy pips
    energy_pips = ""
    for i in range(ENERGY_PER_TURN):
        spent = " spent" if i >= state.player_energy else ""
        energy_pips += f'<div class="energy-pip{spent}"></div>'

    # Shadow hand (face-down cards)
    shadow_hand_count = len(getattr(state, 'shadow_hand', []))
    shadow_hand_html = ""
    for i in range(4):
        if i < shadow_hand_count:
            shadow_hand_html += '<div class="card-back-shadow" title="Shadow card"></div>'
        else:
            shadow_hand_html += '<div class="card-slot empty"></div>'

    # Shadow field (cards played this turn)
    shadow_field_html = ""
    if shadow_played_cards:
        for cd in shadow_played_cards[:3]:
            c = Card.from_dict(cd)
            shadow_field_html += f"""
            <div class="card shadow-card" style="--card-rgb:{c.archetype_color_rgb};width:80px;height:112px;" title="{_esc(c.flavor_text)}">
              <div class="card-header"><div class="card-cost">{c.cost}</div><div class="card-rarity rarity-{c.rarity}">&#9670;</div></div>
              <div class="card-icon-zone" style="font-size:1.2rem;">{c.archetype_icon}</div>
              <div class="card-name" style="font-size:0.55rem;">{_esc(c.name)}</div>
            </div>"""
    else:
        shadow_field_html = '<div class="field-placeholder">Shadow watches\u2026</div>'

    # Player field (cards played this turn)
    player_field_html = ""
    played = getattr(state, "player_played_cards", [])
    if played:
        for cd in played:
            c = Card.from_dict(cd)
            player_field_html += _card_html(c, clickable=False, slot_size=True)
    else:
        player_field_html = '<div class="field-placeholder">Drag or click a card to play</div>'

    # Deck counts
    player_draw_count = len(state.player_deck_data.get("draw_pile", []))
    player_discard_count = len(state.player_deck_data.get("discard_pile", []))
    shadow_draw_count = len(state.shadow_deck_data.get("draw_pile", []))
    shadow_discard_count = len(state.shadow_deck_data.get("discard_pile", []))

    # Player hand cards
    hand_html = ""
    for cd in hand_cards:
        c = Card.from_dict(cd)
        hand_html += _card_html(c, clickable=state.is_player_turn and not state.game_over)
    if not hand_cards:
        hand_html = '<div class="field-placeholder" style="padding:16px;">No cards in hand.</div>'

    # Dialogue
    dialogue_html = ""
    if dialogue_line:
        dialogue_html = f"""
        <div class="dialogue-box">
          <div class="dialogue-speaker">Your Shadow</div>
          <div class="dialogue-text">{_esc(dialogue_line)}</div>
        </div>"""

    # Log styling
    log_class = ""
    if "corrupt" in log_message.lower():
        log_class = " event-corrupt"
    elif "shadow" in log_message.lower():
        log_class = " event-shadow"
    elif log_message:
        log_class = " event-player"

    # End turn button state
    end_turn_disabled = 'disabled' if not (state.is_player_turn and not state.game_over) else ''

    return f"""
    <div id="battle-screen" class="screen-enter">
      {_battle_background_html()}

      <!-- ========== TOP ROW: Shadow side ========== -->
      <div class="battle-top-row">
        <div class="profile-area shadow-profile-area">
          {_shadow_portrait_html(state.shadow_personality)}
          {_hp_bar(state.shadow_hp, SHADOW_MAX_HP, "shadow-bar")}
          <div class="profile-name">{_esc(state.shadow_personality)}</div>
        </div>

        <div class="hand-zone shadow-hand-zone">
          {shadow_hand_html}
        </div>

        <div class="deck-zone">
          <div class="deck-stack shadow-deck-stack" title="Shadow draw pile: {shadow_draw_count} cards">
            <div class="deck-count">{shadow_draw_count}</div>
          </div>
          <div class="deck-label">Draw: {shadow_draw_count}</div>
          <div class="deck-label-sub">Discard: {shadow_discard_count}</div>
        </div>
      </div>

      <!-- ========== MIDDLE: Battle Field (orange border) ========== -->
      <div class="battle-field-wrapper">
        <div class="turn-indicator">
          <div class="turn-badge{badge_class}">{badge_text}</div>
          <div class="turn-number">TURN {state.turn_number}</div>
        </div>

        {dialogue_html}

        <div class="battle-field" id="battle-field">
          <div class="field-half shadow-field">
            <div class="field-label">Shadow Plays</div>
            <div class="field-cards">{shadow_field_html}</div>
          </div>
          <div class="field-divider"></div>
          <div class="field-half player-field" id="player-field">
            <div class="field-label">Your Field</div>
            <div class="field-cards">{player_field_html}</div>
          </div>
        </div>

        <div class="game-log{log_class}">{_esc(log_message)}</div>
      </div>

      <!-- ========== BOTTOM ROW: Player side ========== -->
      <div class="battle-bottom-row">
        <div class="deck-zone">
          <div class="deck-stack player-deck-stack" title="Your draw pile: {player_draw_count} cards">
            <div class="deck-count">{player_draw_count}</div>
          </div>
          <div class="deck-label">Draw: {player_draw_count}</div>
          <div class="deck-label-sub">Discard: {player_discard_count}</div>
        </div>

        <div class="player-hand-zone">
          <div class="hand-info-row">
            <div class="hand-label">Your hand ({len(hand_cards)} cards)</div>
            <div class="energy-row">
              <span class="energy-label">Energy</span>
              {energy_pips}
            </div>
          </div>
          <div class="hand-cards" id="hand-cards-container">
            {hand_html}
          </div>
        </div>

        <div class="profile-area player-profile-area">
          <div class="player-avatar" title="The Self">
            <div class="player-avatar-inner">\u2726</div>
          </div>
          {_hp_bar(state.player_hp, PLAYER_MAX_HP)}
          <div class="profile-name">The Self</div>
          <button class="end-turn-btn" onclick="document.getElementById('btn-end-turn').click()" {end_turn_disabled}>\u27f3 End Turn</button>
        </div>
      </div>
    </div>"""


# ---------------------------------------------------------------------------
# SCREEN: Ending Summary
# ---------------------------------------------------------------------------

def ending_screen_html(
    state: BattleState,
    reflection_text: str,
    player_deck_stats: dict,
) -> str:
    outcome_label = "Victory" if state.outcome == "win" else "Defeat"
    outcome_color = "rgba(140,200,160,0.9)" if state.outcome == "win" else "rgba(220,100,120,0.9)"

    paragraphs = reflection_text.strip().split("\n\n")
    reflection_html = "".join(f"<p>{_esc(p.strip())}</p>" for p in paragraphs if p.strip())

    avoided = ", ".join(player_deck_stats.get("never_played_archetypes", [])[:3]) or "none"
    most_used = player_deck_stats.get("most_used_archetype", "unknown") or "unknown"
    cards_played_count = player_deck_stats.get("total_played", 0)

    personality_sigils = {
        "The Accuser": "\u261e",
        "The Watcher": "\u25c9",
        "The Mourner": "\u2193",
        "The Tyrant": "\u265b",
        "The Forgotten One": "\u2234",
    }
    sigil = personality_sigils.get(state.shadow_personality, "\u25c6")

    return f"""
    <div class="ss-screen screen-enter" style="background:var(--bg-base);padding:32px 20px;">
      <div class="summary-card">
        <div style="position:absolute;top:12px;left:12px;width:18px;height:18px;border-top:1px solid rgba(180,160,220,0.4);border-left:1px solid rgba(180,160,220,0.4);"></div>
        <div style="position:absolute;top:12px;right:12px;width:18px;height:18px;border-top:1px solid rgba(180,160,220,0.4);border-right:1px solid rgba(180,160,220,0.4);"></div>
        <div style="position:absolute;bottom:12px;left:12px;width:18px;height:18px;border-bottom:1px solid rgba(180,160,220,0.4);border-left:1px solid rgba(180,160,220,0.4);"></div>
        <div style="position:absolute;bottom:12px;right:12px;width:18px;height:18px;border-bottom:1px solid rgba(180,160,220,0.4);border-right:1px solid rgba(180,160,220,0.4);"></div>

        <div class="summary-sigil">{sigil}</div>
        <div class="summary-title">Psychological Reflection</div>
        <div class="summary-subtitle">Observation Record · SHADOWSELF</div>

        <div class="summary-divider"></div>

        <div class="summary-stat-grid">
          <div class="summary-stat-row">
            <div class="summary-stat-label">Shadow Personality</div>
            <div class="summary-stat-value">{_esc(state.shadow_personality)}</div>
          </div>
          <div class="summary-stat-row">
            <div class="summary-stat-label">Battle Outcome</div>
            <div class="summary-stat-value" style="color:{outcome_color};">{outcome_label}</div>
          </div>
          <div class="summary-stat-row">
            <div class="summary-stat-label">Turns Endured</div>
            <div class="summary-stat-value">{state.turn_number}</div>
          </div>
          <div class="summary-stat-row">
            <div class="summary-stat-label">Cards Played</div>
            <div class="summary-stat-value">{cards_played_count}</div>
          </div>
          <div class="summary-stat-row">
            <div class="summary-stat-label">Most Reached For</div>
            <div class="summary-stat-value">{_esc(most_used)}</div>
          </div>
          <div class="summary-stat-row">
            <div class="summary-stat-label">Corruptions Suffered</div>
            <div class="summary-stat-value">{state.corruptions_triggered}</div>
          </div>
        </div>

        <div class="summary-divider"></div>

        <div class="summary-reflection">
          {reflection_html}
        </div>

        <div class="summary-divider"></div>

        <div class="summary-inscription">
          The mirror has been put away. · SHADOWSELF
        </div>
      </div>
    </div>"""
