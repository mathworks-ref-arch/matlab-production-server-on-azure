# MATLAB Production Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Linked to a [MathWorks Account](https://www.mathworks.com/mwaccount/).
    - Concurrent license type. To check your license type, see [MathWorks License Center](https://www.mathworks.com/licensecenter/). 
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server License for Use on the Cloud](https://www.mathworks.com/help/mps/server/configure-matlab-production-server-license-for-use-on-the-cloud.html).   
-   A Microsoft Azure™ account.

# Costs
You are responsible for the cost of the Azure services used when you create cloud resources using this guide. Resource settings, such as instance type, affect
the cost of deployment. For cost estimates, see the pricing pages for each Azure
service you are using. Prices are subject to change.


# Introduction 

The following guide will help you automate the process of running MATLAB
Production Server on Azure using your Azure account. The automation is
accomplished using an Azure Resource Manager (ARM) template. The template is a JSON
file that defines the resources needed to deploy and manage MATLAB Production
Server on Azure. Once deployed, you can manage the server using the
MATLAB Production Server Dashboard&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). 

# Deployment Steps

## Step 1. Launch Template
Click the **Deploy to Azure** button to deploy resources on
    Azure. This opens the Azure Portal in your web browser.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2022b%2Ftemplates%2Fazuredeploy22b.json)

> MATLAB Release: R2022b


For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)
<p><strong>Note:</strong> Creating resources on Azure can take at least 30 minutes.</p>

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal :

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> VERTHAM Dev</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Resource group**          | Choose a name for the resource group that will hold the resources. It is recommended you create a new resource group for each deployment. This allows all resources in a group to be deleted simultaneously. <p><em>Example:</em> Saveros</p>                                                                                                                                                                                                                                                                       |
| **Region**                | Choose the region to start resources in. Select a region which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). MathWorks recommends using East US or East US 2. <p><em>Example:</em> East US</p>                                                                                                                                                                                                                          |
| **Location**                | Specify the location where the MATLAB Production Server instance will be deployed or use the default value. |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Production Server instance runs on a VM and each instance runs multiple workers. We recommend you choose a VM size where the number of cores on your VM matches the number of MATLAB workers per VM you plan on using. The template defaults to Standard_D4s_v3. This configuration has 4 vCPUs and 16 GiB of memory. For more information, see the [Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D4s_v3</p> |
| **Dashboard VM Size** | Specify the size of the VM you plan on using for the MATLAB Production Server dashboard. The dashboard lets you configure server settings and manage deployed applications. In most cases, choosing the smallest VM size is adequate. The template defaults to Standard_D1_v2. For more information, see the [Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D1_v2</p> |
| **Instance Count**          | Number of VMs to run MATLAB Production Server instances. Each MATLAB Production Server instance runs on a VM and each instance runs multiple workers. <p><em>Example:</em> 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select Standard_D4s_v3 VM (4 cores) as the Server VM Instance Size, you need 6 VMs to fully use the workers in your license. Therefore, your instance count will be 6.</p><p>You can always underprovision the number of VMs, in which case you may end up using fewer workers than you are licensed for.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Username**          | Specify the administrator username for all VMs. Use this username to log in to the MATLAB Production Server dashboard and network license manager. |
| **Admin Password**          | Specify the administrator password for all VMs. Use this password to log in to the MATLAB Production Server dashboard and network license manager. |
| **Allow connections from** | Specify the IP address range that is allowed to connect to the dashboard that manages the server and to the network license manager. The format for this field is IP Address/Mask. <p><em>Example</em>: 10.0.0.1/32</p> <ul><li>This is the public IP address which can be found by searching for "what is my ip address" on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>If you need a range of IP addresses, use a [CIDR calculator](https://www.ipaddressguide.com/cidr).</li><li>To determine which address is appropriate, contact your IT administrator.</li></ul></p> |
| **Create Azure Redis Cache**| Choose whether you want to create an Azure Redis Cache service. Creating this service will allow you to use the persistence functionality of the server. Persistence provides a mechanism to cache data between calls to MATLAB code running on a server instance.|
| **Use Public IP Addresses**| Choose 'Yes' if you want to make your solution available over the Internet. <br/>If you choose 'No', the ARM template does not assign a public IP address for the VM that hosts the dashboard. To access the dashboard, you can use a different VM located in the same virtual network as the VM that hosts the dashboard.  |
|**Platform**| Choose the operating system for the server. Microsoft Windows and Linux are the only available options. |                                                            
|**New or Existing Virtual Network**|  Select 'new' to create a new virtual network for your deployment using the default values shown in the parameters after this one. Any changes to these parameter values are ignored. <br/><br/> Select 'existing' to specify an existing virtual network by updating the parameters after this one. <br/><br/> When deploying in a new virtual network, by default, the deployment keeps open the ports listed in [How do I use an existing virtual network to deploy MATLAB Production Server?](#How-do-I-use-an-existing-virtual-network-to-deploy-MATLAB-Production-Server). You can close ports 22 and 3389 after deployment is complete. |
| **Virtual Network Name** |  Specify the name of your existing virtual network or use the default value.   |
| **Virtual Network CIDR Range** |  Specify the IP address range of the virtual network in CIDR notation or use the default value. |
| **Subnet 1 CIDR Range** |  Specify the IP address range of the first subnet in CIDR notation or use the default value. The first subnet hosts the dashboard and other resources. | 
| **Subnet 2 CIDR Range** | Specify the IP address range of the second subnet in CIDR notation or use the default value. The second subnet hosts the application gateway. |
| **Available Subnet 2 IP Address** |   Specify an unused IP address from Subnet 2 or use the default value. This IP address serves as the private IP of the application gateway. |
| **Resource Group Name Of Virtual Network** |   Specify the resource group name of the virtual network or use the default value.    |
|**Deploy Network License Manager for MATLAB**| Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for the MATLAB reference architecture. Select 'No' if you want to use an existing license server. |
| **Certificate Input Type** |   Select how you want to specify the SSL certificate for the Azure application gateway to use. The Azure application gateway provides an HTTPS endpoint that you use to connect to server instances and the MATLAB Production Server dashboard. You must select one of these options:<p><ul><li>KeyVault: Specify an SSL certificate that exists in the Azure Key Vault.</li><li>Base64-encoded PFX Certificate: Specify a string that is a base64-encoded value of an SSL certificate that is in PFX format.</li></ul></p><p>Specify the certificate data for your selected option in the parameters that follow. |

If you set **Certificate Input Type** to 'KeyVault', specify these parameters:
| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Key Vault Certificate Secret ID** |   Enter the secret ID of the SSL certificate present in the Key Vault. To create a Key Vault and add a certificate, see [Add a certificate to Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/certificates/quick-create-portal#add-a-certificate-to-key-vault) (Azure). <br/>    |
| **Managed Identity Resource ID for Key Vault** |   Enter the resource ID of the user-assigned managed identity that has permission to access the Key Vault. If your managed identity does not have access to the Key Vault, the deployment fails.<ul><li>To create a managed identity, see [Create a user-assigned managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-manage-ua-identity-portal#create-a-user-assigned-managed-identity) (Azure).</li><li>To grant your managed identity access to the Key Vault, assign it an access policy with at least "Get" permissions to the key, secret, and certificate. See [Assign a Key Vault access policy](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy) (Azure).</li></ul> |

If you set **Certificate Input Type** to 'Base64-encoded PFX Certificate', specify these parameters:
| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Base64Encoded PFX Certificate Data** |   Enter a string that is a base64-encoded value of an SSL certificate in PFX format.    |
| **Password For Base64Encoded PFX Certificate** |   If the certificate requires a password, enter it here. Otherwise, leave the field blank.    |

Click **Create** to begin the deployment. This can take up to 40 minutes.

## Step 3. Upload License File
The Network License Manager for MATLAB manages the MATLAB Production Server license file. The MATLAB Production Server deployment template provides an option to deploy the license manager or use an existing license manager. For more information about the Network License Manager for MATLAB, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-azure). The following steps show how to upload the license file using the Network License Manager for MATLAB dashboard: 
> **Note**: You must provide a fixed license server MAC address to get a license file from the MathWorks License Center. For more information, see [Configure MATLAB Production Server License for Use on the Cloud](https://www.mathworks.com/help/mps/server/configure-matlab-production-server-license-for-use-on-the-cloud.html).     
1. In the Azure Portal, click **Resource
    groups** and select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane and click **Microsoft.Template**.
1. Click **Outputs**. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the administrator username and password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Follow the instructions in the Network License Manager for MATLAB dashboard to upload your MATLAB Production Server license.


## Step 4. Connect and Log In to the Dashboard
The MALAB Production Server dashboard provides a web-based interface to
configure and manage server instances on the cloud. If your solution uses private IP addresses, you can connect to the dashboard from a VM that belongs to the same virtual network as the VM that hosts the dashboard.
>   **Note:** Complete these steps only after your resource group has been successfully created.

> **Note:** The Internet Explorer web browser is not supported for interacting with the dashboard. 

1.  In the Azure Portal, click **Resource
    groups** and select the resource group you created for this deployment from the list.
1.  Select **Deployments** from the left pane and click **Microsoft.Template**.
1.  Click **Outputs** from the left pane. Copy the parameter value for **dashboardURL** and paste it in a browser.  
1.  Log in using the administrator username and password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.

![MATLAB Production Server Dashboard](/releases/R2022b/images/dashboardLogin.png?raw=true) 

You are now ready to use MATLAB Production Server on Azure. 

For more information on how to use the dashboard, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).

Configuring role-based access control for the dashboard is recommended. Role-based access control uses Azure AD to let you grant users the privileges to perform tasks on the dashboard and server, based on their role. For more information on how to configure role-based access control, see [Dashboard Access Control](https://www.mathworks.com/help/mps/server/dashboard-access-control-for-azure-reference-architecture.html).

To run applications on MATLAB Production Server, you will need to create applications using MATLAB Compiler SDK. For more information, see [Create Deployable Archive for MATLAB Production Server](https://www.mathworks.com/help/compiler_sdk/mps_dev_test/create-a-deployable-archive-for-matlab-production-server.html).

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

*Architecture on Azure*

![Cluster Architecture](/releases/R2022b/images/mps-ref-arch-azure-architecture-diagram.jpg?raw=true)

### Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MATLAB Production Server dashboard virtual machine | `servermachine`           | 1                   | Virtual machine (VM) that hosts the MATLAB Production Server dashboard. Use the dashboard to: <ul><li>Get HTTP/HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li></ul><p>For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).   |
| MATLAB Production Server dashboard public IP                           | `servermachine-public-ip` | 1                   | Public IP address to connect to MATLAB Production Server dashboard.<p>**NOTE**: Provides HTTPS endpoint to the dashboard for managing server instances.</p>                                                                                                                                                                                                                                                            |
| Virtual machine scale set                                                  | `vmss<uniqueID>`        | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Application gateway                                                        | `vmss<uniqueID>-agw`    | 1                   | Provides routing and load balancing service to MATLAB Production Server instances. The MATLAB Production Server dashboard retrieves the HTTP/HTTPS endpoint for making requests to the server from the application gateway resource.<p>**NOTE**: Provides HTTPS endpoint to the server for making requests.</p>                                                                                           |
| Storage account                                                            | `serverlog<uniqueID>`   | 1                  | Storage account where the deployable archives (CTF files) created by MATLAB® Compiler SDK™ will be stored. The deployable archives (CTF files) will be stored in a file share.                                                                                                                                                                                                  |
| Virtual network                                                           | `vmss<uniqueID>-vnet`   | 1                   | Enables resources to communicate with each other.                                                                                                                                                                                                                                                                                  |
| Azure Cache for Redis |  `vmss<uniqueID>redis` | 1 | Enables caching of data between calls to MATLAB code running on a server instance. |
| Application Insights |  `logs-apmservice` | 1 | Enables storing and viewing of all logs associated with deployment. |

# FAQ
## How do I use an existing virtual network to deploy MATLAB Production Server?
In addition to the parameters specified in the section [Configure Cloud Resources](#step-2-configure-cloud-resources), you will also need to open the following ports in your virtual network:

| Port | Description |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `443` | Required for communicating with the dashboard. |
| `8000`, `8004`, `8080`, `9090`, `9910` | Required for communication between the dashboard, MATLAB Production Server workers, and various microservices within the virtual network.  These ports do not need to be open to the Internet. |
| `27000` | Required for communication between the network license manager and the workers. |
| `65200` - `65535` | Required for the Azure application gateway health check to work. These ports need to be accessible over the Internet. For more information, see [MSDN Community](https://social.msdn.microsoft.com/Forums/azure/en-US/96a77f18-3b71-45d2-a213-c4ba63fd4e63/internal-application-gateway-backend-health-is-unkown?forum=WAVirtualMachinesVirtualNetwork). |
| `22`, `3389` | (Optional) Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |

## How do I launch a template that uses a previous MATLAB release?
You may use one of the deploy buttons below to deploy an older release of MATLAB Production Server Reference Architecture. Note that the operating system is a parameter of the ARM template.
| Release | Windows Server / Ubuntu                                                                                                                                                                                                                                                                         | 
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2022a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2022a%2Ftemplates%2Fazuredeploy22a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |
| R2021b  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2021b%2Ftemplates%2Fazuredeploy21b.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |
| R2021a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2021a%2Ftemplates%2Fazuredeploy21a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |


For more information, see [previous releases](/releases).


## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime |
|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|-----------------|---------------|
| MATLAB R2021a |  R2018b | R2019a | R2019b | R2020a | R2020b | R2021a |
| MATLAB R2021b |  |  R2019a | R2019b | R2020a | R2020b |R2021a | R2021b |
| MATLAB R2022a |  |  |  R2019b | R2020a | R2020b |R2021a | R2021b | R2022a |
| MATLAB R2022b |  |  |  | R2020a | R2020b | R2021a |R2021b | R2022a | R2022b |



## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors occur either when CORS is not enabled on the server or when the server endpoint uses a self-signed certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and JavaScript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Alternatively, you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate to Application Gateway](https://www.mathworks.com/help/mps/server/configure-azure-resources-reference-architecture.html#mw_6ae700e7-b895-4e90-b0fb-7292e905656e_sep_mw_1fd15ea2-d161-4694-963d-41a81fc773bf). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
