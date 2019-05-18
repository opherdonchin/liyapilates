from django.test import TestCase
from django.urls import resolve, reverse
from .views import client_list, client_details
from .models import PilatesClient

# Create your tests here.
# TODO: Create tests for view: client_details
# TODO: Create tests for view: lesson_details
# TODO: Create tests for view: lesson_list


class HomeTests(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'

    def setUp(self):
        PilatesClient.objects.create(name=self.client_name1,
                                     slug=self.client_slug1,
                                     card=None)
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, client_list)

    def test_home_view_contains_client_link(self):
        client_details_url = reverse('client_details', kwargs={'client_slug': self.client_slug1})
        self.assertContains(self.response, 'href="{0}"'.format(client_details_url))


class ClientDetailsTests(TestCase):
    client_name1 = 'Sarah Shadlock'
    client_slug1 = 'sarah-shadlock'
    nonexistent_slug = 'missing-client'

    def setUp(self):
        PilatesClient.objects.create(name=self.client_name1,
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
