from django.contrib import admin
from .models import (
    disease_table,
    pathy_table,
    summary_table,
    data_table,
    source_table,
    case_table,
    sex_table,
    book_table,
    whatsapp_table,
)


class DiseaseAdmin(admin.ModelAdmin):
    list_filter = ("show",)
    search_fields = ("name",)


class PathyAdmin(admin.ModelAdmin):
    list_filter = ("disease","show",)
    search_fields = ("name",)


class DataAdmin(admin.ModelAdmin):
    list_display = ("title","pk","pathy","source",)
    list_filter = ("pathy__disease","pathy__name","source","show",)
    search_fields = ("title","pk",)


class SourceAdmin(admin.ModelAdmin):
    search_fields = ("title","pk")


class CaseAdmin(admin.ModelAdmin):
    list_display = ("title","pk",)
    list_filter = ("pathy__disease","pathy__name","show",)
    search_fields = ("pk", "title", "first_name", "last_name")


class SexAdmin(admin.ModelAdmin):
    list_filter = ("show",)


class BookAdmin(admin.ModelAdmin):
    list_display = ("name","author","rating")
    list_filter = ("pathy__disease","pathy__name","show",)
    search_fields = ("name","author",)


class WhatsappAdmin(admin.ModelAdmin):
    list_display = ("pathy",)
    list_filter = ("pathy__disease","pathy__name","show",)
    search_fields = ("pathy__name",)


admin.site.register(disease_table, DiseaseAdmin)
admin.site.register(pathy_table, PathyAdmin)
admin.site.register(summary_table)
admin.site.register(data_table, DataAdmin)
admin.site.register(source_table, SourceAdmin)
admin.site.register(case_table, CaseAdmin)
admin.site.register(sex_table, SexAdmin)
admin.site.register(book_table, BookAdmin)
admin.site.register(whatsapp_table, WhatsappAdmin)
