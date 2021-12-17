# MATLAB Production Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Current on [Software Maintenance Service (SMS)](https://www.mathworks.com/services/maintenance.html).  
    - Linked to a [MathWorks Account](https://www.mathworks.com/mwaccount/).
    - Concurrent license type. To check your license type, see [MathWorks License Center](https://www.mathworks.com/licensecenter/). 
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/help/licensingoncloud/matlab-production-server-on-the-cloud.html).   
-   A Microsoft Azure™ account.

# Costs
You are responsible for the cost of the Azure services used when you create cloud resources using this guide. Resource settings, such as instance type, will affect
the cost of deployment. For cost estimates, see the pricing pages for each Azure
service you will be using. Prices are subject to change.


# Introduction 

The following guide will help you automate the process of running MATLAB
Production Server on Azure using your Azure account. The automation is
accomplished using an Azure Resource Manager (ARM) template. The template is a JSON
file that defines the resources needed to deploy and manage MATLAB Production
Server on Azure. Once deployed, you can manage the server using the
MATLAB Production Server Dashboard&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [Manage MATLAB Production Server using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). 

# Deployment Steps

## Step 1. Launch Template
Click the **Deploy to Azure** button to deploy resources on
    Azure. This will open the Azure Portal in your web browser.

 <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2021b%2Ftemplates%2Fazuredeploy21b.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a>

> MATLAB Release: R2021b


For other releases, see [How do I launch a template that uses a previous MATLAB release?](#how-do-i-launch-a-template-that-uses-a-previous-matlab-release)
<p><strong>Note:</strong> Creating resources on Azure can take at least 30 minutes.</p>

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal :

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> VERTHAM Dev</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Resource group**          | Choose a name for the resource group that will hold the resources. It is recommended you create a new resource group for each deployment. This allows all resources in a group to be deleted simultaneously. <p><em>Example:</em> Saveros</p>                                                                                                                                                                                                                                                                       |
| **Location**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). We recommend you use East US or East US 2. <p><em>Example:</em> East US</p>                                                                                                                                                                                                                          |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Production Server instance runs on a VM and each instance will run multiple workers. We recommend you choose a VM size where the number of cores on your VM match the number of MATLAB workers per VM you plan on using. The template defaults to: Standard_D4s_v3. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D4s_v3</p> |
| **Instance Count**          | Number of VMs to run MATLAB Production Server instances. Each MATLAB Production Server instance runs on a VM and each instance will run multiple workers. <p><em>Example:</em> 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select Standard_D4s_v3 VM (4 cores) as the Server VM Instance Size, you will need 6 VMs to fully utilize the workers in your license. Therefore, your instance count will be 6.</p><p>You can always under provision the number of VMs. In which case you may end up using fewer workers than you are licensed for.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Username**          | Specify the administrator user name for all VMs. Use this user name to log in to the MATLAB Production Server dashboard.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Password**          | Specify the administrator password for all VMs. Use this password to log in to the MATLAB Production Server dashboard. If you also deploy the network license manager, use this password to log in to the network license manager dashboard.|
| **Allow connections from** | This is the IP address range that will be allowed to connect to the dashboard that manages the server, and the network license manager. The format for this field is IP Address/Mask. <p><em>Example</em>: </p>10.0.0.1/32 <ul><li>This is the public IP address which can be found by searching for "what is my ip address" on the web. The mask determines the number of IP addresses to include.</li><li>A mask of 32 is a single IP address.</li><li>Use a [CIDR calculator](https://www.ipaddressguide.com/cidr) if you need a range of more than one IP addresses.</li><li>You may need to contact your IT administrator to determine which address is appropriate.</li></ul></p> |
| **Create Azure Redis Cache**| Choose whether you want to create an Azure Redis Cache service. Creating this service will allow you to use the persistence functionality of the server. Persistence provides a mechanism to cache data between calls to MATLAB code running on a server instance.|
| **Use Public IP Addresses**| Choose 'Yes' if you want to make your solution available over the internet. <br/>If you choose 'No', the ARM template does not assign a public IP address for the VM that hosts the dashboard. To access the dashboard, you can use a different VM located in the same virtual network as the VM that hosts the dashboard.  |
|**Platform**| Choose the operating system for the server. Microsoft Windows and Linux are the only available options. |                                                            
|**Deploy Network License Manager**| Select whether you want to deploy the Network License Manager for MATLAB to manage your license files. Selecting 'Yes' deploys the Network License Manager for MATLAB reference architecture. Select 'No' if you want to use an exisitng license server. |
|**New or Existing Virtual Network**|  Specify whether you want to create a new virtual network for your deployment or use an exisiting one. You can use the default values or enter new values based on your network setup for the following paramaters.|
| **Virtual Network Name** |  Specify the name of your existing virtual network or use the default value.   |
| **Virtual Network CIDR Range** |  Specify the IP address range of the virtual network in CIDR notation or use the default value. |
| **Subnet 1 CIDR Range** |  Specify the IP address range of the first subnet in CIDR notation or use the default value. The first subnet hosts the dashboard and other resources. | 
| **Subnet 2 CIDR Range** | Specify the IP address range of the second subnet in CIDR notation or use the default value. The second subnet hosts the application gateway. |
| **Available Subnet 2 IP Address** |   Specify an unused IP address from Subnet 2 or use the default value. This IP address serves as the private IP of the application gateway. |
| **Resource Group Name Of Virtual Network** |   Specify the resource group name of the virtual network or use the default value.    |
| **Certificate Input Type** |   Specify an SSL certificate for the Azure application gateway to use. The application gateway provides an HTTPS endpoint that you use to connect to server instances and the MATLAB Production Server dashboard.<br/>The deployment template provides an option to use either an SSL certificate that already exists in the Azure KeyVault or specify a string that is a base64-encoded value of an SSL certificate that is in PFX format. <br/><br/>Prerequisites for using the KeyVault:<br/><ul><li>KeyVault with an SSL certificate. For information about creating a KeyVault and adding a certificate, see [Azure documentation](https://docs.microsoft.com/en-us/azure/key-vault/certificates/quick-create-portal). <br/>Record the secret ID of the certificate. You will need to enter it in the MATLAB Production Server deployment template.</li><li>User-assigned managed identity in Azure that has permission to access the KeyVault. For details on creating a managed identity, see [Azure documentation](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-manage-ua-identity-portal#create-a-user-assigned-managed-identity).<br/>Record the resource ID of the managed identity that you create. You will need to enter it in the MATLAB Production Server deployment template.<br/>Grant your managed identity access to the KeyVault. To do so, navigate to the KeyVault you created earlier and add a role assignment that has at least read access to the KeyVault. For details on adding a role assignment, see [Azure documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal?tabs=current#step-2-open-the-add-role-assignment-pane).</li></ul><br/>Select if you will use a certificate from the Azure KeyVault or enter a base64-encoded PFX certificate string. <br/><br/>If you select KeyVault, enter values for **Managed Identity Resource ID for KeyVault** and **Secret ID of Certificate in KeyVault**.<br/><br/>If you select Base-64 encoded PFX Certificate, enter values for **Base64-encoded PFX Certificate Data** and **Password for Base64-encoded PFX Certificate**.|
| **Secret ID of Certificate in KeyVault** |   Enter the secret ID of the SSL certificate present in the KeyVault.    |
| **Managed Identity Resource ID for KeyVault** |   Enter the resource ID of the managed identity that has permission to access the KeyVault.    |
| **Base64Encoded PFX Certificate Data** |   Enter a string that is a base64-encoded value of an SSL certificate in PFX format.    |
| **Password for Base64-encoded PFX Certificate** |   If the certificate requires a password, enter it here. Otherwise, leave the field blank.    |

Click **Purchase** to begin the deployment. This can take up to 40 minutes.

## Step 3. Upload License File
The Network License Manager for MATLAB manages the MATLAB Production Server license file. The MATLAB Production Server deployment template provides an option to deploy the license manager or use an existing license manager. For more information about the Network License Manager for MATLAB, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-azure). The following steps show how to upload the license file using the Network License Manager for MATLAB dashboard: 
> **Note**: You must provide a fixed license server MAC address to get a license file from the MathWorks License Center. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/help/licensingoncloud/matlab-production-server-on-the-cloud.html).     
1. In the Azure Portal, click **Resource
    groups** and select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane and click **Microsoft.Template**.
1. Click **Outputs**. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
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
1.  Log in using the administrator user name and password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.

![MATLAB Production Server Dashboard](/releases/R2021b/images/dashboardLogin.png?raw=true) 

You are now ready to use MATLAB Production Server on Azure. 

For more information on how to use the dashboard, see [MATLAB Production Server Reference Architecture Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).

Configuring role-based access control for the dashboard is recommended. Role-based access control uses Azure AD to let you grant users the privileges to perform tasks on the dashboard and server, based on their role. For more information on how to configure role-based access control, see [Dashboard Access Control](https://www.mathworks.com/help/mps/server/dashboard-access-control-for-azure-reference-architecture.html).

To run applications on MATLAB Production Server, you will need to create applications using MATLAB Compiler SDK. For more information, see [Deployable Archive Creation](https://www.mathworks.com/help/mps/deployable-archive-creation.html) in the MATLAB Production Server product documentation.

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

*Architecture on Azure*

![Cluster Architecture](/releases/R2021b/images/mps-ref-arch-azure-architecture-diagram.jpg?raw=true)

### Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MATLAB Production Server dashboard virtual machine | `servermachine`           | 1                   | Virtual machine (VM) that hosts the MATLAB Production Server dashboard. Use the dashboard to: <ul><li>Get HTTP/HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li></ul><p>For more information, see [MATLAB Production Server Reference Architecture Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).   |
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
| `8000`, `8004`, `8080`, `9090`, `9910` | Required for communication between the dashboard, MATLAB Production Server workers, and various microservices within the virtual network.  These ports do not need to be open to the internet. |
| `27000` | Required for communication between network license manager and the workers. |
| `65200` - `65535` | Required for the Azure application gateway health check to work. These ports need to be accessible over the internet. For more information, see [MSDN Community](https://social.msdn.microsoft.com/Forums/azure/en-US/96a77f18-3b71-45d2-a213-c4ba63fd4e63/internal-application-gateway-backend-health-is-unkown?forum=WAVirtualMachinesVirtualNetwork). |
| `22`, `3389` | Required for Remote Desktop functionality. This can be used for troubleshooting and debugging. |

## How do I launch a template that uses a previous MATLAB release?
You may use one of the deploy buttons below to deploy an older release of MATLAB Production Server Reference Architecture. Note that the operating system is a parameter of the ARM template.
| Release | Windows Server / Ubuntu                                                                                                                                                                                                                                                                         | 
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2021a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2021a%2Ftemplates%2Fazuredeploy21a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |
| R2020b  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2020b%2Ftemplates%2Fazuredeploy20b.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |
| R2020a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2020a%2Ftemplates%2Fazuredeploy20a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> |


For more information, see [previous releases](/releases).


## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime |
|---------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| MATLAB R2020a | R2017b | R2018a | R2018b | R2019a | R2019b | R2020a |
| MATLAB R2020b |  | R2018a | R2018b | R2019a | R2019b | R2020a | R2020b |
| MATLAB R2021a |  |  | R2018b | R2019a | R2019b | R2020a | R2020b | R2021a |
| MATLAB R2021b |  |  |  | R2019a | R2019b | R2020a | R2020b |R2021a | R2021b |



## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors result from either CORS not being enabled on the server or due to the fact that the server endpoint uses a self-signed 
certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit the Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and Javascript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Or you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate to Application Gateway](https://www.mathworks.com/help/mps/server/configure-azure-resources-reference-architecture.html#mw_6ae700e7-b895-4e90-b0fb-7292e905656e_sep_mw_1fd15ea2-d161-4694-963d-41a81fc773bf). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
 