from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import uuid


class Country(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        db_table = 'countries'


class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='profile_avatars/')


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)


class Contact(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = 'Contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return self.user.get_full_name()
