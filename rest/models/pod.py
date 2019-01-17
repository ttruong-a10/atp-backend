from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete


from rest import helpers
from rest import choices
from .others import AccessToken


class Pod(models.Model):
    name = models.CharField(
        max_length=60, 
        verbose_name='Pod Name',
        unique=True
    ) 
    slug = models.SlugField(
        max_length=150, 
        editable=False
    )
    number = models.IntegerField(
        editable=False
    )
    course = models.ForeignKey(
        'Course', 
        on_delete=models.CASCADE, 
        related_name="pods"
    )
    location = models.CharField(
        max_length=50, 
        verbose_name='Cloud Region',
    ) 

    vm_size = models.CharField(
        max_length=100, 
        blank=True, null=True,
        verbose_name="Azure VM Size"
    )
    image_src = models.CharField(
        max_length=300, 
        blank=True, null=True,
        verbose_name="Azure Image"
    )
    allow_internet_outbound = models.BooleanField(
        default=False,
        verbose_name="Allow Outbound Internet Access"
    )
    blueprint = models.ForeignKey(
        'Blueprint',
        on_delete=models.SET_NULL,
        related_name='pod',
        null=True
    )

    status = models.CharField(
        max_length=100,
        choices=choices.STATUS, 
        default='undeployed'
    )
    public_ip = models.GenericIPAddressField(
        blank=True, null=True, 
        verbose_name='Public IP Address'
    )
    hostname = models.CharField(
        max_length=150, 
        verbose_name='Hostname',
        blank=True, null=True
    )
    next_stop = models.DateTimeField(
        blank=True, null=True
    )
    access_token = models.ForeignKey(
        'AccessToken',
        on_delete=models.SET_NULL,
        related_name='pod',
        blank=True,null=True
    )
    student = models.ForeignKey(
        'Student', 
        on_delete=models.SET_NULL,
        related_name='pods',
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Newly created object
        if not self.id:
             # Append random id suffix
            # self.name = helpers.append_random_haiku(self.name)
            # Set slug
            self.slug = slugify(self.name)
            # Iterate pod number
            self.number = helpers.iterate_pod_number(self.course)
            # Generate random access token
            if not self.access_token:
                new_token = AccessToken.objects.create(name=self.name)
                self.access_token = new_token 
        super(Pod, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.name
        
    def get_short_name(self):
        return self.name.split("_")[-1]

    def update_status(self, status):
        self.status = status
        self.save()
        return status
        

# This allows the related object to be deleted when Pod is deleted
@receiver(post_delete, sender=Pod)
def post_delete_student(sender, instance, *args, **kwargs):
    if instance.student: # just in case student is not specified
        instance.student.delete()

# This allows the related object to be deleted when Pod is deleted
@receiver(post_delete, sender=Pod)
def post_delete_access_token(sender, instance, *args, **kwargs):
    if instance.access_token: # just in case student is not specified
        instance.access_token.delete()