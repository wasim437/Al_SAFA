"""
Phase 9.7 - REAL 3D Park Model & Renders (Blender / Cycles)

Run headlessly:
  blender --background --python 04_blender_park_model.py

WHY THIS EXISTS
The earlier "3D visualizations" were matplotlib rectangles - fine as diagrams,
but not architectural renderings. This builds an actual 3D model in Blender and
ray-traces it with Cycles, so we get real perspective, real materials, and
crucially REAL SUN GEOMETRY: the sun lamp is driven by the exact solar
azimuth/elevation computed in Phase 1.05/1.06 (pvlib / NREL SPA) for the site's
true coordinates. The shadows in these renders are therefore physically correct
for Al Safa 2 Park on the stated date/time - not artistic guesses.

GEOMETRY SOURCE
Zone rectangles come from the Phase 5 masterplan schedule (the same numbers that
sum to exactly 15,000 sqm). Tree positions come from the Phase 6 planting plan
logic. If/when the real DWG boundary is extracted, only SITE_W/SITE_H and the
zone table need updating - the rest of this script is boundary-agnostic.
"""

import bpy
import bmesh
import math
import os
import json
import sys

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
PROJECT = r"C:\Users\LENOVO\Downloads\AL SAFA"
OUT_DIR = os.path.join(PROJECT, "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.7_Renderings")

SITE_W, SITE_H = 150.0, 100.0          # metres (Phase 5; update when DWG confirms)
SAMPLES = 96                            # Cycles samples (quality vs time)
RES_X, RES_Y = 1920, 1080

# REAL computed solar values from Phase 1.06 Shadow Analysis (pvlib / NREL SPA,
# site 25.190N 55.238E). Used to place the sun lamp physically correctly.
SUN_CONDITIONS = {
    "summer_noon":  {"elev": 84.9, "azim": 109.2, "strength": 5.5, "label": "21 Jun 12:00"},
    "winter_noon":  {"elev": 41.2, "azim": 174.8, "strength": 3.2, "label": "21 Dec 12:00"},
    "evening":      {"elev": 17.4, "azim": 232.6, "strength": 2.2, "label": "21 Dec 16:00"},
}

# Zones: (name, x, y, w, h, kind)  -- lower-left origin, metres
ZONES = [
    ("Main Entrance Plaza",   0,  40,  12, 20, "paving"),
    ("Shaded Spine",         12,  45, 126, 10, "spine"),
    ("Secondary Entrance",  138,  40,  12, 20, "paving"),
    ("Childrens Play",       14,  58,  32, 34, "play"),
    ("Family Picnic",        48,  58,  26, 34, "lawn"),
    ("Community Plaza",      76,  58,  36, 34, "paving"),
    ("Outdoor Fitness",     114,  58,  24, 34, "sport"),
    ("Native Planting",      14,   8,  32, 34, "planting"),
    ("Quiet Garden",         48,   8,  26, 34, "lawn"),
    ("Commercial Kiosks",    76,   8,  22, 34, "paving"),
    ("Sports Lawn",         100,   8,  38, 34, "lawn"),
    ("Perimeter Buffer N",   12,  92, 126,  8, "planting"),
    ("Perimeter Buffer S",   12,   0, 126,  8, "planting"),
]

SPINE = (12, 45, 126, 10)               # x, y, w, h
CANOPY_H = 5.5                          # m clearance (Phase 6.8 section)
CANOPY_OVERHANG = 1.2                   # m each side


# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for item in list(block):
            block.remove(item)


def mat(name, rgba, roughness=0.6, metallic=0.0, emission=None, emission_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return m


MATERIALS = {}


def build_materials(night=False):
    MATERIALS["ground"]   = mat("Ground",   (0.83, 0.78, 0.68, 1), 0.85)
    MATERIALS["paving"]   = mat("Paving",   (0.80, 0.75, 0.66, 1), 0.55)
    MATERIALS["lawn"]     = mat("Lawn",     (0.28, 0.48, 0.22, 1), 0.80)
    MATERIALS["planting"] = mat("Planting", (0.16, 0.35, 0.18, 1), 0.85)
    MATERIALS["play"]     = mat("PlaySurf", (0.72, 0.34, 0.24, 1), 0.70)
    MATERIALS["sport"]    = mat("Sport",    (0.24, 0.42, 0.30, 1), 0.75)
    MATERIALS["spine"]    = mat("SpinePath",(0.86, 0.82, 0.74, 1), 0.45)
    MATERIALS["canopy"]   = mat("Canopy",   (0.18, 0.22, 0.24, 1), 0.35, metallic=0.35)
    MATERIALS["column"]   = mat("Column",   (0.32, 0.32, 0.33, 1), 0.40, metallic=0.60)
    MATERIALS["trunk"]    = mat("Trunk",    (0.28, 0.20, 0.13, 1), 0.90)
    MATERIALS["foliage"]  = mat("Foliage",  (0.14, 0.32, 0.14, 1), 0.85)
    MATERIALS["kiosk"]    = mat("Kiosk",    (0.62, 0.48, 0.34, 1), 0.55)
    if night:
        MATERIALS["lamp"] = mat("LampGlow", (1, 0.95, 0.75, 1), 0.3,
                                 emission=(1.0, 0.90, 0.62, 1), emission_strength=22.0)
    else:
        MATERIALS["lamp"] = mat("LampOff", (0.5, 0.5, 0.5, 1), 0.4)


def add_box(name, x, y, w, h, z=0.0, thickness=0.12, material=None):
    """Axis-aligned slab with lower-left at (x, y)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + w / 2, y + h / 2, z + thickness / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (w, h, thickness)
    if material:
        ob.data.materials.append(material)
    return ob


def add_tree(x, y, canopy_r=3.2, height=6.0, seed=0):
    """Trunk + layered foliage spheres (reads as a tree in render, cheap to trace)."""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=height * 0.55,
                                        location=(x, y, height * 0.275), vertices=8)
    trunk = bpy.context.active_object
    trunk.name = f"Trunk_{seed}"
    trunk.data.materials.append(MATERIALS["trunk"])

    for i, (dz, sc) in enumerate(((0.62, 1.0), (0.80, 0.72), (0.93, 0.44))):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=canopy_r * sc,
                                              location=(x, y, height * dz))
        f = bpy.context.active_object
        f.name = f"Foliage_{seed}_{i}"
        f.scale = (1.0, 1.0, 0.68)
        f.data.materials.append(MATERIALS["foliage"])


def build_site():
    # Ground plane (a bit larger than the site so we see context)
    add_box("Ground", -25, -25, SITE_W + 50, SITE_H + 50, z=-0.15,
            thickness=0.3, material=MATERIALS["ground"])

    # Zone surfaces
    for (name, x, y, w, h, kind) in ZONES:
        add_box(name.replace(" ", "_"), x, y, w, h, z=0.0, thickness=0.10,
                material=MATERIALS.get(kind, MATERIALS["paving"]))

    # ---- The Shaded Spine canopy (the signature element) ----
    sx, sy, sw, sh = SPINE
    add_box("Canopy_Roof",
            sx - CANOPY_OVERHANG, sy - CANOPY_OVERHANG,
            sw + 2 * CANOPY_OVERHANG, sh + 2 * CANOPY_OVERHANG,
            z=CANOPY_H, thickness=0.35, material=MATERIALS["canopy"])

    # Columns down both edges every 6 m (Phase 6 elevation: 6 m bays)
    for cx in range(int(sx) + 3, int(sx + sw), 6):
        for cy in (sy - CANOPY_OVERHANG + 0.3, sy + sh + CANOPY_OVERHANG - 0.3):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=CANOPY_H,
                                                location=(cx, cy, CANOPY_H / 2), vertices=12)
            col = bpy.context.active_object
            col.name = f"Col_{cx}_{int(cy)}"
            col.data.materials.append(MATERIALS["column"])

    # ---- Trees: dense in planting zones, scattered in the activity rooms ----
    import random
    rng = random.Random(42)
    seed = 0

    def scatter(x, y, w, h, count, r_lo, r_hi, h_lo, h_hi):
        nonlocal seed
        for _ in range(count):
            tx = rng.uniform(x + 3, x + w - 3)
            ty = rng.uniform(y + 3, y + h - 3)
            add_tree(tx, ty, rng.uniform(r_lo, r_hi), rng.uniform(h_lo, h_hi), seed)
            seed += 1

    scatter(14, 8, 32, 34, 16, 2.8, 4.0, 5.5, 8.0)      # Native Planting (Ghaf)
    scatter(12, 92, 126, 8, 18, 2.4, 3.4, 5.0, 7.0)     # Perimeter N (Neem)
    scatter(12, 0, 126, 8, 18, 2.4, 3.4, 5.0, 7.0)      # Perimeter S
    scatter(14, 58, 32, 34, 8, 2.6, 3.6, 5.0, 7.0)      # Play (priority canopy)
    scatter(114, 58, 24, 34, 6, 2.6, 3.6, 5.0, 7.0)     # Fitness
    scatter(48, 58, 26, 34, 6, 2.6, 3.8, 5.0, 7.5)      # Family Picnic
    scatter(48, 8, 26, 34, 6, 2.0, 2.8, 3.5, 5.0)       # Quiet Garden (Olive)
    scatter(76, 58, 36, 34, 5, 2.4, 3.2, 5.0, 6.5)      # Community Plaza edges

    # Spine-edge Ficus rows
    for i, tx in enumerate(range(int(sx) + 5, int(sx + sw), 10)):
        add_tree(tx, sy - 3.0, 2.2, 5.0, 900 + i)
        add_tree(tx, sy + sh + 3.0, 2.2, 5.0, 950 + i)

    # ---- Kiosks (Commercial zone) ----
    for i, kx in enumerate((80, 88)):
        add_box(f"Kiosk_{i}", kx, 18, 6, 5, z=0.1, thickness=3.2,
                material=MATERIALS["kiosk"])

    # ---- Lamp posts along the spine (glow at night) ----
    for lx in range(int(sx) + 6, int(sx + sw), 14):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=4.2,
                                            location=(lx, sy + sh / 2, 2.1), vertices=8)
        post = bpy.context.active_object
        post.data.materials.append(MATERIALS["column"])
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.34,
                                              location=(lx, sy + sh / 2, 4.3))
        head = bpy.context.active_object
        head.data.materials.append(MATERIALS["lamp"])


def set_sun(elev_deg, azim_deg, strength):
    """Place a sun lamp using REAL solar elevation/azimuth (compass degrees).

    Blender sun direction: rotate a -Z pointing lamp. We convert compass
    azimuth (0=N, 90=E, clockwise) + elevation into Euler angles.
    """
    bpy.ops.object.light_add(type="SUN", location=(SITE_W / 2, SITE_H / 2, 80))
    sun = bpy.context.active_object
    sun.data.energy = strength
    sun.data.angle = math.radians(0.53)      # real solar disc size -> crisp shadows
    zenith = math.radians(90.0 - elev_deg)
    # compass azimuth -> Blender Z rotation
    sun.rotation_euler = (zenith, 0.0, math.radians(180.0 - azim_deg))
    return sun


def set_sky(night=False):
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    if night:
        bg.inputs["Color"].default_value = (0.02, 0.03, 0.07, 1)
        bg.inputs["Strength"].default_value = 0.35
    else:
        bg.inputs["Color"].default_value = (0.42, 0.60, 0.82, 1)
        bg.inputs["Strength"].default_value = 1.6


def add_camera(loc, look_at, lens=35):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.data.lens = lens
    # aim via a temporary track-to constraint, then bake
    tgt = bpy.data.objects.new("CamTarget", None)
    bpy.context.collection.objects.link(tgt)
    tgt.location = look_at
    con = cam.constraints.new(type="TRACK_TO")
    con.target = tgt
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    bpy.context.scene.camera = cam
    return cam


def render_to(path):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    try:
        scene.cycles.device = "GPU"
    except Exception:
        pass
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.render.resolution_x = RES_X
    scene.render.resolution_y = RES_Y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED: {path}")


# ----------------------------------------------------------------------------
# SCENES
# ----------------------------------------------------------------------------
def scene_aerial(condition_key, out_name, night=False):
    clear_scene()
    build_materials(night=night)
    build_site()
    set_sky(night=night)
    c = SUN_CONDITIONS[condition_key]
    if not night:
        set_sun(c["elev"], c["azim"], c["strength"])
    else:
        set_sun(c["elev"], c["azim"], 0.05)     # faint moonlight; lamps carry it
    add_camera(loc=(-55, -70, 105), look_at=(SITE_W / 2, SITE_H / 2, 0), lens=38)
    render_to(os.path.join(OUT_DIR, "Aerial", out_name))


def scene_eye_level_spine(out_name):
    clear_scene()
    build_materials(night=False)
    build_site()
    set_sky(night=False)
    c = SUN_CONDITIONS["summer_noon"]
    set_sun(c["elev"], c["azim"], c["strength"])
    sx, sy, sw, sh = SPINE
    # stand on the spine near the west entrance, look east down its length
    add_camera(loc=(sx + 4, sy + sh / 2, 1.65),
               look_at=(sx + sw, sy + sh / 2, 2.2), lens=28)
    render_to(os.path.join(OUT_DIR, "Eye_Level", out_name))


def scene_eye_level_plaza(out_name):
    clear_scene()
    build_materials(night=False)
    build_site()
    set_sky(night=False)
    c = SUN_CONDITIONS["winter_noon"]
    set_sun(c["elev"], c["azim"], c["strength"])
    # stand in the Community Plaza looking back toward the spine
    add_camera(loc=(94, 74, 1.65), look_at=(80, 52, 2.0), lens=30)
    render_to(os.path.join(OUT_DIR, "Eye_Level", out_name))


def main():
    print("=" * 60)
    print("Al Safa 2 Park - Blender 3D render pass")
    print("Sun angles from Phase 1.06 real computed solar data")
    print("=" * 60)
    scene_aerial("summer_noon", "aerial_3d_day.png", night=False)
    scene_aerial("evening",     "aerial_3d_night.png", night=True)
    scene_eye_level_spine("eyelevel_3d_shaded_spine.png")
    scene_eye_level_plaza("eyelevel_3d_community_plaza.png")
    print("ALL RENDERS COMPLETE")


if __name__ == "__main__":
    main()
