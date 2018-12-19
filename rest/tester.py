from . import azure


def test1():
  client = azure.get_client('resource')

  rg = 'ADC414P2_softdew'

  result = azure.check_resource_group_exist(client, rg)
  print(result)