from rest_framework import serializers
from movies_app.models import Query, File


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['title', 'value']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']
