import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase,APIClient
from rest_framework.test import force_authenticate
from rest_framework import viewsets


# Create your tests here.
client = Client()


class UserTest(TestCase):

    def test_not_allowed(self):
        # get API response
        response = client.get(reverse('userlist'))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class EndpointViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()

    def test_token_auth(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        # self.client.force_login(user=self.user)
        response = self.client.get(reverse('userlist'),HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.render().content)['results']
