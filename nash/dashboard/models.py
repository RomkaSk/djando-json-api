from django.db import models
import datetime

# Create your models here.
class ExelFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/exels/')
    date = models.DateField(auto_now_add=True)
