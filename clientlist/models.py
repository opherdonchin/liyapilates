from django.db import models
from datetime import date, datetime, timedelta
from django.core.validators import MinValueValidator

# Create your models here.


class CardType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_lessons = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_valid_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=35, default='0', unique=True, primary_key=True)
    added_on = models.DateField(auto_now_add=True)
    joined_on = models.DateField(default=date.today)
    notes = models.CharField(max_length=4000, blank=True)

    def __str__(self):
        return self.name

    @property
    def latest_lesson(self):
        return self.lessons.latest('held_at')

    @property
    def lessons_left(self):
        if self.card:
            lessons_since_card = self.lessons.filter(held_at__gte=self.card.purchased_on)
            return self.card.num_lessons - lessons_since_card.count()
        else:
            return 0


class Card(models.Model):
    type = models.ForeignKey(CardType, on_delete=models.PROTECT)
    purchased_on = models.DateField(default=date.today)
    begins_on = models.DateField(default=date.today)
    expires = models.DateField(null=True)
    num_lessons = models.PositiveIntegerField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.expires:
            self.expires = self.default_expiration()
        if not self.num_lessons:
            self.num_lessons = self.type.num_lessons
        super(Card, self).save(*args, **kwargs)

    def default_expiration(self):
        return self.purchased_on + timedelta(days=self.type.num_valid_days)

    def lessons_used(self):
        return self.client.lessons.filter(held_at__gte=self.begins_on, recordDate__lte=self.expires)

# TODO: Add lessons_left and expiry_date to Client
# TODO: Maybe add model for PurchasedCard that would be based on Card


# TODO: Change type property to full_name in SessionType
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
