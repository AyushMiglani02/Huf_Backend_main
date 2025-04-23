from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from simple_history.models import HistoricalRecords

class feedback_table(models.Model):
    rating = models.IntegerField(
        validators= [
            MinValueValidator(1, "rating should be greater than or equal to 1"),
            MaxValueValidator(5, "rating should be less than or equal to 5")
        ]
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return f"{self.feedback[:20]}..."
    
    def get_average_rating(self):
        average = feedback_table.objects.all().aggregate(Avg("rating"))["rating__avg"]
        return round(average, 2) if average is not None else None