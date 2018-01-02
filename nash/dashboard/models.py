from django.db import models
import datetime
from .validators import validate_file_extension

# Create your models here.
class ExcelFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/xlsx/', validators=[validate_file_extension])
    date = models.DateField(auto_now_add=True)
