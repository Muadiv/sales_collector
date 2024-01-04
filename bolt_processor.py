import glob

import pandas as pd

from constants import PRODUCT_LIST, PROVIDER_DICT

BOLT_LOCATION_MAP = {
    "La Paisanita Restaurant": "Petrovice",
    "La Paisanita Bistro": "Zizkov",
    "La paisanita - Dejvice": "Dejvice",
}


def process_bolt_data(download_folder):
    pattern = PROVIDER_DICT["Bolt"]
    files = glob.glob(f"{download_folder}/{pattern}")
    all_data = []
    for file in files:
        df = pd.read_csv(file)
        if df.empty:
            print(f"Skipping empty file: {file}")
            continue
        df["Date"] = pd.to_datetime(df["Fecha del pedido"], format="%Y-%m-%d %H:%M").dt.date
        df["Location"] = df["Nombre del local"].map(BOLT_LOCATION_MAP)
        df["Provider"] = "Bolt"
        item_counts = df["Artículos"].apply(process_items)
        df = pd.concat([df, item_counts], axis=1)
        df = df[["Date", "Location", "Provider"] + PRODUCT_LIST]
        df.fillna(0, inplace=True)
        all_data.append(df)
    combined_data = pd.concat(all_data).groupby(["Date", "Location", "Provider"]).sum().reset_index()
    return combined_data


def process_items(items_str):
    items = items_str.split(",")
    item_counts = {product: 0 for product in PRODUCT_LIST}
    for item in items:
        name = " ".join(word for word in item.split() if word.isalpha())
        if name in PRODUCT_LIST:
            count = get_count(item, name)
            item_counts[name] += count
    return pd.Series(item_counts)


def get_count(item_str, product_name):
    if "Chipá x 12" in item_str:
        return 2 if product_name == "Chipá" else 0
    if "Chipá x 6" in item_str:
        return 1 if product_name == "Chipá" else 0
    try:
        count = int("".join(filter(str.isdigit, item_str.split("x")[0])))
    except ValueError:
        count = 0
    return count
