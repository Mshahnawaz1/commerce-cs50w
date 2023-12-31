from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *


def index(request):
    if request.method == 'POST':
        new_data = request.POST.get("post")
        print(request.user)

        # add new post to db
        new_post = Posts.objects.create(post=new_data, user=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        all_post = Posts.objects.order_by('-timestamp')
        p = Paginator(all_post, 10)
        print(p.page(1).object_list)
        print(p.num_pages)

        return render(request, "network/index.html", {
            "posts": p.page(1).object_list,
            "page_num": 1
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
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


def profile(request, username):
    # get request.user data and get info
    try:
        profile_user = User.objects.get(username=username)
        session_user = User.objects.get(username=request.user.username)
        print(profile_user, session_user)
    except:
        return render(request, "network/error.html")

    # check if user is following
    is_following = Follow.objects.filter(
        user=session_user, followed=profile_user).exists()

    # handle get request
    if request.method == "GET":

        posts = Posts.objects.filter(user=profile_user).order_by('-timestamp')

        print("profile load...")
        followings = profile_user.following.all().count()
        followers = profile_user.followers.all().count()

        return render(request, "network/profile.html", {
            "posts": posts,
            "profile_user": profile_user,
            "is_following": is_following
        })


@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')
        print(user, action)

        try:
            session_user = User.objects.get(username=request.user.username)
            profile_user = User.objects.get(username=user)
        except:
            return JsonResponse({"error": "User not found"}, status=403)
        print(session_user, profile_user)

        # make the follow and unfollow action
        if action == "Follow":
            new_data = Follow.objects.create(
                user=session_user, followed=profile_user)
            new_data.save()
            print("followed")
            
            response_data = {
                "status" : "201",
                "message": "followed user",
                "action": "Unfollow",
                "followers" : profile_user.followers.all().count()
            }
            return JsonResponse(response_data, status=201)
        else:

            data = Follow.objects.get(user=session_user, followed=profile_user)
            data.delete()
            print("unfollowed")
            response_data = {
                "status" : "201",
                "message": "Unfollowed user",
                "action": "Follow",
                "followers" : profile_user.followers.all().count()
            }
            return JsonResponse(response_data, status=201)

    return JsonResponse({"error": "Cannot perform the request."}, status=403)


def following(request, username):
    user = User.objects.get(username=username)
    followings = user.following.all()

    # get all posts from user followings party
    posts = []
    for f in followings:
        post = Posts.objects.filter(user=f.followed)
        posts.extend(post)

    print(posts)
    return render(request, "network/following.html", {
        "posts": posts
    })


def make_pages(request, page_id):
    # TODO
    return HttpResponse("sdfjkl")

def like(request, page):
    
    return JsonResponse({"error": "Cannot perform the request."}, status=403)

def edit(request):
    if request.method == "POST":
        user = request.GET.get("user")
        post = request.GET.get("post")
        id = request.GET.get("id")
        console.log(user, post, id)
        try:
            post = Post.objects.get(pk=id)
        except:
            return JsonResponse({"error": "there was error"}, status=403)
    return JsonResponse({"message": "hell"}, status=201)