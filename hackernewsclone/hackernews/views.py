from django.shortcuts import render
import requests


def top_stroies_show(request):
    top_stroies_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response =requests.get(top_stroies_url)
    topStroies = response.json()
    print(response.status_code)
    top_30_ids = topStroies[:30]
    stories = []
    for story_id in top_30_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}/.json"
        resp = requests.get(story_url)
        data = resp.json()
        print(resp.status_code)
        stories.append({
            "title":data.get("title"),
            "url" : data.get("url"),
            "by": data.get("by"),
            "descendants" : data.get("descendants")
    })
    return render(request,"hackernews/homepage.html",{"stories":stories})

def index(request):
    return render(request,"base.html")
# Create your views here.
