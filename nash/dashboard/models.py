from django.db import models
from .validators import * 


class ExcelFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/xlsx/', validators=[validate_file_extension])
    date = models.DateField(auto_now_add=True)


class Algorithm(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/algorithms/', validators=[validate_algorithm_file_extension])
    date = models.DateField(auto_now_add=True)


class Result(models.Model):
    file_name = models.ForeignKey('ExcelFile')
    algorithm = models.ForeignKey('Algorithm')
    file = models.FileField(upload_to='uploads/result/')
    date = models.DateField(auto_now_add=True)
