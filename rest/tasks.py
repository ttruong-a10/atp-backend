from __future__ import absolute_import, unicode_literals

from celery import shared_task, task, group, current_task
# from msrestazure.azure_exceptions import CloudError

# from .models.pod import Pod
# from .models.course import Course
from . import choices
from .models.pod import Pod
from .models.course import Course
from .models.others import VmSize
from .azure_wrapper import get_filtered_vm_sizes, update_pod_status
from .serializers import VmSizeSerializer


'''
@task
def task_pod_stop_reminder(pod_name):
    pod = Pod.objects.get(name=pod_name)
    task_id = current_task.request.id
    
    try:
        vhelpers.pod_azure_stop_reminder(pod) 
    except Exception:
        task_found = Task.objects.get(task_id=task_id)
        task_found.delete()
        raise
    else:
        print("Stop reminder executed ssuccessfully")
   
    # delete task from db
    task_found = Task.objects.get(task_id=task_id)
    task_found.delete()
    
    return task_pod_stop.request.id 

@task
def task_pod_stop(pod_name):
    pod = Pod.objects.get(name=pod_name)
    task_id = current_task.request.id
    
    try:
        vhelpers.pod_azure_stop(pod) 
    except Exception:
        task_found = Task.objects.get(task_id=task_id)
        task_found.delete()
        raise
    else:
        print("Pod stopped successfully")
    
    # delete task from db
    task_found = Task.objects.get(task_id=task_id)
    task_found.delete()
    
    return task_pod_stop.request.id 
      
      
@task
def task_pod_start(pod_name):
    pod = Pod.objects.get(name=pod_name)
    task_id = current_task.request.id
    
    try:
        vhelpers.pod_azure_start(pod)
    except Exception:
        task_found = Task.objects.get(task_id=task_id)
        task_found.delete()
        raise
    else:
        print("Pod started successfully")
        
    # delete task from db
    task_found = Task.objects.get(task_id=task_id)
    task_found.delete()
    
    return task_pod_start.request.id 
'''
      
      
##################################################
######### PERIODIC TASKS
#####

@task
def sync_azure_vm_sizes_to_db():
    
    ## Destroy old data first !!!
    VmSize.objects.all().delete()
    
    ## Fetch and write new data
    for location, dummy in choices.CLOUD_REGION:
        vm_sizes_available_in_sku = get_filtered_vm_sizes(location);
        for vm_size in vm_sizes_available_in_sku:
            serializer = VmSizeSerializer(data=vm_size)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
@task
def sync_all_vm_status_in_db():
    queryset = Pod.objects.all()
    
    for pod in queryset:
        update_pod_status(pod)
        