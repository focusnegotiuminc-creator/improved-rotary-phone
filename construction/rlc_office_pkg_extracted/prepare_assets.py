from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
LOGO_DIR = ROOT / "assets" / "logos"
SKETCH_DIR = ROOT / "assets" / "sketches"
OUTPUT_LOGO_DIR = LOGO_DIR / "clean"
OUTPUT_SKETCH_DIR = SKETCH_DIR / "trace"
OUTPUT_LOGO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_SKETCH_DIR.mkdir(parents=True, exist_ok=True)


def remove_black_square_keep_art(src: Path, dest: Path) -> None:
    img = Image.open(src).convert("RGBA")
    data = img.load()
    width, height = img.size
    # Treat the background as near-black within the outer 15% margin to preserve interior black artwork.
    margin_x = int(width * 0.15)
    margin_y = int(height * 0.15)
    for y in range(height):
        for x in range(width):
            if x < margin_x or x > width - margin_x or y < margin_y or y > height - margin_y:
                r, g, b, a = data[x, y]
                if r < 30 and g < 30 and b < 30:
                    data[x, y] = (r, g, b, 0)
    img.save(dest)


def make_white_background_transparent(src: Path, dest: Path, threshold: int = 245) -> None:
    img = Image.open(src).convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    img.save(dest)


def trace_sketch(src: Path, dest: Path) -> None:
    img = Image.open(src).convert("L")
    # Invert and threshold for lines
    bw = img.point(lambda p: 255 if p < 160 else 0, mode="1")
    # Crop to bounding box of ink
    bbox = bw.getbbox()
    if bbox:
        bw = bw.crop(bbox)
    bw = bw.convert("L")
    # thicken lines slightly
    bw = bw.point(lambda p: 0 if p < 128 else 255)
    bw.save(dest)


def main() -> None:
    rlc = LOGO_DIR / "rlc.png"
    focus = LOGO_DIR / "focus inc.jpg"
    if rlc.exists():
        remove_black_square_keep_art(rlc, OUTPUT_LOGO_DIR / "rlc_clean.png")
    if focus.exists():
        make_white_background_transparent(focus, OUTPUT_LOGO_DIR / "focus_inc_clean.png")

    for sketch_name in ["floor.jpg", "download.jpg"]:
        sketch_path = SKETCH_DIR / sketch_name
        if sketch_path.exists():
            out_name = sketch_path.stem + "_trace.png"
            trace_sketch(sketch_path, OUTPUT_SKETCH_DIR / out_name)


if __name__ == "__main__":
    main()
