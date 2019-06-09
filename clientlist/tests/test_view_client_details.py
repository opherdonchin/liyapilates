from django.test import TestCase
from django.urls import resolve, reverse
from ..views import client_details
from ..models import Client


# TODO: Add test for expiration date and num lessons left


class ClientDetailsTests(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'
    nonexistent_slug = 'missing-client'

    def setUp(self):
        Client.objects.create(name=self.client_name1,
                              slug=self.client_slug1,
                              card=None)

    def test_client_details_view_status_success_code(self):
        url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_client_details_not_found_status_code(self):
        url = reverse('client_details', kwargs={'client_slug': self.nonexistent_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_client_details_resolves_client_details_view(self):
        view = resolve('/client/' + self.client_slug1 + '/')
        self.assertEquals(view.func, client_details)

    def test_client_details_view_contains_homepage_link(self):
        client_view_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        response = self.client.get(client_view_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'a href="{0}"'.format(homepage_url))
