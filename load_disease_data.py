import json
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from disease.models import disease_table, pathy_table, summary_table

# Load Disease.json
with open("Disease.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def decode_base64_image(image_data, name):
    """Ensure proper base64 padding and decode image"""
    image_data = image_data.split(",")[-1]  # Extract actual base64 string
    missing_padding = len(image_data) % 4
    if missing_padding:
        image_data += "=" * (4 - missing_padding)  # Add required padding

    try:
        image_bytes = base64.b64decode(image_data)
        return ContentFile(image_bytes, name=f"{name}.webp")
    except base64.binascii.Error:
        print(f"Error decoding base64 for image: {name}")
        return None

# Decode and save disease image
image_file = decode_base64_image(data["imageLink"], data["disease"])

if image_file:
    # Create disease entry
    disease = disease_table.objects.create(
        name=data["disease"].lower(),  # Ensure lowercase as per validation
        text=data["text"],
        summary=data["summary"],
        image_link=image_file
    )

    # Load pathies
    def create_pathy(pathy_type, pathy_list):
        for pathy in pathy_list:
            pathy_image_file = decode_base64_image(pathy["imageLink"], pathy["name"].lower())
            if pathy_image_file:
                new_pathy = pathy_table.objects.create(
                    disease=disease,
                    name=pathy["name"].lower(),
                    type=pathy_type,
                    image_link=pathy_image_file
                )
                summary_table.objects.create(
                    pathy=new_pathy,
                    summary=pathy["summary"]
                )

    for pathy_type, pathy_list in data["pathies"].items():
        create_pathy(pathy_type, pathy_list)

    print("Disease Data Loaded Successfully!")
else:
    print("Failed to load disease image.")
