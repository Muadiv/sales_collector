import glob
import os
import traceback

import pandas as pd

from bolt_processor import process_bolt_data
from constants import DOWNLOAD_FOLDER, PROVIDER_DICT
from foodora_processor import process_foodora_data
from wolt_processor import process_wolt_data


def delete_provider_files(download_folder):
    for pattern in PROVIDER_DICT.values():
        for file in glob.glob(f"{download_folder}/{pattern}"):
            os.remove(file)
            print(f"Deleted file: {file}")


def main():
    try:
        # Process data from all providers
        wolt_data = process_wolt_data(DOWNLOAD_FOLDER)
        bolt_data = process_bolt_data(DOWNLOAD_FOLDER)
        foodora_data = process_foodora_data(DOWNLOAD_FOLDER)

        # Combine data from all providers
        combined_data = pd.concat([wolt_data, bolt_data, foodora_data])

        # Sort and process the combined data
        combined_data.sort_values(by=["Date", "Provider", "Location"], inplace=True)
        daily_summary = combined_data.groupby((["Date", "Location"])).sum().reset_index()
        # daily_summary["Location"] = "All Locations"
        daily_summary["Provider"] = "All Providers"
        final_data = pd.concat([combined_data, daily_summary])
        final_data.sort_values(by=["Date", "Provider", "Location"], inplace=True)

        # Format and output the final data
        formatted_data = final_data.to_string(index=False)
        print(formatted_data)

        # Copy the formatted data to clipboard in a tab-delimited format
        final_data.to_clipboard(index=False, header=False, sep="\t")

        # Delete the provider files after successful processing
        # delete_provider_files(DOWNLOAD_FOLDER)

    except Exception:
        print(f"An error occurred:\n {traceback.format_exc()}")


if __name__ == "__main__":
    main()
