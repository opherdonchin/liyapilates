from django.urls import resolve, reverse
from django.utils import timezone
from datetime import timedelta

from .test_case_clientlist import ClientListTestCase
from ..views import new_lesson
from ..models import Client, Lesson, LessonType
from ..forms import NewLessonForm


class LessonDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.lesson_pk = self.lesson.pk
        url = reverse('new_lesson')
        self.response = self.client.get(url)

    def test_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_view(self):
        view = resolve('/new_lesson/')
        self.assertEquals(view.func, new_lesson)

    def test_contains_button_links(self):
        homepage_url = reverse('home')
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))

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

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewLessonForm)

    def test_form_inputs(self):
        num_lesson_types = LessonType.objects.count()
        num_participants = Client.objects.count()

        self.assertContains(self.response, '<input type="hidden"', 1)
        self.assertContains(self.response, '<input type="text" name="held_at"', 1)
        self.assertContains(self.response, '<option', num_lesson_types+1)
        self.assertContains(self.response, '<textarea name="notes"', 1)
        self.assertContains(self.response, '<input type="checkbox"', num_participants)


class SuccessfulLessonDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('new_lesson')
        self.new_held_at = timezone.now() + timedelta(days=2)
        self.new_type = self.lesson_type
        self.new_participants = [self.client_slug1, ]
        self.new_notes = 'New notes'
        self.response = self.client.post(self.url,
                                         {'held_at': self.new_held_at,
                                          'type': self.new_type.pk,
                                          'notes': self.new_notes,
                                          'participants': self.new_participants})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('lesson_list'))

    def test_lesson_created(self):
        lesson = Lesson.objects.get(held_at=self.new_held_at)
        self.assertTrue(lesson)
        self.assertEquals(lesson.type, self.new_type)
        self.assertEquals(lesson.notes, self.new_notes)
        new_participants = list(lesson.participants.all().values_list('slug', flat=True).distinct())
        self.assertEquals(new_participants, self.new_participants)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('new_lesson')
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
