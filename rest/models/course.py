from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Q

from rest import helpers
from rest import choices

from rest.validators import validate_course_name, validate_alphanumerics 



class Course(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name="Course Title", 
        unique=True,
        validators=[ validate_alphanumerics, validate_course_name  ]
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
            # Set slug
            self.slug = slugify(self.name)
        
        super(Course, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        
    def get_total_number_pods(self):
        return len(self.pods.all())
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', args=[self.slug])
        
    def is_owner(self, user):
        if user != self.owner:
            return False
        else:
            return True
            
    def get_pod_statuses(self):
        status = {
          'started': len(self.pods.filter(status='started')),
          'stopped': len(self.pods.filter(status='stopped')),
          'processing': len(self.pods.filter(Q(status='starting') | Q(status='stopping'))),
          'undeployed': len(self.pods.filter(status='undeployed'))
        }
        return status
        
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
        