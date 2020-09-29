import os
import sys
import time
import re
import requests
import random

import cloud_deployment_testtools.AzureAuthentication as AzureAuth
import cloud_deployment_testtools.deploy as DeployOp

from datetime import date

def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, ipAddress):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-azure'

    # Common parameters for template deployment.
    tenant_id = tenant_id_arg
    client_id = client_id_arg
    client_secret = client_secret_arg
    credentials = AzureAuth.authenticate_client_key(tenant_id, client_id, client_secret)
    subscription_id = subscription_id_arg

    parameters = {
        "adminUsername": username,
        "adminPassword": password,
        "Allow connections from": ipAddress,
        "Platform": "Linux"
    }

    location = 'eastus'
    resource_group_name = "mps-refarch-health-check-" + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))

    # Find latest MATLAB release from Github page and get template json path.
    res = requests.get(
        f"https://github.com/mathworks-ref-arch/{ref_arch_name}/blob/master/releases/"
    )
    matlab_release = re.findall("master/releases/(R\d{4}[ab]\\b)", res.text)[-1]
    github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
    jsonpath = f"{matlab_release}/templates/azuredeploy{matlab_release[3:]}.json"
    template_name = f"{github_base_dir}/{ref_arch_name}/master/releases/{jsonpath}"
    
    try:
        DeployOp.deploy_production_template(credentials,
                                            subscription_id,
                                            resource_group_name,
                                            location,
                                            ref_arch_name,
                                            template_name,
                                            parameters
                                            )
    except Exception as e:
        raise (e)

   
    # delete the deployment
    DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])