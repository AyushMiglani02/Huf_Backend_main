import json
from user_forms.models import join_us_table  # Adjust the import path as per your project structure
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def load_join_us_data(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create and save the join_us_table entry
    join_us_entry = join_us_table(
        name=data["name"],
        age=int(data["age"]),
        gender=data["gender"],
        email_address=data["email_address"],
        phone_number=data["phone_number"],
        address=data["address"],
        pincode=data["pincode"],
        city=data["city"],
        state=data["state"],
        country=data["country"],
        profession=data["profession"],
        message=data["message"],
    )

    # Handle file uploads
    if "photograph" in data:
        photo_path = f"join_us/images/{data['photograph']}"
        with default_storage.open(photo_path, "rb") as photo_file:
            join_us_entry.photograph.save(data["photograph"], ContentFile(photo_file.read()), save=False)

    if "document" in data:
        doc_path = f"join_us/documents/{data['document']}"
        with default_storage.open(doc_path, "rb") as doc_file:
            join_us_entry.document.save(data["document"], ContentFile(doc_file.read()), save=False)

    join_us_entry.save()
    print("Join Us Data Loaded Successfully!")

# Call the function with the JSON file path
load_join_us_data("JoinUs.json")