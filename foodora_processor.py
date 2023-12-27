import pandas as pd
import glob
from constants import PRODUCT_LIST, PROVIDER_DICT

# Mapping for Foodora locations
FOODORA_LOCATION_MAP = {
    "Bistro La Paisanita": "Zizkov",
    "La Paisanita Petrovice": "Petrovice",
    "La Paisanita Dejvice": "Dejvice"
}

def process_foodora_data(download_folder):
    pattern = PROVIDER_DICT['Foodora']
    files = glob.glob(f"{download_folder}/{pattern}")
    all_data = []

    for file in files:
        df = pd.read_csv(file)
        # df['Date'] = pd.to_datetime(df['Order Create Datetime'], format='%m/%d/%Y %H:%M').dt.date
        df['Date'] = pd.to_datetime(df['Order Create Datetime'], format='%Y-%m-%d %H:%M:%S').dt.date
        df['Location'] = df['Provider Name'].map(FOODORA_LOCATION_MAP)
        df['Provider'] = 'Foodora'

        # Correct the item names and count the items
        df['Item Name'] = df['Item Name'].replace({
            'ChipÃ¡': 'Chipá',
            'ChampiÃ±ones': 'Champiñones',
            '30 ml': 'Chimichurri chico',
            '12 pcs': 'Chipá'  # Assuming that '12 pcs' refers to double the count for Chipá
        })
        df['Item Amount'] = df['Item Amount'].replace({'12 pcs': 2}).astype(int)

        # Group by Date, Location, and Provider, and sum the Item Amount
        grouped_data = df.groupby(['Date', 'Location', 'Provider', 'Item Name'])['Item Amount'].sum().reset_index()
        
        all_data.append(grouped_data)

    combined_data = pd.concat(all_data)

    return combined_data
