import pandas as pd
from constants import DOWNLOAD_FOLDER, PRODUCT_LIST
from wolt_processor import process_wolt_data
from bolt_processor import process_bolt_data
from foodora_processor import process_foodora_data
from output_processor import format_and_output

def main():
    # Process data from all providers
    wolt_data = process_wolt_data(DOWNLOAD_FOLDER)
    bolt_data = process_bolt_data(DOWNLOAD_FOLDER)
    foodora_data = process_foodora_data(DOWNLOAD_FOLDER)

    # Combine data from all providers
    combined_data = pd.concat([wolt_data, bolt_data, foodora_data])

    # Ensure all dates, providers, and locations are present
    provider_order = ['Wolt', 'Bolt', 'Foodora']
    location_order = ['Zizkov', 'Dejvice', 'Petrovice']
    dates = combined_data['Date'].unique()

    # Initialize an empty list to store the aggregated data frames
    frames = []

    # Aggregate data for each date, provider, and location
    for date in dates:
        for provider in provider_order:
            for location in location_order:
                group_data = combined_data[
                    (combined_data['Date'] == date) &
                    (combined_data['Provider'] == provider) &
                    (combined_data['Location'] == location)
                ]
                sum_data = group_data[PRODUCT_LIST].sum().astype(int).to_frame().T
                sum_data['Date'] = date
                sum_data['Location'] = location
                sum_data['Provider'] = provider
                frames.append(sum_data)

    # Combine all frames
    aggregated_data = pd.concat(frames, ignore_index=True)

    # Calculate the summary line for each day and append
    summary_data = combined_data.groupby('Date')[PRODUCT_LIST].sum().astype(int).reset_index()
    summary_data['Location'] = 'All Locations'
    summary_data['Provider'] = 'All Providers'
    aggregated_data = pd.concat([aggregated_data, summary_data], ignore_index=True)

    # Reorder columns to have 'Date', 'Location', 'Provider' at the beginning
    col_order = ['Date', 'Location', 'Provider'] + PRODUCT_LIST
    aggregated_data = aggregated_data[col_order]

    # Sort the data
    aggregated_data.sort_values(by=['Date', 'Provider', 'Location'], inplace=True)

    # Format and output the final data
    formatted_data = format_and_output(aggregated_data)

    # Copy the formatted data to clipboard in a tab-delimited format
    formatted_data.to_clipboard(index=False, header=True, sep='\t')
    print(formatted_data)

if __name__ == "__main__":
    main()