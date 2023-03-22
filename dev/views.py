from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Review, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def project(request):
    projects = Post.objects.all()
    context = {'projects': projects}
    return render(request, 'social/projects.html', context)

def projectDetail(request, id):
    projects = Post.objects.get(id=id)
    tags = projects.tags.all()
    context = {'project': projects, 'tags': tags}
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