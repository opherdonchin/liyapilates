from django.test import TestCase
from django.urls import resolve, reverse
from ..views import client_list
from ..models import Client


class ClientListViewTests(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'

    def setUp(self):
        Client.objects.create(name=self.client_name1,
                              slug=self.client_slug1,
                              card=None)
        url = reverse('client_list')
        self.response = self.client.get(url)

    def test_client_list_view_status_code(self):
        url = reverse('client_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_client_list_url_resolves_client_list_view(self):
        view = resolve('/client_list/')
        self.assertEquals(view.func, client_list)

    def test_client_list_view_contains_client_link(self):
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.assertContains(self.response, 'href="{0}"'.format(client_details_url))
