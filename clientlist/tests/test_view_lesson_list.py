from django.urls import resolve, reverse
from datetime import datetime

from .test_case_clientlist import ClientListTestCase
from ..views import lesson_list
from ..models import Client, Lesson


class LessonListViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        url = reverse('lesson_list')
        self.response = self.client.get(url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/lesson_list/')
        self.assertEquals(view.func, lesson_list)

    def test_contains_button_links(self):
        home_url = reverse('home')
        new_lesson_url = reverse('new_lesson')
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}" class="btn'.format(new_lesson_url))

    def test_html_data(self):
        self.assertContains(self.response, '<tr>', 2)

        lesson_url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.assertContains(self.response, '<td><a href="{0}">{1:%d/%m/%y}</a></td> \
                    <td><a href="{0}">{1:%A}</a></td> \
                    <td><a href="{0}">{1:%H:%M}</a></td> \
                    <td>{2}</td> \
                    <td>{3}</td>'.format(lesson_url, self.lesson_held_at,
                                         self.lesson_type_short_name, "2"), html=True)

    def test_breadcrumbs(self):
        home_url = reverse('home')
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)

    def test_navbar(self):
        client_list_url = reverse('client_list')
        lesson_list_url = reverse('lesson_list')
        new_lesson_url = reverse('new_lesson')
        new_client_url = reverse('new_client')

        self.assertContains(self.response, '<a class="nav-link" href="{0}">Clients</a>'
                            .format(client_list_url), html=True)
        self.assertContains(self.response, '<a class="nav-link" href="{0}">Lessons</a>'
                            .format(lesson_list_url), html=True)
        self.assertContains(self.response, '<a class="nav-link" href="{0}">Add client</a>'
                            .format(new_client_url), html=True)
        self.assertContains(self.response, '<a class="nav-link" href="{0}">Add lesson</a>'
                            .format(new_lesson_url), html=True)
