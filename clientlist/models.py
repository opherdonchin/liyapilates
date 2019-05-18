from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import MinValueValidator

# Create your models here.


class Card(models.Model):
    card_type = models.CharField(max_length=30, unique=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_lessons = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_valid_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.card_type

# TODO: Return PilatesCLient to Client
class PilatesClient(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=35, default='0', unique=True, primary_key=True)
    added_on = models.DateField(auto_now_add=True)
    joined_on = models.DateField(default=date.today)
    card = models.ForeignKey(Card, on_delete=models.PROTECT, null=True)
    purchased_on = models.DateField(default=date.today)

    def __str__(self):
        return self.name


# TODO: Change type property to full_name in SessionType
class SessionType(models.Model):
    type = models.CharField(max_length=25)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name


class Lesson(models.Model):
    held_at = models.DateTimeField(default=timezone.now, unique=True)
    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    participants = models.ManyToManyField(PilatesClient, related_name='lessons')

    def __str__(self):
        return self.held_at.strftime('%Y-%m-%d %H:%M') + ': ' + self.session_type.short_name
