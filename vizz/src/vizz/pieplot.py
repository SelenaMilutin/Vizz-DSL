import pandas as pd

from common import get_value, resolve_expression, strip_str


def draw_pie_plot(df, ax, element):
    elems = element.elements
    max_slice = element.max_slice
    values = get_value(elems, "Values", "values", None)
    labels = get_value(elems, "Labels", "labels", None)
    title = get_value(elems, "Title", "title", None)
    if values is not None:
        data = values.values
    else:
        data = resolve_expression(df, get_value(elems, "X", "x", None))

    if labels is None:

        # Convert to pandas Series for safety
        s = pd.Series(data)

        # If numeric → treat as numeric slices
        if pd.api.types.is_numeric_dtype(s):
            pie_values = s
            pie_labels = None

        # If categorical → count
        else:
            counts = s.value_counts()

            # Limit number of slices
            if len(counts) > max_slice:
                counts = counts.nlargest(max_slice)

            pie_values = counts.values
            pie_labels = counts.index.astype(str)
    else:
        pie_values = data
        pie_labels = [strip_str(l) for l in labels.values]

    ax.pie(
        pie_values,
        labels=pie_labels,
        autopct='%1.1f%%',
        startangle=90
    )

    if title:
        ax.set_title(strip_str(title))