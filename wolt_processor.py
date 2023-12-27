import pandas as pd
import glob
from constants import PRODUCT_LIST, PROVIDER_DICT

def process_wolt_data(download_folder):
    all_data = []
    for location, pattern in PROVIDER_DICT.items():
        if "Wolt" in location:  # Process only Wolt files
            files = glob.glob(f"{download_folder}/{pattern}")
            for file in files:
                df = pd.read_csv(file)
                df['Date'] = pd.to_datetime(df['Order placed'], format='%d.%m.%y %H:%M').dt.date
                df['Location'] = location.split('_')[-1]  # Extract location from the location key
                df['Provider'] = 'Wolt'

                # Process the items
                item_counts = df['Items'].apply(process_items)

                # Merge the item counts into the DataFrame
                df = pd.concat([df, item_counts], axis=1)
                
                all_data.append(df)

    combined_data = pd.concat(all_data)

    # Specify the columns to group by and sum
    group_columns = ['Date', 'Location', 'Provider'] + PRODUCT_LIST
    processed_data = combined_data[group_columns].groupby(['Date', 'Location', 'Provider']).sum().reset_index()

    return processed_data

def process_items(items_str):
    items = items_str.split(',')
    item_counts = {product: 0 for product in PRODUCT_LIST}
    
    for item in items:
        name = ' '.join(word for word in item.split() if word.isalpha() and not word.endswith('CZK'))
        if name in PRODUCT_LIST:
            count = int(item.split('x')[0].strip())
            item_counts[name] += count

    return pd.Series(item_counts)
