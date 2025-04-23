import json
from pathy.models import pathy_table, effective_table

# Load Pathy.json
with open("Pathy.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Load data into pathy_table and effective_table
for item in data.get("pathyList", []):
    pathy = pathy_table.objects.create(
        title=item["title"],
        text=item["text"],
        image=item["imageLink"],
    )

    for disease in item.get("diseaseList", []):
        effective_table.objects.create(
            pathy=pathy,
            name=disease["disease"],
            link=disease["link"],
        )

print("Pathy Data Loaded Successfully!")


