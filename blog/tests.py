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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OneUserTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()

    def test_userlist(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        # self.client.force_login(user=self.user)
        response = self.client.get('/users/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.render().content)   #['results']
        # print(json_response)

    def test_add_delete_post(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.uid = str(self.user.id)
        response = self.client.post('/posts/',
                                    data={"user": self.user.id, "title": "post1", "body": "body"},
                                    # content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.post = json.loads(response.render().content)['id']
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/posts/1/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete('/posts/' + str(self.post) + '/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/posts/1/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)

    def test_postlist(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.uid = str(self.user.id)
        response = self.client.get('/postsbyuser/' + self.uid, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.render().content)['results']
        # json_response = json.loads(response.render().content)   #['results']
        # print(response, json_response)


class TwoUserTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(
            username='user1@foo.com', email='user1@foo.com', password='top_secret')
        self.token1 = Token.objects.create(user=self.user1)
        self.token1.save()
        self.user2 = User.objects.create_user(
            username='user2@foo.com', email='user2@foo.com', password='top_top_secret')
        self.token2 = Token.objects.create(user=self.user2)
        self.token1.save()
        self.client = APIClient()

    def test_add_delete_post(self):
        self.client.force_authenticate(user=self.user1, token=self.token1)
        # self.uid1 = str(self.user.id)
        response = self.client.post('/posts/',
                   data={"user": self.user1.id, "title": "post1", "body": "body1"},
                   # content_type='application/json',
                   HTTP_AUTHORIZATION=self.token1)
        self.post = json.loads(response.render().content)['id']
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/posts/' + str(self.post) + '/', HTTP_AUTHORIZATION=self.token1)
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(user=self.user2, token=self.token2)
        response = self.client.delete('/posts/' + str(self.post) + '/', HTTP_AUTHORIZATION=self.token2)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user1, token=self.token1)
        response = self.client.delete('/posts/' + str(self.post) + '/', HTTP_AUTHORIZATION=self.token1)
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/posts/' + str(self.post) + '/', HTTP_AUTHORIZATION=self.token1)
        self.assertEqual(response.status_code, 404)
