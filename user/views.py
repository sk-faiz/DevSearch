from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .forms import *

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'user/login_registration.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out successfully')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account created successfully ')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'user/login_registration.html',context)

def profile(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'user/profiles.html', context)

def profile_detail(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.filter(description__isnull=False)[:3]
    other_skills = profile.skill_set.filter(description__isnull=True)
    project = profile.post_set.all()
    context = {'profile': profile, 'top_skills': top_skills, 'other_skills': other_skills, 'projects': project}
    return render(request, 'user/user-profile.html', context)

@login_required(login_url='login')
def userAccounts(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    project = profile.post_set.all()
    context = {'profile': profile, 'skills': skills,'projects': project}
    return render(request, 'user/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request,'Account deleted successfully')
            return redirect('account')
    profile = request.user.profile
    skills = profile.skill_set.all()
    project = profile.post_set.all()
    context = {'profile': profile, 'skills': skills,'projects': project, 'form': form}
    return render(request, 'user/profile_form.html', context) 

@login_required(login_url='login')
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request,'Skill added successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'user/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.info(request,'Skill updated successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'user/skill_form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.info(request,'Skill deleted successfully')
        return redirect('account')
    context = {'object': skill, 'label': skill.name}
    return render(request, 'social/delete_form.html', context)
             
