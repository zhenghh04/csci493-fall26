"""Reference solution — plot sin(x) over [0, 2*pi] and save to sin.png.

The lab's point is to have opencode WRITE this from a plain-language prompt;
this file is the instructor's answer key / projector fallback.

    python plot_sin.py        # writes sin.png in the current folder

Requires: numpy, matplotlib  (pip install numpy matplotlib)
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless: save to a file without needing a display
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x)

plt.figure(figsize=(6, 3.5))
plt.plot(x, y, color="#2962a8", linewidth=2)
plt.axhline(0, color="0.7", linewidth=0.8)
plt.title("y = sin(x)")
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.tight_layout()
plt.savefig("sin.png", dpi=150)
print("wrote sin.png")
