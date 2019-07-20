from django.urls import resolve, reverse

from .test_case_clientlist import ClientListTestCase
from ..views import lesson_details
from ..models import Client, Lesson
from ..forms import LessonDetailsForm


class LessonDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.lesson_pk = self.lesson.pk
        url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.response = self.client.get(url)

    def test_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_found_status_code(self):
        url = reverse('lesson_details', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_resolves_view(self):
        view = resolve('/lesson/{0}/'.format(self.lesson_pk))
        self.assertEquals(view.func, lesson_details)

    def test_contains_button_links(self):
        homepage_url = reverse('home')
        edit_lesson_url = reverse('edit_lesson', kwargs={'pk': self.lesson_pk})
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))
        self.assertContains(self.response, 'a href="{0}" class="btn'.format(edit_lesson_url))

    def test_html_data(self):
        self.assertContains(self.response, '<th>Held at:</th><td>{0:%A %B %d, %Y at %H:%M}</td>'
                            .format(self.lesson_held_at), html=True)
        self.assertContains(self.response,
                            '<th>Lesson type:</th><td>{0}</td>'.format(self.lesson_type_name), html=True)
        self.assertContains(self.response, '<th>Number of participants:</th><td>{0}</td>'
                            .format(2), html=True)

    def test_breadcrumbs(self):
        home_url = reverse('home')
        lesson_list_url = reverse('lesson_list')
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'.format(home_url),
                            html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Lessons</a>'
                            .format(lesson_list_url), html=True)

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
        self.assertIsInstance(form, LessonDetailsForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', Client.objects.count() + 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulLessonDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.lesson_pk = self.lesson.pk
        self.url = reverse('lesson_details', kwargs={'pk': self.lesson_pk})
        self.new_participants = [self.client1.pk, ]
        self.new_notes = 'New notes'
        self.response = self.client.post(self.url,
                                         {'notes': self.new_notes,
                                          'clients_attending': self.new_participants,
                                          'client_not_attending': []})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('lesson_details',
                                                    kwargs={'pk': self.lesson_pk}))

    def test_lesson_updated(self):
        updated_lesson = Lesson.objects.get(pk=self.lesson_pk)
        self.assertEquals(updated_lesson.notes, self.new_notes)
        updated_participants = list(updated_lesson.participants.all().values_list('pk', flat=True).distinct())
        self.assertEquals(updated_participants, self.new_participants)


