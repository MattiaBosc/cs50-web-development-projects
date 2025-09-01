from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


@login_required
def profile(request):
    return render(request, "network/profile.html")


@login_required
def following(request):
    return render(request, "network/following.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.user.online = True
            request.user.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
def logout_view(request):
    request.user.online = False
    request.user.save()
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def save_post(request, action):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    body = data.get("content")
    if not body:
        return JsonResponse({"error": "New post can't be empty."}, status=400)

    post_id = data.get("post_id")
    if action == "new":
        post = Post(author=request.user, body=body)
    elif action == "edit" and post_id:
        try:
            post_id = int(post_id.split("-")[1])
            post = Post.objects.get(pk = post_id)
        except:
            return JsonResponse({"error": "Post not found"}, status=400)
        if str(post.author) == request.user.username:
            post.body = body
            post.timestamp = timezone.now()
        else:
            return JsonResponse({"error": "Permission denied"}, status=400)
    else:
        return JsonResponse({"error": "Invalid action"}, status=400)
    
    post.save()
    return JsonResponse({"message": "Post saved successfully."}, status=201)


@csrf_exempt
def load_posts(request, page):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    if data.get("action") == "all":
        posts = Post.objects.all().order_by("-timestamp")
        
    elif data.get("action") == "profile":
        posts = Post.objects.filter(author = request.user).order_by("-timestamp")
         
    elif data.get("action") == "following":
        following = request.user.following.values_list('id', flat=True)
        posts = Post.objects.filter(author__in=following).order_by("-timestamp")
        
    else:
        return JsonResponse({"error": "Invalid action"}, status=400)
    
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    return JsonResponse({"posts": [post.serialize() for post in page_obj],
                         "page_number": page,
                         "current_user": request.user.username,
                         "pages": paginator.num_pages}, safe=False)


@login_required
def online_users(request):
    following = request.user.following.count()
    followers = request.user.follower.count()
    online_users = User.objects.filter(online=True).exclude(username=request.user.username)
    users_info = []

    for user in online_users:
        users_info.append({
            "username": user.username,
            "follower": request.user.pk in user.follower.values_list('id', flat=True)})

    return JsonResponse({"users_info": users_info, "followers": followers, "following": following}, status=200)
    
 
@csrf_exempt
@login_required   
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    user = get_object_or_404( User, username = data.get("username"))
    
    if data.get("follower"): #usernamea are unique fields in Django's User Model
        user.follower.remove(request.user)
    else:
        user.follower.add(request.user)
    
    user.save()
    return JsonResponse({"message": "POST request was successfull"}, status=200)


@login_required   
def like(request, post_id):
    
    post = get_object_or_404(Post, pk = post_id)
    if request.user.username not in post.likes.all().values_list('username', flat=True):
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    
    post.save()   
    return JsonResponse({"message": "GET request was successful"}, status=200)
    