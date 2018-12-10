from django.db import models
from django.contrib.auth.models import User

from rest import choices


class Blueprint(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name='Blueprint Name',
        unique=True
    ) 
    cloud_region = models.CharField(
        max_length=100, 
        choices=choices.CLOUD_REGION, 
        blank=True, null=True
    )
    vm_size = models.CharField(
        max_length=100, 
        blank=True, null=True,
        verbose_name='Azure VM Size'
    )
    image_id = models.CharField(
        max_length=300, 
        blank=True, null=True,
        verbose_name='Azure Image'
    )
    allow_internet_outbound = models.BooleanField(
        default=False,
        verbose_name='Allow Outbound Internet Access'
    )
    owner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name="blueprints",
        null=True,editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.name

    