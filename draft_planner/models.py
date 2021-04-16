from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your models here.
class draft_plan(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    draftname = models.CharField(max_length=40)
    generation = models.CharField(max_length=10)
    associatedleague = models.IntegerField(null=True)
    team=ArrayField(models.CharField(max_length=50),null=True)
