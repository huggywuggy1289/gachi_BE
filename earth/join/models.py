from django.db import models
from users.models import User

# Create your models here.
class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     tutorial_completed = models.BooleanField(default=False)