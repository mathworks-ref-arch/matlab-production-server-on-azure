import unittest
import os
import time
import re
import requests
import random
import sys
from datetime import date
import datetime

import cloud_deployment_testtools.AzureAuthentication as AzureAuth
import cloud_deployment_testtools.deploy as DeployOp
from azure.mgmt.network import NetworkManagementClient

def main(tenant_id_arg, client_id_arg, client_secret_arg, subscription_id_arg, username, password, ipAddress, base64certdata, base64password, location_arg, platform_arg):

    # Deploy template
    # Reference architecture in production.
    ref_arch_name = 'matlab-production-server-on-azure'

    # Common parameters for template deployment.
    tenant_id = tenant_id_arg
    client_id = client_id_arg
    client_secret = client_secret_arg
    subscription_id = subscription_id_arg
    location = location_arg

    # Subnets & virtual network info
    subnets_cidr = ['10.0.0.0/24', '10.0.1.0/24']
    vnet_cidr = '10.0.0.0/16'

    # Resource group where virtual network is created
    resource_name_vnet = 'vnet_resource_group'

    # Deploy a resource group with a virtual network and specified number of subnets
    try:
          subnet_names, vnet_name = DeployOp.create_vnet(credentials,
                                                        subscription_id,
                                                        location,
                                                        subnets_cidr,
                                                        resource_name_vnet,
                                                        vnet_cidr)

    except Exception as e:
        raise(e)
    print(subnet_names[0])
    print(subnet_names[1])
    # Parameters for deployment
    parameters = {
       "adminUsername": username,
       "adminPassword": password,
       "Allow connections from": "0.0.0.0/0",
       "Platform": platform_arg,
       "NewOrExistingVirtualNetwork": "existing",
       "VirtualNetworkName": vnet_name,
       "Subnet1": subnet_names[0],
       "Subnet2": subnet_names[1],
       "Subnet1CIDRRange": subnets_cidr[0],
       "Subnet2CIDRRange": subnets_cidr[1],
       "ResourceGroupNameOfVirtualNetwork": resource_name_vnet,
       "CertificateInputType": "Base64-encoded PFX Certificate",
       "Base64EncodedPFXCertificateData": base64certdata,
       "PasswordForBase64EncodedPFXCertificate": base64password
    }

    print(parameters)

    # Find latest MATLAB release from Github page and get template json path.
    res = requests.get(
        f"https://github.com/mathworks-ref-arch/{ref_arch_name}/blob/master/releases/"
    )

    latest_releases = [re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-1], re.findall("releases/(R\d{4}[ab]\\b)", res.text)[-2]]
    for i in range(2):
        matlab_release = latest_releases[i]
        print("Testing Health Check Release: " + matlab_release + "\n")
        github_base_dir = "https://raw.githubusercontent.com/mathworks-ref-arch"
        jsonpath = f"{matlab_release}/templates/azuredeploy{matlab_release[3:]}.json"
        template_name = f"{github_base_dir}/{ref_arch_name}/master/releases/{jsonpath}"
        resource_group_name = "mps-refarch-health-check-existing-vnet" + matlab_release + date.today().strftime('%m-%d-%Y') + str(random.randint(1,101))
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
            raise(e)
        finally:
            # Delete the deployment which is deployed using existing virtual network
            deployment_deletion = DeployOp.delete_resourcegroup(credentials, subscription_id, resource_group_name)
            print("Deleted the deployment which is deployed using existing virtual network")
            # Wait for above deployment deletion
            time.sleep(900)
            # Delete deployment with virtual network
            DeployOp.delete_resourcegroup(credentials, subscription_id, resource_name_vnet)
            print("Deleted the deployment which contains the virtual network")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
