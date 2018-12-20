'''

  Custom Validators

'''
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator 

from . import azure
from .models import course

validate_alphanumerics = RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Only alphanumerics, undescore, hypens characters are allowed.')

def validate_course_name(courseName):
  # check if exists in azure
  rg = courseName
  resource_client = azure.get_client('resource')
  try:
    exists = azure.check_resource_group_exist(resource_client, rg)
  except:
    raise ValidationError('Name failed to validate with Azure')
  else:
    # Case insensitive match
    if exists or course.Course.objects.filter(name__iexact=courseName).first():
        raise ValidationError("Course name already exists. Try a different name")
        return True
    else:
      return False




