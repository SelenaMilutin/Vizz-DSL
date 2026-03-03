import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def load_kaggle(source):
    api = KaggleApi()
    api.authenticate()
    dataset_dir = "datasets"

    api.dataset_download_files(
        source,
        path=dataset_dir,
        unzip=True
    )

    csv_files = [
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if f.endswith(".csv")
    ]

    csv_path = max(csv_files, key=os.path.getmtime)

    return pd.read_csv(csv_path)



def load_df_localy_or_kaggle(source):
    try:
        return pd.read_csv(strip_str(source)) if source else None
    except:
        return load_kaggle(source)

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
