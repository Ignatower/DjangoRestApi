from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from movies_app.models import Query, File
from movies_app.serializers import QuerySerializer, FileSerializer
from movies_app.queries import handle_queries


MOVIES = 'movies.csv'


class QueryList(APIView):
    """
    List all queries, get a query, and create a file.
    """

    def check_if_query_exists_by_title(self, title):
        count = Query.objects.filter(title = title).count()
        return count != 0

    def get_query_by_title(self, title):
        try:
            return Query.objects.get(title=title)
        except Query.DoesNotExist:
            raise Http404

    # get a query or list all queries
    def get(self, request, format=None, *args, **kwargs):
        """
        if url is ../mytitle/ then  get the query that its title is
        mytitle. Otherwise, get and list all queries
        """
        queries = Query.objects.all()
        serializer = QuerySerializer(queries, many=True)
        if self.kwargs:
            querytitle = self.kwargs['querytitle']
            query = self.get_query_by_title(querytitle)
            serializer = QuerySerializer(query)
            return Response(serializer.data)

        return Response(serializer.data)
        
    # post a file, the file must not be empty
    def post(self, request, format=None):
        """
        if the file is MOVIES then create two queries
        """
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            filename = request.FILES['file'].name
            # if the file is the movies csv, handle the queries
            if filename == MOVIES:
                avg, total = handle_queries()
                total = '$ ' + str(total)
                query = Query()
                # create query instance of the total cost of the movies
                query.create('total', total)
                query.save()
                avg = '$ ' + str(avg)
                query = Query()
                # create query instance of the avg cost of the movies
                query.create('average', avg)
                query.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
