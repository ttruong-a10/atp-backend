'''
  Functions for Azure Operations

'''

import os
import traceback
import functools
import inspect

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.commerce import UsageManagementClient
from msrestazure.azure_exceptions import CloudError


### Decorators ###
def cloudError(func):
  @functools.wraps(func) # Keeps function identity
  def wrapper_handleCloudError(*args, **kwargs):
    async_result = None
    try:
      func_name = func.__name__

      print('\nRunning {}'.format(func_name))
      async_result = func(*args, **kwargs)
    except CloudError:
        print('{} Failed'.format(func_name), traceback.format_exc(), sep='\n')
        raise 
    except:
        print('{} Unknown Error'.format(func_name), traceback.format_exc(), sep='\n')
        raise
    else:
      print('{} ran successfully!'.format(func_name))
      return async_result

  return wrapper_handleCloudError

### End Decorators ###

def get_credentials():
  '''
  
  Login to Azure using Service Principal
  
  '''
  
  #subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
  #subscription_id = "6ae7c2c3-63d3-4fb6-952e-f7216b6523ab"
  subscription_id = "2b00f0fb-8864-4952-971f-86a58a102ea4"
  credentials = ServicePrincipalCredentials(
      client_id="90aff430-448c-46d9-845f-5f0f77ff99a5",
      secret="Z1BG3GbDRZppa4AXUetQOfPXssOuIVulugTNONrl9tQ=",
      tenant="91d27ab9-8c5e-41d4-82e8-3d1bf81fcb2f"
  )
  '''
  # client_id=os.environ['AZURE_CLIENT_ID'],
  # secret=os.environ['AZURE_CLIENT_SECRET'],
  # tenant=os.environ['AZURE_TENANT_ID']
  
  client_id="a2d3ba19-1033-4463-8341-1cd2377964b7",
  secret="w0OgdZjH9nbJCTx//tj8h85g5g9WN1qW6zlwCab/9oM=",
  tenant="6dc3f120-acaa-46c4-8021-413e40a3425c"
  '''
  
  return credentials, subscription_id


def get_client(client_type):
  '''
  
  Login to Azure and get requested client object
  
  '''
  
  credentials, subscription_id = get_credentials()
  
  if client_type == 'compute':
      return ComputeManagementClient(credentials, subscription_id)
  elif client_type == 'resource':
      return ResourceManagementClient(credentials, subscription_id)
  elif client_type == 'network':
      return NetworkManagementClient(credentials, subscription_id)
  elif client_type == 'storage':
      return StorageManagementClient(credentials, subscription_id)
  elif client_type == 'commerce':
      return UsageManagementClient(credentials, subscription_id)
  else:
      return None


@cloudError
def check_resource_group_exist(resource_client, rg):
  return resource_client.resource_groups.check_existence(rg)
      

@cloudError
def get_images(compute_client):
  return compute_client.images.list() 