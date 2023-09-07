from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Stats, Entry, Workout
from django.utils.timezone import datetime


def index(request):

    if request.user.is_authenticated:
        
        logged_user = request.user

        if Stats.objects.filter(user = logged_user).exists():
            
            stats = Stats.objects.get(user = logged_user)

            today = datetime.today().strftime('%Y-%m-%d')

            entries1 = Entry.objects.all()
            entries = entries1.filter(user=logged_user, date=today)

            sum = 0

            for entry in entries:
                sum = sum + entry.value

            ratio = 1 - (sum / stats.bmr)

            percent = (sum/stats.bmr)*100
            percent = round(percent)
            
            if ratio <= 0:
                total = 0
            else:
                total = 722.2 * ratio
            

            return render(request, "network/index.html",{
                "stats":stats,
                "entries":entries,
                "form":ChangeDate(),
                "date":today,
                "total":total,
                "percent":percent,
            })
        
        else:
            return render(request,"network/update.html",{
                'form':UpdateStats()
            })
        
    else:
        return render(request,"network/index.html")
    


class CreateWorkout(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title','description','link']

        labels = {'title':'Name of the Workout', 
                  'description':'Describe the workout (Sets and Reps or general)',
                  'link':'Add a youtube link for a demonstration of the workout'
                  }
        
        widgets =   {
                    'title':forms.TextInput(),
                    'description':forms.TextInput(),
                    'link':forms.URLInput(),
                    }



@csrf_exempt
@login_required
def create_workout(request):

    logged_user = request.user

    if request.method =='POST':
        workout = CreateWorkout(request.POST)

        if workout.is_valid():
            title = workout.cleaned_data['title']
            description = workout.cleaned_data['description']
            link = workout.cleaned_data['link']

            Workout.objects.create(creator=logged_user, title=title, description=description, link=link)

            workouts = Workout.objects.all().order_by('-id')

            paginate = Paginator(workouts, 5)
            page_num = request.GET.get("page")
            current_page = paginate.get_page(page_num)
            workouts = current_page
            

            return render(request,"network/explore.html",{
                "workouts":workouts,
            })
    
    return render(request,"network/create_workout.html",{
        'form':CreateWorkout(),
    })
    


@csrf_exempt
@login_required
def explore(request):

    workouts = Workout.objects.all().order_by('-id')

    paginate = Paginator(workouts, 5)
    page_num = request.GET.get("page")
    current_page = paginate.get_page(page_num)
    workouts = current_page



    return render(request, "network/explore.html",{
        "workouts":workouts,
    })



@csrf_exempt
@login_required
def saved_workouts(request):

    logged_user = request.user

    all_w = Workout.objects.all()

    created_workouts = all_w.filter(creator=logged_user)

    saved_workouts = all_w.filter(savers = logged_user)

    workouts1 = created_workouts | saved_workouts

    workouts = workouts1.order_by('-id')

    paginate = Paginator(workouts, 5)
    page_num = request.GET.get("page")
    current_page = paginate.get_page(page_num)
    workouts = current_page

    return render(request, "network/saved.html",{
    "workouts":workouts,
    })




@csrf_exempt
@login_required  
def workout_save(request,ID):

    logged_user = request.user

    workout = Workout.objects.get(pk=ID)

    if logged_user in workout.savers.all():
        workout.savers.remove(logged_user)
        reaction = True
    else:
        workout.savers.add(logged_user)
        reaction = False

    values={
        'reaction': reaction,
    }

    return JsonResponse(values, safe=False)

@csrf_exempt
@login_required
def delete_workout(request, ID):

    workout = Workout.objects.get(pk=ID)
    workout.delete()
    reaction = True

    values={
        'reaction': reaction,
    }

    return JsonResponse(values, safe=False)



class ChangeDate(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date']

        labels = {'date':'Request a Date for the Tracker'}

        widgets= {'date': forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type':'date', 'placeholder':'yyyy-mm-dd', 'class': 'form-control'},
        ),}



class UpdateStats(forms.ModelForm):
    class Meta:
        model = Stats
        fields = ['weight','height','age']

        labels =    {
                    'weight':'Weight (Enter your weight in KG, **note: 1kg = 2.204 lbs)',
                    'height':'Height (Enter your Height in CM)',
                    'age':'Age (Enter your Age)'
                    }

        widgets =   {
                    'weight':forms.NumberInput(),
                    'height':forms.NumberInput(),
                    'age':forms.NumberInput()
                    }


@csrf_exempt
@login_required
def update(request):
    logged_user = request.user
    logged_id = request.user.id

    if request.method =='POST':
        update_stats = UpdateStats(request.POST)

        if update_stats.is_valid():
            weight_update = update_stats.cleaned_data['weight']
            height_update = update_stats.cleaned_data['height']
            age_update = update_stats.cleaned_data['age']
            bmr_update = 88.362 + (13.397*weight_update) + (4.799*height_update) - (5.677*age_update)

            if Stats.objects.filter(user=logged_user).exists():
                user_stats = Stats.objects.get(user=logged_user)
                user_stats.weight = weight_update
                user_stats.height = height_update
                user_stats.age = age_update
                user_stats.bmr = bmr_update
                user_stats.save()
            else:
                Stats.objects.create(user=logged_user, weight=weight_update, height=height_update, age=age_update, bmr=bmr_update)
                
            stats = Stats.objects.get(user = logged_user)

            today = datetime.today().strftime('%Y-%m-%d')
            entries1 = Entry.objects.all()
            entries = entries1.filter(user=logged_user, date=today)


            
            sum = 0

            for entry in entries:
                sum = sum + entry.value

            ratio = 1 - (sum / stats.bmr)

            percent = (sum/stats.bmr)*100
            percent = round(percent)
            
            if ratio <= 0:
                total = 0
            else:
                total = 722.2 * ratio


            return render(request, "network/index.html",{
                    "stats":stats,
                    "entries":entries,
                    "form":ChangeDate(),
                    "date":today,
                    "total":total,
                    "percent":percent,
            })


    return render(request,"network/update.html",{
        'form':UpdateStats()
    })



@csrf_exempt
@login_required
def create_entry(request, name, amount, value, date):

    logged_user = request.user

    entry = Entry.objects.create(user=logged_user, date=date, name=name, amount=amount, value=value)

    return JsonResponse(entry.serialize(), safe=False)


@csrf_exempt
@login_required
def update_meter(request, date):
    
    logged_user = request.user
    
    entries1 = Entry.objects.all()
    entries = entries1.filter(user=logged_user, date=date)

    stats = Stats.objects.get(user = logged_user)

    sum = 0

    for entry in entries:
        sum = sum + entry.value

    ratio = 1 - (sum / stats.bmr)
    percent = (sum/stats.bmr)*100
    percent = round(percent)
            
    if ratio <= 0:
        total = 0 
    else:
        total = 722.2 * ratio

    data={
        "total":total,
        "percent":percent,
    }
    return JsonResponse(data, safe=False)




@csrf_exempt
@login_required
def change_date(request):

    logged_user = request.user

    if request.method =='POST':
        update_date = ChangeDate(request.POST)

        if update_date.is_valid():
            date1 = update_date.cleaned_data['date']

            entries1 = Entry.objects.all()
            entries = entries1.filter(user=logged_user, date=date1)

            stats = Stats.objects.get(user = logged_user)


            sum = 0

            for entry in entries:
                sum = sum + entry.value

            ratio = 1 - (sum / stats.bmr)
            percent = (sum/stats.bmr)*100
            percent = round(percent)
            
            if ratio <= 0:
                total = 0 
            else:
                total = 722.2 * ratio

            date = date1.strftime('%Y-%m-%d')

            return render(request, "network/index.html",{
                "stats":stats,
                "entries":entries,
                "form":ChangeDate(),
                "date":date,
                "total":total,
                "percent":percent,
            })



@csrf_exempt
@login_required
def remove_entry(request,ID,date):

    logged_user = request.user

    entries1 = Entry.objects.all()
    entry = entries1.get(pk=ID)
    entry.delete()

    entries2 = Entry.objects.all()
    entries = entries2.filter(user=logged_user, date=date)
    
    stats = Stats.objects.get(user = logged_user)

    sum = 0

    for entry in entries:
        sum = sum + entry.value

    ratio = 1 - (sum / stats.bmr)
    percent = (sum/stats.bmr)*100
    percent = round(percent)
    
    if ratio <= 0:
        total = 0
    else:
        total = 722.2 * ratio

    data={
        'total': total,
        'percent': percent,
    }
    return JsonResponse(data, safe=False)






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
