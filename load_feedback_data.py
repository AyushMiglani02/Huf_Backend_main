import json
from feedback.models import feedback_table

# Load feedback data from JSON
with open("Feedback.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Create a new entry in feedback_table
feedback_entry = feedback_table.objects.create(
    rating=int(data["rating"]),
    feedback=data["feedback"],
)

print("Feedback Data Loaded Successfully!")
