from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^download/(?P<file_path>.+)/$', views.download_file, name='download_file'),
]
