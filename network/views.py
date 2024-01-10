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


def index(request):
    if request.method == 'POST':
        new_data = request.POST.get("post")

        # add new post to db
        new_post = Post.objects.create(post=new_data, user=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        all_post = Post.objects.order_by('-timestamp')
        p = Paginator(all_post, 10)
        x= p.page(1).object_list

        posts = Post.objects.all()
        print(request.user)

        for post in posts:
            if request.user in post.like.all():
                print(post.like.all(), post.id)

        return render(request, "network/index.html", {
            "posts": all_post,
            "page_num": 1
        })


def profile(request, username):
    # get request.user data and get info
    try:
        profile_user = User.objects.get(username=username)
        session_user = User.objects.get(username=request.user.username)

    except:
        return render(request, "network/error.html")

    # check if user is following
    is_following = Follow.objects.filter(
        user=session_user, followed=profile_user).exists()

    # handle get request
    if request.method == "GET":

        posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

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

        try:
            session_user = User.objects.get(username=request.user.username)
            profile_user = User.objects.get(username=user)
        except:
            return JsonResponse({"error": "User not found"}, status=403)

        # make the follow and unfollow action
        if action == "Follow":
            new_data = Follow.objects.create(
                user=session_user, followed=profile_user)
            new_data.save()
            
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
        post = Post.objects.filter(user=f.followed)
        posts.extend(post)

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
        postText = request.POST.get("post")
        id = request.POST.get("id")

        try:
            # checks if request is from owner of page
            post = Post.objects.get(pk=id, user=request.user)
            post.post = postText
            post.save()
        except:
            return JsonResponse({"error": "user post not found"}, status=403)

    response_data = {
        "post" : postText,
        "id" : id,

    }
    return JsonResponse({"message": "hell", "post" : postText}, status=201)

def lik(request):
    if request.method == "POST":
        id = request.POST.get("id")
        liked = request.POST.get("action")

        print(id, liked)
        try:
            post = Post.objects.get(id=id)
            print("liked", post)
        except:
            return JsonResponse({"error" : "cannot find post"}, status=403)

        # update the db
        if (liked == "false"):
            
            try:
                post.like.add(request.user)
                post.save()

                console.log(post)
                response_data = {
                    "status" : "201",
                    "message" : "successfully liked post"
                    
                }
                return JsonResponse(response_data, status=201)
            except:
                return JsonResponse({"error" : "cannot like post"}, status=403)

        else:
            try:
                post.like.remove(request.user)
                post.save()
                
                response_data = {
                    "message": "Unliked the post",
                    "status" : "201",
                    "likes" : post.like.all().count()
                }
                return JsonResponse(response_data, status=201)
            except:
                return JsonResponse({"error" : "cannot unlike post"}, status=403)

    return JsonResponse({"error": "Cannot perform the request."}, status=403)


def like(request):
    if request.method == "POST":
        liked = request.POST.get("status")
        id = request.POST.get("id")

        try:
            post = Post.objects.get(id=id)
            print("post",post)
        except:
                return JsonResponse({"error" : "cannot find post"}, status=403)


        if (liked == "true" and request.user in post.like.all()):
            post.like.remove(request.user)
            liked = "false"
        else:
            post.like.add(request.user)
            liked = "true"
    
        response_data = {
                    "status" : "201",
                    "message" : "successfully liked post",
                    "liked" : liked,
                    "likes" : post.like.all().count()
                }
        return JsonResponse(response_data, status=201)






