from .models import *
from django.db.models import Q

def searchProjects(request):
    search_query = ''
    if request.GET.get('search'):
        search_query = request.GET.get('search')
    tags = Tag.objects.filter(Q(name__icontains=search_query))
    projects = Post.objects.distinct().filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(tags__in=tags) | Q(owner__name__icontains=search_query))

    return projects
