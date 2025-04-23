from django.db import models
from simple_history.models import HistoricalRecords
from datetime import datetime
from django.core.exceptions import ValidationError

def validate_webp_image(value):
    if not value.name.lower().endswith('.webp'):
        raise ValidationError("Only webp images allowed")

def validate_date_time(timestamp_str):
    try:
        datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        return True
    except ValueError:
        return False


class members_table(models.Model):
    TEAM_CHOICES = [
        ("lead-members", "lead-members"),
        ("data-management-team", "data-management-team"),
        ("regional-representatives", "regional-representatives"),
        ("our-well-wishers", "our-well-wishers"),
        ("website-management-team", "website-management-team"),
        ("our-members", "our-members")
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="members_images/", validators=[validate_webp_image])
    designation = models.CharField(max_length=200)
    about = models.CharField(max_length=400)
    team = models.CharField(max_length=100, choices=TEAM_CHOICES)
    linkedin_url = models.URLField(null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        # rename the image as name_timestamp.webp
        name = self.image.name.split('/')[-1].split('.')[0]
        if (len(name)<=19) or (not validate_date_time(name[-19:])):
            current_datetime = datetime.now()
            timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            self.image.name = self.image.name.replace(name, f"{name}_{timestamp}")
        super().save(*args, **kwargs)


class key_value_table(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return f"{self.key}"
    



