# Sales Data Processor for Food Delivery Services

## Overview
This project is a Python-based solution for processing and analyzing sales data from various food delivery service providers, including Wolt, Bolt, and Foodora. The script reads CSV files from these providers, processes the data to extract meaningful insights, and outputs a summary of sales data, organized by date, provider, and location.

## Features
- **Data Aggregation**: Combines sales data from multiple providers.
- **Data Processing**: Processes and cleans data to a uniform format.
- **Summary Generation**: Generates a daily summary of sales data.
- **Clipboard Export**: Exports processed data to the clipboard for easy pasting into spreadsheet applications.
- **File Management**: Automatically deletes source CSV files after successful processing to maintain a clean workspace.

## Getting Started
To use this project, clone the repository to your local machine and ensure you have Python installed. Place your CSV data files from Wolt, Bolt, and Foodora in the designated download folder.

### Prerequisites
- Python 3.x
- Pandas library

### Installation
Clone the repository using:
```
git clone https://github.com/Muadiv/sales_collector.git
```
Install the required dependencies:
```
pip install pandas
```

## Usage
Run the main script to process the data:
```
python main.py
```
After successful execution, the script will print the processed data to the console and copy it to the clipboard. The source CSV files will be deleted afterward.

## Contributing
Contributions to this project are welcome! Whether it's improving the code, adding new features, or fixing bugs, your input is valued.

To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is open source and available under the [Apache 2.0].

## Contact
For any queries or further assistance, please reach out to me 😁.
