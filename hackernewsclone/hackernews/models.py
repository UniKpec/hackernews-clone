from django.db import models
from django.contrib.auth.models import User
class Story(models.Model):
    title = models.CharField(max_length=150,null=True)
    url = models.URLField(null=True, blank=True)
    by = models.CharField(max_length=100)
    descendants = models.IntegerField(null=True , blank=True)
    score = models.IntegerField(null=True, blank=True)
    domain = models.CharField(max_length=100, null=True,blank=True)
    hn_id = models.IntegerField(unique=True) # Hacker News ID
    story_type = models.CharField(max_length=20, default="top") #top,new,job gib sayfaların türlerini tutacağız. filtreleme için yararlı.
    time = models.DateTimeField(null=True,blank=True)

class SubmitStory(models.Model):
    title = models.CharField(max_length=100, blank=True)
    url = models.URLField(null=True,blank=True)
    domain = models.CharField(null=True,blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)




# Create your models here.
