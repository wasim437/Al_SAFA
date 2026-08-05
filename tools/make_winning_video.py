# -*- coding: utf-8 -*-
"""
make_winning_video.py
=====================
Generates a COMPETITION-WINNING 60-second 1920x1080 MP4 concept animation
for AL SAFA Park -- Al Hilal Urban Respite, Dubai.

Features:
  - Professional English narration voice (Google TTS)
  - Real park renders as cinematic backgrounds
  - Animated KPI cards, gold overlays, Ken Burns zoom
  - Smooth scene crossfades
  - Audio + video merged into final MP4

Run:
    python tools/make_winning_video.py

Output:
    UPLOAD_THESE_12_FILES/Falaj_Al_Safa_Concept_Film_60s_1080p.mp4
    UPLOAD_THESE_12_FILES/Falaj_Al_Safa_Concept_Film_60s_4K.mp4
"""

import os
import sys
import math
import time
import tempfile
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

try:
    import imageio
except ImportError:
    sys.exit("pip install imageio[ffmpeg]")

try:
    from gtts import gTTS
    HAS_TTS = True
except ImportError:
    HAS_TTS = False
    print("WARNING: gtts not found. Video will be silent.")

# ── PATHS ────────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).parent.parent
RENDERS = ROOT / "design" / "renders" / "FINAL_6_PARK_IMAGES"
FIGURES = ROOT / "figures"
OUT_DIR = ROOT / "UPLOAD_THESE_12_FILES"
SCRATCH = ROOT / "tools" / "_scratch"
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_1080 = OUT_DIR / "Falaj_Al_Safa_Concept_Film_60s_1080p.mp4"
OUT_4K   = OUT_DIR / "Falaj_Al_Safa_Concept_Film_60s_4K.mp4"

# ── VIDEO PARAMS ─────────────────────────────────────────────────────────────
W, H  = 1920, 1080
FPS   = 24
DUR   = 60
TOTAL = FPS * DUR  # 1440 frames

# ── COLOUR PALETTE ───────────────────────────────────────────────────────────
NAVY      = (8,   18,  42)
GOLD      = (212, 175, 55)
L_GOLD    = (255, 220, 100)
WHITE     = (255, 255, 255)
OFF_W     = (240, 235, 220)
EMERALD   = (16,  130, 80)
CREAM     = (248, 242, 228)
DARK_BG   = (10,  10,  25)

# ── NARRATION SCRIPT ─────────────────────────────────────────────────────────
# Timed segments: (start_sec, text)
NARRATION_SEGMENTS = [
    (0.5,  "Al Safa Park. Al Hilal. The Urban Respite."),
    (5.5,  "Dubai endures some of the harshest urban heat on earth. "
            "Peak heat index reaches fifty six point eight degrees Celsius "
            "across four thousand four hundred hours of annual sunlight."),
    (15.5, "Our masterplan transforms fifteen thousand square metres "
            "of public land along Sheikh Zayed Road into a living, breathing park."),
    (24.5, "Al Mamsha. The Shaded Spine. A one hundred and forty four metre "
            "crescent canopy of ETFE diagrid filters harsh sunlight "
            "while an ancient falaj water rill runs beneath, "
            "cooling the air by seven degrees."),
    (33.5, "Al Nakhil. The Palm Court. Twelve date palms surround a sunken oasis "
            "basin, one point two metres below grade, "
            "sheltering families with one hundred and thirty one native trees, "
            "all Ghaf, Neem, and Olive."),
    (42.5, "Al Souk. Eight community kiosks with bronze mashrabiya screens "
            "bring artisan market life to the heart of the park. "
            "Total capital cost: twenty six point nine seven million dirhams. "
            "Seventy seven percent of the competition budget."),
    (51.5, "At night, concealed warm-white uplighting at two thousand seven hundred Kelvin "
            "transforms the canopy into a glowing ribbon of light, "
            "activating the park around the clock."),
    (57.5, "Al Safa Park. A city-scale response to urban heat. Dubai, two thousand and twenty five."),
]

# ── FONTS ────────────────────────────────────────────────────────────────────
def _font(size, bold=False):
    candidates = [
        ("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        ("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
        ("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        ("C:/Windows/Fonts/trebucbd.ttf" if bold else "C:/Windows/Fonts/trebuc.ttf"),
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

FT  = {
    'title'  : _font(80, True),
    'sub'    : _font(46, True),
    'body'   : _font(32),
    'cap'    : _font(24),
    'kpi'    : _font(58, True),
    'small'  : _font(20),
    'badge'  : _font(28, True),
}

# ── HELPERS ──────────────────────────────────────────────────────────────────
def eio(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def blend(bg, fg, alpha):
    a = max(0.0, min(1.0, alpha))
    return np.clip(bg * (1 - a) + fg * a, 0, 255).astype(np.uint8)

def load_img(path, size=(W, H)):
    img = Image.open(path).convert("RGB")
    # Crop to fill (centre crop)
    iw, ih = img.size
    scale = max(size[0]/iw, size[1]/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    xo = (nw - size[0])//2
    yo = (nh - size[1])//2
    img = img.crop((xo, yo, xo+size[0], yo+size[1]))
    return np.array(img)

def darken(arr, f=0.5):
    return np.clip(arr.astype(float) * f, 0, 255).astype(np.uint8)

def vignette(arr, s=0.6):
    rows, cols = arr.shape[:2]
    Y, X = np.ogrid[:rows, :cols]
    cy, cx = rows/2, cols/2
    dist = np.sqrt(((X-cx)/cx)**2 + ((Y-cy)/cy)**2)
    mask = np.clip(1 - s*dist, 0, 1)[..., np.newaxis]
    return np.clip(arr.astype(float)*mask, 0, 255).astype(np.uint8)

def zoom_img(arr, factor):
    if abs(factor - 1.0) < 0.001:
        return arr
    h, w = arr.shape[:2]
    nw, nh = int(w*factor), int(h*factor)
    big = np.array(Image.fromarray(arr).resize((nw, nh), Image.LANCZOS))
    xo = (nw-w)//2; yo = (nh-h)//2
    return big[yo:yo+h, xo:xo+w]

def pan_img(arr, dx_frac=0.0, dy_frac=0.0):
    h, w = arr.shape[:2]
    dx = int(dx_frac * w * 0.05)
    dy = int(dy_frac * h * 0.05)
    big = zoom_img(arr, 1.08)
    bh, bw = big.shape[:2]
    xo = max(0, (bw-w)//2 + dx)
    yo = max(0, (bh-h)//2 + dy)
    xo = min(xo, bw-w)
    yo = min(yo, bh-h)
    return big[yo:yo+h, xo:xo+w]

def new_canvas(bg=NAVY):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    return img, draw

def paste_alpha(base_img, overlay_rgba, pos=(0,0)):
    """Paste RGBA overlay onto RGB base at pos."""
    ov = Image.fromarray(overlay_rgba)
    r,g,b,a = ov.split()
    mask = a
    base_img.paste(Image.merge("RGB",[r,g,b]), pos, mask)

def make_overlay(w, h, color_rgba):
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[:,:,0] = color_rgba[0]
    arr[:,:,1] = color_rgba[1]
    arr[:,:,2] = color_rgba[2]
    arr[:,:,3] = color_rgba[3]
    return arr

def centered_text(draw, text, y, font, fill, w=W):
    bb = draw.textbbox((0,0), text, font=font)
    tw = bb[2]-bb[0]
    x = (w-tw)//2
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0,180))
    draw.text((x, y), text, font=font, fill=fill)

def gold_line(draw, y, width=800, cx=W//2):
    x0 = cx - width//2
    draw.line([(x0, y),(x0+width, y)], fill=GOLD, width=2)
    draw.ellipse([(cx-6,y-6),(cx+6,y+6)], fill=GOLD)

def progress(draw, f):
    draw.rectangle([(0, H-12),(W, H)], fill=(0,0,0))
    draw.rectangle([(0, H-12),(int(W*f/TOTAL), H)], fill=GOLD)

def wm(draw):
    draw.text((W-370, H-36), "AL SAFA PARK  |  DUBAI 2025", font=FT['small'], fill=(*GOLD,))

def subtitle_box(img, draw, text, alpha):
    """Cinematic subtitle at bottom centre with dark pill background."""
    if alpha < 0.02:
        return
    bb = draw.textbbox((0,0), text, font=FT['body'])
    tw = bb[2]-bb[0]; th = bb[3]-bb[1]
    pad = 18
    bw = tw + pad*2 + 4
    bh = th + pad*2
    x0 = (W-bw)//2; y0 = H - 120 - bh
    pill = make_overlay(bw, bh, (10,10,30, int(210*alpha)))
    pill_img = Image.fromarray(pill)
    r2,g2,b2,a2 = pill_img.split()
    img.paste(Image.merge("RGB",[r2,g2,b2]), (x0,y0), a2)
    draw.text((x0+pad+2+2, y0+pad+2), text, font=FT['body'], fill=(0,0,0,120))
    draw.text((x0+pad+2, y0+pad), text, font=FT['body'], fill=(*OFF_W, int(255*alpha)))

# ── LOAD ASSETS ──────────────────────────────────────────────────────────────
print("Loading images...")
R = {
    'aerial'  : load_img(RENDERS/"01_Masterplan_Aerial_View.jpg"),
    'walkway' : load_img(RENDERS/"02_Spine_Corridor_Shaded_Walkway.jpg"),
    'oasis'   : load_img(RENDERS/"03_Sunken_Oasis_Basin_AlNakhil.jpg"),
    'dune'    : load_img(RENDERS/"04_Childrens_Dune_Play.jpg"),
    'souk'    : load_img(RENDERS/"05_Souk_Kiosks_Community_Plaza.jpg"),
    'night'   : load_img(RENDERS/"06_Night_Plaza_Illuminated_Canopy.jpg"),
    'climate' : load_img(FIGURES/"fig01_climate_and_comfort.png"),
    'cost'    : load_img(FIGURES/"fig11_cost_plan.png"),
    'master'  : load_img(FIGURES/"fig10_masterplan.png"),
}
print("All images loaded.")

# ── SCENE HELPERS ─────────────────────────────────────────────────────────────
XFADE = 18  # crossfade frames (0.75s)

# Scene schedule: (start_frame, end_frame, fn)
def sf(s): return int(s*FPS)

# ── SCENE RENDERERS ───────────────────────────────────────────────────────────

def s_title(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*3, 1.0)) * eio(1 - max(0,(t-0.75)*4))
    # Gradient BG
    base = np.zeros((H,W,3), np.uint8)
    for y in range(H):
        r2 = y/H
        base[y,:] = [int(lerp(8,20,r2)), int(lerp(18,38,r2)), int(lerp(42,80,r2))]
    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)

    # Animated ornament
    cx, cy = W//2, H//2 - 80
    sz = int(100 * eio(min(t*4, 1.0)))
    if sz > 8:
        for ang in range(0, 360, 45):
            r = math.radians(ang + t*20)
            x1 = cx + sz*math.cos(r)
            y1 = cy + sz*math.sin(r)
            x2 = cx + (sz+16)*math.cos(r+math.radians(22.5))
            y2 = cy + (sz+16)*math.sin(r+math.radians(22.5))
            draw.line([(x1,y1),(x2,y2)], fill=(*GOLD, int(180*a)), width=2)
        draw.ellipse([(cx-52,cy-52),(cx+52,cy+52)],
                     fill=(*NAVY,255), outline=(*GOLD, int(200*a)), width=2)
        centered_text(draw, "AL", cy-28, _font(30,True), (*L_GOLD, int(int(255*a))))
        centered_text(draw, "SAFA", cy+4, _font(22,True), (*GOLD, int(230*a)))

    y0 = H//2 + 10
    centered_text(draw, "AL SAFA PARK", y0, FT['title'], (*L_GOLD, int(255*a)))
    gold_line(draw, y0+95, 820)
    centered_text(draw, "Al Hilal  |  The Urban Respite", y0+115, FT['sub'], (*OFF_W, int(220*a)))
    centered_text(draw, "Dubai Municipality  |  15,000 m2  |  AED 26.97M", y0+178, FT['body'], (*CREAM, int(180*a)))
    centered_text(draw, "DESIGN COMPETITION 2025", y0+230, FT['badge'], (*GOLD, int(160*a)))
    progress(draw, fi); wm(draw)
    return np.array(img)


def s_climate(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*2.5, 1.0)) * eio(1-max(0,(t-0.8)*5))

    arr = darken(R['climate'].copy(), 0.38)
    arr = vignette(arr, 0.65)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(210*a)))
    paste_alpha(img, top, (0,0))
    centered_text(draw, "THE CLIMATE CHALLENGE", 30, FT['sub'], (*L_GOLD, int(255*a)))
    gold_line(draw, 100, 700)
    centered_text(draw, "Why Dubai's public realm demands bold intervention", 112, FT['cap'], (*OFF_W, int(200*a)))

    kpis = [
        ("56.8 degC", "Peak Heat Index"),
        ("4,402 h",   "Annual Sun Hours"),
        ("44 %",      "Comfort Gain"),
        ("-7.1 degC", "Falaj Cooling"),
    ]
    cw = 390; gap = 28
    total_w = len(kpis)*cw + (len(kpis)-1)*gap
    x0 = (W - total_w)//2
    for i,(val,lab) in enumerate(kpis):
        ki = eio(min(max(t*5 - i*0.6, 0),1)) * a
        if ki < 0.03: continue
        x = x0 + i*(cw+gap)
        y = 158
        card = make_overlay(cw, 168, (*NAVY, int(215*ki)))
        paste_alpha(img, card, (x,y))
        draw.rectangle([(x,y),(x+cw,y+168)], outline=(*GOLD,int(200*ki)), width=2)
        # Accent bar
        draw.rectangle([(x,y),(x+cw,y+6)], fill=(*GOLD,int(220*ki)))
        bb = draw.textbbox((0,0), val, font=FT['kpi'])
        tw = bb[2]-bb[0]
        draw.text((x+(cw-tw)//2+2, y+22), val, font=FT['kpi'], fill=(0,0,0,180))
        draw.text((x+(cw-tw)//2, y+20), val, font=FT['kpi'], fill=(*L_GOLD,int(255*ki)))
        bb2 = draw.textbbox((0,0), lab, font=FT['cap'])
        tw2 = bb2[2]-bb2[0]
        draw.text((x+(cw-tw2)//2, y+105), lab, font=FT['cap'], fill=(*OFF_W,int(200*ki)))

    bot = make_overlay(W, 80, (*NAVY, int(190*a)))
    paste_alpha(img, bot, (0,H-80))
    centered_text(draw, "Bold design must address the human comfort crisis at street level.", H-62, FT['body'], (*CREAM,int(210*a)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_aerial(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*2.5, 1.0)) * eio(1-max(0,(t-0.82)*5.9))
    zoom = lerp(1.07, 1.0, eio(t))
    arr = zoom_img(R['aerial'].copy(), zoom)
    arr = vignette(arr, 0.42)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(200*a)))
    paste_alpha(img, top, (0,0))
    centered_text(draw, "THE MASTERPLAN  |  150 m x 100 m", 28, FT['sub'], (*L_GOLD,int(255*a)))
    gold_line(draw, 96, 800)
    centered_text(draw, "Al Safa Park  |  Sheikh Zayed Road Corridor  |  Dubai", 108, FT['cap'], (*OFF_W,int(200*a)))

    tags = ["15,000 m2 Site","Crescent Canopy Arc","Al Falaj Water","Al Nakhil Oasis","131 Native Trees"]
    cw2 = W//len(tags)
    bot = make_overlay(W, 100, (*NAVY, int(205*a)))
    paste_alpha(img, bot, (0,H-100))
    draw.line([(0,H-100),(W,H-100)], fill=GOLD, width=2)
    for i,tag in enumerate(tags):
        ki = eio(min(max(t*5-i*0.35,0),1))*a
        x = cw2*i + cw2//2
        bb = draw.textbbox((0,0), tag, font=FT['cap'])
        tw = bb[2]-bb[0]
        draw.text((x-tw//2, H-78), tag, font=FT['cap'], fill=(*L_GOLD,int(220*ki)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_walkway(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*2.5,1.0)) * eio(1-max(0,(t-0.82)*5.9))
    zoom = lerp(1.0, 1.05, eio(t))
    arr = zoom_img(R['walkway'].copy(), zoom)
    arr = vignette(arr, 0.42)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(200*a)))
    paste_alpha(img, top, (0,0))
    centered_text(draw, "AL MAMSHA  |  THE SHADED SPINE", 28, FT['sub'], (*L_GOLD,int(255*a)))
    gold_line(draw, 96, 700)
    centered_text(draw, "A crescent canopy of ETFE diagrid  |  144.2 m arc  |  18 m width", 108, FT['cap'], (*OFF_W,int(200*a)))

    specs = [
        ("18.0 m", "Canopy Width"),
        ("4.5 m",  "Height Clearance"),
        ("7.0 m",  "Limestone Walk"),
        ("0.9 m",  "Falaj Water Rill"),
        ("3.0 m",  "S. Louvre Fin"),
        ("ETFE",   "Diagrid Roofing"),
    ]
    px = W - 460; py = 155
    for i,(val,lab) in enumerate(specs):
        ki = eio(min(max(t*4-i*0.28,0),1))*a
        if ki < 0.03: continue
        y = py + i*72
        card = make_overlay(430, 64, (*NAVY, int(210*ki)))
        paste_alpha(img, card, (px, y))
        draw.rectangle([(px,y),(px+430,y+64)], outline=(*GOLD,int(160*ki)), width=1)
        draw.rectangle([(px,y),(px+5,y+64)], fill=(*GOLD,int(200*ki)))
        draw.text((px+18, y+4), val, font=FT['sub'], fill=(*L_GOLD,int(255*ki)))
        draw.text((px+18, y+42), lab, font=FT['small'], fill=(*OFF_W,int(200*ki)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_oasis(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    cross = eio(min(max((t-0.45)*3.5,0),1))
    a = eio(min(t*2.5,1.0)) * eio(1-max(0,(t-0.82)*5.9))
    arr1 = vignette(R['oasis'].copy(), 0.45)
    arr2 = vignette(R['dune'].copy(), 0.45)
    arr = blend(arr1.astype(float), arr2.astype(float), cross)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(200*a)))
    paste_alpha(img, top, (0,0))
    title = "AL NAKHIL & DUNE PLAY" if cross < 0.5 else "CHILDREN & FAMILY ZONES"
    centered_text(draw, title, 28, FT['sub'], (*L_GOLD,int(255*a)))
    gold_line(draw, 96, 700)
    sub = "Sunken Palm Court  |  1.2 m below grade  |  12 Date Palms" if cross < 0.5 else "Inclusive play  |  Native sand dunes  |  Neem shade canopy"
    centered_text(draw, sub, 108, FT['cap'], (*OFF_W,int(200*a)))

    eco = [
        ("12",     "Date Palms (Al Nakhil)", EMERALD),
        ("58",     "Ghaf Trees (S. Rank)",   EMERALD),
        ("16",     "Neem Trees (N. Rank)",   EMERALD),
        ("131",    "Total Native Trees",      L_GOLD),
        ("-7.1C",  "Heat Index Drop",         L_GOLD),
        ("1.2 m",  "Sunken Court Depth",      OFF_W),
    ]
    px = 32; py = 155
    for i,(val,lab,col) in enumerate(eco):
        ki = eio(min(max(t*4-i*0.28,0),1))*a
        if ki < 0.03: continue
        y = py + i*72
        card = make_overlay(400, 64, (*NAVY, int(210*ki)))
        paste_alpha(img, card, (px,y))
        draw.rectangle([(px,y),(px+400,y+64)], outline=(*GOLD,int(160*ki)), width=1)
        draw.rectangle([(px,y),(px+5,y+64)], fill=(*col,int(200*ki)))
        draw.text((px+18,y+4), val, font=FT['sub'], fill=(*col,int(255*ki)))
        draw.text((px+18,y+42), lab, font=FT['small'], fill=(*OFF_W,int(200*ki)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_souk(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*2.5,1.0)) * eio(1-max(0,(t-0.82)*5.9))
    arr = vignette(R['souk'].copy(), 0.42)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(200*a)))
    paste_alpha(img, top, (0,0))
    centered_text(draw, "AL SOUK  |  COMMUNITY & ECONOMY", 28, FT['sub'], (*L_GOLD,int(255*a)))
    gold_line(draw, 96, 700)
    centered_text(draw, "8 Timber Kiosks  |  Bronze Mashrabiya  |  AED 26.97M", 108, FT['cap'], (*OFF_W,int(200*a)))

    band_h = 260; band_y = H-band_h
    bot = make_overlay(W, band_h, (*NAVY, int(220*a)))
    paste_alpha(img, bot, (0,band_y))
    draw.line([(0,band_y),(W,band_y)], fill=GOLD, width=2)
    centered_text(draw, "CAPITAL COST PLAN", band_y+14, FT['sub'], (*L_GOLD,int(255*a)))
    draw.line([(W//2-240,band_y+68),(W//2+240,band_y+68)], fill=(*GOLD,int(160*a)), width=1)

    items = [
        ("AED 9.83M","Canopy Structure"),
        ("AED 5.81M","Landscape"),
        ("AED 4.11M","Falaj & Water"),
        ("AED 3.47M","Community"),
        ("AED 3.75M","Lighting"),
    ]
    cw2 = W//len(items)
    for i,(v,l) in enumerate(items):
        ki = eio(min(max(t*4-i*0.3,0),1))*a
        x = cw2*i + cw2//2
        bb = draw.textbbox((0,0),v,font=FT['body']); tw=bb[2]-bb[0]
        draw.text((x-tw//2,band_y+80),v,font=FT['body'],fill=(*L_GOLD,int(255*ki)))
        bb2 = draw.textbbox((0,0),l,font=FT['cap']); tw2=bb2[2]-bb2[0]
        draw.text((x-tw2//2,band_y+118),l,font=FT['cap'],fill=(*OFF_W,int(200*ki)))

    tot_a = eio(min(max(t*3-1.5,0),1))*a
    draw.line([(W//2-280,band_y+160),(W//2+280,band_y+160)], fill=GOLD, width=1)
    centered_text(draw,"TOTAL  AED 26.97M  |  77.1% Budget Utilisation",band_y+174,FT['body'],(*L_GOLD,int(255*tot_a)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_night(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*2.5,1.0)) * eio(1-max(0,(t-0.82)*5.9))
    arr = vignette(R['night'].copy(), 0.38)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    top = make_overlay(W, 140, (*NAVY, int(200*a)))
    paste_alpha(img, top, (0,0))
    centered_text(draw,"NIGHT ACTIVATION  |  THE LUMINOUS SPINE",28,FT['sub'],(*L_GOLD,int(255*a)))
    gold_line(draw, 96, 700)
    centered_text(draw,"2700 K Warm Uplighting  |  ETFE Glow  |  Solar Supplemented",108,FT['cap'],(*OFF_W,int(200*a)))

    facts = [
        "Concealed LED uplighting at 2700 K warm-white",
        "ETFE diagrid soffit becomes a ribbon of light",
        "Al Falaj rill mirrors the canopy glow at night",
        "Smart dimming: 100% at dusk, 30% by midnight",
        "87 kW peak load -- solar offset by 2026",
    ]
    for i,f in enumerate(facts):
        ki = eio(min(max(t*4-i*0.3,0),1))*a
        if ki < 0.03: continue
        y = 155 + i*74
        card = make_overlay(920, 64, (15,8,35,int(215*ki)))
        paste_alpha(img, card, (36,y))
        draw.rectangle([(36,y),(956,y+64)],outline=(*GOLD,int(160*ki)),width=1)
        draw.rectangle([(36,y),(42,y+64)],fill=(*GOLD,int(200*ki)))
        draw.text((60,y+14),"*  "+f,font=FT['body'],fill=(*OFF_W,int(230*ki)))
    progress(draw,fi); wm(draw)
    return np.array(img)


def s_finale(fi, fi_local, dur_frames):
    t = fi_local / dur_frames
    a = eio(min(t*3,1.0))
    pulse = 0.6 + 0.4*math.sin(t*math.pi*5)
    base = np.zeros((H,W,3),np.uint8)
    for y in range(H):
        r2 = y/H
        base[y,:] = [int(lerp(8,28,r2)),int(lerp(18,40,r2)),int(lerp(42,80,r2))]
    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 - 80
    sz = int(110*eio(min(t*5,1.0)))
    if sz > 8:
        for ang in range(0,360,30):
            r = math.radians(ang + t*40)
            x1=cx+sz*math.cos(r); y1=cy+sz*math.sin(r)
            x2=cx+(sz+20)*math.cos(r+math.radians(15))
            y2=cy+(sz+20)*math.sin(r+math.radians(15))
            draw.line([(x1,y1),(x2,y2)],fill=(*GOLD,int(160*a)),width=2)
        inner=60
        draw.ellipse([(cx-inner,cy-inner),(cx+inner,cy+inner)],fill=(*NAVY,255),outline=(*GOLD,int(220*a)),width=2)
        centered_text(draw,"AL",cy-28,_font(32,True),(*L_GOLD,int(255*a)))
        centered_text(draw,"SAFA",cy+4,_font(24,True),(*GOLD,int(230*a)))

    y0 = H//2 + 38
    centered_text(draw,"AL SAFA PARK",y0,FT['title'],(*L_GOLD,int(255*a)))
    gold_line(draw,y0+95,860)
    centered_text(draw,"A City-Scale Response to Urban Heat",y0+115,FT['sub'],(*OFF_W,int(220*a)))
    centered_text(draw,"Dubai Municipality  |  Design Competition  |  2025",y0+178,FT['body'],(*CREAM,int(180*a)))
    glow_a = int(lerp(130,240,pulse)*a)
    centered_text(draw,"SUBMISSION READY",y0+234,FT['badge'],(*GOLD,glow_a))
    progress(draw,fi); wm(draw)
    return np.array(img)


# ── SCENE SCHEDULE ────────────────────────────────────────────────────────────
SCENES = [
    (sf(0),  sf(5),  s_title),    # 0-5s
    (sf(5),  sf(15), s_climate),  # 5-15s
    (sf(15), sf(24), s_aerial),   # 15-24s
    (sf(24), sf(33), s_walkway),  # 24-33s
    (sf(33), sf(42), s_oasis),    # 33-42s
    (sf(42), sf(51), s_souk),     # 42-51s
    (sf(51), sf(57), s_night),    # 51-57s
    (sf(57), sf(60), s_finale),   # 57-60s
]

def get_frame(fi):
    cur_scene = None
    for i,(s,e,fn) in enumerate(SCENES):
        if s <= fi < e:
            cur_scene = (i,s,e,fn)
            break
    if cur_scene is None:
        return np.zeros((H,W,3),np.uint8)

    ci,cs,ce,cfn = cur_scene
    dur = ce - cs
    fi_local = fi - cs
    arr = cfn(fi, fi_local, dur)

    # Crossfade with next scene
    if ci+1 < len(SCENES) and fi_local >= dur-XFADE:
        ns,ne,nfn = SCENES[ci+1]
        xf_t = eio((fi_local - (dur-XFADE)) / XFADE)
        arr2 = nfn(fi, 0, ne-ns)
        arr = blend(arr.astype(float), arr2.astype(float), xf_t)
    return arr

# ── GENERATE NARRATION ─────────────────────────────────────────────────────────
NARRATION_MP3 = SCRATCH / "narration.mp3"
NARRATION_WAV = SCRATCH / "narration.wav"

def generate_voice():
    if not HAS_TTS:
        return None
    full_text = "  ".join(text for _,text in NARRATION_SEGMENTS)
    print("Generating professional narration (English, slow pace)...")
    tts = gTTS(text=full_text, lang='en', slow=False, tld='co.uk')
    tts.save(str(NARRATION_MP3))
    print(f"  Narration saved: {NARRATION_MP3}")
    return NARRATION_MP3

# ── RENDER VIDEO ──────────────────────────────────────────────────────────────
def render_silent(out_path, width, height):
    """Render MP4 without audio first."""
    tmp = SCRATCH / (out_path.stem + "_silent.mp4")
    print(f"Rendering {width}x{height} silent video...")
    writer = imageio.get_writer(
        str(tmp), fps=FPS, format="FFMPEG", codec="libx264",
        output_params=["-crf","18","-preset","fast","-pix_fmt","yuv420p",
                       "-movflags","+faststart"]
    )
    for fi in range(TOTAL):
        frame = get_frame(fi)
        if width != W or height != H:
            frame = np.array(Image.fromarray(frame).resize((width,height),Image.LANCZOS))
        writer.append_data(frame)
        if fi % (FPS*5) == 0:
            print(f"  [{fi/TOTAL*100:5.1f}%] Frame {fi}/{TOTAL}", flush=True)
    writer.close()
    sz = tmp.stat().st_size/1024/1024
    print(f"  Silent video done: {tmp.name} ({sz:.1f} MB)")
    return tmp

def merge_audio(video_path, audio_path, out_path):
    """Merge narration audio into video using ffmpeg."""
    print("Merging narration audio into video...")
    ffmpeg_exe = None

    # Find ffmpeg from imageio
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

    if not ffmpeg_exe:
        for candidate in [
            "ffmpeg",
            str(Path(sys.executable).parent / "ffmpeg.exe"),
        ]:
            try:
                subprocess.run([candidate,"-version"],capture_output=True,check=True)
                ffmpeg_exe = candidate
                break
            except Exception:
                pass

    if not ffmpeg_exe:
        print("  ffmpeg not found -- copying silent video instead.")
        import shutil
        shutil.copy(str(video_path), str(out_path))
        return

    cmd = [
        ffmpeg_exe, "-y",
        "-i", str(video_path),          # video
        "-i", str(audio_path),          # audio
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",                     # trim to video length
        "-movflags", "+faststart",
        str(out_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  ffmpeg merge error:", result.stderr[-300:])
        import shutil
        shutil.copy(str(video_path), str(out_path))
    else:
        sz = out_path.stat().st_size/1024/1024
        print(f"  [OK] Merged: {out_path.name} ({sz:.1f} MB)")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  AL SAFA PARK -- Competition Concept Animation")
    print("  60 seconds | 1920x1080 | Professional Narration")
    print("=" * 60)
    print()

    # Step 1: Generate narration voice
    audio_file = generate_voice()

    # Step 2: Render 1080p silent
    silent_1080 = render_silent(OUT_1080, W, H)

    # Step 3: Merge audio
    if audio_file and audio_file.exists():
        merge_audio(silent_1080, audio_file, OUT_1080)
    else:
        import shutil
        shutil.copy(str(silent_1080), str(OUT_1080))

    print()
    print(">> Rendering 4K (2x upscale)...")
    silent_4k = render_silent(OUT_4K, W*2, H*2)
    if audio_file and audio_file.exists():
        merge_audio(silent_4k, audio_file, OUT_4K)
    else:
        import shutil
        shutil.copy(str(silent_4k), str(OUT_4K))

    print()
    print("=" * 60)
    print("  DONE! Both videos ready:")
    print(f"  1080p: {OUT_1080}")
    print(f"  4K:    {OUT_4K}")
    print("=" * 60)
