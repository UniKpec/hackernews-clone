from django.shortcuts import render
from .models import Story
from urllib.parse import urlparse
import requests

def fetch_and_store_stories():
    top_stroies_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response =requests.get(top_stroies_url)
    topStroies = response.json()[:30]
    print("Bıg ",response.status_code)
    for story_id in topStroies:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}/.json"
        story_data = requests.get(story_url).json()

        Story.objects.update_or_create(
            hn_id = story_id,
            defaults={
                "title":story_data.get("title"),
                "url": story_data.get("url"),
                "by": story_data.get("by"),
                "score":story_data.get("score"),
                'domain': urlparse(story_data.get('url', '')).netloc,  
                "descendants": story_data.get("descendants", 0),} 
                
        ) # eğer descendants verisi jsonda yoksa 0 dondur.
           
def top_stroies_show(request):
        fetch_and_store_stories()  # her istekle API'den veri çeker
        stories = Story.objects.all()
        return render(request, 'hackernews/homepage.html', {'stories': stories})


def index(request):
    return render(request,"base.html")
# Create your views here.
