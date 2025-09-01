from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following")
    online = models.BooleanField(default=True, blank=False)


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=False)
    likes = models.ManyToManyField("User", default=0, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "likes": [user.username for user in self.likes.all()],
            "likes_count": self.likes.count(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }