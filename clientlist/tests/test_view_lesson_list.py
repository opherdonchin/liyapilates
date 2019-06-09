from django.test import TestCase
from django.urls import resolve, reverse
from datetime import datetime
from ..views import lesson_list
from ..models import Client, Lesson, SessionType


class LessonListViewTests(TestCase):
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
        url = reverse('lesson_list')
        self.response = self.client.get(url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_lesson_list_url_resolves_lesson_list_view(self):
        view = resolve('/lesson_list/')
        self.assertEquals(view.func, lesson_list)

    def test_lesson_list_view_contains_lesson_link(self):
        lesson_details_url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.assertContains(self.response, 'href="{0}"'.format(lesson_details_url))

    def test_lesson_list_view_contains_homepage_link(self):
        homepage_url = reverse('home')
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))
