'''

  Custom Validators

'''
from django.core.exceptions import ValidationError

from . import azure


def validate_course_name(courseName):
  rg = courseName
  resource_client = azure.get_client('resource')
  exists = azure.check_resource_group_exist(resource_client, rg)
  if exists:
      raise ValidationError("Course name already exists. Try a different name")