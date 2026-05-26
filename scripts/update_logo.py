"""Replace every inline mango SVG with the high-fidelity painterly version
matching the brand reference image."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "brand.html"),
]

def painterly_svg(width: int, suffix: str) -> str:
    """Return a painterly mango SVG with the given size and unique gradient IDs."""
    s = suffix
    return (
        f'<svg width="{width}" height="{width}" viewBox="0 0 100 100" fill="none" aria-hidden="true">\n'
        f'<defs>\n'
        f'<radialGradient id="mb{s}" cx="38%" cy="32%" r="78%">\n'
        f'<stop offset="0%" stop-color="#FFEFB2"/>\n'
        f'<stop offset="22%" stop-color="#FFCE63"/>\n'
        f'<stop offset="50%" stop-color="#F49E2D"/>\n'
        f'<stop offset="78%" stop-color="#DD7314"/>\n'
        f'<stop offset="100%" stop-color="#B14E08"/>\n'
        f'</radialGradient>\n'
        f'<radialGradient id="mbl{s}" cx="75%" cy="55%" r="45%">\n'
        f'<stop offset="0%" stop-color="#D33D0C" stop-opacity="0.42"/>\n'
        f'<stop offset="100%" stop-color="#D33D0C" stop-opacity="0"/>\n'
        f'</radialGradient>\n'
        f'<linearGradient id="ml{s}" x1="0" y1="0" x2="1" y2="1">\n'
        f'<stop offset="0%" stop-color="#7CB85E"/>\n'
        f'<stop offset="60%" stop-color="#509B3D"/>\n'
        f'<stop offset="100%" stop-color="#367A26"/>\n'
        f'</linearGradient>\n'
        f'</defs>\n'
        # mango body
        f'<path d="M50 24 C 32 24, 19 38, 19 58 C 19 80, 33 92, 54 92 C 74 92, 86 77, 86 58 C 86 39, 70 24, 50 24 Z" fill="url(#mb{s})"/>\n'
        # right-side blush
        f'<path d="M50 24 C 32 24, 19 38, 19 58 C 19 80, 33 92, 54 92 C 74 92, 86 77, 86 58 C 86 39, 70 24, 50 24 Z" fill="url(#mbl{s})"/>\n'
        # small brown stem
        f'<path d="M50 24 C 49.5 21, 49.8 18, 51 16 C 52.3 17.2, 52.8 20, 52 24 Z" fill="#6F4F2E"/>\n'
        # leaf on LEFT (oval, tilted)
        f'<path d="M44 18 C 34 12, 22 14, 20 22 C 24 28, 38 28, 46 21 Z" fill="url(#ml{s})"/>\n'
        # leaf vein
        f'<path d="M22 22 C 30 23, 40 22, 45 19" stroke="#2F5A1F" stroke-width="0.6" fill="none" opacity="0.5"/>\n'
        f'</svg>'
    )

# Counter for unique gradient IDs across replacements within a single file
def make_replacer():
    n = {"i": 0}
    def repl(m):
        # detect width from "width=...." in the original tag
        m_size = re.search(r'width="(\d+)"', m.group(0))
        width = int(m_size.group(1)) if m_size else 32
        n["i"] += 1
        return painterly_svg(width, str(n["i"]))
    return repl

# Match an entire <svg ... viewBox="0 0 [64|32]..."> ... </svg> block.
# Greedy enough to catch the multi-line SVGs we wrote earlier.
SVG_PATTERN = re.compile(
    r'<svg[^>]*viewBox="0 0 (?:32|64) (?:32|64)"[^>]*>.*?</svg>',
    re.DOTALL | re.IGNORECASE,
)

for path in FILES:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    repl = make_replacer()
    new_src, n_replaced = SVG_PATTERN.subn(repl, src)
    print(f"{os.path.basename(path)}: {n_replaced} svg(s) replaced")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_src)

print("done")
