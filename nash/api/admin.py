from django.contrib import admin
from .models import Entry
from dashboard.models import ExelFile

# Register your models here.
admin.site.register(Entry)
admin.site.register(ExelFile)