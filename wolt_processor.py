import glob

import pandas as pd

from constants import PRODUCT_LIST, PROVIDER_DICT


def process_wolt_data(download_folder):
    all_data = []
    for location, pattern in PROVIDER_DICT.items():
        if "Wolt" in location:
            files = glob.glob(f"{download_folder}/{pattern}")
            for file in files:
                df = pd.read_csv(file)
                df["Date"] = pd.to_datetime(df["Order placed"], format="%d.%m.%y %H:%M").dt.date
                df["Location"] = location.split("_")[-1]
                df["Provider"] = "Wolt"
                item_counts = df["Items"].apply(process_items)
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
        name = " ".join(word for word in item.split() if word.isalpha() and not word.endswith("CZK"))
        if name in PRODUCT_LIST:
            count = int(item.split("x")[0].strip())
            item_counts[name] += count
    return pd.Series(item_counts)
