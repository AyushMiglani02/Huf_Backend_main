import os

# List of required JSON files
json_files = [
    "Pathy.json",
    "Clinics.json",
    "Feedback.json",
    "Members.json",
    "Share experience.json",
    "Ask suggestion.json"
]

# Create each JSON file
for file in json_files:
    with open(file, "w", encoding="utf-8") as f:
        f.write("{}")  # Empty JSON object

print("All JSON files have been created successfully!")
