from django.contrib import admin
from .models import footer_table
# Register your models here.
class FooterAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

admin.site.register(footer_table, FooterAdmin)