from django.db import models
from user.models import User


class Log(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.TextField()

