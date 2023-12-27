import pandas as pd
import pyperclip

def format_and_output(data):
    # Logic to format the data and copy to clipboard
    formatted_data = data  # Apply your formatting here

    # Copy to clipboard and return for printing
    pyperclip.copy(formatted_data.to_string(index=False))
    return formatted_data
