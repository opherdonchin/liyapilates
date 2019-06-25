from django.urls import reverse, resolve

from .test_case_clientlist import ClientListTestCase
from ..models import Client
from ..views import edit_client
from ..forms import EditClientForm


class EditClientViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_client', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_correct_view(self):
        view = resolve('/client/{0}/edit'.format(self.client_slug1))
        self.assertEquals(view.func, edit_client)

    def test_contains_breadcrumb_links(self):
        home_url = reverse('home')
        edit_client_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">{1}</a>'
                            .format(edit_client_url, self.client_name1), html=True)

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
        self.assertIsInstance(form, EditClientForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulEditClientViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_client', kwargs={'client_slug': self.client_slug1})
        self.new_name = 'Jake Blake'
        self.new_notes = 'New notes'
        self.response = self.client.post(self.url,
                                         {'name': self.new_name,
                                          'notes': self.new_notes})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.client_slug1}))

    def test_post_edited(self):
        updated_client = Client.objects.get(slug=self.client_slug1)
        self.assertEquals(updated_client.name, self.new_name)
        self.assertEquals(updated_client.notes, self.new_notes)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_client', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
