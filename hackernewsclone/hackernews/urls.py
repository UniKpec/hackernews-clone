from django.urls import path
from . import views

app_name = "hackernews"

urlpatterns = [
    path("",views.index,name="index"),
    path("news/",views.top_stories_show,name="news"),
    path("new/",views.new_stories_show,name="new"),
    path("job/",views.job_stories_show,name="job"),
    path("show/",views.show_stories_show,name="show"),
    path("ask/",views.show_stories_ask,name="ask"),
    path("ask/<int:hn_id>/",views.ask_detail,name="ask_detail"),
]