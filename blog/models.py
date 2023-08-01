from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    body = models.TextField()
    created = models.DateTimeField(
        verbose_name='Время создания', auto_now_add=True)

    def __str__(self):
        return self.title
