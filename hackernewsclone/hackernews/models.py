from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField(null=True, blank=True)
    by = models.CharField(max_length=100)
    descendants = models.IntegerField(null=True , blank=True)
    score = models.IntegerField(null=True, blank=True)
    domain = models.CharField(max_length=100, null=True,blank=True)
    hn_id = models.IntegerField(unique=True) # Hacker News ID
# Create your models here.
