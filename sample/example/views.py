from django.contrib.auth.models import User, Group
from .models import Entry
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, EntrySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class EntrysViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows entrys to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


# class EntryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows entrys to be viewed or edited.
#     """
    
#     queryset = Entry.objects.filter()
#     serializer_class = EntrySerializer
    