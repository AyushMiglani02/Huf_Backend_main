from django.contrib import admin
from .models import feedback_table

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("feedback", "rating", "average_rating",)
    list_filter = ("rating",)
    readonly_fields = ("average_rating",)

    def average_rating(self, obj):
        return obj.get_average_rating()
    average_rating.short_description = "Average Rating"

admin.site.register(feedback_table, FeedbackAdmin)
