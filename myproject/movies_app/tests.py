import os
from rest_framework.test import APITestCase
from rest_framework import status
from movies_app.models import Query, File
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory

from movies_app.views import QueryList


url = 'http://127.0.0.1:8000/movies/'
MOVIES = 'movies.csv'


class QueryTests(APITestCase):

    def test_list_queries(self):
        """
        Ensure that the response is 200 when we list the queries
        """
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_existing_query_by_title(self):
        """
        Ensure that we can get a query by its title if it exists
        """
        query = Query()
        query.title = 'mytitle'
        query.value = 'myvalue'
        query.save()
        response = self.client.get(url+'mytitle/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title':'mytitle','value':'myvalue'})

    def test_get_not_existing_query_by_title(self):
        """
        Ensure that the response is 400 if the query does not exist
        """
        response = self.client.get(url+'mytitasdasdle/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_is_forbidden(self):
        """
        Ensure that the response is 403 if the method is forbidden
        """
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FileTests(APITestCase):
    def test_post_without_authorization(self):
        """
        Ensure that we cann't post without authorization
        """
        file={'file': open('hola.txt', 'rb')}
        response = self.client.post(url, data=file)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_file(self):
        """
        Ensure that we can create a file
        """
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        factory = APIRequestFactory()
        view = QueryList.as_view()
        file={'file': open('hola.txt', 'rb')}
        request = factory.post(url, data=file)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)
       
        """
        https://docs.djangoproject.com/en/3.2/topics/testing/overview/#the-test-database

        def test_if_movies_file_is_created_then_queries_total_avg_exists(self):
        
        Ensure that if we create the movies file, then total and avg 
        queries exist
        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        factory = APIRequestFactory()
        view = QueryList.as_view()
        file={'file': open(MOVIES, 'rb')}
        request = factory.post(url, data=file)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Query.objects.filter(title='total').count(), 1)
        self.assertEqual(Query.objects.filter(title='average').count(), 1)
        q = Query.objects.get(title='total')
        w = Query.objects.get(title='average')
        self.assertEqual(q.value, '$ 127088278638')
        self.assertEqual(w.value, '$ 4457517')
        """
