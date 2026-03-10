import os
import sys
import time
import requests
import random
import traceback
from datetime import date
import datetime
import cloud_deployment_testtools.AzureAuthentication as AzureAuth
import cloud_deployment_testtools.git_utils as git_utils
import cloud_deployment_testtools.deploy as DeployOp


def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, base64certdata, base64password, location_arg, platform_arg, git_token):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-azure'
    branch_name = git_utils.get_current_branch()
    
    # Common parameters for template deployment.
    tenant_id = tenant_id_arg
    client_id = client_id_arg
    client_secret = client_secret_arg
    subscription_id = subscription_id_arg
    location = location_arg
    ipAddress = requests.get("https://api.ipify.org").text + "/32"
    
    parameters = {
        "adminUsername": username,
        "adminPassword": password,
        "Allow connections from": ipAddress,
        "Platform": platform_arg,
        "CertificateInputType": "Base64-encoded PFX Certificate",
        "Base64EncodedPFXCertificateData": base64certdata,
        "PasswordForBase64EncodedPFXCertificate": base64password
    }
    
    # With a GitHub token
    headers = {
        'Authorization': f'token {git_token}'
    }
    
    # Use GitHub API which has clearer rate limits
    api_url = f"https://api.github.com/repos/mathworks-ref-arch/{ref_arch_name}/contents/releases?ref={branch_name}"
    res = requests.get(api_url, headers=headers)
    
    if res.status_code != 200:
        print(f"Error fetching releases from GitHub API: {res.status_code}")
        print(f"Response: {res.text}")
        raise Exception(f"Failed to fetch releases from GitHub API")
    
    files = res.json()
    # Extract release names from file names and sort to get latest
    releases = sorted([f['name'] for f in files if f['name'].startswith('R')], reverse=True)
    
    if len(releases) < 2:
        print(f"Warning: Found only {len(releases)} release(s). Expected at least 2.")
    
    # Get the two latest releases
    latest_releases = releases[:2]
    
    for matlab_release in latest_releases:
        print(f"Testing Health Check Release: {matlab_release}\n")
        
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        jsonpath = f"{matlab_release}/templates/azuredeploy{matlab_release[3:]}.json"
        template_name = f"{github_base_dir}/{ref_arch_name}/{branch_name}/releases/{jsonpath}"
        resource_group_name = f"mps-refarch-health-check-{matlab_release}{date.today().strftime('%m-%d-%Y')}{random.randint(1,101)}"
        
        ct = datetime.datetime.now()
        print(f"Date time before deployment of stack: {ct}")
        
        credentials = AzureAuth.authenticate_client_key(tenant_id, client_id, client_secret)
        
        try:
            print("Deploying the resource group")
            deployment_result = DeployOp.deploy_production_template(
                credentials,
                subscription_id,
                resource_group_name,
                location,
                ref_arch_name,
                template_name,
                parameters
            )
            print("Success deploying the resource group")
        except Exception as e:
            print(f"Error deploying resource group: {e}")
            traceback.print_exc()
            raise e
        finally:
            # Delete the deployment
            print(f"Deleting the resource group: {resource_group_name}")
            DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
            print("Success deleting the resource group\n")
            ct = datetime.datetime.now()
            print(f"Date time after deployment and deletion of stack: {ct}")


if __name__ == '__main__':
    if len(sys.argv) < 12:
        print("Error: Missing required arguments")
        print("Usage: python script.py <tenant_id> <client_id> <client_secret> <subscription_id> <username> <password> <base64certdata> <base64password> <location> <platform> <git_token>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
