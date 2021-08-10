from azure.mgmt.resource import ResourceManagementClient

def get_resource_client(credentials, subscription_id) : 
    resource_client = ResourceManagementClient(credentials, subscription_id)
    return resource_client
