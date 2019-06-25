from django.urls import resolve, reverse
from .test_case_clientlist import ClientListTestCase
from ..views import ClientCards


class ClientCardsViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_cards', kwargs={'client_slug': self.client_slug2})
        self.response = self.client.get(self.url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/client/{0}/cards'.format(self.client_slug2))
        self.assertEquals(view.func.view_class, ClientCards)

    def test_contains_button_links(self):
        home_url = reverse('home')
        add_card_url = reverse('add_card', kwargs={'client_slug': self.client_slug2})
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}" class="btn'.format(add_card_url))

    def test_html_data(self):
        self.assertContains(self.response, '<h1>{0}: List of cards</h1>'
                            .format(self.client_name2))
        self.assertContains(self.response, '<tr>', 3)
        self.assertContains(self.response, '<td>{0:%B %#d, %Y}</td> \
                    <td>{1:%B %#d, %Y}</td> \
                    <td>{2:%B %#d, %Y}</td> \
                    <td>{3}</td> \
                    <td>1</td> \
                    <td>{4}</td>'.format(self.card_purchased_on,
                                         self.card_begins_on,
                                         self.card_expires,
                                         self.card_num_lessons,
                                         self.card_num_lessons - 1), html=True)

    def test_breadcrumbs(self):
        home_url = reverse('home')
        client_list_url = reverse('client_list')
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug2})
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Clients</a>'
                            .format(client_list_url), html=True)
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">{1}</a>'
                            .format(client_details_url, self.client_name2), html=True)

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
