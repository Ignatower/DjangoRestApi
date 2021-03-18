from django.db import models


class Query(models.Model):
    title = models.CharField(max_length=100, default='')
    value = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title

    # method to handle doing queries in the view
    def create(self, title, value):
        self.title = title
        self.value = value


class File(models.Model):
    file = models.FileField(upload_to='movies_app/files')
