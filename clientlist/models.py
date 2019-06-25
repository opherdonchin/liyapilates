from django.db import models
from django.core.validators import MinValueValidator
from django.utils.html import mark_safe
from datetime import date, datetime, timedelta
from markdown import markdown

# Create your models here.


class CardType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_lessons = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_valid_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


# TODO: Add phone number and e-mail to client and add support for class reminders
class Client(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=35, default='0', unique=True, primary_key=True)
    added_on = models.DateField(auto_now_add=True)
    joined_on = models.DateField(default=date.today)
    notes = models.CharField(max_length=4000, blank=True, default='')

    def __str__(self):
        return self.name

    def latest_lesson(self):
        return self.lessons.latest('held_at')

    def get_notes_as_markdown(self):
        return mark_safe(markdown(self.notes, safe_mode='escape'))


class Card(models.Model):
    type = models.ForeignKey(CardType, on_delete=models.PROTECT)
    purchased_on = models.DateField(default=date.today)
    begins_on = models.DateField(default=date.today)
    expires = models.DateField(null=True)
    num_lessons = models.PositiveIntegerField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True,
                               related_name='cards')

    def save(self, *args, **kwargs):
        if not self.expires:
            self.expires = self.default_expiration()
        if not self.num_lessons:
            self.num_lessons = self.type.num_lessons
        super(Card, self).save(*args, **kwargs)

    def default_expiration(self):
        return self.purchased_on + timedelta(days=self.type.num_valid_days)

    @property
    def lessons_used(self):
        return self.client.lessons.filter(held_at__gte=self.begins_on, held_at__lte=self.expires).count()

    @property
    def lessons_left(self):
        return self.num_lessons - self.lessons_used


class LessonType(models.Model):
    name = models.CharField(max_length=25)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name


class Lesson(models.Model):
    held_at = models.DateTimeField(default=datetime.now().replace(microsecond=0, second=0, minute=0), unique=True)
    type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    notes = models.CharField(max_length=4000, blank=True)
    participants = models.ManyToManyField(Client, related_name='lessons')

    def __str__(self):
        return self.held_at.strftime('%Y-%m-%d %H:%M') + ': ' + self.type.short_name
