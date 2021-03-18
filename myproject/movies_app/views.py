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
    List all queries, get query, and create a file.
    """
    def get_query(self, title):
        try:
            return Query.objects.get(title=title)
        except Query.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        queries = Query.objects.all()
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        if 'query' in request.data.keys():
            title = request.data['query']
            query = self.get_query(title)
            serializer = QuerySerializer(query)
            return Response(serializer.data)
            
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # the file must not be empty
    def post(self, request, format=None):
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
