
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    
    # API Routes
    path("save_post/<str:action>", views.save_post, name="save_post"),
    path("load_posts/<int:page>", views.load_posts, name="load_posts"),
    path("online_users", views.online_users, name="online_users"),
    path("follow", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
]
