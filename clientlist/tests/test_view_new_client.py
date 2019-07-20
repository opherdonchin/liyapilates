from django.urls import reverse, resolve
from datetime import date

from .test_case_clientlist import ClientListTestCase
from ..models import Client
from ..views import new_client
from ..forms import NewClientForm


class AddCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('new_client')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_correct_view(self):
        view = resolve('/new_client/')
        self.assertEquals(view.func, new_client)

    def test_contains_breadcrumb_links(self):
        home_url = reverse('home')
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)

    def test_contains_navbar_links(self):
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
        self.assertIsInstance(form, NewClientForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulAddCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('new_client')
        self.new_client_name = 'Jop Bop'
        self.new_client_joined = date.today()
        self.new_client_notes = 'Notes for new client'
        self.response = self.client.post(self.url,
                                         {'name': self.new_client_name,
                                          'joined_on': self.new_client_joined,
                                          'notes': self.new_client_notes})
        self.new_client = Client.objects.get(name=self.new_client_name)

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.new_client.slug}))

    def test_post_edited(self):
        self.assertEquals(self.new_client.name, self.new_client.name)
        self.assertEquals(self.new_client.joined_on, self.new_client_joined)
        self.assertEquals(self.new_client.notes, self.new_client_notes)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('new_client')
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
