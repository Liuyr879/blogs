from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    enabled = models.BooleanField(default=False)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'


class Category(models.Model):
    title = models.TextField()
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'
