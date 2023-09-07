from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView


from django import forms
from .models import User, Posts


def index(request):

    posts = Posts.objects.all().order_by('-id')

    paginate = Paginator(posts, 10)
    page_num = request.GET.get("page")
    current_page = paginate.get_page(page_num)
    posts = current_page

    data={
        'posts':posts
    }
    return render(request, "network/index.html", data)



class PostUpdate(UpdateView):
    model = Posts
    fields =  ['text']
    template_name_suffix = '_update_form'


@csrf_exempt
@login_required
def edit_post(request, ID, new_text):

    if request.method == "POST":

        post = Posts.objects.get(pk =ID)

        update = json.loads(request.body)
        new_post_text = update.get("post_text","")

        post.post_edit = True
        post.text = new_post_text
        
        post.save()
        

    post = post = Posts.objects.get(pk =ID)

    return JsonResponse(post.serialize(), safe=False)



@login_required
def profile(request, ID):

    post1 = Posts.objects.all().order_by('-id')
    posts = post1.filter(user_id = ID)

    profile_user = User.objects.get(pk=ID)

    followcount = profile_user.followers.count()
    followingcount = profile_user.following.count()


    paginate = Paginator(posts, 10)
    page_num = request.GET.get("page")
    current_page = paginate.get_page(page_num)
    posts = current_page

    data={
        'posts':posts,
        'profile_user':profile_user,
        'followcount': followcount,
        'following': followingcount,
    }

    return render(request, "network/profile.html", data)

@login_required
def following(request):

    logged_user_id = request.user.id
    logged_user = User.objects.get(pk = logged_user_id)

    following_users = request.user.following.all()
    following_posts = Posts.objects.filter(user__in = following_users)


    posts = following_posts.order_by('-id')

    paginate = Paginator(posts, 10)
    page_num = request.GET.get("page")
    current_page = paginate.get_page(page_num)
    posts = current_page

    follow_count = following_users.count()

    data={
        'posts':posts,
        'follow_count':follow_count,
    }

    return render(request, "network/following.html", data)


@csrf_exempt
@login_required
def like_post(request, ID):

    if request.method == "POST":

        log_user = request.user
        log_user_ID = log_user.id
        logged_user = User.objects.get(pk=log_user_ID)

        post = Posts.objects.get(pk=ID)

        if logged_user in post.reaction.all():
            post.reaction.remove(logged_user)
            reaction = False
        else:
            post.reaction.add(logged_user)
            reaction = True

        likecount = post.reaction.count()

        values ={
            'reaction': reaction,
            'likecount': likecount
        }    

        return JsonResponse(values, safe=False)
  
@csrf_exempt
@login_required
def follow_user(request, ID):

    if request.method == "POST":

        log_user = request.user
        log_user_ID = log_user.id
        logged_user = User.objects.get(pk=log_user_ID)

        profile_user = User.objects.get(pk=ID)

        if log_user_ID == ID:
        
            reaction = None
            followcount = logged_user.followers.count()
            followingcount = logged_user.following.count()  
            
            values ={
                'reaction': reaction,
                'followcount': followcount,
                'following': followingcount
            }
        
            return JsonResponse(values, safe=False) 
        
        elif logged_user in profile_user.followers.all():
            profile_user.followers.remove(logged_user)
            logged_user.following.remove(profile_user)
            reaction = False
        
        else:
            profile_user.followers.add(logged_user)
            logged_user.following.add(profile_user)
            reaction = True

        followcount = profile_user.followers.count()
        followingcount = profile_user.following.count()

        values ={
            'reaction': reaction,
            'followcount': followcount,
            'following': followingcount
        }    

        return JsonResponse(values, safe=False)

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

class CreatePost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['text']
        labels = {'text' : 'Write the content of your Post below'}

        widgets =   {
                    'text' : forms.TextInput()
                    
                    }
        
def create_view(request):

    if request.method == 'POST':
        create_post = CreatePost(request.POST)

        if create_post.is_valid():
            post_text = create_post.cleaned_data['text']
            creator = request.user

            #if not post_text:
             #   return render(request,"network/create.html")

            Posts.objects.create(text=post_text, user=creator)
            posts = Posts.objects.all().order_by('-id')

        return render(request, "network/index.html",{"posts":posts})
    
    return render(request, "network/create.html",{'form':CreatePost()})

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



## API routes used for testing

@csrf_exempt
@login_required
def postbox(request, postbox, page_number):
    
    if postbox == "allposts":
        post_box = Posts.objects.all()
        
    elif postbox == "userposts":
        post_box = Posts.objects.filter(
            user = request.user, 
        )
    elif postbox == "followingposts":

        follows = request.user.following.all()
        post_box = Posts.objects.filter(user__in = follows)
    
    postz = post_box.all().order_by('-id')
    
    post_count = postz.count()

    final_page = page_number*10
    page_post_num = final_page -9

    posts = Posts.objects.none()
    
    for x in range(page_post_num, final_page):
        posts |= Posts.objects.filter(pk=x)


    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def following_list(request, ID):

    try:
        list = User.objects.get(pk = ID)
    except User.DoesNotExist:
        return JsonResponse({"error": "Following List not found."}, status=404)

    if request.method == "POST":

        log_user = request.user
        log_user_ID = log_user.id

        logged_user = User.objects.get(pk=log_user_ID)
        following_user = User.objects.get(pk = ID)

        if logged_user in following_user.followers.all():
            logged_user.following.remove(following_user)
            following_user.followers.remove(logged_user)
        else:
            logged_user.following.add(following_user)
            following_user.followers.add(logged_user)

        return JsonResponse(list.serialize())
        

    if request.method == "GET":
        return JsonResponse(list.serialize())
    else:
        return JsonResponse({"error": "Get request required."}, status=400)


@login_required
def logged_user(request):
    logged_user  = request.user
    return JsonResponse(logged_user.serialize())
