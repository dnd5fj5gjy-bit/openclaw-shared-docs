#!/usr/bin/env python3
"""Generate cinematic scene images for Wildernests Frontier video."""
import subprocess, os, sys, time

OUT_DIR = os.path.join(os.path.dirname(__file__), "images")
TOOL = os.path.expanduser("~/agents/shared/tools/generate_image.py")

BASE_STYLE = "cinematic, photorealistic, 16:9 wide angle, anamorphic lens, film grain, dark moody atmosphere, no text, no watermarks, ultra detailed"

SCENES = [
    ("s01", f"Pre-dawn aerial shot over vast untouched wilderness. A lone horseman barely visible far below in tall golden grass. Dark indigo sky, first light on the horizon. Wide open landscape, no human structures. {BASE_STYLE}"),
    ("s02", f"Low tracking shot following a lone rider through tall grass, camera skimming the earth, grass blurring in the foreground. Morning light, golden grass, wild open landscape stretching to hills. {BASE_STYLE}"),
    ("s04", f"Ancient Mesopotamia, 5000 BC. Eye-level with early farmers at the fertile banks of the Euphrates. Dark rich soil, reed structures, palm trees, workers bent over in the fields. Warm ancient light. {BASE_STYLE}"),
    ("s05", f"Medieval hilltop stone settlement. Practical stone walls, terraced fields below, trade roads converging from multiple directions. Overcast European light, smoke from hearths, horses in the distance. {BASE_STYLE}"),
    ("s06", f"Cold modern infrastructure. Row of towering electricity pylons across a grey landscape. Motorway interchange, water treatment towers, industrial grey. Wide shot, dehumanizing scale, flat winter light. {BASE_STYLE}"),
    ("s07", f"Dark urban compression. Dense high-rise tower blocks, neon reflections on wet tarmac, crowds in motion blur, traffic light trails. Overwhelming, claustrophobic, dystopian city night scene. {BASE_STYLE}"),
    ("s08", f"First reveal of an architecturally stunning off-grid home in a remote mountain valley. Wide aerial shot approaching. The structure is small, perfect, isolated against vast ancient landscape. Dawn light. {BASE_STYLE}"),
    ("s09", f"Close architectural detail of the home exterior at dawn. Low golden sun raking across integrated solar cladding panels. Light pouring across the structure, warm amber tones, dew on surfaces. {BASE_STYLE}"),
    ("s10", f"Wide aerial night shot. A single off-grid home glowing warm amber from within in an ocean of pitch-black wilderness. No roads, no other lights, no neighbours for miles. Stars above. {BASE_STYLE}"),
    ("s11", f"Beautifully lit interior shot of an atmospheric water generation machine. Treated with architectural reverence, almost sculptural. Brushed metal, blue LED, water condensing. Technical beauty. {BASE_STYLE}"),
    ("s12", f"Extreme close-up detail of the atmospheric water generator in operation. Viewing port showing condensation collecting, flowing mechanism, engineering precision. Technical macro photography. {BASE_STYLE}"),
    ("s13", f"Macro shot: clean crystal clear water pouring from a tap into a glass held by a weathered, strong hand. Through the window behind, vast wilderness in soft focus. Warm interior light. {BASE_STYLE}"),
    ("s14", f"Exterior of the off-grid home. Sky darkening rapidly, storm approaching. Armoured steel shutters sliding silently into place across the windows, automated. Ominous sky, rising wind bending grass. {BASE_STYLE}"),
    ("s15", f"Storm at full power. Rain sheeting horizontally against closed steel shutters. Lightning strike illuminating dark clouds behind the sealed home. The structure completely unmoved. {BASE_STYLE}"),
    ("s16", f"Wall of wildfire in a distant valley below. Orange inferno, smoke column. The off-grid home in the foreground, shutters closed, completely protected. Fire will not reach it. Dramatic contrast. {BASE_STYLE}"),
    ("s17", f"Ground tremor. Cracked earth in the foreground, dust rising. The off-grid home on solid ground, structure intact and holding, undamaged. Dramatic geological scale. {BASE_STYLE}"),
    ("s18", f"Flash flood rushing through a valley below. The off-grid home elevated on the hillside above, completely untouched by the floodwater. Dramatic aerial perspective, churning water below. {BASE_STYLE}"),
    ("s19", f"The off-grid home in a remote wild valley at dusk. No road. No power line. No fence. No other structure visible in any direction. Pure wilderness. Complete independence. {BASE_STYLE}"),
    ("s20", f"Time-lapse construction: a skilled team assembling the off-grid home structure, motion blur suggesting rapid progress. Three days of building compressed into one frame. Raw materials, skilled hands. {BASE_STYLE}"),
    ("s21", f"Hero shot at golden hour. The off-grid home perfectly framed in a sweeping landscape. A single figure stands outside looking at the mountains they chose as home. Wide, epic, aspirational. {BASE_STYLE}"),
    ("s22", f"Aerial retreat shot. Camera slowly pulling back and rising. The off-grid home grows smaller, the wilderness expanding to fill the frame in every direction. Final reveal of scale. {BASE_STYLE}"),
]

for scene_id, prompt in SCENES:
    out_file = os.path.join(OUT_DIR, f"{scene_id}.png")
    if os.path.exists(out_file):
        print(f"  [skip] {scene_id}")
        continue
    print(f"  [gen]  {scene_id}...")
    result = subprocess.run(
        ["python3", TOOL, "--prompt", prompt, "--filename", out_file, "--resolution", "2K"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  [err]  {scene_id}: {result.stderr[:300]}")
        # Try 1K fallback
        result2 = subprocess.run(
            ["python3", TOOL, "--prompt", prompt, "--filename", out_file, "--resolution", "1K"],
            capture_output=True, text=True
        )
        if result2.returncode == 0:
            print(f"  [ok]   {scene_id} (1K fallback)")
        else:
            print(f"  [FAIL] {scene_id}")
    else:
        print(f"  [ok]   {scene_id}")
    time.sleep(0.5)

print("Image generation complete.")
