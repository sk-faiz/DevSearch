from django.db import models

# Create your models here.

from user.models import Profile

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=200, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_count = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_count', '-created_at']

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set
    
    @property
    def getVoteCount(self):
        review = self.review_set.all()
        upvotes = review.filter(value='up').count()
        total = review.count()
        ratio = (upvotes / total) * 100
        self.vote_count = total
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value + ' - ' + self.project.title


