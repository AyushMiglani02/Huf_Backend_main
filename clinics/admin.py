from django.contrib import admin
from .models import clinics_table

class ClinicsAdmin(admin.ModelAdmin):
    list_filter = ("show",)
    search_fields = ("name",)

admin.site.register(clinics_table, ClinicsAdmin)
