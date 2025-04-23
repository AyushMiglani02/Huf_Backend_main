from django.contrib import admin
from .models import pathy_table, effective_table

class PathyAdmin(admin.ModelAdmin):
    list_display = ("title", "show",)
    list_filter = ("show",)
    search_fields = ("title",)

class EffectiveAdmin(admin.ModelAdmin):
    list_display = ("name", "pathy","show")
    list_filter = ("show","pathy")
    search_fields = ("name",)

admin.site.register(pathy_table, PathyAdmin)
admin.site.register(effective_table, EffectiveAdmin)
