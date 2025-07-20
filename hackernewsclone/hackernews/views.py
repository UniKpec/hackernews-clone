from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Story
from .forms import SignupForm,LoginForm
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
          


def login_signup_view(request):
      print("METHOD:", request.method)  
      print("POST DATA:", request.POST)
      login_form = LoginForm(request, data=request.POST or None,prefix="login")
      signup_form = SignupForm(request.POST or None, prefix="signup")

      if request.method == "POST":
          
          if "login-submit" in request.POST and login_form.is_valid():
               
            user = login_form.get_user()
            login(request,user)
            return redirect('hackernews:news')
          elif "signup-submit" in request.POST :
            print("POST DATA:", request.POST)
            if signup_form.is_valid():
                  print("Signup form geçerli")
                  user = signup_form.save(commit=False)
                  user.set_password(signup_form.cleaned_data["password"])
                  user.save()
                  login(request,user)
                  return redirect('hackernews:job')
      return render(request, 'hackernews/login_signup.html',context={"login_form":login_form,"signup_form":signup_form}) 


   
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


def fetch_comments_by_story_id(request,hn_id):
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{hn_id}.json"
    story_data = requests.get(story_url).json()

    comments = []
    for kid_id in story_data.get("kids", []):
        comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
        comment_data = requests.get(comment_url).json()
        comments.append(comment_data)

    return render(request, "hackernews/new_comments.html", {"comments": comments,
                                                              "story": story_data})


def past_stories_show(request):
    past_stories = Story.objects.filter(story_type='top').order_by('-time')[:30] 
    return render(request, 'hackernews/past.html', {'stories': past_stories})

def domain_show(request,domain):
     stories = Story.objects.filter(domain=domain).order_by("-time")
     return render(request, 'hackernews/domain_show.html',{"stories": stories,"domain":domain })
     
     

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
