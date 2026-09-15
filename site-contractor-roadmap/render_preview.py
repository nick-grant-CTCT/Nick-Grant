#!/usr/bin/env python3
"""16:9 PNG preview of the companion stacked-column slide."""

from pathlib import Path

import csv
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib import font_manager
from PIL import Image

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "sales-forward-cumulative.csv"
OUT = ROOT / "extra-cumulative-sales.png"
CUBE = ROOT / "ctct-cube.png"

font_manager.fontManager.addfont("/usr/share/fonts/truetype/macos/Inter-Regular.ttf")
font_manager.fontManager.addfont("/usr/share/fonts/truetype/macos/Inter-Bold.ttf")
font_manager.fontManager.addfont("/usr/share/fonts/truetype/macos/Inter-Medium.ttf")
plt.rcParams["font.family"] = "Inter"

ORANGE = "#FF8B00"
GRAY = "#8A9196"
DARK = "#595959"
MUTED = "#8A8A8A"
GRID = "#E6E6E6"


def main():
    rows = list(csv.DictReader(CSV_PATH.open()))
    years = [r["Year"] for r in rows]
    cur = [int(r["Current capacity (cumulative)"]) for r in rows]
    ext = [int(r["Extra from added capacity"]) for r in rows]
    added = [c + e for c, e in zip(cur, ext)]

    fig = plt.figure(figsize=(10, 5.625), dpi=180, facecolor="white")
    ax = fig.add_axes([0.11, 0.20, 0.60, 0.60])
    ax.set_facecolor("white")
    x = list(range(len(years)))
    w = 0.52
    ax.bar(x, cur, width=w, color=GRAY, label="Current capacity", zorder=3)
    ax.bar(x, ext, width=w, bottom=cur, color=ORANGE, label="Extra from added capacity", zorder=3)
    for i, (c, e, a) in enumerate(zip(cur, ext, added)):
        ax.text(i, a + 140, f"{a:,}", ha="center", va="bottom", color=DARK, fontsize=9)
        if e >= 900:
            ax.text(i, c + e / 2, f"+{e:,}", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
        else:
            ax.text(i + 0.30, c + e + 40, f"+{e:,}", ha="left", va="bottom", color=ORANGE, fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years, color=DARK, fontsize=11)
    ax.set_ylabel("System sales", color=DARK, fontsize=10, fontweight="bold")
    ax.set_ylim(0, 7000)
    ax.set_xlim(-0.6, 3.6)
    ax.set_yticks([0, 2000, 4000, 6000])
    ax.set_yticklabels(["0", "2,000", "4,000", "6,000"], color=MUTED, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(DARK)
    ax.spines["bottom"].set_color(DARK)
    ax.tick_params(axis="y", length=0)
    ax.yaxis.grid(True, color=GRID, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.04, 1.02), labelcolor=DARK, fontsize=10)

    fig.text(0.045, 0.92, "Added capacity accumulates extra system sales", fontsize=17, fontweight="bold", color=DARK)
    fig.text(
        0.045,
        0.865,
        "Cumulative extra vs the current-capacity path (same rough estimates as the previous slide).",
        fontsize=9.5,
        color=MUTED,
    )

    fig.patches.append(
        FancyBboxPatch(
            (0.755, 0.42),
            0.20,
            0.22,
            boxstyle="square,pad=0",
            transform=fig.transFigure,
            facecolor="#F2F2F2",
            edgecolor="none",
        )
    )
    fig.text(0.765, 0.58, "1,000", fontsize=18, fontweight="bold", color=ORANGE)
    fig.text(0.765, 0.445, "extra systems by 2034\nvs the current-\ncapacity path", fontsize=8.5, color=DARK, va="bottom")

    ax.text(0, -900, "MVP (added)", ha="center", color=ORANGE, fontsize=8, clip_on=False)
    ax.text(1, -900, "Table stakes (added)", ha="center", color=ORANGE, fontsize=8, clip_on=False)

    fig.text(0.045, 0.035, "6", fontsize=10, color=MUTED)
    fig.text(
        0.09,
        0.035,
        "Rough estimates. Total bar = added-capacity path; gray = current path; orange = extra.",
        fontsize=7,
        color=MUTED,
    )

    fig.savefig(OUT, dpi=180)
    plt.close(fig)

    if CUBE.exists():
        slide = Image.open(OUT).convert("RGBA")
        cube = Image.open(CUBE).convert("RGBA")
        cube = cube.resize((52, 52), Image.Resampling.LANCZOS)
        slide.paste(cube, (slide.width - 70, slide.height - 68), cube)
        slide.convert("RGB").save(OUT, quality=95)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
