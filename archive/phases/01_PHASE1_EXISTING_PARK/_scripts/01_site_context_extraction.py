"""
Phase 1 - Existing Park Understanding
Site Context Extraction from Master Plan Location Image

Input : 99_SOURCE_FILES/Ai Park - Master Plan (4).jpg
Output: 01_PHASE1_EXISTING_PARK/outputs/
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
SRC = os.path.join(BASE, "99_SOURCE_FILES", "Ai Park - Master Plan (4).jpg")
OUT = os.path.join(os.path.dirname(__file__), "..", "02_Urban_Context", "outputs")
os.makedirs(OUT, exist_ok=True)

img = Image.open(SRC).convert("RGB")
arr = np.array(img)
h, w, _ = arr.shape
print(f"Image loaded: {w}x{h}px")

# --- Isolate the greenish park footprint drawn on the location map ---
r, g, b = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
green_mask = (g > 100) & (g > r + 15) & (g > b + 5)

green_px = int(green_mask.sum())
total_px = h * w
green_pct = 100 * green_px / total_px

print(f"Green (park footprint) pixels: {green_px} ({green_pct:.2f}% of image)")

# Bounding box of the green footprint -> approximate park extent within the graphic
ys, xs = np.where(green_mask)
if len(xs) > 0:
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
else:
    x_min = x_max = y_min = y_max = 0

# --- Visualization: original + highlighted mask + bounding box ---
fig, axes = plt.subplots(1, 2, figsize=(20, 9))
axes[0].imshow(arr)
axes[0].set_title("Al Safa Park 2 - Location Map (Source)")
axes[0].axis("off")

overlay = arr.copy()
overlay[green_mask] = [255, 0, 0]
axes[1].imshow(overlay)
if len(xs) > 0:
    rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                          fill=False, edgecolor="yellow", linewidth=3)
    axes[1].add_patch(rect)
axes[1].set_title("Detected Park Footprint (highlighted red) + Bounding Box")
axes[1].axis("off")

plt.tight_layout()
fig.savefig(os.path.join(OUT, "site_context_footprint_detection.png"), dpi=150)
print("Saved: site_context_footprint_detection.png")

# --- Write findings to a text summary (proof of analysis) ---
summary_path = os.path.join(OUT, "site_context_summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("PHASE 1 - EXISTING PARK - SITE CONTEXT EXTRACTION\n")
    f.write("=" * 55 + "\n\n")
    f.write(f"Source image: {os.path.basename(SRC)}\n")
    f.write(f"Image resolution: {w} x {h} px\n\n")
    f.write("DETECTED PARK FOOTPRINT (from location map graphic):\n")
    f.write(f"  Green-flagged pixels : {green_px} ({green_pct:.2f}% of image)\n")
    f.write(f"  Bounding box (px)    : x[{x_min}-{x_max}], y[{y_min}-{y_max}]\n\n")
    f.write("CONTEXT LANDMARKS IDENTIFIED FROM MAP (manual read):\n")
    f.write("  - Al Wasl Street (north-west edge)\n")
    f.write("  - Sheikh Zayed Road / E11 (east side, major arterial)\n")
    f.write("  - Al Manara Street (south)\n")
    f.write("  - ONPASSIVE Metro Station (east, walkable distance)\n")
    f.write("  - Umm Suqeim Model School for Basic Education (adjacent, north-east)\n")
    f.write("  - Dubai Physiotherapy & Rehabilitation Center (adjacent, north)\n")
    f.write("  - Aisha Butti Al Mulla Masjid (adjacent, south-east)\n\n")
    f.write("NEIGHBORHOOD CONTEXT:\n")
    f.write("  - Bounded by: Umm Suqeim First (west), Al Safa Second (north-east),\n")
    f.write("    Al Manara (south), Al Qouz Industrial First (east, across SZR)\n\n")
    f.write("SITE FACTS FROM COMPETITION BRIEF (Schedule 1):\n")
    f.write("  - Site area           : 15,000 sqm (neighborhood park)\n")
    f.write("  - Location            : Al Safa 2, Dubai\n")
    f.write("  - Implementation budget: AED 35,000,000\n")
    f.write("  - Classification      : District/Community/Neighborhood park archetype\n")
    f.write("    (per Neighborhood Parks Manual: low pop. density band -> min 4,000 / max 500,000 sqm range,\n")
    f.write("     but this site sits at the smaller end typical of a neighborhood-scale park)\n\n")
    f.write("NOTE ON CAD FILE:\n")
    f.write("  'Al Safa Park 2 Plan (5).dwg' is a binary AutoCAD 2018 (AC1032) file.\n")
    f.write("  Full geometric extraction (exact boundary polygon, layers, existing features)\n")
    f.write("  requires conversion to DXF via ODA File Converter or opening in AutoCAD/BricsCAD.\n")
    f.write("  Pending action logged in 00_MASTER_TRACKER.\n")

print("Saved:", summary_path)
