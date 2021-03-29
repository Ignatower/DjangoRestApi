from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from movies_app import views

urlpatterns = [
    path('', views.SavedQueryList.as_view()),
    re_path('^(?P<querytitle>.+)/$', views.SavedQueryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
