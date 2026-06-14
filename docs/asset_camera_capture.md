# ASSET SPEC: CAMERA CAPTURE UI
### SHADOWSELF · Visual Asset Specification v1.0

---

## PURPOSE

The camera capture moment is the game's first act of intimacy.  
The player offers their face. The game accepts it and transforms it.  
This moment must feel **ceremonial, not technical**.

The player should not feel like they are uploading a photo.  
They should feel like they are looking into a mirror that will look back.

---

## EXPERIENCE FLOW

```
PHASE 1: INVITATION
↓ (prose text invites player)

PHASE 2: VIEWFINDER ACTIVE
↓ (webcam shown in ritual frame)

PHASE 3: CAPTURE
↓ (player clicks capture button)

PHASE 4: SILHOUETTE EXTRACTION
↓ (image processed → silhouette)

PHASE 5: TRANSFORMATION SEQUENCE
↓ (silhouette animated reveal)

PHASE 6: SHADOW BIRTH
↓ (shadow portrait finalized → proceed to battle)
```

---

## PHASE 1: INVITATION TEXT

Before the webcam activates, a full-screen text invitation appears.

### Text Content
```
The mirror is ready.

Before you begin, it will need to see you.

Not your name.
Not your history.
Just your face.

What it finds there
will become your Shadow.

[Click to Continue]
```

### Typography
- Font: Cormorant Garamond, Italic
- Size: `1.4rem`, line-height `2.2`
- Color: `rgba(210, 200, 240, 0.85)`
- Center-aligned
- Text appears with stagger: each line fades in `0.4s` after the previous

### Button
- Text: "I'm ready." (lowercase, intimate)
- Font: Cinzel, `0.85rem`, letter-spacing `0.3em`
- Style: Minimal — just a bottom border, no fill
- On hover: glows softly purple
- On click: text fades out, webcam phase begins

---

## PHASE 2: VIEWFINDER UI

### Overall Layout
```
┌─────────────────────────────────────────────┐
│                                             │
│      "Look into the mirror."               │
│                                             │
│  ┌──────────────────────────────────┐      │
│  │                                  │      │
│  │         [ WEBCAM FEED ]          │      │
│  │           480 × 360              │      │
│  │                                  │      │
│  │   ◥ ─────────────────────── ◤   │      │
│  │   │   FACE PLACEMENT GUIDE  │   │      │
│  │   ◣ ─────────────────────── ◢   │      │
│  │                                  │      │
│  └──────────────────────────────────┘      │
│                                             │
│           [ CAPTURE ]                       │
│                                             │
│  "The mirror will remember this."           │
│                                             │
└─────────────────────────────────────────────┘
```

### Viewfinder Frame

The webcam feed is NOT shown in a plain rectangle.  
It is shown in a **ritualistic circular vignette** with frame ornaments.

```css
.viewfinder-container {
  position: relative;
  width: 400px;
  height: 400px;
  border-radius: 50%;        /* Circular crop */
  overflow: hidden;
  border: 2px solid rgba(180, 160, 220, 0.4);
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.8),
    0 0 40px rgba(100, 50, 180, 0.3),
    inset 0 0 60px rgba(0, 0, 0, 0.5);   /* Vignette inside */
}

.webcam-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);    /* Mirror flip — always intuitive */
  filter: brightness(0.9) contrast(1.05);
}

/* Dark vignette overlay on webcam */
.viewfinder-vignette {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(
    circle at 50% 50%,
    transparent 50%,
    rgba(0, 0, 0, 0.6) 100%
  );
  pointer-events: none;
}
```

### Rotating Outer Ring
```css
.viewfinder-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 1px solid transparent;
  background: conic-gradient(
    rgba(180, 160, 220, 0.6) 0%,
    rgba(180, 160, 220, 0.1) 50%,
    rgba(180, 160, 220, 0.6) 100%
  ) border-box;
  -webkit-mask: linear-gradient(#fff 0 0) padding-box,
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  animation: ring-rotate 8s linear infinite;
}

@keyframes ring-rotate {
  to { transform: rotate(360deg); }
}
```

### Corner Marks (Face Placement Guide)
4 corner bracket marks inside the circle, indicating face placement:
- `◥ ◤` top-left, top-right
- `◣ ◢` bottom-left, bottom-right
- Color: `rgba(180, 160, 220, 0.5)`
- These pulse gently: `opacity 0.5 → 0.9 → 0.5` every `2s`

---

## CAPTURE BUTTON

### Design
- Shape: Circular, `64px × 64px`
- Outer ring: `2px solid rgba(180, 160, 220, 0.6)`
- Inner fill: `rgba(180, 160, 220, 0.08)`
- Center icon: Camera shutter or "◉" symbol
- Font for label: Cinzel, `0.75rem`, letter-spacing `0.2em`, below button

### Hover State
```css
.capture-btn:hover {
  background: rgba(180, 160, 220, 0.15);
  box-shadow: 0 0 20px rgba(140, 100, 240, 0.5);
  transform: scale(1.05);
}
```

### Active/Click State
```css
.capture-btn:active {
  transform: scale(0.95);
  box-shadow: 0 0 40px rgba(140, 100, 240, 0.9);
  transition: all 0.1s ease;
}
```

---

## PHASE 3: CAPTURE MOMENT

When the player clicks capture:

1. **Flash**: Full-screen white flash, `opacity: 0 → 0.7 → 0` over `0.4s`
2. **Freeze**: Webcam feed freezes on captured frame
3. **Ring pulse**: The rotating ring accelerates to `2s` speed for `1s`, then stops
4. **Transition**: Captured image scales down to small thumbnail while transformation begins

```css
@keyframes capture-flash {
  0%   { opacity: 0; }
  20%  { opacity: 0.7; }
  100% { opacity: 0; }
}

.capture-flash-overlay {
  position: fixed;
  inset: 0;
  background: white;
  pointer-events: none;
  animation: capture-flash 0.4s ease-out forwards;
  z-index: 9999;
}
```

---

## PHASE 4: SILHOUETTE EXTRACTION

### Processing Display

While `rembg` / background removal runs (typically < 2s):

```
┌──────────────────────────────────────────┐
│                                          │
│   [ Frozen captured image — dimmed ]     │
│                                          │
│         ◎ Extracting your shadow...      │
│                                          │
│         ══════════░░░░░  62%             │
│                                          │
└──────────────────────────────────────────┘
```

- Loading text cycles: "Extracting your shadow…" / "Finding what you carry…" / "The mirror is learning you…"
- Progress bar: simulated smooth progress (even if actual processing is instant)
- Captured image visible but darkened: `brightness(0.4) grayscale(0.6)`

### Technical Implementation
```python
# In silhouette.py
from rembg import remove
from PIL import Image
import io

def extract_silhouette(image_bytes: bytes) -> bytes:
    """
    Removes background and converts to pure black silhouette.
    Returns PNG bytes of silhouette on transparent background.
    """
    # Remove background
    output_bytes = remove(image_bytes)
    img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    
    # Convert non-transparent pixels to pure black
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 10:  # Not transparent
                pixels[x, y] = (0, 0, 0, a)  # Black silhouette
    
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()
```

---

## PHASE 5: TRANSFORMATION SEQUENCE

The most cinematic moment in the entire game's opening.  
Duration: approximately 4–5 seconds.

### Sequence

```
t=0.0s  Captured image visible, processing complete
t=0.5s  Image begins desaturating (grayscale over 0.8s)
t=1.3s  Image inverts to silhouette (CSS filter: invert)
         + edge-detect effect: sharpen briefly
t=2.0s  Silhouette detaches from background (fade background to black)
t=2.5s  Silhouette pulses: grows very slightly then settles
t=3.0s  Purple glow appears around silhouette
t=3.5s  Smoke tendrils begin emanating from silhouette edges
t=4.0s  Text fades in: "Your Shadow has taken shape."
t=5.0s  → Transition to prologue / battle
```

### CSS Transformation Sequence

```css
@keyframes transform-to-silhouette {
  0%   { filter: none; }
  25%  { filter: grayscale(1) brightness(0.8); }
  50%  { filter: grayscale(1) invert(1) brightness(0.9) contrast(2); }
  75%  { filter: grayscale(1) invert(1) brightness(0.5) contrast(3); }
  100% { filter: none; }  /* rembg output applied */
}

@keyframes silhouette-emerge {
  0%   { opacity: 0; transform: scale(0.9); }
  100% { opacity: 1; transform: scale(1.0);
         filter: drop-shadow(0 0 40px rgba(100, 40, 200, 0.6)); }
}
```

### Smoke Emergence Effect

After silhouette is revealed:
- 4–6 CSS pseudo-elements blurred with `filter: blur(8px)`
- Each one drifts upward from the silhouette edges
- Color: `rgba(80, 20, 140, 0.4)`
- Duration: `3–5s` each, staggered starts

---

## PHASE 6: SHADOW BIRTH TEXT

Final text appearing after transformation:

```
Your Shadow has taken shape.

It has been waiting for this moment
longer than you know.

It has something to say.
```

- Font: Cormorant Garamond Italic
- Size: `1.2rem`
- Color: `rgba(210, 200, 240, 0.85)`
- Appears line by line with `0.5s` stagger
- After last line: Button appears — "Face your Shadow."

---

## FALLBACK: NO WEBCAM

If the player's device has no webcam, or they decline camera permission:

- Show a message: *"No camera found. A shadow has been summoned from memory instead."*
- Generate a generic humanoid silhouette using pure CSS/SVG
- Game proceeds normally with generated silhouette
- The AI proceeds without the photo — card generation and personality are still fully AI-driven

```css
/* Generic silhouette fallback */
.silhouette-fallback {
  width: 160px;
  height: 320px;
  background: #000000;
  border-radius: 80px 80px 40px 40px / 60px 60px 40px 40px;
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  filter: drop-shadow(0 0 30px rgba(100, 40, 200, 0.5));
}
```

---

## COLOR PALETTE (CAMERA CAPTURE)

```css
--viewfinder-ring:     rgba(180, 160, 220, 0.5);
--viewfinder-glow:     rgba(100, 50, 180, 0.35);
--capture-btn-border:  rgba(180, 160, 220, 0.6);
--capture-btn-hover:   rgba(180, 160, 220, 0.15);
--flash-color:         rgba(255, 255, 255, 0.7);
--smoke-color:         rgba(80, 20, 140, 0.4);
--processing-bar:      linear-gradient(90deg, #6B21A8, #A855F7);
```
