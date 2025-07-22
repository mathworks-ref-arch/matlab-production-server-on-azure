import os
import sys
import time
import re
import requests
import random
import traceback
from datetime import date
import datetime

import cloud_deployment_testtools.AzureAuthentication as AzureAuth
import cloud_deployment_testtools.deploy as DeployOp

def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, base64certdata, base64password, location_arg, platform_arg):
    # Reference architectures in production.
    ref_arch_name = 'matlab-production-server-on-azure'

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

    # Find latest MATLAB release from Github page and get template json path.
    res = requests.get(
        f"https://github.com/mathworks-ref-arch/{ref_arch_name}/blob/master/releases/"
    )

    latest_releases = [
        re.findall(r"releases/(R\d{4}[ab]\b)", res.text)[-1],
        re.findall(r"releases/(R\d{4}[ab]\b)", res.text)[-2]
    ]
    for i in range(2):
        matlab_release = latest_releases[i]
        print("Testing Health Check Release: " + matlab_release + "\n")
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        jsonpath = f"{matlab_release}/templates/azuredeploy{matlab_release[3:]}.json"
        template_name = f"{github_base_dir}/{ref_arch_name}/master/releases/{jsonpath}"
        resource_group_name = "mps-refarch-health-check-" + matlab_release + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))
        ct = datetime.datetime.now()
        print("Date time before deployment of stack:-", ct)
        credentials = AzureAuth.authenticate_client_key(tenant_id, client_id, client_secret)
        try:
            deployment_result = DeployOp.deploy_production_template(credentials,
                                                   subscription_id,
                                                   resource_group_name,
                                                   location,
                                                   ref_arch_name,
                                                   template_name,
                                                   parameters
                                                   )
        except Exception as e:
            raise (e)
        finally:
            # delete the deployment
            DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
            ct = datetime.datetime.now()
            print("Date time after deployment and deletion of stack:-", ct)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
