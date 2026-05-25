"""
Rewire index.html to use the locally-stored, already-annotated YOLO demo
images, and remove all client-side bbox overlays (no longer needed).

Uses BeautifulSoup with the html.parser backend so we don't lose any markup
or restructure unrelated nodes.
"""
import os
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")

MAP = [
    ("hero.jpg",            "Detecção YOLO de ônibus e pedestres em via urbana"),
    ("case-auto.jpg",       "Detecção de peças automotivas com bounding boxes por componente"),
    ("case-saude.jpg",      "Triagem de TCs cerebrais com classificação positive/negative"),
    ("case-varejo.jpg",     "Detecção densa de SKUs em gôndolas de varejo"),
    ("case-logistica.jpg",  "Detecção de EPI (helmet, vest) em operadores de campo"),
    ("case-agro.jpg",       "Detecção de espigas de trigo em lavoura"),
    ("app-industria.jpg",   "Segmentação de trincas em superfícies industriais"),
    ("app-saude.jpg",       "Detecção de pílulas em ambiente farmacêutico"),
    ("app-varejo.jpg",      "Heatmap de fluxo de clientes em supermercado"),
    ("app-agro.jpg",        "Rastreio de plantas individuais em talhão"),
    ("app-documentos.jpg",  "Detecção de assinaturas em documentos digitalizados"),
    ("app-mobilidade.jpg",  "Detecção OBB de veículos em vista aérea de rodovia"),
    ("frame-pessoas.jpg",   "Contagem de pessoas por região em praça pública"),
    ("frame-transito.jpg",  "Rastreio de veículos em rodovia (track-IDs)"),
    ("frame-epi.jpg",       "Detecção de EPI em trabalhadores de construção"),
    ("frame-sports.jpg",    "Detecção de jogadores em partida de futebol"),
]

with open(HTML, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# 1. Replace each Unsplash <img> in document order
imgs = [t for t in soup.find_all("img") if t.get("src", "").startswith("https://images.unsplash.com/")]
print(f"unsplash <img> found: {len(imgs)}")
assert len(imgs) == len(MAP), f"expected {len(MAP)}, got {len(imgs)}"

for tag, (fname, alt) in zip(imgs, MAP):
    tag["src"] = f"assets/cases/{fname}"
    tag["alt"] = alt
    tag["loading"] = "lazy"

# 2. Remove all .bbox-overlay divs entirely
overlays = soup.find_all("div", class_="bbox-overlay")
for div in overlays:
    div.decompose()
print(f"bbox-overlay removed: {len(overlays)}")

# 3. Remove the .hero__overlay div entirely
hero_overlays = soup.find_all("div", class_="hero__overlay")
for div in hero_overlays:
    div.decompose()
print(f"hero__overlay removed: {len(hero_overlays)}")

# 4. Defensive: remove any straggler .bbox divs (none should exist after #2/#3)
strays = soup.find_all("div", class_="bbox")
for div in strays:
    div.decompose()
print(f"stray bbox elements removed: {len(strays)}")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("OK")
