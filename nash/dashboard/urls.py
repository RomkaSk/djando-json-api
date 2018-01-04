from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.projects_view),
    url(r'^project/(?P<project_id>[0-9]+)$', views.project_view),
    url(r'^upload-file/', views.upload_file),
    url(r'^file/(?P<file_id>[0-9]+)$', views.file_view),
    url(r'^file/del$', views.delete_file),
    url(r'^file/execude$', views.execude_file),
    url(r'^algorithm/del$', views.delete_file),
]
