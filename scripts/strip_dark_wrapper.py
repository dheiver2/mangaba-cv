import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "assets", "styles.css")

with open(path, "r", encoding="utf-8") as f:
    src = f.read()

marker = "/* =========================================================\n   DARK WRAPPER MODE"
i = src.find(marker)
assert i > 0, "marker not found"
print(f"found at {i}; trimming {len(src) - i} chars")

with open(path, "w", encoding="utf-8") as f:
    f.write(src[:i].rstrip() + "\n")
print("ok")
