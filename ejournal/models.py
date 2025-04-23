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


class ejournal_table(models.Model):
    name = models.CharField(max_length=1000, validators=[validate_small_letters])
    image = models.ImageField(upload_to="ejournal_docs/cover_images/", validators=[validate_webp_image])
    file = models.FileField(upload_to="ejournal_docs/files/", validators=[validate_pdf_file])
    show = models.BooleanField(default=True)
    publish_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # rename the image as name_timestamp.webp
        name = self.image.name.split('/')[-1].split('.')[0]
        if (len(name)<=19) or (not validate_date_time(name[-19:])):
            current_datetime = datetime.now()
            timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            self.image.name = self.image.name.replace(name, f"{name}_{timestamp}")

        # rename the file as file_timestamp.pdf
        name = self.file.name.split('/')[-1].split('.')[0]
        if (len(name)<=19) or (not validate_date_time(name[-19:])):
            current_datetime = datetime.now()
            timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            self.file.name = self.file.name.replace(name, f"{name}_{timestamp}")
        super().save(*args, **kwargs)


class subscription_table(models.Model):
    email_address = models.EmailField()
    send = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.email_address


class key_value_table(models.Model):
    key = models.CharField(max_length=1000)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def __str__(self):
        return self.key
