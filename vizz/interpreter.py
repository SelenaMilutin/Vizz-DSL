import sys
import pandas as pd
import matplotlib.pyplot as plt
from textx import metamodel_from_file

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

        df = pd.read_csv(strip_str(source)) if source else None

        figure, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = axes.flatten() if rows * cols > 1 else [axes]

        if title:
            figure.suptitle(strip_str(title))

        plot_index = 0

        for element in fig.elements:
            if element.__class__.__name__ not in ("LinePlot", "BarPlot", "ScatterPlot", "PiePlot"):
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

            if element.__class__.__name__ == "LinePlot":
                x = resolve_expression(df, get_value(elems, "X", "x", None))
                y = resolve_expression(df, get_value(elems, "Y", "y", None))

                ax.plot(x, y, label=label, color=color)

                xlabel = get_value(elems, "XLabel", "xlabel", None)
                ylabel = get_value(elems, "YLabel", "ylabel", None)

                if xlabel:
                    ax.set_xlabel(strip_str(xlabel))
                if ylabel:
                    ax.set_ylabel(strip_str(ylabel))

            elif element.__class__.__name__ == "BarPlot":
                x = resolve_expression(df, get_value(elems, "X", "x", None))
                y_list = get_value(elems, "YList", "y", None)

                ax.bar(
                    x if x is not None else range(len(y_list.values)),
                    y_list.values,
                    label=label,
                    color=color
                )

            elif element.__class__.__name__ == "ScatterPlot":
                x = resolve_expression(df, get_value(elems, "X", "x", None))
                y = resolve_expression(df, get_value(elems, "Y", "y", None))

                ax.scatter(x, y, color=color, label=label)

            elif element.__class__.__name__ == "PiePlot":
                values = get_value(elems, "Values", "values", None)
                labels = get_value(elems, "Labels", "labels", None)
                title = get_value(elems, "Title", "title", None)

                ax.pie(
                    values.values,
                    labels=[strip_str(l) for l in labels.values] if labels else None,
                    autopct='%1.1f%%',
                    startangle=90
                )

                if title:
                    ax.set_title(strip_str(title))

            if grid:
                ax.grid()
            
            if legend and label:
                ax.legend()

        plt.tight_layout()

        if output:
            plt.savefig(strip_str(output))
            
        plt.show()

def get_element(elements, cls_name):
    for el in elements:
        if el.__class__.__name__ == cls_name:
            return el
    return None

def get_value(elements, cls_name, attr, default=None):
    el = get_element(elements, cls_name)
    return getattr(el, attr) if el else default

def strip_str(val):
    return val.strip('"') if isinstance(val, str) else val

def to_bool(val, default=False):
    if val is None:
        return default

    if isinstance(val, bool):
        return val

    if isinstance(val, str):
        return val.lower() == "true"

    return default

def resolve_expression(df, expr):
    if expr is None:
        return None

    if isinstance(expr, str):
        name = expr.split(".")[-1]
    else:
        name = expr.id

    if name not in df.columns:
        raise ValueError(f"Column '{name}' not found in CSV")

    return df[name]

def main():
    mm = metamodel_from_file("vizz.tx")
    model = mm.model_from_file(sys.argv[1])
    interpret(model)


if __name__ == "__main__":
    main()
