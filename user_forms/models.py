from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

def validate_jpg_jpeg_png_image(value):
    if not (value.name.lower().endswith('.jpg') or value.name.lower().endswith('.jpeg') or value.name.lower().endswith('.png')):
        raise ValidationError("Only jpg, jpeg and png images allowed.")

def validate_date_time(timestamp_str):
    try:
        datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        return True
    except ValueError:
        return False
    
def validate_pdf_file(value):
    if value and (not value.name.lower().endswith('.pdf')):
        raise ValidationError("Only PDF files are allowed.")

class join_us_table(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[
        MinValueValidator(0, "Age can not be negative"),
        MaxValueValidator(200, "Age can't be greater than 200")
    ])
    gender = models.CharField(max_length=200)
    email_address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200)
    pincode = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    profession = models.CharField(max_length=300)
    message = models.TextField()
    photograph = models.ImageField(upload_to="join_us/images/", validators=[validate_jpg_jpeg_png_image])
    document = models.FileField(upload_to="join_us/documents/", validators=[validate_pdf_file])
    email_verfied = models.BooleanField(default=False)
    identity_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def save(self, *args, **kwargs):
        # rename the image as name_timestamp.jpg
        name = self.photograph.name.split('/')[-1].split('.')[0]
        if (len(name)<=19) or (not validate_date_time(name[-19:])):
            current_datetime = datetime.now()
            timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            self.photograph.name = self.photograph.name.replace(name, f"{name}_{timestamp}")

        # rename the document as name_timestamp.pdf
        name = self.document.name.split('/')[-1].split('.')[0]
        if (len(name)<=19) or (not validate_date_time(name[-19:])):
            current_datetime = datetime.now()
            timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            self.document.name = self.document.name.replace(name, f"{name}_{timestamp}")
        super().save(*args, **kwargs)

# class join_us_otp_table(models.Model):
#     join_us = models.ForeignKey(join_us_table, on_delete=models.CASCADE)
#     email_address = models.EmailField()
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at =  models.DateTimeField(null=True)

#     class Meta:
#         ordering = ["-created_at"]  # ordered by decending timestamp
    
#     def save(self, *args, **kwargs):
#         self.expires_at = datetime.now() + timedelta(minutes=15)
#         super().save(*args, **kwargs)

class share_experience_table(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[
        MinValueValidator(0, "Age can not be negative"),
        MaxValueValidator(200, "Age can't be greater than 200")
    ])
    gender = models.CharField(max_length=200)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email_address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    disease = models.CharField(max_length=500, null=True, blank=True)
    pathies = models.TextField(null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    experience = models.TextField()
    show_name = models.BooleanField(default=False)
    preferred_communication = models.CharField(max_length=100, null=True, blank=True)
    reports = models.FileField(upload_to="share_experience/", validators=[validate_pdf_file], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def save(self, *args, **kwargs):
        # rename the document as name_timestamp.pdf if exists
        if self.reports:
            name = self.reports.name.split('/')[-1].split('.')[0]
            if (len(name)<=19) or (not validate_date_time(name[-19:])):
                current_datetime = datetime.now()
                timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
                self.reports.name = self.reports.name.replace(name, f"{name}_{timestamp}")
        super().save(*args, **kwargs)


class ask_suggestion_table(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[
        MinValueValidator(0, "Age can not be negative"),
        MaxValueValidator(200, "Age can't be greater than 200")
    ])
    gender = models.CharField(max_length=200)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email_address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    disease = models.CharField(max_length=500, null=True, blank=True)
    pathies = models.TextField(null=True, blank=True)
    query = models.TextField()
    show_study = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    reports = models.FileField(upload_to="ask_suggestion/", validators=[validate_pdf_file], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]  # ordered by decending timestamp

    def save(self, *args, **kwargs):
        # rename the document as name_timestamp.pdf if exists
        if self.reports:
            name = self.reports.name.split('/')[-1].split('.')[0]
            if (len(name)<=19) or (not validate_date_time(name[-19:])):
                current_datetime = datetime.now()
                timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
                self.reports.name = self.reports.name.replace(name, f"{name}_{timestamp}")
        super().save(*args, **kwargs)