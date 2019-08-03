from django.urls import reverse, resolve
from datetime import date

from .test_case_clientlist import ClientListTestCase
from ..models import CardType, Client
from ..views import edit_card
from ..forms import EditCardForm


class EditCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_card', kwargs={'client_slug': self.client_slug1, 'card_pk': self.card1.pk})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_correct_view(self):
        view = resolve('client/{0}/edit_card/{1}/'.format(
            self.client_slug1, self.card1.pk))
        self.assertEquals(view.func, edit_card)

    def test_contains_breadcrumb_links(self):
        home_url = reverse('home')
        client_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        cards_url = reverse('client_cards', kwargs={'client_cards': self.client_slug1})
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">{1}</a>'
                            .format(client_url, self.client_name1), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Cards</a>'
                            .format(cards_url), html=True)

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
        self.assertIsInstance(form, EditCardForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)


class SuccessfulEditCardViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('edit_card', kwargs={'client_slug': self.client_slug1})
        self.new_card_type = self.card_type_name
        self.new_card_purchased = date.today()
        self.response = self.client.post(self.url,
                                         {'type': "{0}".format(self.new_card_type.pk),
                                          'purchased_on': self.new_card_purchased})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('client_details',
                                                    kwargs={'client_slug': self.client_slug1}),
                             status_code=302, target_status_code=200)

    def test_card_added(self):
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
