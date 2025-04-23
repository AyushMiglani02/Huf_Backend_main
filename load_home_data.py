import json
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from home.models import testimonial_table, video_table, key_value_table

# Load home.json
def load_home_data(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Load topSearchPage data
    if "topSearchPage" in data and "diseaseList" in data["topSearchPage"]:
        key_value_table.objects.create(
            key="topSearchPage",
            value=", ".join(data["topSearchPage"]["diseaseList"]),
        )

    # Load ourMissionPage data
    if "ourMissionPage" in data:
        our_mission_text = data["ourMissionPage"].get("outMissionText", "")
        youtube_link = data["ourMissionPage"].get("youtubeLink", "")
        key_value_table.objects.create(key="ourMissionText", value=our_mission_text)
        key_value_table.objects.create(key="youtubeLink", value=youtube_link)

    # Load testimonialPage data
    if "testimonialPage" in data and "testimonialList" in data["testimonialPage"]:
        for item in data["testimonialPage"]["testimonialList"]:
            name = item.get("name") or item.get("name")  # Handling potential typo
            testimonial_table.objects.create(
                heading=item["heading"],
                text=item["text"],
                name=name,
                location=item["location"],
            )

    # Load videoPage data
    if "videoPage" in data and "videoList" in data["videoPage"]:
        for item in data["videoPage"]["videoList"]:
            image_data = item.get("imageLink", "")
            image_file = None
            
            if image_data.startswith("data:image/"):
                try:
                    format_str, img_str = image_data.split(",", 1)
                    img_str += "=" * ((4 - len(img_str) % 4) % 4)  # Fix incorrect padding
                    ext = format_str.split("/")[1].split(";")[0]
                    image_file = ContentFile(base64.b64decode(img_str), name=f"{item['heading'].replace(' ', '_')}.webp")
                except Exception as e:
                    print(f"Error decoding image for {item['heading']}: {e}")

            video_table.objects.create(
                heading=item["heading"],
                image=image_file,
                ytplaylist_link=item["ytPlaylistLink"],
            )

    # Load bottomSearchPage data
    if "bottomSearchPage" in data and "text" in data["bottomSearchPage"]:
        key_value_table.objects.create(
            key="bottomSearchPage",
            value=data["bottomSearchPage"]["text"],
        )
    
    print("Home Data Loaded Successfully!")

# Call the function with the JSON file path
load_home_data("home.json")
