from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("Your tweet has been posted"))
                return redirect('home')
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, "home.html", {"tweets": tweets, "form": form})
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, "home.html", {"tweets": tweets})

def ProfileList(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to use this page"))
        return redirect('home')

def UserProfile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk) 
        tweets = Tweet.objects.filter(user_id = pk) 

        # post form logic 
        if request.method == 'POST':
            # get current user id
            curr_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # decide to follow or unfollow 
            if action == 'unfollow':
                curr_user_profile.follows.remove(profile)
            elif action == 'follow':
                curr_user_profile.follows.add(profile)
            # save profile 
            curr_user_profile.save()
        return render(request, 'profile.html', {"profile": profile, "tweets": tweets}) 
    else:
        messages.success(request, ("You must be logged in to use this page"))
        return redirect('home')

def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!  Get MEEPING!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out"))
    return redirect('home')

def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            # log in user
            user = authenticate(username= username, password=password)
            login(request, user)
            messages.success(request, ("You've Successfully registered, Welcome!"))
            return redirect('home')
    return render(request, 'register.html', {'form': form})