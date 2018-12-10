from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

from rest import helpers
from rest import choices


class Student(models.Model):
    first_name = models.CharField(
        max_length=100, 
    )
    last_name = models.CharField(
        max_length=100, 
        blank=True
    )
    email = models.EmailField(
        error_messages={'invalid':"Invalid email format!"}, 
        blank=True,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
            
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
        
    def get_course(self):
        course = self.pods.get().course
        return course 


class AccessToken(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True
    )
    key = models.CharField(
        max_length=64, 
        editable=False,
        unique=True
    )
    start_date = models.DateTimeField(
        blank=True, null=True
    )
    end_date = models.DateTimeField(
        blank=True, null=True
    )  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = helpers.generate_random_token(16)
        super(AccessToken, self).save(*args, **kwargs)
