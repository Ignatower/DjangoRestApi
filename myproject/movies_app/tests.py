from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from movies_app.models import Query, File
import os

url = 'http://127.0.0.1:8000/'
MOVIES = 'movies.csv'


class QueryTests(APITestCase):

    def test_list_queries(self):
        """
        Ensure that response is 200 when we list queries
        """
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_existing_query_by_title(self):
        query = Query()
        query.title = 'mytitle'
        query.value = 'myvalue'
        query.save()
        response = self.client.get(url+'mytitle')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_get_not_existing_query_by_title(self):
        response = self.client.get(url+'mytitasdasdle')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)


class FileTests(APITestCase):

    def test_create_file(self):
        """
        Ensure that we can create a file
        """
        file={'file': open('hola.txt', 'rb')}
        response = self.client.post(url, data=file)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)

    def test_if_movies_file_is_created_then_queries_total_avg_exists(self):
        """
        Ensure that if we creates then movies file then total and avg 
        queries exists
        """
        file={'file': open(MOVIES, 'rb')}
        response = self.client.post(url, data=file)
        self.assertEqual(Query.objects.filter(title='total').count(), 1)
        self.assertEqual(Query.objects.filter(title='average').count(), 1)
        

