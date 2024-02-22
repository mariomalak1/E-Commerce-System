from datetime import datetime, timedelta
import random
import string

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    suspend = models.BooleanField(null=True, blank=True, default=False)
    USERNAME_FIELD = "email"
    # first_name = None
    # username = None

class ResetCode(models.Model):
    user_ = models.ForeignKey(User, on_delete=models.CASCADE)
    generatedCode = models.CharField(max_length=15)
    sendTime = models.DateTimeField(default=datetime.now)
    confirmedTime = models.DateTimeField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:  # Check if the object is newly created
            generated_code = ResetCode.generateUniqueCode()
            while generated_code:
                if ResetCode.objects.filter(generatedCode=generated_code).first():
                    generated_code = ResetCode.generateUniqueCode()
                else:
                    break
            self.generatedCode = generated_code
        super(ResetCode, self).save(*args, **kwargs)

    @staticmethod
    def generateUniqueCode():
        code = ''
        for i in range(6):
            code += random.choice(string.digits)
        return code


    # to check that is passed 15 min from time of sned code
    def isCodeExpired(self):
        timeNow = datetime.now()
        quaterHour = timedelta(minutes=15)
        if timeNow >= self.sendTime + quaterHour:
            return True
        return False

        # if self.confirmedTime:
        #     if timeNow >= self.confirmedTime + quaterHour:
        #         return True