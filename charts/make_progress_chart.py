"""Render the residual-constant progress chart (charts/progress.png, charts/progress.svg)."""
from datetime import date
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # validated categorical slots 1 and 2

openai = (date(2026, 9, 23), 1642)
ours = [
    (date(2026, 10, 9), 1034, "initial draft"),
    (date(2026, 10, 9), 980, "PR #1 active supports"),
    (date(2026, 10, 10), 190, "PR #2 sequential count"),
    (date(2026, 10, 10), 30, "PR #3 defect overlaps"),
]

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=160)
fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.grid(axis="y", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
ax.tick_params(colors=INK2, labelsize=9)

# OpenAI baseline: point plus reference line it set
ax.axhline(openai[1], color=ORANGE, linewidth=2, linestyle=(0, (4, 3)), zorder=2)
ax.plot([openai[0]], [openai[1]], marker="o", markersize=9, color=ORANGE,
        markeredgecolor=SURFACE, markeredgewidth=2, linestyle="none", zorder=4, label="OpenAI preprint (Sept 23)")
ax.annotate("1642", (openai[0], openai[1]), textcoords="offset points", xytext=(0, 10),
            ha="center", color=INK, fontsize=10, fontweight="bold")

# Our refinements as a step from the baseline
xs = [openai[0]] + [d for d, _, _ in ours]
ys = [openai[1]] + [v for _, v, _ in ours]
ax.step(xs, ys, where="post", color=BLUE, linewidth=2, zorder=3, label="rohanarun/sidorenko-template-refinements")
ax.plot([d for d, _, _ in ours], [v for _, v, _ in ours], marker="o", markersize=9, color=BLUE,
        markeredgecolor=SURFACE, markeredgewidth=2, linestyle="none", zorder=4)
offsets = [(8, 6), (8, -16), (-10, 8), (10, 4)]
for (d, v, name), off in zip(ours, offsets):
    ax.annotate(f"{v}  {name}", (d, v), textcoords="offset points", xytext=off,
                ha="left" if off[0] > 0 else "right", color=INK, fontsize=10, fontweight="bold")

ax.set_ylim(0, 1800)
ax.set_xlim(date(2026, 9, 20), date(2026, 10, 14))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
ax.set_ylabel("Even dimension D sufficient for the\nnondirect residual step (lower is better)", color=INK2, fontsize=10)
ax.set_title("Sidorenko counterexample: the residual-counting constant over time",
             loc="left", color=INK, fontsize=13, fontweight="bold", pad=14)
leg = ax.legend(loc="lower left", frameon=False, fontsize=9, labelcolor=INK2)
fig.text(0.01, 0.012, "Sources: openai/math preprint (Sept 23, 2026); github.com/rohanarun/sidorenko-template-refinements.\n"
         "Only this one counting step is lowered; the other dimension thresholds in the proof are unchanged.",
         color=INK2, fontsize=7.5)
fig.tight_layout(rect=(0, 0.05, 1, 1))
out = Path(__file__).resolve().parent
fig.savefig(out / "progress.png", facecolor=SURFACE)
fig.savefig(out / "progress.svg", facecolor=SURFACE)
print("wrote", out / "progress.png")
