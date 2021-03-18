from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from movies_app import views

urlpatterns = [
    path('files/', views.FileList.as_view()),
    #re_path(r'^files/(?P<filename>[^/]+)$', views.FileList.as_view()),
    path('queries/', views.QueryList.as_view()),
    path('queries/<int:pk>/', views.QueryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)