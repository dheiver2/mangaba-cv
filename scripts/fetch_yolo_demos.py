"""
Fetch real annotated demo images from the official Ultralytics YOLO assets repo
(github.com/ultralytics/assets, served via jsDelivr CDN). These images already
contain authentic YOLO inference output bounding boxes — no client-side overlay
needed.

Converts AVIF -> JPEG and writes to assets/cases/ for use as plain <img>.
"""
import io
import os
import sys
from urllib.request import urlopen, Request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "cases")
os.makedirs(OUT_DIR, exist_ok=True)

CDN = "https://cdn.jsdelivr.net/gh/ultralytics/assets@main/docs/{}"

# slot_name -> (ultralytics_file, max_width)
JOBS = {
    "hero":             ("yolo-inference-results-on-bus.avif", 1600),
    "case-auto":        ("carparts-detection.avif", 1400),
    "case-saude":       ("brain-tumor-dataset-sample-image.avif", 1400),
    "case-varejo":      ("densely-packed-retail-shelf-1.avif", 1400),
    "case-logistica":   ("personal-protective-equipment-detection.avif", 1400),
    "case-agro":        ("wheat-head-detection-sample.avif", 1400),
    "app-industria":    ("crack-segmentation-sample.avif", 1200),
    "app-saude":        ("medical-pills-dataset-sample-image.avif", 1200),
    "app-varejo":       ("ultralytics-yolov8-retail-heatmap.avif", 1200),
    "app-agro":         ("plants-tracking-in-zone-using-ultralytics-yolo11.avif", 1200),
    "app-documentos":   ("signature-detection-mosaiced-sample.avif", 1200),
    "app-mobilidade":   ("vehicle-detection-using-obb.avif", 1200),
    "frame-pessoas":    ("people-counting-different-region-ultralytics-yolov8.avif", 1400),
    "frame-transito":   ("vehicle-tracking.avif", 1400),
    "frame-epi":        ("construction-ppe-dataset-sample.avif", 1400),
    "frame-sports":     ("football-players-detection.avif", 1400),
}


def fetch(name, src, max_w):
    url = CDN.format(src)
    print(f"  -> {name} ({src})")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
    out = os.path.join(OUT_DIR, f"{name}.jpg")
    img.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return len(data), os.path.getsize(out)


print(f"Fetching {len(JOBS)} Ultralytics YOLO annotated demos -> {OUT_DIR}")
ok = 0
for name, (src, mw) in JOBS.items():
    try:
        rd, sz = fetch(name, src, mw)
        ok += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}", file=sys.stderr)
print(f"\nDone: {ok}/{len(JOBS)} fetched.")
