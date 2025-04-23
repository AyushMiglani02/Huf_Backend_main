import json
from footer.models import footer_table

# Load Footer.json
with open("Footer.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Load data into footer_table
footer_data = data.get("footer", {})

for key, value in footer_data.items():
    for sub_key, sub_value in value.items():
        footer_table.objects.create(
            key=f"{key}_{sub_key}",
            value=sub_value
        )

print("Footer Data Loaded Successfully!")
