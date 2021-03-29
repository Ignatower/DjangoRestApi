from rest_framework import serializers
from movies_app.models import SavedQuery, File


class SavedQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedQuery
        fields = ['title', 'value']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']
