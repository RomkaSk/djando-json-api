from django.db import models
from .validators import * 


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class InputFile(models.Model):
    title = models.CharField(max_length=255, default='File')
    project = models.ForeignKey('Project')
    file = models.FileField(upload_to='uploads/input-files/', validators=[validate_input_file_extension])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Algorithm(models.Model):
    title = models.CharField(max_length=255, default='Algorithm')
    project = models.ManyToManyField('Project')
    file = models.FileField(upload_to='uploads/algorithms/', validators=[validate_algorithm_file_extension])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Result(models.Model):
    file_name = models.ForeignKey('InputFile')
    algorithm = models.ForeignKey('Algorithm')
    file = models.FileField(upload_to='uploads/result/')
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
        # return str(self.title)
