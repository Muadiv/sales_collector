import pandas as pd
import glob
import os

def read_sales_data(file_path, provider):
    files = glob.glob(file_path)
    all_data = []

    for file in files:
        if "Wolt" in provider:
            df = pd.read_csv(file, encoding='utf-8', usecols=["Order placed", "Items"])
            df.rename(columns={"Order placed": "Date"}, inplace=True)
            df['Provider'] = 'Wolt'
            df['Location'] = extract_location_from_filename(os.path.basename(file), provider)
        elif provider == "Foodora":
            df = pd.read_csv(file, encoding='utf-8', usecols=["Order Create Datetime", "Provider Name", "Item Name", "Item Amount"])
            df.rename(columns={"Order Create Datetime": "Date", "Item Name": "Items"}, inplace=True)
            df['Location'] = df['Provider Name'].apply(map_foodora_location)
            df['Provider'] = 'Foodora'
        elif provider == "Bolt":
            df = pd.read_csv(file, encoding='utf-8', usecols=["Fecha del pedido", "Nombre del local", "Artículos"])
            df.rename(columns={"Fecha del pedido": "Date", "Nombre del local": "Location", "Artículos": "Items"}, inplace=True)
            df['Provider'] = 'Bolt'
        else:
            continue

        processed_df = process_file(df, provider)
        all_data.append(processed_df)

    return pd.concat(all_data, ignore_index=True) if all_data else None

def extract_location_from_filename(filename, provider):
    # Logic to extract location from filename based on provider
    if "Zizkov" in provider:
        return "Zizkov"
    elif "Petrovice" in provider:
        return "Petrovice"
    elif "Dejvice" in provider:
        return "Dejvice"
    return "Unknown"

def map_foodora_location(provider_name):
    location_map = {
        "Bistro La Paisanita": "Zizkov",
        "La Paisanita Petrovice": "Petrovice",
        "La Paisanita Dejvice": "Dejvice"
    }
    return location_map.get(provider_name, "Unknown")

def process_file(df, provider):
    # Implement any specific processing needed for each provider's file
    return df
