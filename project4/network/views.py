from cProfile import Profile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import datetime

from requests import post
from network.models import *
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, Count, F
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User



def index(request):
    
    if request.user.is_authenticated:
        user = request.user
        likes =Likes.objects.filter(post_id=OuterRef('id'), user_id=user)
        posts = Post.objects.filter().order_by('-time').annotate(curr_like=Count(likes.values('id')))
    else:
        posts = Post.objects.order_by("-time").all()

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    pager = paginator.get_page(page_num)

    return render(request, "network/index.html", {
        "posts": pager
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

def all_post(request):

    if request.user.is_authenticated:
        user = request.user
        likes =Likes.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter().order_by('-time').annotate(curr_like=Count(likes.values('id')))
    else:
        posts = Post.objects.order_by("-time").all()

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    pager = paginator.get_page(page_num)

    return render(request, "network/allPost.html",{
        "posts": pager
    })

@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        date_time = datetime.date
        if content is not None:
           post = Post()
           post.user = request.user
           post.content = content
           post.time = date_time
           post.save()
           user = request.user
           likes =Likes.objects.filter(post=OuterRef('id'), user_id=user)
           posts = Post.objects.filter().order_by('-time').annotate(curr_like=Count(likes.values('id')))

           paginator = Paginator(posts, 10)
           page_num = request.GET.get('page')
           pager = paginator.get_page(page_num)

           return render(request, "network/allPost.html",{
               "posts": pager
            })
        else:
            return render(request, "newPost.html", {
                "message": "Post cannot be empty!"
            })
    else:
        return render(request, "network/newPost.html")

def profile_page(request, username):
    follows=0
    profile = User.objects.get(username=username)
    if request.user.is_authenticated:
        user = request.session['_auth_user_id']
        follows = Follower.objects.filter(
        follower=user, following=profile).count()
        likes =Likes.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter(user=profile).order_by("-time").annotate(curr_like=Count(likes.values('id')))
    else:
        posts = Post.objects.filter(
            user=profile).order_by('time').all()
        user = request.user

    
    following = Follower.objects.filter(
        follower=profile).count()
    followers = Follower.objects.filter(
        following=profile).count()
    
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    pager = paginator.get_page(page_num)

    return render(request, "network/profile.html",{
        "profile": profile,
        "user_prof": user,
        "follows": follows,
        "posts": pager,
        "following": following,
        "followers": followers
    })

@login_required
@csrf_exempt
def follow(request, id):
    try:
        result = 'follow'
        user = User.objects.get(id=request.session['_auth_user_id'])
        prof = User.objects.get(id=id)
        follower = Follower.objects.get_or_create(
            follower=user, following=prof)
        if not follower[1]:
            Follower.objects.filter(
                follower=user, following=prof).delete()
            result = 'unfollow'
        followers = Follower.objects.filter(
            following=prof).count()
        following = Follower.objects.filter(
            follower=prof).count()
        likes =Likes.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter(user = prof).order_by("-time").annotate(curr_like=Count(likes.values('id')))
        follows = Follower.objects.filter(
        follower=user, following=prof).count()

        paginator = Paginator(posts, 10)
        page_num = request.GET.get('page')
        pager = paginator.get_page(page_num)

        return render(request, "network/profile.html",{
            "profile": prof,
            "user": user,
            "posts": pager,
            "following": following,
            "followers": followers,
            "follows": follows
        })
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no like chosen")

@login_required
@csrf_exempt
def following(request):
    if request.user.is_authenticated:
        user = request.user
        following = Follower.objects.filter(follower=user)
        likes =Likes.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter(user_id__in=following.values('following_id')).order_by("-time").annotate(curr_like=Count(likes.values('id')))
    else:
        return HttpResponseRedirect(reverse("login"))
    
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    pager = paginator.get_page(page_num)
    
    return render(request, "network/following.html",{
        "posts": pager,
        "following": following
    })

@login_required
@csrf_exempt
def editpost(request):
    if request.method == "POST":
        postid = request.POST.get('id')
        edit = request.POST.get('post')
        try:
            post = Post.objects.get(id=postid)
            if post.user == request.user:
                post.content = edit.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)

@login_required
@csrf_exempt
def likeDislike(request, id):
    try:
        user = User.objects.get(id=request.session['_auth_user_id'])
        post = Post.objects.get(id=id)
        post1 = Post.objects.filter(id=id)
        like = Likes.objects.get_or_create(user = user, post = post)
        css = "fas fa-heart"
        if not like[1]:
            Likes.objects.filter(user = user, post = post).delete()

            css = "far fa-heart"
        
        likes = Likes.objects.filter(post = post).count()
        post1.update(like=likes)
    except:
        return HttpResponseBadRequest("Sorry something went wrong")
    return JsonResponse({
        "like": id, "css": css, "likes": likes
    })
