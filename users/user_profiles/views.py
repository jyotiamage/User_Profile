from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, get_user_model,logout
from django.contrib.auth import login as dj_login
from .form import UserLoginForm, SignUpForm, UserForm, ProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import update_session_auth_hash
#from django.core.mail import send_mail, BadHeaderError
# Create your views here.

def signup_view(request):
    title="Signup"
    print(request.method)
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username = form.cleaned_data.get('username'),
            password = form.cleaned_data.get('password1'), email=form.cleaned_data.get('email'),
            is_staff=form.cleaned_data.get('is_staff'), is_superuser=form.cleaned_data.get('is_superuser'))
            user.save()
            user= authenticate(username=username, password=password)
            dj_login(request, user)
            return show_home(request,user)
    form = SignUpForm()
    return render(request, 'signup.html',{'form':form,"title":title})

def show_home(request,user):
    try:
        if user.is_staff and user.is_superuser and user.is_active:
            return HttpResponseRedirect("/user/"+request.user.username+"/home")
        return HttpResponseRedirect("/user/user_profile/"+request.user.username)
    except  RelatedObjectDoesNotExist:
        return HttpResponseRedirect("/user/edit_profile/"+request.user.username)

def login_view(request):
    title ="Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user= authenticate(username=username, password=password)
        dj_login(request, user)
        return show_home(request,user)
    return render(request,"login.html",{"form":form,"title":title})

@login_required(login_url="/user/login")
def logout_view(request,username):
    logout(request)
    return HttpResponseRedirect("/user/login")

def get_users(request):
    users= User.objects.all()
    return render(request,"error.html", {"users":users})

@login_required(login_url="/user/login")
def changePassword_view(request, username):
    title="Change Password"
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            user=User.objects.get(username=username)
            if user.is_staff or user.is_superuser:
                return get_users(request)

            user.set_password(form.cleaned_data['password1'])
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect("/user/user_profile/"+user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        if "cancel" in request.GET:
            return HttpResponseRedirect("/user/user_profile/"+request.user.username)
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {
        'form': form,'title':title
    })


@login_required(login_url="/user/login")
def admin_view(request,username):
    users= User.objects.all()
    return render(request, "admin.html",{"users":users})

@login_required(login_url="/user/login")
def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, "profile_user.html", {"user":user})

@login_required(login_url="/user/login")
def update_profile(request, username):
    if request.method == 'POST':
        user=User.objects.get(username=username)
        if "cancel" in request.POST:
            if user.is_staff or user.is_superuser:
                return HttpResponseRedirect("/user/"+user.username+"/home")
            return  HttpResponseRedirect("/user/user_profile/"+user.username)
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST,  request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            print("Inside form valid")
            user_form.save(commit=True)
            profile_form.save(commit=True)
            messages.success(request, 'Your profile was successfully updated!')
            return  HttpResponseRedirect("/user/user_profile/"+user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:

        if "cancel" in request.GET and (request.user.is_superuser or request.user.is_staff):
            return  HttpResponseRedirect("/user/"+request.user.username+"/home")

        elif "cancel" in request.GET:
            return  HttpResponseRedirect("/user/user_profile/"+request.user.username)

        elif "edit" in request.GET and (request.user.is_superuser or request.user.is_staff):
            user=User.objects.get(username=username)
            if (user.is_staff or user.is_superuser) and user.username!=request.user.username:
                return get_users(request)
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=user.profile)
            request.user.username=user.username
            return render(request, 'profile.html', {
                'user_form': user_form,
                'profile_form': profile_form,
            })
        else:

            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            return render(request, 'profile.html', {
                'user_form': user_form,
                'profile_form': profile_form,

            })
