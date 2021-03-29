from django.contrib import admin
from .models import SavedQuery, File

# Register your models here.
admin.site.register(SavedQuery)
admin.site.register(File)
