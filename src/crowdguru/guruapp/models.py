from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=300)

class Achievement(models.Model):
    description = models.CharField(max_length=300)

class Item(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category)


class UserDetails(models.Model):
    '''
    To hold custom User model details
    '''
    user = models.ForeignKey(User)
    email = models.CharField(blank=True, max_length=40)
    birthday = models.DateField(blank=True, null=True)
    firstname = models.CharField(blank=True, max_length=30)
    lastname = models.CharField(blank=True, max_length=30)
    bio = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=200)
    interests = models.CharField(blank=True, max_length=1000)
    # models.ManyToManyField(Category, blank=True)


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(Category)
    created_at = models.DateTimeField(default=timezone.now)
    preferences = models.CharField(max_length=1000) # JSON list of strings
    tags = models.CharField(max_length=500) # JSON list of strings
    is_resolved = models.BooleanField()

    def get_absolute_url(self):
        return '/question/%i' % self.id

    def __str__(self):
        return '[{}] {} by {}'.format(self.category.name, self.title, self.author.username)

class Recommendation(models.Model):
    question = models.ForeignKey(Question)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User)
    recommendation = models.TextField()
    is_star = models.BooleanField()


class QuestionVote(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    value = models.IntegerField() # either -1 or 1

class RecommendationVote(models.Model):
    user = models.ForeignKey(User)
    recommendation = models.ForeignKey(Recommendation)
    value = models.IntegerField() # either -1 or 1

class QuestionSpamVote(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)

class RecommendationSpamVote(models.Model):
    user = models.ForeignKey(User)
    recommendation = models.ForeignKey(Recommendation)
