from django.shortcuts import render
from .models import Story
from urllib.parse import urlparse
import requests
import datetime

def fetch_stories(story_type="top"):
      endpoints = {
            "top" : "topstories",
            "new" : "newstories",
            "ask" : "askstories",
            "show": "showstories",
            "job": "jobstories"
      }
      url = f"https://hacker-news.firebaseio.com/v0/{endpoints[story_type]}.json"
      response = requests.get(url)
      ids = response.json()[:30]
      print(response.status_code,endpoints[story_type])

      for story_id in ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_data = requests.get(story_url).json()

            Story.objects.update_or_create(
                  hn_id = story_id,
                  defaults= {
                        "title": story_data.get("title"),
                        "url": story_data.get("url"),
                        "by": story_data.get("by","anonmymous"),
                        "score": story_data.get("score", 0),
                        "descendants": story_data.get("descendants", 0),
                        "domain": urlparse(story_data.get("url", "")).netloc,
                        "story_type": story_type,
                        "time": datetime.datetime.fromtimestamp(story_data.get("time", 0)),
                  })
          
      
def ask_detail(request, hn_id):
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{hn_id}.json"
    story_data = requests.get(story_url).json()

    
    comments = []
    for kid_id in story_data.get("kids", []):
        comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
        comment_data = requests.get(comment_url).json()
        comments.append(comment_data)

    return render(request, "hackernews/ask_detail.html", {
        "story": story_data,
        "comments": comments
    })

           
def top_stories_show(request):
        fetch_stories()
        stories = Story.objects.filter(story_type = "top")
        return render(request, 'hackernews/homepage.html', {'stories': stories})

def new_stories_show(request):
      fetch_stories("new")
      stories = Story.objects.filter(story_type = "new")
      return render(request, 'hackernews/new.html',context= {'stories':stories})

def job_stories_show(request):
      fetch_stories("job")
      stories = Story.objects.filter(story_type = "job")
      return render(request,'hackernews/job.html',context={'stories':stories})

def show_stories_show(request):
      fetch_stories("show")
      stories = Story.objects.filter(story_type = "show")
      return render(request,'hackernews/show.html',context={"stories":stories})

def show_stories_ask(request):
      fetch_stories("ask")
      stories = Story.objects.filter(story_type = "ask")
      return render(request,'hackernews/ask.html',context={"stories":stories})


def index(request):
    return render(request,"base.html")
# Create your views here.
