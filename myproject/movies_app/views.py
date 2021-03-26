from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movies_app.models import Query, File, Movie
from movies_app.serializers import QuerySerializer, FileSerializer
from movies_app.handle_csv import create_db_from_file, create_queries



MOVIES = 'movies.csv'


class QueryList(APIView):
    """
    List all queries, get a query, and create a file.
    """
    def get_query_by_title(self, title):
        try:
            return Query.objects.get(title=title)
        except Query.DoesNotExist:
            raise Http404

    # Get a query or list all queries
    def get(self, request, format=None, *args, **kwargs):
        """
        If url is ../mytitle/ then  get the query that its title is
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
        
    # Post a file, the file must not be empty
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        # if file is valid, then write on disk. 
        if serializer.is_valid():
            # Save it in ../movies_app/files/
            serializer.save()
            filename = request.FILES['file'].name
            if filename == MOVIES:
                # if MOVIES haven't been posted yet
                if Movie.objects.count() == 0:
                    # save the movies in the DB
                    create_db_from_file(filename)
                    create_queries()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
