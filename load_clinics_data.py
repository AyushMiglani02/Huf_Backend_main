import json
from clinics.models import clinics_table

# Load clinics data from JSON
with open("Clinics.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Load data into clinics_table
for clinic in data.get("clinicsList", []):
    clinics_table.objects.create(
        name=clinic["name"],
        image=clinic["imageLink"],
        location=clinic["location"],
        address=clinic["address"],
        locationLink=clinic.get("LocationLink"),  # Handle optional field
        summary=clinic["summary"],
        contact=clinic["contact"],
        tags="_".join(clinic["tagList"]).lower(),  # Convert list to a single string with underscores
    )

print("Clinics Data Loaded Successfully!")
