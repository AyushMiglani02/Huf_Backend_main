from django.contrib import admin
from .models import members_table, key_value_table

class MembersAdmin(admin.ModelAdmin):
    list_display = ("name","team",)
    search_fields = ("name",)
    list_filter = ("show","team")

admin.site.register(members_table, MembersAdmin)
admin.site.register(key_value_table)


