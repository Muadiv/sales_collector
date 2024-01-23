import glob

import pandas as pd

from constants import PRODUCT_LIST, PROVIDER_DICT

FOODORA_LOCATION_MAP = {
    "La Paisanita Restaurant": "Petrovice",
    "La Paisanita Bistro": "Zizkov",
    "La paisanita - Dejvice": "Dejvice",
}


def process_foodora_data(download_folder):
    pattern = PROVIDER_DICT["Foodora"]
    files = glob.glob(f"{download_folder}/{pattern}")
    all_data = []
    for file in files:
        df = pd.read_csv(file)
        if df.empty:
            print(f"Skipping empty file: {file}")
            continue
        df["Order received at"] = df["Order received at"].astype(str)
        df["Date"] = pd.to_datetime(df["Order received at"], format="%m-%d-%Y %H:%M", errors="coerce").dt.date

        # df["Date"] = pd.to_datetime(df["Order received at"], format="%Y-%m-%d %H:%M").dt.date
        df["Location"] = df["Restaurant name"].map(FOODORA_LOCATION_MAP)
        df["Provider"] = "Foodora"
        item_counts = df["Order Items"].apply(process_items)
        df = pd.concat([df, item_counts], axis=1)
        df.dropna(subset=["Date"], inplace=True)
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
