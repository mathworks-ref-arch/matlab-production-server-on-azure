from azure.common import credentials
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
import adal

def authenticate_client_key(tenant_id, client_id, client_secret):

    """
    Authenticate using service principal w/ key.
    """
    authority_host_uri = 'https://login.microsoftonline.com'
    authority_uri = authority_host_uri + '/' + tenant_id
    resource_uri = 'https://management.core.windows.net/'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)
    credentials = ClientSecretCredential(tenant_id, client_id, client_secret)

    return credentials