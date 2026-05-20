import matplotlib as mpl
import matplotlib.pyplot as plt

def set_plot_style():
    mpl.rcParams.update({

        # -------------------------------------------------
        # LaTeX / Fonts
        # -------------------------------------------------
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "mathtext.fontset": "cm",

        # -------------------------------------------------
        # Figure
        # -------------------------------------------------
        "figure.figsize": (6.0, 4.0),
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",

        # -------------------------------------------------
        # Axes
        # -------------------------------------------------
        "axes.labelsize": 16,
        "axes.titlesize": 16,
        "axes.linewidth": 1.2,

        # -------------------------------------------------
        # Ticks
        # -------------------------------------------------
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.minor.size": 3,
        "ytick.minor.size": 3,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,

        # -------------------------------------------------
        # Legend
        # -------------------------------------------------
        "legend.fontsize": 12,
        "legend.frameon": True,

        # -------------------------------------------------
        # Lines
        # -------------------------------------------------
        "lines.linewidth": 2.0,
        "lines.markersize": 6,

        # -------------------------------------------------
        # Grid
        # -------------------------------------------------
        "grid.alpha": 0.3,

        # -------------------------------------------------
        # Color cycle
        # -------------------------------------------------
        # Use FlatUI colors for better visibility
        "axes.prop_cycle": plt.cycler(color=[
            "#e74c3c",  # red
            "#3498db",  # blue
            "#2ecc71",  # green
            "#9b59b6",  # purple
            "#f1c40f",  # yellow
            "#e67e22",  # orange
            "#1abc9c",  # turquoise
            "#34495e",  # dark blue-gray
        ]),


    })