from configparser import MAX_INTERPOLATION_DEPTH
from lib2to3.pytree import Node
import re
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    content = models.CharField(max_length=200, default=None)
    time = models.DateTimeField(auto_now_add=True)  
    like = models.IntegerField(default=0)

    def __str__(self):
        return (f" {self.content} by {self.user} on {self.time} total likes = {self.like}")

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="text")

    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return f"{self.post} liked by {self.user}"
    
class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower', default=None)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following', default=None)

    class Meta:
        unique_together = (('follower', 'following'),)
    def __str__(self):
            return f"{self.follower} is following {self.following}"




