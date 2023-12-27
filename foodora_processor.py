import pandas as pd
import glob
from constants import PRODUCT_LIST, PROVIDER_DICT

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
        df['Date'] = pd.to_datetime(df['Order Create Datetime'], format='%Y-%m-%d %H:%M:%S').dt.date
        df['Location'] = df['Provider Name'].map(FOODORA_LOCATION_MAP)
        df['Provider'] = 'Foodora'

        df['Item Name'] = df['Item Name'].replace({
            'ChipÃ¡': 'Chipá',
            'ChampiÃ±ones': 'Champiñones',
            '30 ml': 'Chimichurri chico',
            '12 pcs': 'Chipá'
        })
        df['Item Amount'] = df['Item Amount'].replace({'12 pcs': 2}).astype(int)

        grouped_data = df.groupby(['Date', 'Location', 'Provider', 'Item Name'])['Item Amount'].sum().reset_index()

        pivot_data = grouped_data.pivot_table(
            index=['Date', 'Location', 'Provider'], 
            columns='Item Name', 
            values='Item Amount', 
            fill_value=0
        )
        pivot_data.reset_index(inplace=True)

        for product in PRODUCT_LIST:
            if product not in pivot_data.columns:
                pivot_data[product] = 0

        # Convert all product columns to integers
        pivot_data[PRODUCT_LIST] = pivot_data[PRODUCT_LIST].astype(int)

        all_data.append(pivot_data)

    combined_data = pd.concat(all_data)

    # Reorder columns to match PRODUCT_LIST
    final_columns = ['Date', 'Location', 'Provider'] + PRODUCT_LIST
    combined_data = combined_data[final_columns]

    return combined_data
