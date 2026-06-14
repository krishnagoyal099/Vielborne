"""
styles.py — Complete CSS for SHADOWSELF.

Assembled from asset specifications in /docs/.
Injected into Gradio via gr.Blocks(css=CSS).
"""

CSS = """
/* ============================================================
   GOOGLE FONTS IMPORT (Moved to head_html in app.py)
   ============================================================ */

/* ============================================================
   DESIGN TOKENS
   ============================================================ */
:root {
  --bg-void:          #000000;
  --bg-deep:          #06050D;
  --bg-base:          #09070F;
  --bg-surface:       #0E0B18;
  --bg-elevated:      #141020;
  --bg-hover:         #1A1530;

  --border-subtle:    rgba(180,160,220,0.12);
  --border-default:   rgba(180,160,220,0.25);
  --border-strong:    rgba(180,160,220,0.5);
  --border-focus:     rgba(180,160,220,0.8);

  --text-primary:     rgba(230,220,255,0.95);
  --text-secondary:   rgba(200,185,240,0.75);
  --text-muted:       rgba(160,145,200,0.45);

  --accent-primary:   #A855F7;
  --accent-light:     #C084FC;
  --accent-dark:      #7C3AED;
  --accent-silver:    rgba(200,190,230,0.8);

  --font-display:     'Cinzel Decorative', serif;
  --font-heading:     'Cinzel', serif;
  --font-body:        'Cormorant Garamond', serif;

  --transition-base:   0.25s ease;
  --transition-ritual: 0.6s cubic-bezier(0.22,1,0.36,1);

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
}

/* ============================================================
   GRADIO OVERRIDES
   ============================================================ */
.gradio-container {
  background: transparent !important;
  max-width: 100% !important;
  padding: 0 !important;
}
footer { display: none !important; }
.gr-prose { display: none !important; }
#component-0 { background: transparent !important; }
.contain { background: transparent !important; }
.gap { background: transparent !important; gap: 0 !important; }
.form { background: transparent !important; border: none !important; }

/* ============================================================
   UTILITIES
   ============================================================ */
.sr-only {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0,0,0,0) !important;
  border: 0 !important;
  white-space: nowrap !important;
}

/* ============================================================
   GLOBAL BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%;
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

::selection { background: rgba(168,85,247,0.3); color: var(--text-primary); }
:focus-visible { outline: 1px solid rgba(168,85,247,0.6); outline-offset: 2px; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: rgba(168,85,247,0.3); border-radius: var(--radius-pill); }

/* ============================================================
   SHADOWSELF GAME WRAPPER
   ============================================================ */
#shadowself-app {
  min-height: 100vh;
  background: var(--bg-void);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  position: relative;
  overflow: hidden;
}

/* ============================================================
   LOADING SCREEN
   ============================================================ */
#loading-screen {
  position: relative;
  width: 100%;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: screen-enter 1s ease-out forwards;
}

.eclipse-symbol {
  width: 72px; height: 72px;
  position: relative;
  margin-bottom: 32px;
  animation: eclipse-rotate 20s linear infinite;
}
.eclipse-outer {
  width: 100%; height: 100%;
  border-radius: 50%;
  background: transparent;
  border: 2px solid rgba(192,180,220,0.5);
  position: relative;
  box-shadow: 0 0 20px rgba(168,85,247,0.3);
}
.eclipse-inner {
  position: absolute;
  width: 56px; height: 56px;
  background: #08080D;
  border-radius: 50%;
  top: 6px; left: 12px;
}
@keyframes eclipse-rotate { to { transform: rotate(360deg); } }

.logo-title {
  font-family: var(--font-display);
  font-size: clamp(2rem,5vw,4rem);
  font-weight: 700;
  letter-spacing: 0.35em;
  color: #fff;
  text-shadow: 0 0 24px rgba(200,180,255,0.7);
  text-transform: uppercase;
  margin-bottom: 8px;
  animation: logo-appear 2s ease-out forwards;
}

.logo-tagline {
  font-family: var(--font-body);
  font-style: italic;
  font-size: 1rem;
  letter-spacing: 0.2em;
  color: rgba(200,180,255,0.6);
  margin-bottom: 48px;
}

@keyframes logo-appear {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.loading-bar-track {
  width: 320px; height: 3px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(200,180,255,0.15);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 12px;
}
.loading-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #6B21A8, #A855F7, #E9D5FF);
  box-shadow: 0 0 12px rgba(168,85,247,0.8);
  animation: loading-fill 2.5s ease-in-out forwards;
}
@keyframes loading-fill {
  from { width: 0%; }
  to   { width: 100%; }
}

.loading-text {
  font-family: var(--font-body);
  font-style: italic;
  font-size: 0.85rem;
  color: rgba(200,180,255,0.5);
  letter-spacing: 0.1em;
}

/* Floating particles */
.particle {
  position: absolute;
  width: 2px; height: 2px;
  border-radius: 50%;
  background: rgba(168,85,247,0.5);
  animation: particle-float linear infinite;
  pointer-events: none;
}
@keyframes particle-float {
  0%   { transform: translateY(100vh) translateX(0); opacity: 0; }
  10%  { opacity: 0.6; }
  90%  { opacity: 0.4; }
  100% { transform: translateY(-10vh) translateX(30px); opacity: 0; }
}

/* ============================================================
   SCREEN SYSTEM
   ============================================================ */
.ss-screen {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  position: relative;
  background: var(--bg-base);
}

@keyframes screen-enter {
  from { opacity: 0; transform: scale(1.02); filter: blur(4px); }
  to   { opacity: 1; transform: scale(1.0);  filter: blur(0px); }
}
.screen-enter { animation: screen-enter 0.6s ease-out forwards; }

/* ============================================================
   BATTLE BACKGROUND
   ============================================================ */
.battle-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.battle-bg-void {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 55%, #130B1E 0%, #0C0714 40%, #07040F 70%, #000 100%);
}
.ground-fog {
  position: absolute; bottom: 0; left: 0; right: 0; height: 35%;
  background: linear-gradient(to top, rgba(60,20,100,0.35) 0%, rgba(60,20,100,0.15) 50%, transparent 100%);
  filter: blur(12px);
  animation: fog-drift 12s ease-in-out infinite alternate;
}
@keyframes fog-drift {
  0%   { transform: translateX(-3%) scaleX(1.05); opacity: 0.8; }
  100% { transform: translateX(3%) scaleX(0.97); opacity: 1.0; }
}
.fog-cloud {
  position: absolute; border-radius: 50%;
  filter: blur(40px); pointer-events: none; mix-blend-mode: screen;
}
.mirror-shard {
  position: absolute;
  background: rgba(20,10,40,0.9);
  border: 1px solid rgba(200,180,255,0.3);
  filter: drop-shadow(0 0 4px rgba(140,100,200,0.4));
  pointer-events: none;
}
.eclipse-overhead {
  position: absolute; top: 16px; left: 50%; transform: translateX(-50%);
  width: 48px; height: 48px; opacity: 0.65;
}

/* ============================================================
   CAMERA SCREEN
   ============================================================ */
.camera-screen {
  max-width: 640px;
  text-align: center;
}

.invitation-text {
  font-family: var(--font-body);
  font-style: italic;
  font-size: 1.3rem;
  line-height: 2.2;
  color: rgba(210,200,240,0.85);
  margin-bottom: 40px;
}

.viewfinder-wrapper {
  position: relative;
  width: 340px; height: 340px;
  margin: 0 auto 32px;
}
.viewfinder-circle {
  width: 100%; height: 100%;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(180,160,220,0.4);
  box-shadow: 0 0 40px rgba(100,50,180,0.3), inset 0 0 60px rgba(0,0,0,0.5);
  position: relative;
}
.viewfinder-vignette {
  position: absolute; inset: 0; border-radius: 50%;
  background: radial-gradient(circle at 50% 50%, transparent 50%, rgba(0,0,0,0.6) 100%);
  pointer-events: none; z-index: 2;
}
.viewfinder-ring {
  position: absolute; inset: -10px;
  border-radius: 50%;
  border: 1px solid transparent;
  background: conic-gradient(rgba(180,160,220,0.7) 0%, rgba(180,160,220,0.1) 50%, rgba(180,160,220,0.7) 100%) border-box;
  -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  mask-composite: exclude;
  animation: ring-rotate 8s linear infinite;
  pointer-events: none;
}
@keyframes ring-rotate { to { transform: rotate(360deg); } }

/* ============================================================
   BUTTONS
   ============================================================ */
.ss-btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  font-family: var(--font-heading);
  font-size: 0.75rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-default);
  background: rgba(180,160,220,0.06);
  color: var(--text-secondary);
  cursor: pointer;
  position: relative; overflow: hidden;
  transition: all var(--transition-base);
  user-select: none;
  text-decoration: none;
}
.ss-btn:hover {
  border-color: var(--border-strong);
  color: var(--text-primary);
  box-shadow: 0 0 16px rgba(168,85,247,0.25);
  transform: translateY(-1px);
}
.ss-btn:active { transform: translateY(0); box-shadow: none; }

.ss-btn-primary {
  background: rgba(124,58,237,0.2);
  border-color: rgba(168,85,247,0.6);
  color: rgba(220,200,255,0.95);
  box-shadow: 0 0 20px rgba(124,58,237,0.2);
}
.ss-btn-primary:hover {
  background: rgba(124,58,237,0.35);
  box-shadow: 0 0 30px rgba(168,85,247,0.4);
}

/* ============================================================
   BATTLE SCREEN — 3-ROW LAYOUT (Inscryption style)
   ============================================================ */
#battle-screen {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  padding: 0;
}

/* ---------- TOP ROW: Shadow side ---------- */
.battle-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(6,5,13,0.92);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(8px);
  z-index: 10;
  position: relative;
  gap: 16px;
}

.profile-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 120px;
  flex-shrink: 0;
}
.profile-name {
  font-family: var(--font-heading);
  font-size: 0.68rem;
  letter-spacing: 0.15em;
  color: var(--text-primary);
  text-align: center;
}

/* Shadow portrait override for inline layout */
.shadow-profile-area .shadow-portrait {
  width: 64px;
}
.shadow-profile-area .shadow-body-wrap {
  width: 50px;
  height: 100px;
}

/* Shadow hand zone in top row */
.hand-zone {
  display: flex;
  gap: 8px;
  justify-content: center;
  align-items: center;
  flex: 1;
}
.shadow-hand-zone {
  padding: 8px 12px;
  background: rgba(20,10,40,0.3);
  border-radius: 8px;
  border: 1px dashed rgba(180,160,220,0.15);
}

/* Deck zone (used by both sides) */
.deck-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
  min-width: 72px;
}
.deck-stack {
  position: relative;
  width: 56px;
  height: 78px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: help;
}
.shadow-deck-stack {
  border: 1px solid rgba(220,100,120,0.4);
  background: linear-gradient(135deg, rgba(40,20,30,0.9), rgba(20,10,15,0.9));
  box-shadow: 2px -2px 0 rgba(220,100,120,0.15), 4px -4px 0 rgba(220,100,120,0.05);
}
.player-deck-stack {
  border: 1px solid rgba(160,145,200,0.5);
  background: linear-gradient(135deg, rgba(30,20,40,0.9), rgba(15,10,20,0.9));
  box-shadow: 2px -2px 0 rgba(160,145,200,0.2), 4px -4px 0 rgba(160,145,200,0.1);
}
.deck-count {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  color: rgba(220,200,255,0.9);
  text-shadow: 0 0 6px rgba(120,80,200,0.8);
}
.deck-label {
  font-family: var(--font-heading);
  font-size: 0.55rem;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.deck-label-sub {
  font-family: var(--font-body);
  font-size: 0.6rem;
  color: rgba(160,145,200,0.4);
}

/* ---------- MIDDLE: Battle Field ---------- */
.battle-field-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 32px;
  position: relative;
  z-index: 1;
  gap: 12px;
}

.turn-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.turn-number {
  font-family: var(--font-heading);
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  color: var(--text-muted);
}

.battle-field {
  width: 90%;
  max-width: 800px;
  border: 3px solid rgba(255,140,0,0.4);
  border-radius: 16px;
  background: rgba(10,6,20,0.5);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 0 20px rgba(255,140,0,0.08);
}

.battle-field.drop-target,
.battle-field:has(.player-field.drop-target) {
  border-color: rgba(255,140,0,0.8);
  box-shadow: inset 0 0 30px rgba(255,140,0,0.15), 0 0 40px rgba(255,140,0,0.3);
}

.field-half {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  min-height: 130px;
  gap: 8px;
}
.shadow-field {
  background: rgba(40,10,60,0.15);
}
.player-field {
  background: rgba(10,20,40,0.15);
  transition: background 0.3s ease;
}
.player-field.drop-target {
  background: rgba(255,140,0,0.08);
}

.field-label {
  font-family: var(--font-heading);
  font-size: 0.58rem;
  letter-spacing: 0.25em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 4px;
}
.field-cards {
  display: flex;
  gap: 10px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  min-height: 80px;
}
.field-placeholder {
  font-family: var(--font-body);
  font-style: italic;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.field-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,140,0,0.3) 20%, rgba(255,140,0,0.5) 50%, rgba(255,140,0,0.3) 80%, transparent);
  margin: 0;
}

/* ---------- BOTTOM ROW: Player side ---------- */
.battle-bottom-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px 16px;
  background: rgba(6,5,13,0.92);
  border-top: 1px solid var(--border-subtle);
  backdrop-filter: blur(8px);
  z-index: 10;
  position: relative;
  gap: 16px;
}

.player-hand-zone {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.hand-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Player avatar */
.player-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid rgba(160,145,200,0.4);
  background: rgba(20,15,35,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(120,80,200,0.2);
}
.player-avatar-inner {
  font-size: 1.6rem;
  color: rgba(200,185,255,0.7);
  text-shadow: 0 0 10px rgba(168,85,247,0.5);
}

/* Card back for shadow hand */
.card-back-shadow {
  width: 68px;
  height: 95px;
  background: #020108;
  border: 1px solid rgba(120, 40, 180, 0.25);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card-back-shadow::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20'%3E%3Ccircle cx='10' cy='10' r='8' fill='none' stroke='rgba(180,160,220,0.1)' stroke-width='1'/%3E%3C/svg%3E");
  background-size: 20px 20px;
  opacity: 0.05;
}
.card-back-shadow::after {
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

/* Empty card slot */
.card-slot.empty {
  border: 1px dashed rgba(180, 160, 220, 0.1);
  background: rgba(0, 0, 0, 0.2);
  width: 68px;
  height: 95px;
  border-radius: 8px;
  flex-shrink: 0;
}

/* ============================================================
   CARDS
   ============================================================ */
.card {
  width: 100px; height: 140px;
  border-radius: 8px;
  border: 1.5px solid rgba(var(--card-rgb), 0.5);
  background: linear-gradient(160deg, rgba(var(--card-rgb),0.1) 0%, #0D0A16 40%, #08060F 100%);
  box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 0 18px rgba(var(--card-rgb),0.2);
  position: relative; overflow: hidden; cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s ease;
  display: flex; flex-direction: column;
  user-select: none;
  flex-shrink: 0;
}
.card:hover {
  transform: translateY(-10px) scale(1.06);
  box-shadow: 0 12px 40px rgba(var(--card-rgb),0.5), 0 0 60px rgba(var(--card-rgb),0.2);
  z-index: 50;
}
.card.corrupted {
  border-color: rgba(150,30,80,0.8);
  background: linear-gradient(160deg, rgba(100,10,40,0.2) 0%, #0D0A16 40%, #08060F 100%);
  box-shadow: 0 0 20px rgba(150,30,80,0.4);
}
.card.shadow-card {
  cursor: default;
}
.card.shadow-card:hover { transform: none; }

.card-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 4px 6px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-family: var(--font-heading); font-size: 0.58rem;
  color: var(--text-muted);
}
.card-cost {
  background: rgba(var(--card-rgb),0.25);
  border-radius: 50%;
  width: 16px; height: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.65rem; color: var(--text-primary);
  font-weight: 600;
}
.card-rarity { font-size: 0.55rem; letter-spacing: 0.05em; }
.rarity-common  { color: rgba(180,180,200,0.6); }
.rarity-rare    { color: rgba(140,100,255,0.9); }
.rarity-mythic  { color: rgba(250,200,80,0.9); }

.card-icon-zone {
  flex: 1; display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem;
  text-shadow: 0 0 12px rgba(var(--card-rgb),0.8);
}

.card-name {
  font-family: var(--font-heading);
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.06em;
  color: var(--text-primary);
  padding: 2px 6px;
  border-top: 1px solid rgba(255,255,255,0.05);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.card-desc {
  font-family: var(--font-body);
  font-size: 0.6rem; line-height: 1.3;
  color: var(--text-secondary);
  padding: 3px 6px;
  flex: 1;
}
.card.corrupted .card-desc { color: rgba(240,100,140,0.85); }

.card-stats {
  display: flex; gap: 4px;
  padding: 3px 6px;
  border-top: 1px solid rgba(255,255,255,0.04);
}
.card-stat {
  font-family: var(--font-heading);
  font-size: 0.55rem; color: var(--text-muted);
}
.card-stat span { color: var(--text-primary); font-weight: 600; }

/* ============================================================
   DRAG AND DROP STYLING
   ============================================================ */
.card.dragging {
  opacity: 0.6;
  transform: scale(0.95) rotate(-5deg);
  cursor: grabbing;
  z-index: 1000;
  border-color: rgba(255,140,0,0.9);
  box-shadow: 0 0 30px rgba(255,140,0,0.8), 0 8px 24px rgba(255,140,0,0.5);
}

.card-zone.drop-target {
  background: rgba(255,140,0,0.12);
  border: 3px solid rgba(255,140,0,0.8);
  box-shadow: inset 0 0 30px rgba(255,140,0,0.25), 0 0 30px rgba(255,140,0,0.5);
  transition: all 0.2s ease;
}

/* ============================================================
   PLAYER HAND
   ============================================================ */
.player-hand-section {
  width: 100%; padding: 12px 16px 20px;
  background: rgba(6,5,13,0.9);
  border-top: 1px solid var(--border-subtle);
  position: relative; z-index: 5;
}
.hand-top-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 10px;
}
.hand-label {
  font-family: var(--font-heading);
  font-size: 0.62rem; letter-spacing: 0.25em;
  color: var(--text-muted); text-transform: uppercase;
}
.hand-cards {
  display: flex; gap: 8px;
  justify-content: center; align-items: flex-end;
  flex-wrap: wrap;
}

/* Gradio button overrides for card play */
.ss-card-btn {
  background: none !important;
  border: none !important;
  padding: 0 !important;
  cursor: pointer !important;
}

/* End turn button */
.end-turn-btn {
  padding: 10px 28px;
  font-family: var(--font-heading);
  font-size: 0.72rem; letter-spacing: 0.25em; text-transform: uppercase;
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(168,85,247,0.4);
  color: rgba(200,185,255,0.85);
  border-radius: var(--radius-sm);
  cursor: pointer;
  box-shadow: 0 0 16px rgba(124,58,237,0.15);
  transition: all 0.2s ease;
}
.end-turn-btn:hover {
  background: rgba(124,58,237,0.25);
  border-color: rgba(168,85,247,0.7);
  box-shadow: 0 0 28px rgba(124,58,237,0.35);
  transform: translateY(-2px);
}
.end-turn-btn:disabled { opacity: 0.3; cursor: not-allowed; transform: none; box-shadow: none; }

/* ============================================================
   EFFECT POPUPS
   ============================================================ */
.effect-popup {
  position: fixed;
  font-family: var(--font-heading); font-size: 1.2rem; font-weight: 600;
  pointer-events: none; z-index: 200;
  animation: popup-float 1.4s ease-out forwards;
}
.effect-popup.damage  { color: rgba(240,100,100,0.95); }
.effect-popup.heal    { color: rgba(100,220,140,0.95); }
.effect-popup.armor   { color: rgba(180,180,220,0.95); }
.effect-popup.corrupt { color: rgba(180,40,100,0.95); }
@keyframes popup-float {
  0%   { opacity: 1; transform: translateY(0) scale(1.0); }
  20%  { transform: translateY(-14px) scale(1.2); }
  100% { opacity: 0; transform: translateY(-60px) scale(0.9); }
}

/* ============================================================
   SUMMARY / ENDING SCREEN
   ============================================================ */
.summary-card {
  width: min(680px, 95vw);
  background:
    linear-gradient(170deg, #1A1428 0%, #150F22 30%, #110D1E 60%, #0E0B1A 100%);
  border: 1px solid rgba(180,160,220,0.25);
  border-radius: 6px;
  padding: 40px 48px;
  box-shadow: 0 0 0 4px rgba(10,8,18,0.8), 0 0 60px rgba(80,40,140,0.3), 0 20px 80px rgba(0,0,0,0.7);
  position: relative;
  margin: 32px auto;
  animation: screen-enter 1s ease-out forwards;
}

.summary-sigil {
  text-align: center;
  font-size: 2rem; opacity: 0.5;
  margin-bottom: 8px;
}
.summary-title {
  font-family: var(--font-heading);
  font-size: 0.72rem; letter-spacing: 0.35em;
  color: rgba(180,160,220,0.5);
  text-transform: uppercase; text-align: center;
  margin-bottom: 4px;
}
.summary-subtitle {
  font-family: var(--font-body);
  font-style: italic; font-size: 0.82rem;
  color: rgba(180,160,220,0.35); text-align: center;
  margin-bottom: 24px;
}
.summary-divider {
  height: 1px; margin: 20px 0;
  background: linear-gradient(90deg, transparent, rgba(180,160,220,0.5) 20%, rgba(180,160,220,0.8) 50%, rgba(180,160,220,0.5) 80%, transparent);
  position: relative;
}
.summary-stat-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 8px 24px; margin-bottom: 4px;
}
.summary-stat-row { display: flex; flex-direction: column; gap: 2px; }
.summary-stat-label {
  font-family: var(--font-heading);
  font-size: 0.6rem; letter-spacing: 0.2em;
  color: rgba(180,160,220,0.55); text-transform: uppercase;
}
.summary-stat-value {
  font-family: var(--font-body);
  font-size: 0.95rem; color: rgba(230,220,255,0.9);
}
.summary-reflection {
  font-family: var(--font-body);
  font-size: 1.05rem; line-height: 1.85;
  color: rgba(210,200,240,0.85);
}
.summary-reflection p { margin-bottom: 16px; }
.summary-reflection p:first-child::first-letter {
  font-family: var(--font-heading); font-size: 2.6rem;
  float: left; margin-right: 6px; line-height: 0.85;
  color: rgba(180,160,220,0.9);
}
.summary-inscription {
  font-family: var(--font-display);
  font-size: 0.65rem; letter-spacing: 0.4em;
  color: rgba(180,160,220,0.3); text-align: center;
  margin-top: 8px;
}
.summary-actions {
  display: flex; gap: 12px; justify-content: center;
  margin-top: 28px; flex-wrap: wrap;
}

/* ============================================================
   PROLOGUE / DIALOGUE CHOICE SCREEN
   ============================================================ */
.prologue-screen {
  max-width: 640px; text-align: center;
  padding: 40px 24px;
}
.prologue-shadow-quote {
  font-family: var(--font-body);
  font-style: italic; font-size: 1.2rem; line-height: 1.9;
  color: rgba(210,200,240,0.85);
  margin-bottom: 32px;
  border-left: 2px solid rgba(168,85,247,0.5);
  padding-left: 20px; text-align: left;
}
.prologue-question {
  font-family: var(--font-heading);
  font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--text-muted); margin-bottom: 16px;
}
.choice-buttons {
  display: flex; flex-direction: column; gap: 10px;
  align-items: stretch; max-width: 440px; margin: 0 auto;
}
.choice-btn {
  padding: 12px 20px;
  font-family: var(--font-body); font-size: 1rem;
  color: var(--text-secondary);
  background: rgba(180,160,220,0.05);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer; text-align: left;
  transition: all 0.2s ease;
  font-style: italic;
}
.choice-btn:hover {
  background: rgba(180,160,220,0.12);
  border-color: var(--border-default);
  color: var(--text-primary);
  transform: translateX(4px);
}

/* ============================================================
   SILHOUETTE TRANSFORM SCREEN
   ============================================================ */
.transform-screen {
  text-align: center;
}
.transform-content {
  max-width: 500px; margin: 0 auto; width: 100%;
}
.transform-text {
  font-family: var(--font-body); font-style: italic;
  font-size: 1.1rem; line-height: 1.9;
  color: rgba(210,200,240,0.8); margin-top: 24px;
}
.silhouette-photo-wrapper { position: relative; display: inline-block; }
.silhouette-glow-overlay {
  position: absolute; inset: -20px;
  background: radial-gradient(ellipse at 50% 50%, rgba(80,20,140,0.3) 0%, transparent 70%);
  pointer-events: none;
}

/* ============================================================
   STATUS MESSAGES (game log)
   ============================================================ */
.game-log {
  max-width: 100%; width: 100%;
  font-family: var(--font-body); font-style: italic;
  font-size: 0.88rem; color: var(--text-muted);
  text-align: center; min-height: 22px;
  padding: 8px 16px;
  grid-column: 1 / 4;
  grid-row: 4;
}
.game-log.event-player { color: rgba(140,200,255,0.8); }
.game-log.event-shadow { color: rgba(200,100,150,0.85); }
.game-log.event-corrupt { color: rgba(220,80,120,0.9); }

/* ============================================================
   ANIMATIONS — SCREEN TRANSITIONS
   ============================================================ */
@keyframes screen-exit {
  0%   { opacity: 1; transform: scale(1.0); }
  100% { opacity: 0; transform: scale(0.97); filter: blur(4px); }
}
.screen-exit { animation: screen-exit 0.5s ease-in forwards; }

/* Screen reader only / visually hidden for Gradio components we need to interact with via JS */
.sr-only {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0,0,0,0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

/* ============================================================
   CARD PLAY ANIMATION & CARD BACKS (FEATURE 2 & 3)
   ============================================================ */

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
  /* Use a generic svg circle for the inverse eclipse if no specific url is available */
  background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="8" fill="white"/><circle cx="12" cy="8" r="8" fill="black"/></svg>');
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

.card-slot {
  width: 68px; height: 95px;
  border: 1px dashed rgba(160, 145, 200, 0.2);
  border-radius: 8px;
  background: rgba(0,0,0,0.2);
}
"""
