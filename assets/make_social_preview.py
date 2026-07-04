"""Generate the GitHub social-preview card (1280x640) for tokenomics-autopsy.

The visual is a logarithmic spiral decaying to zero — a death-spiral metaphor —
colored blue -> amber -> red as it collapses inward.

Run:  python make_social_preview.py   ->  social-preview.png
GitHub has no API to set the social preview, so upload the PNG manually:
  repo  ->  Settings  ->  General  ->  Social preview  ->  Upload an image.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

BG = "#0b1220"
W, H = 1280, 640

fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
fig.patch.set_facecolor(BG)

# --- death-spiral graphic (right side) ---
ax = fig.add_axes([0.55, 0.04, 0.43, 0.92])
ax.set_facecolor(BG)
ax.axis("off")
ax.set_aspect("equal")
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)

theta = np.linspace(0, 9 * np.pi, 3000)
r = np.exp(-0.075 * theta)                 # decays toward 0
x, y = r * np.cos(theta), r * np.sin(theta)
pts = np.array([x, y]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

cmap = LinearSegmentedColormap.from_list("ds", ["#2563eb", "#d97706", "#dc2626"])
lc = LineCollection(segs, cmap=cmap, linewidths=np.linspace(5.5, 0.3, len(segs)))
lc.set_array(np.linspace(0, 1, len(segs)))
ax.add_collection(lc)
ax.plot(0, 0, "o", color="#dc2626", ms=7)  # the zero it spirals into

# --- text (left side) ---
fig.text(0.045, 0.75, "Tokenomics Soundcheck", color="white",
         fontsize=42, fontweight="bold")
fig.text(0.047, 0.645, "Sound money needs sound mechanisms.",
         color="#cbd5e1", fontsize=19, style="italic")
fig.text(0.047, 0.55, "Design token economies that don't fuel their own",
         color="#cbd5e1", fontsize=18)
fig.text(0.047, 0.49, "collapse — and stress-test them before they launch.",
         color="#cbd5e1", fontsize=18)
fig.text(0.047, 0.36,
         "50+ collapses   ·   15 failure skills   ·   4 game models   ·   reproducible sims",
         color="#7dd3fc", fontsize=15, fontweight="bold")
fig.text(0.047, 0.26, "λ > 1  →  price becomes the fuel for its own collapse",
         color="#94a3b8", fontsize=14, style="italic")
fig.text(0.047, 0.115, "github.com/wusijian007/tokenomics-autopsy   ·   CC BY 4.0",
         color="#64748b", fontsize=13)

out = Path(__file__).parent / "social-preview.png"
fig.savefig(out, facecolor=BG)
plt.close(fig)
print(f"saved -> {out}  ({W}x{H})")
