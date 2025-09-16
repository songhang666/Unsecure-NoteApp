from django.db import models
from django.contrib.auth.models import User

class RegistrationCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ResetPasswordCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)