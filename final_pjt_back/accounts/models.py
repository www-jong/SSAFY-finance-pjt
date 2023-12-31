from django.db import models
from django.contrib.auth.models import AbstractUser
import os


def user_directory_path(instance, filename):
    # instance.username을 사용하여 경로 생성
    return f'profile_images/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    age = models.IntegerField()
    birth = models.DateField()  # 생년월일 필드
    capital = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    permission = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username

