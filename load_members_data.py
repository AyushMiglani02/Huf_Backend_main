import json
from datetime import datetime
from members.models import members_table, key_value_table
from django.core.files.base import ContentFile
import base64
import os

def save_base64_image(base64_string, file_name, folder="members_images"):
    try:
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]
        if ext != "webp":
            raise ValueError("Only webp images allowed")
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{file_name}_{timestamp}.webp"
        file_path = os.path.join(folder, file_name)
        
        image_data = base64.b64decode(imgstr)
        return ContentFile(image_data, name=file_path)
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

# Load Members.json
with open("Members.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Save text in key_value_table
key_value_table.objects.create(
    key="team_description",
    value=data.get("text", "")
)

team_list = data.get("teamList", [])
key_value_table.objects.create(
    key="team_list",
    value=",".join(team_list)
)

# Load team members data
for team in team_list:
    for member in data.get(team, []):
        image_file = save_base64_image(member["imageBase64"], member["name"]) if "imageBase64" in member else None
        
        members_table.objects.create(
            name=member["name"],
            image=image_file,
            designation=member["designation"],
            about=member["about"],
            team=team,
            linkedin_url=member.get("linkedin_url"),
            email_address=member.get("email_address"),
            phone_number=member.get("phone_number"),
            show=member.get("show", True)
        )

print("Members Data Loaded Successfully!")
