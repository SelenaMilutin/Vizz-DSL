import pandas as pd

from common import get_value, resolve_expression


def draw_bar_plot(df, ax, element, color, label):
    elems = element.elements
    try:
        max_bars = element.max_bars
    except:
        max_bars = None
    x = resolve_expression(df, get_value(elems, "X", "x", None))
    y = resolve_expression(df, get_value(elems, "Y", "y", None))
    if y is None:
        y_list = get_value(elems, "YList", "y", None)
        y = y_list.values
    if max_bars and x is not None and pd.api.types.is_numeric_dtype(x):
        x, y = handle_numeric_x(x, y, max_bars)
    
    elif max_bars and x is not None:
        x, y = handle_label_x(x, y, max_bars)

    ax.bar(
                    x if x is not None else range(len(y)),
                    y,
                    label=label,
                    color=color
                )

def handle_label_x(x, y, max_bars):
    grouped = (
            pd.DataFrame({"x": x, "y": y})
            .groupby("x")["y"]
            .mean()
        )

        # If too many labels → keep top 10 most frequent
    label_counts = x.value_counts()
    if len(label_counts) > max_bars:
        top_labels = label_counts.nlargest(max_bars).index
        grouped = grouped.loc[grouped.index.isin(top_labels)]

    x = grouped.index.astype(str)
    y = grouped.values
    return x,y

def handle_numeric_x(x, y, max_bars):
    unique_values = x.nunique()

    if unique_values > max_bars:
        bins = max_bars

                        # Create bins
        x_binned = pd.cut(x, bins=bins)

                        # Aggregate y by bins (mean)
        grouped = pd.DataFrame({"x": x_binned, "y": y}) \
                                    .groupby("x")["y"] \
                                    .mean()

        x = grouped.index.astype(str)
        y = grouped.values
    return x,y

