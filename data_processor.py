import pandas as pd

def process_data(sales_data, provider):
    if provider == "Wolt":
        # Process Wolt data
        sales_data = sales_data.dropna(subset=["Items"])
        sales_data["Items"] = sales_data["Items"].apply(parse_wolt_items)
    elif provider == "Foodora":
        # Process Foodora data
        sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%Y-%m-%d %H:%M:%S')
        sales_data = sales_data.rename(columns={"Item Name": "Product", "Item Amount": "Quantity"})    
    elif provider == "Bolt":
        # Process Bolt data
        #sales_data['Fecha del pedido'] = pd.to_datetime(sales_data['Fecha del pedido'], format='%Y-%m-%d %H:%M')
        sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%Y-%m-%d %H:%M')

        sales_data = sales_data.rename(columns={"Nombre del local": "Location", "Artículos": "Items"})
        sales_data['Location'] = sales_data['Location'].apply(map_bolt_location)
        sales_data["Items"] = sales_data["Items"].apply(parse_bolt_items)


    return sales_data


def map_bolt_location(local_name):
    location_map = {
        "La Paisanita Restaurant": "Petrovice",
        "La Paisanita Bistro": "Zizkov",
        "La paisanita - Dejvice": "Dejvice"
    }
    return location_map.get(local_name, "Unknown")

def parse_wolt_items(item_string):
    # Correct encoding issues
    item_string = item_string.encode('latin1').decode('utf-8')

    # Split the string by commas to separate each item
    items = item_string.split(', ')
    parsed_items = {}
    for item in items:
        quantity, *product_parts = item.split('x')
        product_name = ' '.join(product_parts).strip()

        # Handle different options for products like Chipa
        if "Chipa" in product_name:
            product_name = handle_chipa_options(product_name)

        parsed_items[product_name] = int(quantity)
    return parsed_items

def parse_bolt_items(item_string):
    # Split the string by commas to separate each item
    items = item_string.split(', ')
    parsed_items = {}
    for item in items:
        parts = item.split(' ')
        quantity = int(parts[0])  # The first part is always the quantity

        # Handle different formats of product names
        if 'x' in item:
            # Format like "1 Chimichurri x 30ml"
            product_name = ' '.join(parts[1:parts.index('x')])
        elif '|' in item:
            # Format like "2 Criolla Vegana | 120 g"
            product_name = ' '.join(parts[1:parts.index('|')])
        else:
            # Other formats
            product_name = ' '.join(parts[1:])

        # Special handling for Chipa
        if "Chipá x 12" in product_name:
            product_name = "Chipa"
            quantity *= 2  # Count as double
        elif "Chipá x 6" in product_name:
            product_name = "Chipa"

        # Add other special cases as needed

        parsed_items[product_name] = parsed_items.get(product_name, 0) + quantity
    return parsed_items


def aggregate_all_data(all_sales_data):
    # Placeholder for aggregation logic
    return pd.concat(all_sales_data, ignore_index=True)

def handle_chipa_options(product_name):
    # Logic to handle different options for products like Chipa
    # Example: You can add logic to differentiate between 6 pieces and 12 pieces
    # This is a placeholder function, adjust it based on your specific needs
    return product_name