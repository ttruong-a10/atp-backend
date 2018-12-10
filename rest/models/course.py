from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

from rest import helpers
from rest import choices


class Course(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name="Course Title", 
        unique=True
    )
    short_name = models.CharField(
        max_length=60, 
        verbose_name="Course Short Name",
        editable=False
    )
    slug = models.SlugField(
        max_length=150, 
        editable=False
    ) 
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="courses",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        # Newly created object 
        if not self.id:
            # Append random id suffix
            self.short_name = self.name
            self.name = helpers.append_random_haiku(self.name)
            # Set slug
            self.slug = slugify(self.name)
        
        super(Course, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        
    def get_pods_list(self):
        return self.pods.all()
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', args=[self.slug])
        
    def is_owner(self, user):
        if user != self.owner:
            return False
        else:
            return True
            
    def get_pods_status_started(self):
        pods = self.pods.filter(status='started')
        number_of_started = len(pods)
        return number_of_started
        
    def get_pods_status_stopped(self):
        pods = self.pods.filter(status='stopped')
        number_of_stopped = len(pods)
        return number_of_stopped
        
    def get_pods_status_transitioning(self):
        pods = self.pods.filter(Q(status='starting') | Q(status='stopping'))
        number_of_trans = len(pods)
        return number_of_trans
        
    def get_pods_status_undeployed(self):
        pods = self.pods.filter(status='undeployed')
        number_of_undeployed = len(pods)
        return number_of_undeployed
        