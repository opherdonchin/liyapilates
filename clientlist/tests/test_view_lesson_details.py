from django.test import TestCase
from django.urls import resolve, reverse
from datetime import datetime
from ..views import lesson_details
from ..models import Client, SessionType, Lesson


class LessonDetailsTests(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'
    type_name = 'group'

    def setUp(self):
        Client.objects.create(name=self.client_name1,
                              slug=self.client_slug1,
                              card=None)
        SessionType.objects.create(type=self.type_name, short_name=self.type_name)
        Lesson.objects.create(
            held_at=datetime.now(),
            session_type=SessionType.objects.get(type=self.type_name),
        )
        self.lesson = Lesson.objects.get(pk=1)
        url = reverse('lesson_details', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_lesson_details_view_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_lesson_details_not_found_status_code(self):
        url = reverse('lesson_details', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_lesson_details_resolves_lesson_details_view(self):
        view = resolve('/lesson/1/')
        self.assertEquals(view.func, lesson_details)

    def test_lesson_details_view_contains_homepage_link(self):
        homepage_url = reverse('home')
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))
