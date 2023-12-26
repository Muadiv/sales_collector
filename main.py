import file_reader
import data_processor
import output_formatter
import pyperclip
import os
import glob
from constants import PROVIDER_DICT, DOWNLOAD_FOLDER

def main():
    all_sales_data = []

    # Read and process files from each provider
    for provider, pattern in PROVIDER_DICT.items():
        file_paths = glob.glob(os.path.join(DOWNLOAD_FOLDER, pattern))
        for file_path in file_paths:
            sales_data = file_reader.read_sales_data(file_path, provider)
            if sales_data is not None:
                processed_data = data_processor.process_data(sales_data, provider)
                all_sales_data.append(processed_data)

    # Aggregate all data
    if all_sales_data:
        final_data = data_processor.aggregate_all_data(all_sales_data)

        # Extract unique dates, locations, and providers
        dates = final_data['Date'].unique()
        locations = final_data['Location'].unique()
        providers = final_data['Provider'].unique()

        # Format data for Google Sheets
        formatted_data = output_formatter.format_for_google_sheets(final_data, dates, locations, providers)
        print(formatted_data)

        # Copy to clipboard
        pyperclip.copy(formatted_data)

        print("Sales data processed and copied to clipboard.")
    else:
        print("No sales data found for today.")

if __name__ == "__main__":
    main()
