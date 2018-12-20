from django.contrib import admin

from .models.pod import Pod
from .models.course import Course
from .models.blueprint import Blueprint
from .models.others import AccessToken, Student


class PodAdmin(admin.ModelAdmin):
    # readonly_fields=('slug', 'number')

    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['slug', 'number', 'blueprint']
        else:
            return ['slug', 'number']


class CourseAdmin(admin.ModelAdmin):
    readonly_fields=('owner', 'slug', 'created_at')

    # Set current user as owner
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
    

class BlueprintAdmin(admin.ModelAdmin):
    readonly_fields=('owner',)

    # Set current user as owner
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
 

class AccessTokenAdmin(admin.ModelAdmin):
    readonly_fields=('key',)


admin.site.register(Pod, PodAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(Blueprint, BlueprintAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
