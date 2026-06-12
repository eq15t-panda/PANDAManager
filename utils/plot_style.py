import matplotlib as mpl
import matplotlib.colors as mcolors
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

# ------------------------------------------------
# ------------------------------------------------
# Color cycle — link blue + cite purple anchor
# ------------------------------------------------
# "axes.prop_cycle": mpl.cycler(color=[
#     "#0072CF",  # link blue
#     "#e05c2a",  # burnt orange
#     "#2ca02c",  # green
#     "#7818c8",  # cite purple
#     "#d62728",  # red
#     "#17becf",  # teal
#     "#8c564b",  # brown
#     "#7f7f7f",  # gray
# ]),
# })
# ------------------------------------------------

def set_plot_style(width_frac=1.0, aspect=None):

    # Add custom colors to CSS4_COLORS for easy use by name
    mcolors.CSS4_COLORS.update({
        "blue390" : "#007dff",
        "red780" : "#ff0000",
    })

    # Set plot style parameters to match LaTeX document style
    mpl.rcParams.update({

        # ------------------------------------------------
        # Typography
        # ------------------------------------------------
        "text.usetex": True,
        "text.latex.preamble":
            r"\usepackage{libertine}"
            r"\usepackage[libertine]{newtxmath}",

        "font.family": "serif",

        # Slightly larger than document body for readability
        "font.size": 12,
        "axes.labelsize": 12,
        "axes.titlesize": 12,

        "xtick.labelsize": 12,
        "ytick.labelsize": 12,

        "legend.fontsize": 12,

        # ------------------------------------------------
        # Figure geometry
        # ------------------------------------------------
        "figure.figsize": fig_size(width_frac, aspect),

        # Higher preview DPI helps notebook rendering
        "figure.dpi": 180,

        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,

        # ------------------------------------------------
        # Axes
        # ------------------------------------------------
        "axes.linewidth": 0.9,
        "axes.labelpad": 6,

        # Cleaner scientific style
        "axes.spines.top": True,
        "axes.spines.right": True,

        # ------------------------------------------------
        # Ticks
        # ------------------------------------------------
        "xtick.direction": "in",
        "ytick.direction": "in",

        "xtick.top": True,
        "ytick.right": True,

        "xtick.major.size": 5,
        "ytick.major.size": 5,

        "xtick.minor.size": 2.5,
        "ytick.minor.size": 2.5,

        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,

        "xtick.minor.width": 0.4,
        "ytick.minor.width": 0.4,

        "xtick.minor.visible": True,
        "ytick.minor.visible": True,

        # ------------------------------------------------
        # Grid
        # ------------------------------------------------
        "grid.alpha": 0.15,
        "grid.linewidth": 0.5,

        # ------------------------------------------------
        # Lines
        # ------------------------------------------------
        "lines.linewidth": 1.8,
        "lines.markersize": 5,

        # ------------------------------------------------
        # Legend
        # ------------------------------------------------
        "legend.frameon": True,

        # ------------------------------------------------
        # Better scientific default colormap
        # ------------------------------------------------
        "image.cmap": "viridis",
    })