"""
silhouette.py — Webcam image → pure black silhouette.

Uses rembg for background removal. Falls back to a CSS/SVG
humanoid silhouette string if rembg is unavailable or image
processing fails.
"""

from __future__ import annotations
import io
import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Primary: rembg-based silhouette extraction
# ---------------------------------------------------------------------------

def extract_silhouette(image_input) -> Optional[str]:
    """
    Convert a webcam image to a pure black silhouette encoded as a base64 PNG data URI.

    Args:
        image_input: PIL Image, numpy array, or bytes from Gradio webcam component.

    Returns:
        "data:image/png;base64,..." string, or None on failure.
    """
    try:
        from rembg import remove
        from PIL import Image
        import numpy as np

        # Normalise input to PIL Image
        if isinstance(image_input, np.ndarray):
            img = Image.fromarray(image_input).convert("RGBA")
        elif isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input)).convert("RGBA")
        elif hasattr(image_input, "convert"):   # already PIL
            img = image_input.convert("RGBA")
        else:
            logger.warning("Unknown image_input type: %s", type(image_input))
            return None

        # Convert to bytes for rembg
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Remove background
        removed = remove(img_bytes.read())

        # Load result and convert all non-transparent pixels to pure black
        result = Image.open(io.BytesIO(removed)).convert("RGBA")
        pixels = result.load()
        width, height = result.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 10:
                    pixels[x, y] = (0, 0, 0, a)

        # Encode to base64
        out = io.BytesIO()
        result.save(out, format="PNG")
        b64 = base64.b64encode(out.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    except ImportError:
        logger.warning("rembg not installed — using CSS fallback silhouette.")
        return None
    except Exception as exc:
        logger.error("Silhouette extraction failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Fallback: pure CSS/SVG humanoid silhouette
# ---------------------------------------------------------------------------

FALLBACK_SILHOUETTE_HTML = """
<div class="silhouette-fallback-wrapper">
  <div class="silhouette-fallback">
    <!-- Head -->
    <div class="sf-head"></div>
    <!-- Neck -->
    <div class="sf-neck"></div>
    <!-- Shoulders + torso -->
    <div class="sf-torso"></div>
    <!-- Lower body fades into smoke -->
    <div class="sf-lower"></div>
  </div>
  <div class="sf-smoke sf-smoke-1"></div>
  <div class="sf-smoke sf-smoke-2"></div>
  <div class="sf-smoke sf-smoke-3"></div>
</div>
<style>
.silhouette-fallback-wrapper {
  position: relative;
  width: 160px;
  height: 320px;
  margin: 0 auto;
}
.silhouette-fallback {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  filter: drop-shadow(0 0 30px rgba(100, 40, 200, 0.6));
}
.sf-head {
  width: 60px; height: 70px;
  background: #000;
  border-radius: 50%;
  margin-top: 10px;
}
.sf-neck {
  width: 22px; height: 18px;
  background: #000;
}
.sf-torso {
  width: 100px; height: 140px;
  background: #000;
  border-radius: 12px 12px 8px 8px;
}
.sf-lower {
  width: 80px; height: 80px;
  background: linear-gradient(to bottom, #000 0%, transparent 100%);
  border-radius: 0 0 30px 30px;
}
.sf-smoke {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;
  filter: blur(20px);
  pointer-events: none;
}
.sf-smoke-1 { width:120px; height:60px; background:rgba(80,20,140,0.4); animation: sf-drift 8s ease-in-out infinite alternate; }
.sf-smoke-2 { width:90px;  height:45px; background:rgba(60,10,120,0.3); animation: sf-drift 11s ease-in-out infinite alternate-reverse; }
.sf-smoke-3 { width:150px; height:50px; background:rgba(100,30,160,0.2); animation: sf-drift 6s ease-in-out infinite alternate; }
@keyframes sf-drift {
  0%   { transform: translateX(-60%) scaleX(1.0); }
  100% { transform: translateX(-40%) scaleX(1.1); }
}
</style>
"""


def get_silhouette_display(image_input) -> tuple[str, bool]:
    """
    Returns (display_content, is_real_photo).

    display_content: Either an <img> tag with base64 silhouette,
                     or the fallback HTML string.
    is_real_photo: True if actual webcam photo was processed.
    """
    if image_input is not None:
        b64 = extract_silhouette(image_input)
        if b64:
            img_html = f"""
            <div class="silhouette-photo-wrapper">
              <img src="{b64}"
                   class="silhouette-photo"
                   alt="Your silhouette"
                   style="width:160px;height:auto;filter:drop-shadow(0 0 30px rgba(100,40,200,0.6));" />
              <div class="silhouette-glow-overlay"></div>
            </div>
            """
            return img_html, True

    # Fallback
    return FALLBACK_SILHOUETTE_HTML, False
