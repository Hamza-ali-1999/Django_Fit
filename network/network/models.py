from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", blank=True, related_name="follower_list")
    following = models.ManyToManyField("User", blank=True, related_name="following_list")

    def serialize(self):
         return{
             "user": self.username,
             "email": self.email,
             "ID": self.id,
             "followers": [user.id for user in self.followers.all()],
             "following": [user.id for user in self.following.all()]
         }


class Posts(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts", null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reaction = models.ManyToManyField(User, blank=True, related_name="likes")
    post_edit = models.BooleanField(default=False)

    def serialize(self):
        return{
            "name": self.user.username,
            "id": self.id,
            "poster": self.user.email,
            "post": self.text,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.id for user in self.reaction.all()], 
            "edited": self.post_edit,
            "user_id": self.user.id
        }
    

