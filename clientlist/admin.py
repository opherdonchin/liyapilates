from django.contrib import admin

# Register your models here.
from .models import Card, PilatesClient, Lesson, SessionType
admin.site.register(Card)
admin.site.register(PilatesClient)
admin.site.register(Lesson)
admin.site.register(SessionType)
