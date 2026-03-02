import sys
import os
import matplotlib.pyplot as plt
from textx import metamodel_from_file

from barplot import draw_bar_plot
from pieplot import draw_pie_plot
from common import *

def find_best_plot_type(element):
    """
    Infer best plot type for DefaultPlot.

    Rules:
    - If Values present → PiePlot
    - If YList present → BarPlot
    - If X and Y present:
        - If X looks categorical → BarPlot
        - Else → LinePlot
    - Fallback → LinePlot
    """

    elems = element.elements

    # Check for PiePlot
    values = get_value(elems, "Values", "values", None)
    labels = get_value(elems, "Labels", "labels", None)
    if values is not None:
        return "PiePlot"

    # Check for BarPlot with YList
    y_list = get_value(elems, "YList", "y", None)
    if y_list is not None:
        return "BarPlot"

    # Check for X/Y
    x = get_value(elems, "X", "x", None)
    y = get_value(elems, "Y", "y", None)

    if x is not None and y is not None:
        if isinstance(x, str):
            name = x.lower()
            if any(word in name for word in ["category", "type", "group", "class"]):
                return "BarPlot"

        # Default numeric relation → line plot
        return "LinePlot"

    # If only Y exists → treat as bar
    if y is not None:
        return "BarPlot"

    # Final fallback
    return "LinePlot"

def interpret(model):
    for fig in model.figures:

        rows = get_value(fig.elements, "Rows", "rows", 1)
        cols = get_value(fig.elements, "Cols", "cols", 1)
        size = get_value(fig.elements, "Size", "size", None)
        title = get_value(fig.elements, "Title", "title", None)
        source = get_value(fig.elements, "Source", "source", None)
        output = get_value(fig.elements, "Save", "output", None)

        figsize = (
            float(size.a), float(size.b)
        ) if size else (8, 6)

        df = load_df_localy_or_kaggle(source)

        figure, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = axes.flatten() if rows * cols > 1 else [axes]

        if title:
            figure.suptitle(strip_str(title))

        plot_index = 0

        for element in fig.elements:
            plot_name = element.__class__.__name__
            if plot_name not in ("LinePlot", "BarPlot", "ScatterPlot", "PiePlot", "DefaultPlot"):
                # plot_name = find_best_plot_type(element)
                continue

            ax = axes[plot_index]
            plot_index += 1

            elems = element.elements

            position = get_element(elems, "Position")
            if position:
                idx = (position.position.a - 1) * cols + (position.position.b - 1)
                ax = axes[idx]

            color = strip_str(get_value(elems, "Color", "color", None))
            label = strip_str(get_value(elems, "Label", "label", None))
            grid = to_bool(get_value(elems, "Grid", "grid", None))
            legend = to_bool(get_value(elems, "Legend", "legend", None))

            if plot_name == "DefaultPlot":
                plot_name = find_best_plot_type(element)

            if plot_name == "LinePlot":
                x = resolve_expression(df, get_value(elems, "X", "x", None))
                y = resolve_expression(df, get_value(elems, "Y", "y", None))

                ax.plot(x, y, label=label, color=color)

                xlabel = get_value(elems, "XLabel", "xlabel", None)
                ylabel = get_value(elems, "YLabel", "ylabel", None)

                if xlabel:
                    ax.set_xlabel(strip_str(xlabel))
                if ylabel:
                    ax.set_ylabel(strip_str(ylabel))

            elif plot_name == "BarPlot":
                draw_bar_plot(df, ax, element, color, label)

            elif plot_name == "ScatterPlot":
                x = resolve_expression(df, get_value(elems, "X", "x", None))
                y = resolve_expression(df, get_value(elems, "Y", "y", None))

                ax.scatter(x, y, color=color, label=label)

            elif plot_name == "PiePlot":
                draw_pie_plot(df, ax, element)

            if grid:
                ax.grid()
            
            if legend and label:
                ax.legend()

        plt.tight_layout()

        if output:
            plt.savefig(strip_str(output))
            
        plt.show()


def main():
    mm = metamodel_from_file(os.path.join(os.path.dirname(__file__), "vizz.tx"))
    model = mm.model_from_file(sys.argv[1])
    interpret(model)


if __name__ == "__main__":
    main()