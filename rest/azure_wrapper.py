import re

from .azure import *

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

