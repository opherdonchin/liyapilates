from django.urls import reverse, resolve
from datetime import date

from .test_case_clientlist import ClientListTestCase
from ..models import CardType, Client
from ..views import add_card
from ..forms import AddCardForm


class AddCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('add_card', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_correct_view(self):
        view = resolve('/client/{0}/new_card'.format(self.client_slug1))
        self.assertEquals(view.func, add_card)

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
        self.assertIsInstance(form, AddCardForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<select', 1)
        self.assertContains(self.response, '<option', 2)


class SuccessfulAddCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('add_card', kwargs={'client_slug': self.client_slug1})
        self.new_card_type = CardType.objects.get(pk=1)
        self.new_card_purchased = date.today()
        self.response = self.client.post(self.url,
                                         {'type': '{0}'.format(self.new_card_type.pk),
                                          'purchased_on': self.new_card_purchased})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.client_slug1}),
                             status_code=302, target_status_code=200)

    def test_post_edited(self):
        added_card = Client.objects.get(slug=self.client_slug1).cards.latest('purchased_on')
        self.assertEquals(added_card.type, self.new_card_type)
        self.assertEquals(added_card.purchased_on, self.new_card_purchased)


class UnsuccessfulClientEditViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('add_card', kwargs={'client_slug': self.client_slug1})
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
