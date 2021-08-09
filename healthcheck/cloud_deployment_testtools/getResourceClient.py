from azure.mgmt.resource import ResourceManagementClient

def get_resource_client(credentials, subscription_id) : 
    resource_client = ResourceManagementClient(credentials, subscription_id, "2019-05-01")
    return resource_client
