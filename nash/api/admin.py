from django.contrib import admin
from .models import Entry
from dashboard.models import InputFile, Result, Algorithm, Project

# Register your models here.
admin.site.register(Entry)
admin.site.register([InputFile, Result, Algorithm, Project])
