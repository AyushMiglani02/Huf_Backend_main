from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from datetime import datetime

def validate_small_letters(value):
    if not value.islower():
        raise ValidationError("Only small letters allowed")
    
def validate_no_space(value):
    if ' ' in str(value):
        raise ValidationError("Spaces not allowed, if some tag contains space then use _ instead")

def validate_date_time(timestamp_str):
    try:
        datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        return True
    except ValueError:
        return False

def validate_webp_image(value):
    if not value.name.lower().endswith('.webp'):
        raise ValidationError("Only webp images allowed")

class clinics_table(models.Model):
    name = models.CharField(max_length=2000)
    image = models.ImageField(upload_to="clinics_images/", validators=[validate_webp_image])
    summary = models.TextField()
    location = models.CharField(max_length=2000, validators=[validate_small_letters])
    address = models.CharField(max_length=2000, null=True)
    locationLink = models.URLField(null=True)
    contact = models.CharField(max_length=200)
    tags = models.TextField(validators=[validate_small_letters, validate_no_space])
    show = models.BooleanField(default=True)
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
        super().save(*args, **kwargs)