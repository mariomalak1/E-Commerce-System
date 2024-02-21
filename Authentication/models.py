from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from project.settings import AUTH_USER_MODEL
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True, )
    username = None
    USERNAME_FIELD = "email"


class ResetPassword(models.Model):
    user_ = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    generatedCode = models.CharField(max_length=15)
    sendTime = models.DateTimeField()
    confirmedTime = models.DateTimeField(null=True, blank=True)



    def isCodeExpired(self):
        quaterHour = timedelta(minutes=15)
        timeNow = datetime.now()
        print(self.confirmedTime)
        if timeNow >= self.sendTime + quaterHour:
            return True
        return False
