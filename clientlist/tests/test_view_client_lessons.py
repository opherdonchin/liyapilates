from django.urls import resolve, reverse

from .test_case_clientlist import ClientListTestCase
from ..models import Client, Lesson
from ..views import client_lessons
from ..forms import ClientLessonsForm

# TODO: Add test for expiration date and num lessons left


class ClientLessonsViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_lessons', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.get(self.url)

    def test_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_found_status_code(self):
        url = reverse('client_lessons', kwargs={'client_slug': self.nonexistent_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_resolves_view(self):
        view = resolve('/client/' + self.client_slug1 + '/lessons/')
        self.assertEquals(view.func, client_lessons)

    def test_contains_button_links(self):
        homepage_url = reverse('home')
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))

    def test_html_data(self):
        self.assertContains(self.response,
                            'Lessons attended')
        self.assertContains(self.response,
                            'Lessons not attended')

    def test_breadcrumbs(self):
        home_url = reverse('home')
        client_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">{1}</a>'
                            .format(client_url, self.client_name1), html=True)

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
        self.assertIsInstance(form, ClientLessonsForm)

    def test_form_inputs(self):
        self.assertContains(self.response, 'class="form-group"', 2)
        self.assertContains(self.response, 'type="checkbox"', Lesson.objects.all().count())


class SuccessfulClientLessonsPostTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_lessons', kwargs={'client_slug': self.client_slug1})
        self.new_lessons_attended = ()
        self.response = self.client.post(self.url, {'lessons_attended': self.new_lessons_attended,
                                                    'lessons_not_attended': self.new_lessons_attended})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.client_slug1}))

    def test_post_edited(self):
        updated_client = Client.objects.get(slug=self.client_slug1)
        self.assertEquals(updated_client.notes, self.client1.lessons.count(), 0)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_lessons', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_form_errors(self):
        self.assertTrue(self.response.context is None)
