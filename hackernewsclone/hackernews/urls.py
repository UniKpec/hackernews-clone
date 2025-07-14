from django.urls import path
from . import views

app_name = "hackernews"

urlpatterns = [
    path("",views.index,name="index"),
    path("news/",views.top_stroies_show,name="news")
]