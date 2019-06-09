from django.contrib import admin

# Register your models here.
from .models import Card, CardType, Client, Lesson, LessonType
admin.site.register(Card)
admin.site.register(Client)
admin.site.register(Lesson)
admin.site.register(LessonType)
admin.site.register(CardType)
