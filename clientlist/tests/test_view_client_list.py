from django.urls import resolve, reverse
from .test_case_clientlist import ClientListTestCase
from ..views import client_list


class ClientListViewTests(ClientListTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('client_list')
        self.response = self.client.get(self.url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/client_list/')
        self.assertEquals(view.func, client_list)

    def test_view_contains_links(self):
        new_client_url = reverse('new_client')
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        lesson_details_url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.assertContains(self.response, 'href="{0}"'.format(new_client_url))
        self.assertContains(self.response, 'href="{0}"'.format(client_details_url))
        self.assertContains(self.response, 'href="{0}"'.format(lesson_details_url))

    def test_client_details_view_no_card(self):
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        lesson_details_url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.assertContains(self.response, '<td><a href="{0}">{1}</a></td> \
                    <td><a href="{2}">{3:%b %#d, %Y}</a></td> \
                    <td>No card</td> \
                    <td>No card</td> \
                    <td>None</td>'.format(client_details_url,
                                          self.client_name1,
                                          lesson_details_url,
                                          self.lesson.held_at), html=True)

    def test_client_details_view_card_data(self):
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug2})
        lesson_details_url = reverse('lesson_details', kwargs={'pk': self.lesson.pk})
        self.assertContains(self.response, '<a href="{0}">{1}</a>'.
                            format(client_details_url, self.client_name2), html=True)
        self.assertContains(self.response, '<a href="{0}">{1:%b %#d, %Y}</a>'
                            .format(lesson_details_url, self.lesson.held_at), html=True)
        self.assertContains(self.response, '{0}'.format(self.card_type_name), html=True)
        self.assertContains(self.response, '{0:%b %#d, %Y}'.format(self.card_expires), html=True)
        self.assertContains(self.response, '{0}'.format(self.card_num_lessons-1), html=True)

    def test_view_breadcrumbs(self):
        home_url = reverse('home')
        self.assertContains(self.response,
                            '<li class="breadcrumb-item"><a href="{0}">Home</a>'
                            .format(home_url), html=True)

    def test_view_navbar(self):
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
