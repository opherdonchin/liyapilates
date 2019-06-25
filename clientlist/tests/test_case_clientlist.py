from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from ..models import Client, Card, CardType, Lesson, LessonType


class ClientListTestCase(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'
    nonexistent_slug = 'missing-client'
    client_name2 = 'Joe Blow'
    client_slug2 = 'joe-blow'
    card_type_name = '12 week'
    card_type_price = 480
    card_type_num_lessons = 12
    card_type_num_valid_days = 60
    card_days_left = 10
    card_purchased_on = timezone.now() - timedelta(days=(card_type_num_valid_days - 10))
    card_begins_on = card_purchased_on
    card_expires = card_begins_on + timedelta(days=card_type_num_valid_days)
    card_num_lessons = card_type_num_lessons
    card_days_left2 = 0
    card_purchased_on2 = timezone.now() - timedelta(days=(card_type_num_valid_days + 10))
    card_begins_on2 = card_purchased_on2
    card_expires2 = card_begins_on2 + timedelta(days=card_type_num_valid_days)
    card_num_lessons2 = card_type_num_lessons
    lesson_type_name = 'group pilates'
    lesson_type_short_name = 'group'
    lesson_held_at = timezone.now() - timedelta(days=1)

    def setUp(self):
        super().setUp()
        card_type = CardType.objects.create(name=self.card_type_name,
                                            price=self.card_type_price,
                                            num_lessons=self.card_type_num_lessons,
                                            num_valid_days=self.card_type_num_valid_days)
        self.client1 = Client.objects.create(name=self.client_name1,
                                             slug=self.client_slug1)
        self.client2 = Client.objects.create(name=self.client_name2,
                                             slug=self.client_slug2)
        Card.objects.create(type=card_type,
                            purchased_on=self.card_purchased_on,
                            begins_on=self.card_begins_on,
                            expires=self.card_expires,
                            num_lessons=self.card_num_lessons,
                            client=self.client2)
        Card.objects.create(type=card_type,
                            purchased_on=self.card_purchased_on2,
                            begins_on=self.card_begins_on2,
                            expires=self.card_expires2,
                            num_lessons=self.card_num_lessons2,
                            client=self.client2)
        self.lesson_type = LessonType.objects.create(name=self.lesson_type_name,
                                                short_name=self.lesson_type_short_name)
        self.lesson = Lesson.objects.create(held_at=self.lesson_held_at,
                                            type=self.lesson_type)
        self.lesson.participants.add(self.client1, self.client2)
