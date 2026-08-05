"""
make_video_mp4.py
=================
Generates a high-quality 60-second 1920x1080 MP4 concept animation for
AL SAFA Park — Al Hilal Urban Respite, Dubai.

Uses only: PIL (Pillow), imageio, numpy  (no OpenCV required).

Run:
    python tools/make_video_mp4.py

Output:
    UPLOAD_THESE_12_FILES/Falaj_Al_Safa_Concept_Film_60s_1080p.mp4
    UPLOAD_THESE_12_FILES/Falaj_Al_Safa_Concept_Film_60s_4K.mp4   (2x upscale)
"""

import os
import sys
import math
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

try:
    import imageio
except ImportError:
    sys.exit("imageio not found. Run: pip install imageio[ffmpeg]")

# ─── PATHS ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
RENDERS = ROOT / "design" / "renders" / "FINAL_6_PARK_IMAGES"
FIGURES = ROOT / "figures"
OUT_DIR = ROOT / "UPLOAD_THESE_12_FILES"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_1080 = OUT_DIR / "Falaj_Al_Safa_Concept_Film_60s_1080p.mp4"
OUT_4K   = OUT_DIR / "Falaj_Al_Safa_Concept_Film_60s_4K.mp4"

# ─── VIDEO PARAMS ─────────────────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 24
TOTAL  = 60          # seconds
FRAMES = FPS * TOTAL  # 1440 frames

# ─── COLOUR PALETTE ───────────────────────────────────────────────────────────
DEEP_NAVY   = (8,   18,  42)
GOLD        = (212, 175, 55)
LIGHT_GOLD  = (255, 220, 100)
WHITE       = (255, 255, 255)
OFF_WHITE   = (240, 235, 220)
EMERALD     = (16,  120, 80)
COOL_BLUE   = (30,  80, 140)
PALE_CREAM  = (248, 242, 228)
DARK_AMBER  = (180, 110, 20)

# ─── FONT HELPER ──────────────────────────────────────────────────────────────
def _font(size: int, bold: bool = False):
    """Try system fonts, fall back to PIL default."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT_TITLE   = _font(72, bold=True)
FONT_SUBTTL  = _font(44, bold=True)
FONT_BODY    = _font(30)
FONT_CAPTION = _font(22)
FONT_KPI     = _font(56, bold=True)
FONT_SMALL   = _font(20)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def ease_in_out(t: float) -> float:
    """Smooth ease-in-out curve [0,1] -> [0,1]."""
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def alpha_blend(bg: np.ndarray, fg: np.ndarray, alpha: float) -> np.ndarray:
    return np.clip(bg * (1 - alpha) + fg * alpha, 0, 255).astype(np.uint8)

def load_render(path: Path, size=(W, H)) -> np.ndarray:
    """Load and resize an image to (W, H), return as uint8 numpy array."""
    img = Image.open(path).convert("RGB").resize(size, Image.LANCZOS)
    return np.array(img)

def darken(arr: np.ndarray, factor: float = 0.55) -> np.ndarray:
    return np.clip(arr * factor, 0, 255).astype(np.uint8)

def vignette(arr: np.ndarray, strength: float = 0.55) -> np.ndarray:
    rows, cols = arr.shape[:2]
    Y, X = np.ogrid[:rows, :cols]
    cy, cx = rows / 2, cols / 2
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    mask = np.clip(1 - strength * dist, 0, 1)[..., np.newaxis]
    return np.clip(arr * mask, 0, 255).astype(np.uint8)

def draw_text_shadow(draw, pos, text, font, fill, shadow=(0,0,0), offset=(2,2)):
    draw.text((pos[0]+offset[0], pos[1]+offset[1]), text, font=font, fill=shadow)
    draw.text(pos, text, font=font, fill=fill)

def gold_separator(draw, y: int, width: int = 900, cx: int = W//2):
    x0 = cx - width//2
    draw.line([(x0, y), (x0+width, y)], fill=GOLD, width=2)
    draw.ellipse([(cx-5, y-5), (cx+5, y+5)], fill=GOLD)

def draw_centered(draw, text, y, font, fill, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw)//2, y), text, font=font, fill=fill)

def draw_centered_shadow(draw, text, y, font, fill, shadow=(0,0,0), width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x+2, y+2), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)

def progress_bar(draw, progress: float, y: int = H-14):
    """Thin gold progress bar at bottom."""
    draw.rectangle([(0, y), (W, H)], fill=(0,0,0,180))
    draw.rectangle([(0, y), (int(W * progress), H)], fill=GOLD)

def watermark(draw):
    draw.text((W-320, H-38), "AL SAFA PARK · DUBAI · 2025", font=FONT_SMALL, fill=(*GOLD, 180))

# ─── LOAD ASSETS ──────────────────────────────────────────────────────────────
print("Loading render images...")
IMG_AERIAL    = load_render(RENDERS / "01_Masterplan_Aerial_View.jpg")
IMG_WALKWAY   = load_render(RENDERS / "02_Spine_Corridor_Shaded_Walkway.jpg")
IMG_OASIS     = load_render(RENDERS / "03_Sunken_Oasis_Basin_AlNakhil.jpg")
IMG_DUNE      = load_render(RENDERS / "04_Childrens_Dune_Play.jpg")
IMG_SOUK      = load_render(RENDERS / "05_Souk_Kiosks_Community_Plaza.jpg")
IMG_NIGHT     = load_render(RENDERS / "06_Night_Plaza_Illuminated_Canopy.jpg")

print("Loading analysis figures...")
FIG_CLIMATE   = load_render(FIGURES / "fig01_climate_and_comfort.png")
FIG_COST      = load_render(FIGURES / "fig11_cost_plan.png")
FIG_SHADE     = load_render(FIGURES / "fig03_shade_by_zone.png")
FIG_MASTER    = load_render(FIGURES / "fig10_masterplan.png")

print(f"All assets loaded. Generating {TOTAL}s @ {FPS}fps = {FRAMES} frames...")

# ─── SCENE SYSTEM ─────────────────────────────────────────────────────────────
# Each scene: (start_sec, end_sec, render_fn)
# render_fn(f, f_in_scene, scene_dur) -> np.ndarray shape (H, W, 3)

def make_frame_pil(w=W, h=H, bg=DEEP_NAVY) -> tuple:
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    return img, draw

# ── SCENE 0 : TITLE CARD (0–5 s) ─────────────────────────────────────────────
def scene_title(f, f_in, dur):
    t = f_in / (dur * FPS)
    alpha = ease_in_out(min(t * 3, 1.0))  # fade in quickly
    fade_out = ease_in_out(max(0, (t - 0.7) * 3.33))
    a = alpha * (1 - fade_out)

    img, draw = make_frame_pil(bg=DEEP_NAVY)
    base = np.array(img)

    # Subtle gradient background
    for y in range(H):
        ratio = y / H
        r = int(lerp(8, 22, ratio))
        g = int(lerp(18, 35, ratio))
        b = int(lerp(42, 70, ratio))
        base[y, :] = [r, g, b]

    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)

    # Central geometric diamond ornament
    cx, cy = W//2, H//2 - 80
    size = int(90 * a)
    pts = [(cx, cy-size), (cx+size, cy), (cx, cy+size), (cx-size, cy)]
    if size > 5:
        draw.polygon(pts, outline=(*GOLD, int(200*a)), width=2)
        inner = int(size * 0.55)
        pts2 = [(cx, cy-inner), (cx+inner, cy), (cx, cy+inner), (cx-inner, cy)]
        draw.polygon(pts2, fill=(*GOLD, int(60*a)))

    y0 = H//2 - 20
    # Main title
    txt = "AL SAFA PARK"
    draw_centered_shadow(draw, txt, y0, FONT_TITLE, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, y0+85, 700)
    # Subtitle
    draw_centered_shadow(draw, "Al Hilal  ·  The Urban Respite", y0+105, FONT_SUBTTL, (*OFF_WHITE, int(220*a)))
    draw_centered(draw, "Dubai, UAE  ·  15,000 m²  ·  AED 26.97M", y0+165, FONT_BODY, (*PALE_CREAM, int(180*a)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 1 : CLIMATE CHALLENGE (5–15 s) ────────────────────────────────────
def scene_climate(f, f_in, dur):
    t = f_in / (dur * FPS)
    fade = ease_in_out(min(t * 2, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.8) * 5))
    a = fade * (1 - fade_out)

    # Use climate figure as backdrop, dark overlay
    fig_arr = FIG_CLIMATE.copy()
    fig_arr = darken(fig_arr, 0.40)
    fig_arr = vignette(fig_arr, 0.7)
    img = Image.fromarray(fig_arr)
    draw = ImageDraw.Draw(img)

    # KPI cards
    kpis = [
        ("56.8 °C", "Peak Heat Index"),
        ("4,402 h", "Annual Sunlight Hours"),
        ("44 %", "Canopy Comfort Gain"),
        ("+7.1 °C", "Falaj Cooling Effect"),
    ]
    card_w = 380
    gap = 30
    total_w = len(kpis) * card_w + (len(kpis)-1) * gap
    x0 = (W - total_w) // 2

    # Title
    txt = "THE CLIMATE CHALLENGE"
    draw_centered_shadow(draw, txt, 60, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 120, 600)

    for i, (val, label) in enumerate(kpis):
        x = x0 + i * (card_w + gap)
        y = 160
        # reveal each KPI sequentially
        ki = ease_in_out(min(max(t * 6 - i * 0.5, 0), 1))
        card_alpha = ki * a
        if card_alpha < 0.05:
            continue
        # Card bg
        overlay = Image.new("RGBA", (card_w, 160), (*DEEP_NAVY, int(210 * card_alpha)))
        img.paste(Image.fromarray(np.array(overlay)[..., :3]),
                  (x, y), mask=Image.fromarray(np.array(overlay)[:,:,3]))
        # Border
        draw.rectangle([(x, y), (x+card_w, y+160)], outline=(*GOLD, int(200*card_alpha)), width=2)
        # Value
        bbox = draw.textbbox((0,0), val, font=FONT_KPI)
        tw = bbox[2]-bbox[0]
        draw.text((x + (card_w-tw)//2 + 1, y+22), val, font=FONT_KPI, fill=(0,0,0))
        draw.text((x + (card_w-tw)//2, y+20), val, font=FONT_KPI, fill=(*LIGHT_GOLD, int(255*card_alpha)))
        # Label
        bbox2 = draw.textbbox((0,0), label, font=FONT_CAPTION)
        tw2 = bbox2[2]-bbox2[0]
        draw.text((x + (card_w-tw2)//2, y+96), label, font=FONT_CAPTION, fill=(*OFF_WHITE, int(200*card_alpha)))

    # Bottom caption
    cap = "Dubai's extreme heat demands bold urban design intervention."
    draw_centered(draw, cap, H-110, FONT_BODY, (*PALE_CREAM, int(200*a)))
    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 2 : AERIAL MASTERPLAN (15–24 s) ────────────────────────────────────
def scene_aerial(f, f_in, dur):
    t = f_in / (dur * FPS)
    # Ken Burns zoom effect: subtle scale from 1.02 -> 1.0
    zoom = lerp(1.06, 1.0, ease_in_out(t))
    fade = ease_in_out(min(t * 2.5, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.82) * 5.9))
    a = fade * (1 - fade_out)

    # Apply zoom
    arr = IMG_AERIAL.copy()
    if zoom != 1.0:
        new_w, new_h = int(W * zoom), int(H * zoom)
        img_big = Image.fromarray(arr).resize((new_w, new_h), Image.LANCZOS)
        xoff = (new_w - W) // 2
        yoff = (new_h - H) // 2
        arr = np.array(img_big)[yoff:yoff+H, xoff:xoff+W]

    arr = vignette(arr, 0.45)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    # Overlay panel at top
    overlay = Image.new("RGBA", (W, 130), (*DEEP_NAVY, int(190*a)))
    img.paste(Image.fromarray(np.array(overlay)[..., :3]), (0,0),
              mask=Image.fromarray(np.array(overlay)[:,:,3]))

    draw_centered_shadow(draw, "SITE MASTERPLAN  ·  150 m x 100 m", 28, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 90, 800)
    draw_centered(draw, "Al Safa Park  ·  Sheikh Zayed Road Corridor  ·  Dubai", 100, FONT_CAPTION, (*OFF_WHITE, int(200*a)))

    # Bottom info band
    overlay_b = Image.new("RGBA", (W, 110), (*DEEP_NAVY, int(200*a)))
    img.paste(Image.fromarray(np.array(overlay_b)[..., :3]), (0, H-110),
              mask=Image.fromarray(np.array(overlay_b)[:,:,3]))

    facts = [
        "Site Area: 15,000 m²",
        "1 Crescent Canopy Arc",
        "Al Falaj Water Channel",
        "Al Nakhil Oasis Basin",
        "131 Native Trees",
    ]
    col_w = W // len(facts)
    for i, fact in enumerate(facts):
        ki = ease_in_out(min(max(t*5 - i*0.3, 0), 1)) * a
        x = col_w * i + col_w // 2
        bbox = draw.textbbox((0,0), fact, font=FONT_CAPTION)
        tw = bbox[2]-bbox[0]
        draw.text((x - tw//2, H-84), fact, font=FONT_CAPTION, fill=(*LIGHT_GOLD, int(220*ki)))
        draw.text((x - tw//2, H-54), "─────", font=FONT_SMALL, fill=(*GOLD, int(180*ki)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 3 : CRESCENT CANOPY WALKWAY (24–33 s) ──────────────────────────────
def scene_walkway(f, f_in, dur):
    t = f_in / (dur * FPS)
    zoom = lerp(1.0, 1.04, ease_in_out(t))  # slow zoom in
    fade = ease_in_out(min(t * 2.5, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.82) * 5.9))
    a = fade * (1 - fade_out)

    arr = IMG_WALKWAY.copy()
    new_w, new_h = int(W*zoom), int(H*zoom)
    img_big = Image.fromarray(arr).resize((new_w, new_h), Image.LANCZOS)
    xoff = (new_w - W)//2; yoff = (new_h - H)//2
    arr = np.array(img_big)[yoff:yoff+H, xoff:xoff+W]
    arr = vignette(arr, 0.45)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    # Top panel
    overlay = Image.new("RGBA", (W, 130), (*DEEP_NAVY, int(190*a)))
    img.paste(Image.fromarray(np.array(overlay)[..., :3]), (0,0),
              mask=Image.fromarray(np.array(overlay)[:,:,3]))
    draw_centered_shadow(draw, "AL MAMSHA  ·  THE SHADED SPINE", 28, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 90, 700)
    draw_centered(draw, "Crescent Canopy  ·  Al Hilal Arch  ·  144.2 m Arc Length", 100, FONT_CAPTION, (*OFF_WHITE, int(200*a)))

    # Right-side stats panel
    panel_x = W - 440
    panel_y = 155
    specs = [
        ("18.0 m",  "Canopy Width"),
        ("4.5 m",   "Height Clearance"),
        ("7.0 m",   "Limestone Walkway"),
        ("0.9 m",   "Falaj Water Rill"),
        ("3.0 m",   "S. Louvre Fin"),
        ("ETFE",    "Diagrid Roofing"),
    ]
    for i, (val, lab) in enumerate(specs):
        ky = ease_in_out(min(max(t*4 - i*0.25, 0), 1)) * a
        y = panel_y + i * 68
        overlay_s = Image.new("RGBA", (410, 60), (*DEEP_NAVY, int(200*ky)))
        img.paste(Image.fromarray(np.array(overlay_s)[..., :3]), (panel_x, y),
                  mask=Image.fromarray(np.array(overlay_s)[:,:,3]))
        draw.rectangle([(panel_x, y), (panel_x+410, y+60)], outline=(*GOLD, int(160*ky)), width=1)
        draw.text((panel_x+16, y+4), val, font=FONT_SUBTTL, fill=(*LIGHT_GOLD, int(255*ky)))
        draw.text((panel_x+16, y+38), lab, font=FONT_SMALL, fill=(*OFF_WHITE, int(200*ky)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 4 : AL FALAJ WATER + OASIS (33–42 s) ────────────────────────────────
def scene_oasis(f, f_in, dur):
    t = f_in / (dur * FPS)
    # Cross-dissolve between oasis and dune play
    cross_t = ease_in_out(min(max((t - 0.5) * 3, 0), 1))
    fade = ease_in_out(min(t * 2.5, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.82) * 5.9))
    a = fade * (1 - fade_out)

    arr1 = vignette(IMG_OASIS.copy(), 0.5)
    arr2 = vignette(IMG_DUNE.copy(), 0.5)
    arr = alpha_blend(arr1, arr2, cross_t)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    # Left side eco stats panel
    panel_x = 30
    panel_y = 155

    title_a = ease_in_out(min(t*3, 1.0)) * a
    overlay = Image.new("RGBA", (W, 130), (*DEEP_NAVY, int(190*a)))
    img.paste(Image.fromarray(np.array(overlay)[..., :3]), (0,0),
              mask=Image.fromarray(np.array(overlay)[:,:,3]))

    title = "AL NAKHIL  ·  WATER & ECOLOGY"
    draw_centered_shadow(draw, title, 28, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 90, 700)
    draw_centered(draw, "Sunken Palm Court  ·  Falaj Revival  ·  Native Planting", 100, FONT_CAPTION, (*OFF_WHITE, int(200*a)))

    eco_stats = [
        ("12",     "Date Palms (Al Nakhil)"),
        ("58",     "Ghaf Trees (Prosopis)"),
        ("16",     "Neem Trees (N. Rank)"),
        ("131",    "Total Native Trees"),
        ("−7.1°C", "Heat Index Reduction"),
        ("1.2 m",  "Sunken Court Depth"),
    ]
    for i, (val, lab) in enumerate(eco_stats):
        ky = ease_in_out(min(max(t*4 - i*0.25, 0), 1)) * a
        y = panel_y + i * 70
        overlay_s = Image.new("RGBA", (390, 62), (*DEEP_NAVY, int(200*ky)))
        img.paste(Image.fromarray(np.array(overlay_s)[..., :3]), (panel_x, y),
                  mask=Image.fromarray(np.array(overlay_s)[:,:,3]))
        draw.rectangle([(panel_x, y), (panel_x+390, y+62)], outline=(*GOLD, int(160*ky)), width=1)
        draw.text((panel_x+14, y+3), val, font=FONT_SUBTTL, fill=(*EMERALD, int(255*ky)))
        draw.text((panel_x+14, y+38), lab, font=FONT_SMALL, fill=(*OFF_WHITE, int(200*ky)))

    # Cross-fade label
    if cross_t > 0.1:
        label2 = "CHILDREN'S DUNE PLAY  ·  Inclusive Design"
        draw_centered(draw, label2, H-90, FONT_BODY, (*LIGHT_GOLD, int(200*cross_t*a)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 5 : COMMUNITY SOUK + COST (42–51 s) ────────────────────────────────
def scene_souk(f, f_in, dur):
    t = f_in / (dur * FPS)
    fade = ease_in_out(min(t * 2.5, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.82) * 5.9))
    a = fade * (1 - fade_out)

    arr = vignette(IMG_SOUK.copy(), 0.45)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, 130), (*DEEP_NAVY, int(190*a)))
    img.paste(Image.fromarray(np.array(overlay)[..., :3]), (0,0),
              mask=Image.fromarray(np.array(overlay)[:,:,3]))
    draw_centered_shadow(draw, "AL SOUK  ·  COMMUNITY & ECONOMY", 28, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 90, 700)
    draw_centered(draw, "8 Timber Kiosks  ·  Bronze Mashrabiya  ·  Community Plaza", 100, FONT_CAPTION, (*OFF_WHITE, int(200*a)))

    # Cost breakdown banner (bottom)
    band_h = 240
    band_y = H - band_h
    overlay_b = Image.new("RGBA", (W, band_h), (*DEEP_NAVY, int(215*a)))
    img.paste(Image.fromarray(np.array(overlay_b)[..., :3]), (0, band_y),
              mask=Image.fromarray(np.array(overlay_b)[:,:,3]))
    draw.line([(0, band_y), (W, band_y)], fill=GOLD, width=2)

    draw_centered_shadow(draw, "CAPITAL COST PLAN", band_y+14, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))

    cost_items = [
        ("AED 9.83M", "Canopy Structure"),
        ("AED 5.81M", "Landscape & Planting"),
        ("AED 4.11M", "Falaj & Water"),
        ("AED 3.47M", "Community Facilities"),
        ("AED 3.75M", "Lighting & Services"),
    ]
    col_w_b = W // len(cost_items)
    for i, (val, lab) in enumerate(cost_items):
        ki = ease_in_out(min(max(t*4 - i*0.3, 0), 1)) * a
        x = col_w_b * i + col_w_b//2
        draw.text((x - 80, band_y+64), val, font=FONT_BODY, fill=(*LIGHT_GOLD, int(255*ki)))
        bbox = draw.textbbox((0,0), lab, font=FONT_CAPTION)
        tw = bbox[2]-bbox[0]
        draw.text((x - tw//2, band_y+100), lab, font=FONT_CAPTION, fill=(*OFF_WHITE, int(200*ki)))

    # Total
    total_alpha = ease_in_out(min(max(t*3 - 1.5, 0), 1)) * a
    draw.line([(W//2-200, band_y+138), (W//2+200, band_y+138)], fill=GOLD, width=1)
    draw_centered_shadow(draw, "TOTAL  AED 26.97M  ·  77.1% Budget Utilisation",
                         band_y+150, FONT_BODY, (*LIGHT_GOLD, int(255*total_alpha)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 6 : NIGHT ACTIVATION (51–57 s) ─────────────────────────────────────
def scene_night(f, f_in, dur):
    t = f_in / (dur * FPS)
    fade = ease_in_out(min(t * 2.5, 1.0))
    fade_out = ease_in_out(max(0, (t - 0.82) * 5.9))
    a = fade * (1 - fade_out)

    arr = vignette(IMG_NIGHT.copy(), 0.42)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", (W, 130), (*DEEP_NAVY, int(190*a)))
    img.paste(Image.fromarray(np.array(overlay)[..., :3]), (0,0),
              mask=Image.fromarray(np.array(overlay)[:,:,3]))
    draw_centered_shadow(draw, "NIGHT ACTIVATION  ·  THE LUMINOUS SPINE", 28, FONT_SUBTTL, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, 90, 700)
    draw_centered(draw, "2700K Warm Uplighting  ·  ETFE Diagrid Soffit  ·  24/7 Activation", 100, FONT_CAPTION, (*OFF_WHITE, int(200*a)))

    night_facts = [
        "Concealed warm-white LED uplighting at 2700 K",
        "ETFE diagrid soffit glows as continuous ribbon of light",
        "Al Falaj rill reflects canopy glow at night",
        "Smart dimming: 100% -> 30% across midnight cycle",
        "Energy: 87 kW peak, solar-supplemented",
    ]
    y0 = 160
    for i, fact in enumerate(night_facts):
        ky = ease_in_out(min(max(t*4 - i*0.3, 0), 1)) * a
        y = y0 + i*70
        overlay_s = Image.new("RGBA", (860, 58), (20, 10, 40, int(210*ky)))
        img.paste(Image.fromarray(np.array(overlay_s)[..., :3]), (40, y),
                  mask=Image.fromarray(np.array(overlay_s)[:,:,3]))
        draw.rectangle([(40, y), (900, y+58)], outline=(*GOLD, int(160*ky)), width=1)
        draw.text((60, y+10), f"*  {fact}", font=FONT_BODY, fill=(*OFF_WHITE, int(230*ky)))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ── SCENE 7 : FINAL CALL TO ACTION (57–60 s) ─────────────────────────────────
def scene_finale(f, f_in, dur):
    t = f_in / (dur * FPS)
    fade = ease_in_out(min(t * 2.5, 1.0))
    pulse = 0.5 + 0.5 * math.sin(t * math.pi * 4)
    a = fade

    base = np.zeros((H, W, 3), dtype=np.uint8)
    for y in range(H):
        ratio = y / H
        r = int(lerp(8, 28, ratio))
        g = int(lerp(18, 40, ratio))
        b = int(lerp(42, 80, ratio))
        base[y, :] = [r, g, b]

    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)

    # Rotating star / ornament
    cx, cy = W//2, H//2 - 60
    for ang in range(0, 360, 45):
        rad = math.radians(ang + t * 30)
        r = 80
        x1 = cx + r * math.cos(rad)
        y1 = cy + r * math.sin(rad)
        x2 = cx + (r+20) * math.cos(rad + math.radians(22.5))
        y2 = cy + (r+20) * math.sin(rad + math.radians(22.5))
        draw.line([(x1,y1),(x2,y2)], fill=(*GOLD, int(180*a)), width=2)

    inner = 55
    draw.ellipse([(cx-inner, cy-inner),(cx+inner, cy+inner)], fill=(*DEEP_NAVY, 255), outline=(*GOLD, int(200*a)), width=2)
    draw_centered_shadow(draw, "AL", cy-28, _font(30, bold=True), (*LIGHT_GOLD, int(255*a)))
    draw_centered_shadow(draw, "SAFA", cy+2, _font(22, bold=True), (*GOLD, int(230*a)))

    y0 = H//2 + 30
    draw_centered_shadow(draw, "AL SAFA PARK", y0, FONT_TITLE, (*LIGHT_GOLD, int(255*a)))
    gold_separator(draw, y0+88, 800)
    draw_centered_shadow(draw, "A City-Scale Response to Urban Heat", y0+108, FONT_SUBTTL, (*OFF_WHITE, int(220*a)))
    draw_centered(draw, "Dubai Municipality Design Competition  ·  2025", y0+170, FONT_BODY, (*PALE_CREAM, int(180*a)))

    glow_alpha = int(lerp(100, 220, pulse) * a)
    draw_centered(draw, "SUBMISSION READY", y0+225, _font(28, bold=True), (*GOLD, glow_alpha))

    progress_bar(draw, f / FRAMES)
    watermark(draw)
    return np.array(img)

# ─── SCENE SCHEDULE ───────────────────────────────────────────────────────────
#  (start_sec, end_sec, render_fn)
SCENES = [
    (0,   5,  scene_title),
    (5,   15, scene_climate),
    (15,  24, scene_aerial),
    (24,  33, scene_walkway),
    (33,  42, scene_oasis),
    (42,  51, scene_souk),
    (51,  57, scene_night),
    (57,  60, scene_finale),
]

# ─── CROSSFADE TRANSITION ──────────────────────────────────────────────────────
XFADE_DUR = 0.6  # seconds of crossfade between scenes

def get_frame(frame_idx: int) -> np.ndarray:
    t_sec = frame_idx / FPS

    # Find current and next scene
    cur = None
    nxt = None
    for i, (s, e, fn) in enumerate(SCENES):
        if s <= t_sec < e:
            cur = (i, s, e, fn)
            if i + 1 < len(SCENES):
                nxt = SCENES[i+1]
            break

    if cur is None:
        return np.zeros((H, W, 3), dtype=np.uint8)

    ci, cs, ce, cfn = cur
    scene_dur = ce - cs
    f_in = t_sec - cs

    arr = cfn(frame_idx, f_in, scene_dur)

    # Apply crossfade at end of scene
    if nxt and f_in >= (scene_dur - XFADE_DUR):
        xf_t = (f_in - (scene_dur - XFADE_DUR)) / XFADE_DUR
        xf_t = ease_in_out(min(xf_t, 1.0))
        ns, ne, nfn = nxt
        nf_in = 0.0
        arr2 = nfn(frame_idx, nf_in, ne - ns)
        arr = alpha_blend(arr.astype(float), arr2.astype(float), xf_t)

    return arr

# ─── RENDER VIDEO ─────────────────────────────────────────────────────────────
def render_video(out_path: Path, width: int, height: int):
    writer = imageio.get_writer(
        str(out_path), fps=FPS, format="FFMPEG",
        codec="libx264", quality=9,
        output_params=["-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p"]
    )

    for fi in range(FRAMES):
        frame = get_frame(fi)
        if width != W or height != H:
            frame = np.array(Image.fromarray(frame).resize((width, height), Image.LANCZOS))
        writer.append_data(frame)

        if fi % (FPS * 5) == 0:
            pct = fi / FRAMES * 100
            print(f"  [{pct:5.1f}%] Frame {fi}/{FRAMES}  ({fi/FPS:.1f}s)", flush=True)

    writer.close()
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"  [OK] Saved: {out_path.name}  ({size_mb:.1f} MB)")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("AL SAFA PARK — 60s Concept Animation Generator")
    print(f"{'='*60}")
    print(f"Output directory: {OUT_DIR}")
    print()

    print(">> Rendering 1080p video...")
    render_video(OUT_1080, W, H)

    print()
    print(">> Rendering 4K video (2x upscale from 1080p)...")
    render_video(OUT_4K, W*2, H*2)

    print()
    print("DONE. Both video files ready in UPLOAD_THESE_12_FILES/")
    print(f"   {OUT_1080.name}")
    print(f"   {OUT_4K.name}")
