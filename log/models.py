from django.db import models
from user.models import User


class Log(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.TextField()

