from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your models here.
class bot_message(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="sender")
    recipient = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="recipient")
    message = models.CharField(max_length=1000)
    