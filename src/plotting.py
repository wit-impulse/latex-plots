import random
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

# import us_cmap
# import custom colormap from us_cmap module
from . import us_cmap

def above_legend_args(ax):
    """
    Returns a dictionary of arguments to place a legend above the plot.
    :param ax: Matplotlib axes object
    :return: Dictionary of legend arguments
    """
    return dict(loc='lower center', bbox_to_anchor=(0.5, 1.0), bbox_transform=ax.transAxes, borderaxespad=0.25)


def add_single_row_legend(ax: matplotlib.pyplot.Axes, title: str, **legend_args):
    """
    Adds a single-row legend to a plot.
    :param ax: Matplotlib axes object
    :param title: Title of the legend
    :param **legend_args: Additional arguments to be passed to the legend function
    """
    # Extracting handles and labels
    try:
        h, l = legend_args.pop('legs')
    except KeyError:
        h, l = ax.get_legend_handles_labels()
    
    # Adding placeholder for title
    ph = mlines.Line2D([], [], color='white')
    handles = [ph] + h
    labels = [title] + l
    
    # Setting number of columns in legend to match number of handles
    legend_args['ncol'] = legend_args.get('ncol', len(handles))
    
    # Creating legend
    leg = ax.legend(handles, labels, **legend_args)
    
    # Adjusting width of legend items
    for vpack in leg._legend_handle_box.get_children()[:1]:
        for hpack in vpack.get_children()[:1]:
            hpack.get_children()[0].set_width(-30)


def filter_duplicate_handles(ax):
    """
    Filters duplicate handles and labels from a plot's legend.
    :param ax: Matplotlib axes object
    :return: Tuple of filtered handles and labels
    """
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    return zip(*unique)


class MaxTickSciFormatter(matplotlib.ticker.Formatter):
    """
    Formatter for log plots that only formats ticks above a certain value.
    """

    def __init__(self, last_tick_value):
        """
        Initializes MaxTickSciFormatter.
        :param last_tick_value: Format all labels with an x/y value equal or above this value.
        """
        super().__init__()
        self.last_tick_value = last_tick_value
        self._sci_formatter = matplotlib.ticker.LogFormatterSciNotation()

    def __call__(self, x, pos=None):
        """
        Formats tick labels.
        :param x: Tick value
        :param pos: Tick position (unused)
        :return: Formatted tick label
        """
        if x >= self.last_tick_value:
            return self._sci_formatter(x, pos)
        else:
            return ''


def get_dimensions(height=140, num_cols=1):
    """
    Calculates the dimensions (in inches) of a plot given its height and number of columns.
    :param height: Height of the plot in points (default 140)
    :param num_cols: Number of columns in the plot (default 1)
    :return: Tuple of width and height in inches
    """
    single_col_pts = 252
    double_col_pts = 516
    inches_per_pt = 1 / 72.27

    if num_cols == 1:
        width_inches = single_col_pts * inches_per_pt + 0.23  # added default matplotlib padding
    elif num_cols == 2:
        width_inches = double_col_pts * inches_per_pt + 0.23
    else:
        width_inches = single_col_pts * num_cols * inches_per_pt + 0.23

    height_inches = height * inches_per_pt
    return width_inches, height_inches


def prepare_matplotlib():
    # Activate the custom US colormap
    us_cmap.activate()

    # Set various parameters for the matplotlib module
    params = {
        'savefig.pad_inches': 0.0,
        'savefig.bbox': 'tight',
        'savefig.transparent': True,
        'font.family': 'Times',
        'font.size': 8,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'axes.titlesize': 8,
        'axes.labelsize': 8,
        'legend.fontsize': 8,
        'figure.titlesize': 8,
        'figure.autolayout': True,
        'axes.labelweight': 'normal',
        'axes.titleweight': 'normal',
        'legend.columnspacing': 0.75,
        'legend.handlelength': 1,
        'legend.handletextpad': 0.2,
        'legend.frameon': False,
        'legend.borderpad': 0
    }

    # Update the matplotlib settings with the specified parameters
    matplotlib.rcParams.update(params)


def prepare_for_latex(preamble=''):
    # If the siunitx package is not in the preamble, add it
    if 'siunitx' not in preamble:
        preamble += '\n' + r'\usepackage{siunitx}'

    # Set various parameters for the matplotlib module
    prepare_matplotlib()

    # Set various parameters for the pgf module (for use with LaTeX)
    params = {
        'backend': 'pgf',
        'text.usetex': True,
        'text.latex.preamble': preamble,
        'pgf.texsystem': 'pdflatex',
        'pgf.rcfonts': False,
        'pgf.preamble': preamble,
        'axes.unicode_minus': False,
    }

    # Update the matplotlib settings with the specified parameters
    matplotlib.rcParams.update(params)

