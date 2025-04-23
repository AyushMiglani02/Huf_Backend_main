from django.contrib import admin
from .models import subscription_table, key_value_table, ejournal_table

class EjournalAdmin(admin.ModelAdmin):
    list_display = ("name","formatted_publish_date",)
    search_fields = ("name","publish_date",)
    list_filter = ("show",)

    def formatted_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y, %H:%M:%S")  # Format the date and time
    formatted_publish_date.short_description = "Publish Date"  # Set column header

class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ("email_address",)
    list_display = ("email_address","send")
    list_filter = ("send",)

admin.site.register(ejournal_table, EjournalAdmin)
admin.site.register(subscription_table, SubscriptionAdmin)
admin.site.register(key_value_table)