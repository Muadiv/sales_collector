from pathlib import Path

# List of products
PRODUCT_LIST = [
    "Criolla", "Angus", "Cerdo", "Arrabalera", "Pollo", "Jamon y Queso", "Queso", "Humita",
    "Champiñones", "Espinaca", "Criolla Vegana", "Vegetales", "Milonguita", "Hongos", "Chipá",
    "Alfajor Negro", "Alfajor Blanco", "Alfajor Maicena", "Chimichurr chico", "Chimichurr grande"
]

# Dictionary mapping providers to their file name patterns
PROVIDER_DICT = {
    "Wolt_Zizkov": "la-paisanita_purchases_*",
    "Wolt_Petrovice": "la-paisanita-petrovice_purchases_*",
    "Wolt_Dejvice": "la-paisanita-dejvice_purchases_*",
    "Bolt": "orderDetails.csv",
    "Foodora": "*_order_items_report_*",
}

# List of point of sales
POINT_OF_SALES = ["Zizkov", "Dejvice", "Petrovice"]

# Path to the download folder (update as needed)
DOWNLOAD_FOLDER = str(Path.home() / "Downloads")
