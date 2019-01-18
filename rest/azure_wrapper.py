import re
import os
import json

from django.conf import settings

from .azure import *

def get_template_json(filename):
    template_path = os.path.join(settings.AZ_TEMPLATE_DIR, filename )
    with open(template_path, 'r') as template_file_fd:
        template = json.load(template_file_fd)    
    return template

def get_filtered_vm_sizes(location):
    '''
        Retrieve vm sizes base on location.
        Then filter using regex for D series.
        Then get price for filtered sizes from rate card
    '''

    compute_client = get_client('compute')
    
    regex_Dv3 = "Standard_D[^sS]*v3"
    regex_D1v2 = "Standard_D1_v2"
    
    vm_sizes = get_vm_sizes_by_location(compute_client, location)
    vm_sizes_filtered = list(filter(
        lambda x: re.match(regex_Dv3, x.name) or re.match(regex_D1v2, x.name), 
        vm_sizes))
    skus_in_location = get_skus_by_location(compute_client, location)
  
    # Filter for specific nested-enabled sizes and is available in sku
    vm_sizes_available_in_sku = []
    for size in vm_sizes_filtered:
        found_sku = next((x for x in skus_in_location if size.name==x.name and not x.restrictions), None)
        if found_sku:
            new_size_name = size.name + ' VM'
            
            memory_in_mb = size.memory_in_mb
            memory_in_gb = int(memory_in_mb)/1000
            
            size_dict = {
                "name": size.name, 
                "location": location,
                "vcpu": size.number_of_cores,
                "memory_gb": memory_in_gb,
            }
        
            vm_sizes_available_in_sku.append(size_dict) 
            
    return vm_sizes_available_in_sku


def generate_dns_prefix(string):
    ''' 
        Azure requires DNS names to be 0-63 characters long and
        allows only lowercase alphumerics and hypens. 
    '''
    return string.lower().replace('_', '-')[0:60]


def generate_fqdn(vm_name, location):
        dns_prefix = generate_dns_prefix(vm_name)
        fqdn = "{}.{}.cloudapp.azure.com".format(dns_prefix, location)
        return fqdn


def update_pod_status(pod):
    compute_client = get_client('compute')
    network_client = get_client('network')
    rg = pod.course.name
    vm_name = pod.name
    public_ip = pod.name + '-publicip'
    
    vm_status = get_vm_status(compute_client, rg, vm_name)
    
    if pod.status != vm_status and vm_status != 'not_found' and vm_status !='undeployed':
        if vm_status == 'started':
            # Get FQDN and Public IP
            public_ip_name = pod.name + '-publicip'
            fqdn = get_vm_fqdn(network_client, rg, public_ip_name)
            public_ip = get_vm_public_ip(network_client, rg, public_ip_name)

            # Update DB
            pod.refresh_from_db()
            pod.hostname = fqdn
            pod.public_ip = public_ip
            
        pod.status = vm_status
        pod.save()

def startPod(pod):
    rg = pod.course.name
    compute_client = get_client('compute')

    ## If pod has already been deployed, just start the pod
    if pod.status not in ['undeployed', 'started']:
        start_vm(compute_client, rg, pod.name) 
        pod.update_status('starting')

         
    ## Else create and start pods
    elif pod.status == 'undeployed':
        # Create pod
        resource_client = get_client('resource')
        params = {
            'trainerId': pod.course.owner.username,
            'virtualMachineName': pod.name, 
            'location': pod.location,
            'imageId': pod.image_src,
            'virtualMachineSize': pod.vm_size,
            'dnsLabelPrefix': generate_dns_prefix(pod.name),
            'allowInternetOutbound': pod.allow_internet_outbound
        }
        
        create_vm_from_template(compute_client,resource_client, rg, params) 
        pod.update_status('starting')


        
def stopPod(pod):
    rg = pod.course.name
    compute_client = get_client('compute')

    if pod.status not in ['undeployed', 'stopped'] :
        stop_vm(compute_client, rg, pod.name)
        # clear IP Address
        pod.refresh_from_db()
        pod.next_stop = None
        pod.public_ip = None
        pod.save()
        pod.update_status('stopping')


def restartPod(pod):
    rg = pod.course.name
    compute_client = get_client('compute')

    if pod.status not in ['undeployed', 'stopped', 'stopping'] :
        restart_vm(compute_client, rg, pod.name)
        pod.update_status('restarting')
