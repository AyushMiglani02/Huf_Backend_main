from django.db import models
from simple_history.models import HistoricalRecords
from PIL import Image
from django.core.exceptions import ValidationError
from datetime import datetime
import os

def validate_webp_image(value):
    if not value.name.lower().endswith('.webp'):
        raise ValidationError("Only webp images allowed")
    
def validate_small_letters(value):
    if not value.islower():
        raise ValidationError("Only small letters allowed")

def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")
    
def validate_date_time(timestamp_str):
    try:
        datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        return True
    except ValueError:
        return False


class testimonial_table(models.Model):
    heading = models.CharField(max_length=100, validators=[validate_small_letters])
    text = models.TextField(max_length=1000)
    name = models.CharField(max_length=50, validators=[validate_small_letters])
    location = models.CharField(max_length=100)
    show = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.heading


class video_table(models.Model):
    heading = models.CharField(max_length=50)
    image = models.ImageField(upload_to="video_table_images/", validators=[validate_webp_image])
    ytplaylist_link = models.URLField(max_length=300)
    show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.heading
    
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
    value = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.key
