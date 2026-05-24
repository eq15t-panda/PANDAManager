import matplotlib as mpl
import matplotlib.pyplot as plt


# ------------------------------------------------
# Document geometry — derived from your preamble
# A4=210mm, margins=2×25mm, binding=10mm
# textwidth = 210 - 50 - 10 = 150mm
# ------------------------------------------------
_mm_to_in   = 1.0 / 25.4
_textwidth  = 150.0 * _mm_to_in          # 5.906 inches — full \textwidth
_golden     = (1.0 + 5.0**0.5) / 2.0    # 1.618 — default aspect ratio


def fig_size(width_frac=1.0, aspect=None):
    """
    Return (width, height) in inches so that matplotlib's font sizes
    match LaTeX's after \includegraphics[width=<width_frac>\textwidth]{...}.

    width_frac : fraction of \\textwidth  (1.0 = full, 0.5 = side-by-side)
    aspect     : height/width ratio. Defaults to 1/golden.
    """
    w = _textwidth * width_frac
    h = w / _golden if aspect is None else w * aspect
    return w, h


def set_plot_style(width_frac=1.0, aspect=None):
    mpl.rcParams.update({

        # ------------------------------------------------
        # LaTeX / Fonts — libertine text + newtxmath
        # ------------------------------------------------
        "text.usetex":          True,
        "text.latex.preamble":  r"\usepackage{libertine}"
                                r"\usepackage[libertine]{newtxmath}",
        "font.family":          "serif",
        "font.serif":           ["Linux Libertine O"],

        # ------------------------------------------------
        # Figure size — must match \includegraphics width
        # so that 10pt in matplotlib = 10pt in the PDF
        # ------------------------------------------------
        "figure.figsize":       fig_size(width_frac, aspect),
        "figure.dpi":           150,       # screen preview only
        "savefig.dpi":          300,
        "savefig.bbox":         "tight",
        "savefig.pad_inches":   0.05,
        "savefig.format":       "pdf",

        # ------------------------------------------------
        # Font sizes — all in pt, anchored to 10pt body
        # Caption uses \bf label (~10pt) + 9pt body text
        # ------------------------------------------------
        "font.size":            10,
        "axes.labelsize":       10,
        "axes.titlesize":       10,
        "xtick.labelsize":       9,
        "ytick.labelsize":       9,
        "legend.fontsize":       9,

        # ------------------------------------------------
        # Axes
        # ------------------------------------------------
        "axes.linewidth":       0.8,
        "axes.labelpad":        4.0,

        # ------------------------------------------------
        # Ticks
        # ------------------------------------------------
        "xtick.direction":      "in",
        "ytick.direction":      "in",
        "xtick.top":            True,
        "ytick.right":          True,
        "xtick.major.size":     4.0,
        "ytick.major.size":     4.0,
        "xtick.minor.size":     2.0,
        "ytick.minor.size":     2.0,
        "xtick.major.width":    0.8,
        "ytick.major.width":    0.8,
        "xtick.minor.width":    0.6,
        "ytick.minor.width":    0.6,
        "xtick.minor.visible":  True,
        "ytick.minor.visible":  True,

        # ------------------------------------------------
        # Legend
        # ------------------------------------------------
        "legend.frameon":       True,
        "legend.framealpha":    0.9,
        "legend.edgecolor":     "0.8",
        "legend.borderpad":     0.5,
        "legend.handlelength":  1.5,

        # ------------------------------------------------
        # Lines and markers
        # ------------------------------------------------
        "lines.linewidth":      1.5,
        "lines.markersize":     5,

        # ------------------------------------------------
        # Grid
        # ------------------------------------------------
        "grid.linewidth":       0.5,
        "grid.alpha":           0.3,

        # ------------------------------------------------
        # Color cycle — link blue + cite purple anchor
        # ------------------------------------------------
        "axes.prop_cycle": mpl.cycler(color=[
            "#0072CF",  # link blue   (your linkcolor)
            "#e05c2a",  # burnt orange
            "#2ca02c",  # green
            "#7818c8",  # cite purple (your citecolor)
            "#d62728",  # red
            "#17becf",  # teal
            "#8c564b",  # brown
            "#7f7f7f",  # gray
        ]),
    })