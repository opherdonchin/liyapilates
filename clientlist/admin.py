from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Card, CardType, Client, Lesson, LessonType

admin.site.register(LessonType)
admin.site.register(CardType)


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(ImportExportModelAdmin):
    pass


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    pass
