"""
Mangaba CV — generate baked-in annotated images for the landing page.

Downloads each source photo, draws bounding boxes + labels directly into the
JPEG, and saves to assets/cases/. The HTML then uses these as plain <img>
elements — no CSS overlays.

Color scheme matches the landing page:
    default = terracotta #D97757
    ok      = green      #4F9C6A
    warn    = amber      #E0A53C
"""
import io
import os
import sys
from urllib.request import urlopen, Request
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "cases")
os.makedirs(OUT_DIR, exist_ok=True)

COLORS = {
    # variant : (border_rgb, label_text_rgb, fill_alpha_rgba)
    "default": ((217, 119, 87),  (255, 255, 255), (217, 119, 87, 35)),
    "ok":      ((79, 156, 106),  (255, 255, 255), (79, 156, 106, 35)),
    "warn":    ((224, 165, 60),  (42, 29, 5),     (224, 165, 60, 40)),
}

def get_font(size):
    for path in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguibl.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def download(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=45) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def draw_bbox(base, x_pct, y_pct, w_pct, h_pct, label, variant="default"):
    W, H = base.size
    x = int(W * x_pct / 100)
    y = int(H * y_pct / 100)
    w = int(W * w_pct / 100)
    h = int(H * h_pct / 100)

    border, text_color, fill = COLORS[variant]
    # line width scales with image size
    lw = max(3, int(min(W, H) / 280))

    # Translucent fill via overlay
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x, y, x + w, y + h], fill=fill, outline=border, width=lw)
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(overlay)
    composed = base_rgba.convert("RGB")
    base.paste(composed)

    # Label chip
    draw = ImageDraw.Draw(base)
    label_size = max(14, int(min(W, H) / 42))
    font = get_font(label_size)

    try:
        bb = draw.textbbox((0, 0), label, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        # textbbox can include ascender padding; use it directly
    except AttributeError:
        tw, th = draw.textsize(label, font=font)

    pad_x, pad_y = 8, 4
    chip_w = tw + 2 * pad_x
    chip_h = th + 2 * pad_y

    # Anchor chip flush with top-left of bbox border
    cx = x - lw // 2
    cy = y - lw // 2
    draw.rectangle([cx, cy, cx + chip_w, cy + chip_h], fill=border)
    draw.text((cx + pad_x, cy + pad_y - 2), label, fill=text_color, font=font)


def render(url, bboxes, output, max_w=1400):
    out_path = os.path.join(OUT_DIR, output)
    print(f"  -> {output}")
    img = download(url)
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
    for bb in bboxes:
        variant = bb[5] if len(bb) > 5 else "default"
        draw_bbox(img, bb[0], bb[1], bb[2], bb[3], bb[4], variant)
    img.save(out_path, "JPEG", quality=84, optimize=True, progressive=True)
    return out_path


JOBS = [
    # ====== HERO ======
    ("https://images.unsplash.com/photo-1565514020179-026b92b84bb6?auto=format&fit=crop&w=1600&q=85",
     [(10, 28, 24, 48, "peca OK 0.97", "ok"),
      (40, 34, 22, 38, "defeito 0.86", "warn"),
      (68, 30, 22, 46, "peca 0.93", "default")],
     "hero.jpg"),

    # ====== CASES REAIS ======
    ("https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&w=1600&q=85",
     [(18, 30, 30, 46, "painel OK 0.97", "ok"),
      (54, 38, 18, 22, "risco 0.84", "warn")],
     "case-auto.jpg"),

    ("https://images.unsplash.com/photo-1530497610245-94d3c16cda28?auto=format&fit=crop&w=1600&q=85",
     [(38, 28, 22, 30, "achado prioritario", "warn"),
      (64, 36, 22, 32, "regiao normal", "ok")],
     "case-saude.jpg"),

    ("https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=1600&q=85",
     [(8, 22, 24, 56, "SKU 4521 0.98", "ok"),
      (38, 36, 20, 30, "ruptura 0.91", "warn"),
      (64, 24, 24, 54, "SKU 8830 0.96", "ok")],
     "case-varejo.jpg"),

    ("https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1600&q=85",
     [(30, 12, 34, 78, "operador 0.96", "default"),
      (34, 14, 24, 18, "capacete OK", "ok"),
      (32, 40, 30, 26, "colete OK", "ok")],
     "case-logistica.jpg"),

    ("https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=1600&q=85",
     [(8, 14, 38, 60, "talhao A sadio", "ok"),
      (52, 42, 24, 28, "falha plantio", "warn"),
      (78, 22, 14, 46, "talhao B sadio", "ok")],
     "case-agro.jpg"),

    # ====== APLICAÇÕES (6) ======
    ("https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1200&q=85",
     [(14, 26, 38, 46, "peca 0.96", "ok"),
      (58, 44, 22, 24, "defeito 0.83", "warn")],
     "app-industria.jpg"),

    ("https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=1200&q=85",
     [(18, 18, 28, 54, "pulmao D 0.97", "ok"),
      (54, 32, 18, 20, "achado 0.84", "warn")],
     "app-saude.jpg"),

    ("https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=1200&q=85",
     [(6, 18, 36, 60, "SKU 12/14", "ok"),
      (48, 52, 18, 24, "ruptura 0.78", "warn")],
     "app-varejo.jpg"),

    ("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85",
     [(8, 14, 46, 62, "talhao 0.92", "ok"),
      (60, 46, 24, 26, "falha 0.81", "warn")],
     "app-agro.jpg"),

    ("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=85",
     [(14, 22, 44, 18, "campo 0.99", "default"),
      (14, 46, 66, 34, "tabela 0.97", "ok")],
     "app-documentos.jpg"),

    ("https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=85",
     [(14, 40, 24, 32, "carro 0.95", "default"),
      (46, 38, 28, 36, "onibus 0.92", "ok"),
      (22, 68, 16, 10, "ABC-1D23", "warn")],
     "app-mobilidade.jpg"),

    # ====== FRAMES (4) ======
    ("https://images.unsplash.com/photo-1519567241046-7f570eee3ce6?auto=format&fit=crop&w=1400&q=85",
     [(14, 30, 14, 54, "pessoa 0.94", "default"),
      (34, 26, 14, 58, "pessoa 0.91", "default"),
      (56, 32, 14, 52, "ID #87", "default"),
      (76, 30, 14, 54, "pessoa 0.89", "default")],
     "frame-pessoas.jpg"),

    ("https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=1400&q=85",
     [(14, 40, 26, 32, "carro 0.95", "default"),
      (50, 44, 30, 30, "caminhao 0.91", "ok"),
      (22, 68, 18, 10, "placa ABC-1D23", "warn")],
     "frame-transito.jpg"),

    ("https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?auto=format&fit=crop&w=1400&q=85",
     [(28, 12, 34, 80, "operador 0.96", "default"),
      (34, 14, 24, 18, "capacete OK", "ok"),
      (30, 40, 30, 26, "colete OK", "ok")],
     "frame-epi.jpg"),

    ("https://images.unsplash.com/photo-1551958219-acbc608c6377?auto=format&fit=crop&w=1400&q=85",
     [(18, 24, 14, 52, "#10 home", "default"),
      (42, 28, 14, 48, "#7 away", "warn"),
      (66, 24, 14, 52, "#3 home", "default"),
      (50, 62, 6, 10, "bola ID 1", "ok")],
     "frame-sports.jpg"),
]

print(f"Generating {len(JOBS)} annotated images -> {OUT_DIR}")
ok = 0
for url, bboxes, out in JOBS:
    try:
        render(url, bboxes, out)
        ok += 1
    except Exception as e:
        print(f"  FAIL {out}: {e}", file=sys.stderr)

print(f"\nDone: {ok}/{len(JOBS)} images generated.")
