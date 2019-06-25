from django.urls import resolve, reverse
from django.utils import timezone
from datetime import timedelta

from .test_case_clientlist import ClientListTestCase
from ..views import edit_lesson
from ..models import Lesson, LessonType
from ..forms import EditLessonForm


class EditLessonTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.lesson_pk = self.lesson.pk
        url = reverse('edit_lesson', kwargs={'pk': self.lesson_pk})
        self.response = self.client.get(url)

    def test_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_view(self):
        view = resolve('/lesson/{0}/edit/'.format(self.lesson_pk))
        self.assertEquals(view.func, edit_lesson)

    def test_contains_button_links(self):
        homepage_url = reverse('home')
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))
        self.assertContains(self.response, '<button type="submit"')

    def test_breadcrumbs(self):
        home_url = reverse('home')
        lesson_details_url = reverse('lesson_details', kwargs={'pk': self.lesson_pk})
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">{1:%B %d, %Y at %H:%M}</a>'
                            .format(lesson_details_url, self.lesson.held_at), html=True)

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
        self.assertIsInstance(form, EditLessonForm)

    def test_form_inputs(self):
        num_lesson_types = LessonType.objects.count()

        self.assertContains(self.response, '<input type="hidden"', 1)
        self.assertContains(self.response, '<input type="text" name="held_at"', 1)
        self.assertContains(self.response, '<option', num_lesson_types+1)
        self.assertContains(self.response, '<textarea name="notes"', 1)

    def test_form_iniitialization(self):
        form = self.response.context.get('form')
        self.assertEquals(form.initial['held_at'], self.lesson.held_at)
        self.assertEquals(form.initial['type'], self.lesson.type.pk)
        self.assertEquals(form.initial['notes'], self.lesson.notes)


class SuccessfulLessonDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.lesson_pk = self.lesson.pk
        self.url = reverse('edit_lesson', kwargs={'pk': self.lesson_pk})
        self.new_held_at = timezone.now() + timedelta(days=2)
        self.new_type = self.lesson_type
        self.new_notes = 'New notes'
        self.response = self.client.post(self.url,
                                         {'held_at': self.new_held_at,
                                          'type': self.new_type.pk,
                                          'notes': self.new_notes})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('lesson_details', kwargs={'pk': self.lesson_pk}))

    def test_lesson_created(self):
        lesson = Lesson.objects.get(pk=self.lesson_pk)
        self.assertEquals(lesson.type, self.new_type)
        self.assertEquals(lesson.notes, self.new_notes)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_lesson', kwargs={'pk': self.lesson.pk})
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
