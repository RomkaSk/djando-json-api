from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index_view'),
    url(r'^upload-file/', views.upload_file, name='upload_file'),
    url(r'^file/(?P<pk>[0-9]+)$', views.file_view, name='file_view'),
    url(r'^file/del$', views.del_file, name='del_file'),
    url(r'^file/execude$', views.execude_file, name='execude_file'),
]
