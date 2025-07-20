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
    path("login/",views.login_signup_view,name="login_signup"),
    path("logout/",views.logout_view,name="logout"),
    path("ask/<int:hn_id>/",views.ask_detail,name="ask_detail"),
    path("past/",views.past_stories_show,name="past"),
    path("submit/",views.submit_view,name="submit_views"),
    path('domain/<str:domain>/', views.domain_show, name='stories_by_domain'),
    path("comments/<int:hn_id>/", views.fetch_comments_by_story_id, name="comments_by_story"),
]