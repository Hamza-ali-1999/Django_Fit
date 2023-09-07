from django.contrib.auth.models import AbstractUser
from django.db import models
from embed_video.fields import EmbedVideoField


class User(AbstractUser):
    pass

class Stats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_stats", null=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField()
    bmr = models.IntegerField()

    def serialize(self):
         return{
              "ID": self.user.id,
              "weight":self.weight,
              "height":self.height,
              "age":self.age,
              "bmr":self.bmr,
         }

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_entries", null=True)
    date = models.DateField()
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    value = models.IntegerField()

    def serialize(self):
        return{
            "date":self.date,
            "name":self.name,
            "amount":self.amount,
            "value":self.value,
            "id":self.id
        }
    
class Workout(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_creator", null=True)
    savers = models.ManyToManyField(User, blank=True, related_name="workout_savers")
    publc = models.BooleanField(default=False)
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = EmbedVideoField()
    
    def serialize(self):
        return{
            "savers": self.savers,
        }
    
    
    def __unicode__(self):
        return self.link
    