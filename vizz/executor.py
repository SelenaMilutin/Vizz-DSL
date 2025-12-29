import pandas as pd
import matplotlib.pyplot as plt


def execute(model):
    for fig in model.figures:
        df = pd.read_csv(fig.source.strip('"'))

        figsize = (float(fig.size.a), float(fig.size.b))
        figure, axes = plt.subplots(fig.rows, fig.cols, figsize=figsize)

        axes = axes.flatten() if fig.rows * fig.cols > 1 else [axes]
        figure.suptitle(fig.title.strip('"'))

        for plot in fig.plots:
            ax = axes[(plot.position.a - 1) * fig.cols + (plot.position.b - 1)]

            if plot.__class__.__name__ == "LinePlot":
                x = resolve_expression(df, plot.x)
                y = resolve_expression(df, plot.y)
                ax.plot(x, y, label=plot.label.strip('"'), color=plot.color.strip('"'))
                ax.set_xlabel(plot.xlabel.strip('"'))
                ax.set_ylabel(plot.ylabel.strip('"'))
                if plot.grid:
                    ax.grid()
                if plot.legend:
                    ax.legend()

            elif plot.__class__.__name__ == "BarPlot":
                x = resolve_expression(df, plot.x)
                ax.bar(x, plot.y.values,
                       label=plot.label.strip('"'),
                       color=plot.color.strip('"'))
                if plot.legend:
                    ax.legend()

            elif plot.__class__.__name__ == "ScatterPlot":
                x = resolve_expression(df, plot.x)
                y = resolve_expression(df, plot.y)

                ax.scatter(x, y,
                        color=plot.color.strip('"'),
                        label=plot.label.strip('"'))

                if to_bool(plot.grid):
                    ax.grid()

                ax.legend()

            elif plot.__class__.__name__ == "PiePlot":
                ax.pie(
                    plot.values.values,
                    labels=[l.strip('"') for l in plot.labels.values],
                    autopct='%1.1f%%',
                    startangle=90
                )
                ax.set_title(plot.title.strip('"'))

        plt.tight_layout()
        plt.savefig(fig.output.strip('"'))
        plt.show()


def resolve_expression(df, expr):
    if isinstance(expr, str):
        if "." in expr:
            column = expr.split(".")[1]
        else:
            column = expr

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in CSV")

        return df[column]

    return expr

def to_bool(val):
    return val == "true"
