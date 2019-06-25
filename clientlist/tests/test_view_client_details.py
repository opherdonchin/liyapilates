from django.urls import resolve, reverse

from .test_case_clientlist import ClientListTestCase
from ..models import Client
from ..views import client_details
from ..forms import ClientNotesForm

# TODO: Add test for expiration date and num lessons left


class ClientDetailsTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.get(self.url)

    def test_status_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_found_status_code(self):
        url = reverse('client_details', kwargs={'client_slug': self.nonexistent_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_resolves_view(self):
        view = resolve('/client/' + self.client_slug1 + '/')
        self.assertEquals(view.func, client_details)

    def test_contains_button_links(self):
        homepage_url = reverse('home')
        add_card_url = reverse('add_card', kwargs={'client_slug': self.client_slug1})
        edit_client_url = reverse('edit_client', kwargs={'client_slug': self.client_slug1})
        client_cards_url = reverse('client_cards', kwargs={'client_slug': self.client_slug1})
        self.assertContains(self.response, 'a href="{0}"'.format(homepage_url))
        self.assertContains(self.response, 'a href="{0}" class="btn'.format(add_card_url))
        self.assertContains(self.response, 'a href="{0}" class="btn'.format(edit_client_url))
        self.assertContains(self.response, 'a href="{0}" class="btn'.format(client_cards_url))

    def test_html_no_data(self):
        self.assertContains(self.response, '<td>No card</td>', count=4)

    def test_html_data(self):
        url = reverse('client_details', kwargs={'client_slug': self.client_slug2})
        response = self.client.get(url)
        self.assertContains(response, '<th>Card type:</th><td>12 week</td>', html=True)
        self.assertContains(response,
                            '<th>Date purchased:</th><td>{0:%B %#d, %Y}</td>'.format(self.card_purchased_on), html=True)
        self.assertContains(response, '<th>Epires on:</th><td>{0:%B %#d, %Y}</td>'.format(self.card_expires), html=True)
        self.assertContains(response, '<th>Lessons left:</th><td>{0}</td>'.format(self.card_num_lessons-1), html=True)

    def test_breadcrumbs(self):
        home_url = reverse('home')
        client_list_url = reverse('client_list')
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Client list</a>'
                            .format(client_list_url), html=True)

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
        self.assertIsInstance(form, ClientNotesForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulClientDetailsPostTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.new_notes = 'New notes'
        self.response = self.client.post(self.url, {'notes': self.new_notes})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.client_slug1}))

    def test_post_edited(self):
        updated_client = Client.objects.get(slug=self.client_slug1)
        self.assertEquals(updated_client.notes, self.new_notes)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
