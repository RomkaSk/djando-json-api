from django.db import models

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=250, verbose_name=u'Title')
    short_text = models.CharField(max_length=250, verbose_name=u'Short desc')
    text = models.TextField(verbose_name=u'Full desc')
    date = models.DateField()
