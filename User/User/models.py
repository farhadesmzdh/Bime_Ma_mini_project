from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class InsuranceBranch(models.Model):
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.code


class Insurance(models.Model):
    branchCode = models.ForeignKey(InsuranceBranch, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=20)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=11)
    age = models.IntegerField()
    BMISmoking = models.BooleanField()
    smokingRatePerDay = models.IntegerField()
    BMIHookah = models.BooleanField()
    hookahRatePerDay = models.IntegerField()

    def __str__(self):
        return self.firstName + " " + self.lastName


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=15)
    insurance = models.OneToOneField(Insurance, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.user.username


