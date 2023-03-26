from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import PostForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import *
from django.contrib import messages

def project(request):
    projects = searchProjects(request)
    context = {'projects': projects}
    return render(request, 'social/projects.html', context)

def projectDetail(request, id):
    projects = Post.objects.get(id=id)
    tags = projects.tags.all()
    reviewform = ReviewForm()
    if request.method == 'POST':
        reviewform = ReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.owner = request.user.profile
            review.project = projects
            review.save()
            projects.getVoteCount
            messages.success(request, 'Your review was successfully submitted')
            return redirect('projectDetail', id=projects.id)
    context = {'project': projects, 'tags': tags, 'reviewform': reviewform}
    return render(request, 'social/single-project.html', context)

@login_required(login_url='login')
def createPost(request):
    user = request.user.profile
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'social/project_form.html', context)

@login_required(login_url='login')
def updatePost(request, postId):
    profile = request.user.profile
    project = profile.post_set.get(id=postId)
    form = PostForm(instance=project)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'social/project_form.html', context)

@login_required(login_url='login')
def deletePost(request, postId):
    profile = request.user.profile
    project = profile.post_set.get(id=postId)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'form': project, 'label': project.title}
    return render(request, 'social/delete_form.html', context)


def createReview(request, postId):
    profile = request.user.profile
    project = Post.objects.get(id=postId)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.owner = profile
        review.post = project
        review.save()
        return redirect('project-detail', id=project.id)
    context = {'form': form}
    return render(request, 'social/single-project.html', context)