"""Build one Quick Look package per spot from the existing rat and bubble USDZs.

Run with Blender 5.x:
  blender --background --python tools/build_ios_spot_usdz.py

iOS Quick Look accepts one USDZ model for an AR placement, so each output
contains both the character and the configured speech bubble.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
SPOTS_PATH = ROOT / "spots.json"
RAT_USDZ = ROOT / "assets" / "character.usdz"
OUTPUT_DIR = ROOT / "assets" / "ios"


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def import_usdz(path: Path) -> list[bpy.types.Object]:
    before = set(bpy.context.scene.objects)
    bpy.ops.wm.usd_import(filepath=str(path), import_materials=True, import_meshes=True)
    imported = list(set(bpy.context.scene.objects) - before)
    if not imported:
        raise RuntimeError(f"No objects imported from {path}")
    return imported


def make_root(objects: list[bpy.types.Object], name: str) -> bpy.types.Object:
    imported = set(objects)
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    for obj in objects:
        if obj.parent not in imported:
            world = obj.matrix_world.copy()
            obj.parent = root
            obj.matrix_world = world
    return root


def world_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points: list[Vector] = []
    for obj in objects:
        if obj.type == "MESH":
            points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    if not points:
        raise RuntimeError("Imported USDZ contains no mesh geometry")
    mins = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    maxs = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return mins, maxs


def build_spot(spot_id: str, spot: dict) -> None:
    bubble_rel = spot.get("companionModelUsdz")
    if not bubble_rel:
        raise RuntimeError(f"Spot {spot_id} has no companionModelUsdz")
    bubble_path = ROOT / Path(bubble_rel)
    if not bubble_path.is_file():
        raise FileNotFoundError(bubble_path)

    clear_scene()
    rat_objects = import_usdz(RAT_USDZ)
    rat_root = make_root(rat_objects, "Character")
    rat_min, rat_max = world_bounds(rat_objects)
    rat_height = rat_max.y - rat_min.y
    model_scale = float(spot.get("modelScale", 1))
    rat_root.scale = (model_scale, model_scale, model_scale)
    rat_root.location.y = -rat_min.y * model_scale

    bubble_objects = import_usdz(bubble_path)
    bubble_root = make_root(bubble_objects, "SpeechBubble")
    bubble_min, bubble_max = world_bounds(bubble_objects)
    scale = float(spot.get("companionScale", 1))
    x_offset = float(spot.get("companionXOffset", 0))
    y_offset = float(spot.get("iosCompanionYOffset", spot.get("companionYOffset", 0.12)))
    bubble_root.scale = (scale, scale, scale)
    bubble_root.location = (
        -((bubble_min.x + bubble_max.x) * 0.5 * scale) + x_offset,
        -rat_min.y * model_scale + rat_height * model_scale + y_offset - bubble_min.y * scale,
        -((bubble_min.z + bubble_max.z) * 0.5 * scale),
    )

    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = ROOT / Path(spot.get("iosModelUsdz", f"assets/ios/spot-{spot_id}-with-bubble.usdz"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.usd_export(
        filepath=str(output_path),
        selected_objects_only=False,
        export_animation=False,
        export_materials=True,
        export_textures_mode="NEW",
        generate_preview_surface=True,
        export_meshes=True,
        export_lights=False,
        export_cameras=False,
        convert_scene_units="METERS",
        meters_per_unit=1.0,
    )
    if not output_path.is_file() or output_path.stat().st_size == 0:
        raise RuntimeError(f"USDZ export did not produce {output_path}")
    print(f"BUILT {spot_id}: {output_path} ({output_path.stat().st_size} bytes)")


def main() -> None:
    spots = json.loads(SPOTS_PATH.read_text(encoding="utf-8"))
    selected_spot = os.environ.get("IOS_USDZ_SPOT")
    for spot_id, spot in spots.items():
        if selected_spot and spot_id != selected_spot:
            continue
        build_spot(spot_id, spot)


if __name__ == "__main__":
    main()
