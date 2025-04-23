import json
import base64
import os
from django.utils.timezone import now
from ejournal.models import ejournal_table, key_value_table

def save_base64_file(base64_string, file_path):
    """Decodes and saves a base64-encoded file, fixing padding issues."""
    try:
        # Ensure padding is correct
        missing_padding = len(base64_string) % 4
        if missing_padding:
            base64_string += '=' * (4 - missing_padding)

        # Decode and save the file
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(base64_string))
    except Exception as e:
        print(f"Error decoding Base64: {e}")

# Load eJournal.json
with open("eJournal.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Process latest eJournal page text
latest_text = data.get("latestEjournalPage", {}).get("text", "")
key_value_table.objects.update_or_create(key="latest_ejournal_text", defaults={"value": latest_text})

# Process all eJournal page text
all_text = data.get("allEjournalPage", {}).get("text", "")
key_value_table.objects.update_or_create(key="all_ejournal_text", defaults={"value": all_text})

# Process eJournals
for index, ejournal in enumerate(data.get("latestEjournalPage", {}).get("ejournals", [])):
    image_path = f"media/ejournal_docs/cover_images/ejournal_{index + 1}.webp"
    file_path = f"media/ejournal_docs/files/ejournal_{index + 1}.pdf"

    # Save Base64-encoded image and file
    save_base64_file(ejournal["imageLink"].split(",")[-1], image_path)
    save_base64_file(ejournal["fileLink"].split(",")[-1], file_path)

    # Create eJournal entry
    ejournal_table.objects.create(
        name=f"ejournal_{index + 1}",
        image=image_path,
        file=file_path,
        publish_date=now(),
    )

print("E-Journal Data Loaded Successfully!")