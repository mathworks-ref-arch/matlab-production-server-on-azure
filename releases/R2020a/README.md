# MATLAB Production Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/help/licensingoncloud/matlab-production-server-on-the-cloud.html). In order to configure the license in the Cloud, you will need the MAC address of the license server on the Cloud. If you deploy the Network License Manager for MATLAB with MATLAB Production Server, you can get the license server MAC address only after deploying the solution to the Cloud. For more information, see [Upload the License File](#step-3-upload-the-license-file).   
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

## Step 1. Launch the Template
Click the **Deploy to Azure** button to deploy resources on
    Azure. This will open the Azure Portal in your web browser.

 <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2020a%2Ftemplates%2Fazuredeploy20a.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a>

> MATLAB Release: R2020a



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
| **Instance Count**          | Number of VMs to run MATLAB Production Server instances. Each MATLAB Production Server instance runs on a VM and each instance will run multiple workers. The maximum number of MATLAB Production Server instances is limited to 24. This means only a maximum of 24 VMs can be provisioned. Therefore, your instance count cannot exceed 24. <p><em>Example:</em> 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select Standard_D4s_v3 VM (4 cores) as the Server VM Instance Size, you will need 6 VMs to fully utilize the workers in your license. Therefore, your instance count will be 6.</p><p>You can always under provision the number of VMs. In which case you may end up using fewer workers than you are licensed for.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Username**          | Specify the admin user name for all VMs. Use this user name to log in to the MATLAB Production Server dashboard. If you also deploy the network license manager, use this username to log in to the network license manager dashboard.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Password**          | Specify the admin password for all VMs. Use this password to log in to the MATLAB Production Server dashboard. If you also deploy the network license manager, use this password to log in to the network license manager dashboard.|
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

Click **Purchase** to begin the deployment. This can take up to 40 minutes.

## Step 3. Upload the License File
The Network License Manager for MATLAB manages the MATLAB Production Server license file. The MATLAB Production Server deployment template provides an option to deploy the license manager or use an existing license manager. For more information about the Network License Manager for MATLAB, see [Network License Manager for MATLAB](https://github.com/mathworks-ref-arch/license-manager-for-matlab-on-azure). The following steps show how to upload the license file using the Network License Manager for MATLAB dashboard, if you have deployed the license manager during the deployment process. 
> **Note**: You must provide a fixed license server MAC address to get a license file from the MathWorks License Center. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/support/cloud/configure-matlab-production-server-licensing-on-the-cloud.html).     
1. In the Azure Portal, click **Resource
    groups**. This will display all your resource groups.
1. Select the resource group containing your cluster resources.
1. Select **Deployments** from the left pane. In the pane that opens, click **Microsoft.Template**.
1. Select **Outputs** from the left pane. 
1. Copy the parameter value for **networkLicenseManagerURL** and paste it in a browser.
1. Log in using the administrator user name and password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.
1. Follow the instructions in the Network License Manager for MATLAB dashboard to upload your MATLAB Production Server license.


## Step 4. Connect and Log In to the Dashboard
The MALAB Production Server dashboard provides a web-based interface to
configure and manage server instances on the Cloud. If your solution uses private IP addresses, you can connect to the dashboard from a VM that belongs to the same virtual network as the VM that hosts the dashboard.
>   **Note:** Complete these steps only after your resource group has been successfully created.

> **Note:** The Internet Explorer web browser is not supported for interacting with the dashboard. 

1.  In the Azure Portal, click **Resource
    groups**. This will display all your resource groups.
1.  Select the resource group you created for this deployment from the list. This
    will display the Azure blade of the selected resource group with its own
    navigation panel on the left.
1.  Select **Deployments** from the left pane. In the pane that opens, click **Microsoft.Template**.
1.  Select **Outputs** from the left pane.
1.  Copy the parameter value for **dashboardURL** and paste it in a browser.  
1.  Log in using the administrator user name and password that you specified in the [Configure Cloud Resources](#step-2-configure-cloud-resources) step of the deployment process.

![MATLAB Production Server Dashboard](/releases/R2020a/images/dashboardLogin.png?raw=true) 

>**Note**: The dashboard uses a self-signed certificate which can be changed. For information on changing the self-signed certificates, see [Change Self-signed Certificate](#change-self-signed-certificate). 

You are now ready to use MATLAB Production Server on Azure. 

For more information on how to use the dashboard, see [MATLAB Production Server Reference Architecture Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).

Configuring role-based access control for the dashboard is recommended. Role-based access control uses Azure AD to let you grant users the privileges to perform tasks on the dashboard and server, based on their role. For more information on how to configure role-based access control, see [Dashboard Access Control](https://www.mathworks.com/help/mps/server/dashboard-access-control-for-azure-reference-architecture.html).

To run applications on MATLAB Production Server, you will need to create applications using MATLAB Compiler SDK. For more information, see [Deployable Archive Creation](https://www.mathworks.com/help/mps/deployable-archive-creation.html) in the MATLAB Production Server product documentation.

# Additional Information 

## Delete Your Resource Group
> **Note**: Your license file is tied to your MAC address. If you delete your
resource group to delete your cluster, you will need to get a new license file.
You are limited to changing your MAC address 4 times per year.

You can remove the resource group and all associated cluster resources when you
are done with them. Note that there is no undo.
1. Login to the Azure Portal.
2. Select the resource group containing your cluster resources.
3. Select the Delete resource group icon to destroy all resources deployed in this group.
4. You will be prompted to enter the name of the resource group to confirm the deletion.

## Security 
When you run MATLAB Production Server on the Cloud you get one HTTPS endpoints that uses a self-signed certificate. This is the endpoint to the application gateway that connects the server instances. This endpoint is displayed as the **MATLAB Execution Endpoint** in the **Overview** tab of the dashboard and is used to make requests to the server.

For information on changing the self-signed certificate, see [Change Self-signed Certificate](#change-self-signed-certificate). 

## View Logs
1. In the Azure Portal, click **Resource groups**.
2. Select the resource group you created for this deployment from the list.
3. Select the resource named `logs-apmservice`.
5. Click the **Logs** tab from the left navigation pane.
8. Create a new query and click **Run**.

To view logs generated by all the server instances, you can use the following query.
```
traces
| where customDimensions.source == "prodServerInstance"
```
To view only the error logs generated by all server instances, you can use the following query.
```
traces
| where customDimensions.source == "prodServerInstance"
| where parse_json(message).severity == "error"
```

<!--Logs are stored in your Azure storage account and can be viewed using the Azure Storage Explorer. To view server logs:

1. Download and install the Microsoft Azure Storage Explorer.
2. Sign-on using your Azure account.
3. Expand the storage account associated with your selected Azure subscription. The storage account name is diplayed in the View Logs section of the cloud console. 
4. Expand Tables and view: MasterController, mpsInstances, mpsNative
    - `MasterController`: Log of user logins, deployed archives (.ctf files), certificate changes, and user interface actions.
    - `mpsInstances`: Log of orchestrator code for server virtual machines.
    - `mpsNative`: Log of activity generated by the server instance.
-->

## Change the Number of Virtual Machines
To change the number of VMs:

1. Log in to the Azure Portal
1. Change the number of virtual machines in the virtual machine scale set resource (`vmss<uniqueID>`).

![Scaling](/releases/R2020a/images/azureScaling.png)

If you have a standard 24 worker MATLAB Production Server license and select `Standard_D4s_v3 VM` as the **Server VM Size** during setup, you will need 6 VMs to fully utilize the workers in your license.

The Azure Resource Manager (ARM) template by default has the `overprovision`
property set to `true`. This means Azure will provision more virtual machines than
necessary for a brief period to buffer against any machines that may fail. Once
all virtual machines are healthy, Azure will scale down to the number of virtual
machines you specified. For more information, see [Azure Virtual Machine Scale Sets FAQs](https://releases/R2020a/docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq).

## Change Self-signed Certificate
You can change the self-signed certificate to the HTTPS endpoint to the application gateway. This endpoint is used to make requests to the server and is used to connect to the dashboard. 

To change the self-signed certificate to the application gateway you need to complete a two step process in the Azure Portal.

1.  Create a listener

2.  Add a rule

### Create a Listener
<ol>
<li>In the resource group for the solution, select the application gateway
    resource with the name <code>vmss&lt;uniqueID&gt;-agw</code>.</li>

<li>Select <strong>Listeners</strong> from the navigation pane on the left and click
    <strong>+Add listener</strong> from the top navigation pane.</li>

<li>Enter parameter values:

<table>
<tbody>
<tr>
<td width="312">
<p><strong>Listener name</strong></p>
</td>
<td width="312">
<p><strong>Value</strong></p>
</td>
</tr>
<tr>
<td width="312">
<p>Name</p>
</td>
<td width="312">
<p>Enter a name for the listener.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Frontend IP configuration</p>
</td>
<td width="312">
<p>Choose <code>Public</code> if your solution uses public IPs; otherwise, choose <code>Private</code>.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Port</p>
</td>
<td width="312">
<p>Enter any free port between 8001 - 10000.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Protocol</p>
</td>
<td width="312">
<p>Select <code>HTTPS</code>.</p>
</td>
</tr>
</tbody>
</table>

<li>Select <strong>Create New</strong> in <strong>Choose a Certificate</strong>, then select <strong>Upload a certificate</strong>.</li>

<li>Upload a PFX certificate, give it a name, and create a password.
    Click <strong>OK</strong>.</li>
</ol>


### Add a Rule
1. In the resource group for the solution, select the application gateway resource with the name <code>vmss&lt;uniqueID&gt;-agw</code>.
2. Select <strong>Rules</strong> from the navigation pane on the left and click <strong>+Request routing rule</strong> from the top navigation pane.
3. In the <strong>Rule name</strong> text box, enter a name to identify the rule.
4. In the <strong>Listener</strong> dropdown, select the listener that you created in [Create a Listener](#create-a-listener).
5. Enter the following parameter values for <strong>Backend targets</strong>:
</ol>
<table>
<tbody>
<tr>
<td width="312">
<p><strong>Parameter name</strong></p>
</td>
<td width="312">
<p><strong>Value</strong></p>
</td>
</tr>
<tr>
<td width="312">
<p>Target type</p>
</td>
<td width="312">
<p>Select <code>Backend pool</code>.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Backend target</p>
</td>
<td width="312">
<p>Select <code>vmss1&lt;uniqueID&gt;pool</code>.</p>
</td>
</tr>
<tr>
<td width="312">
<p>HTTPS settings</p>
</td>
<td width="312">
<p>Select <code>appGwBackendMPSHttpSettings</code>.</p>
</td>
</tr>
</tbody>
</table>
<p>Click <strong>Add</strong>.</p>

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

*Architecture on Azure*

![Cluster Architecture](/releases/R2020a/images/mps-ref-arch-azure-architecture-diagram.jpg?raw=true)

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
| Release | Windows Server 2016 VM                                                                                                                                                                                                                                                                         | Ubuntu 16.04 VM                                                                                                                                                                                                                                                                    |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R2019b  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2019a%2Ftemplates%2FazuredeployBasic19a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> | <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2019a%2Ftemplates%2FazuredeployBasic19a.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a> |
| R2019a  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2019a%2Ftemplates%2FazuredeployBasic19a.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> | <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2019a%2Ftemplates%2FazuredeployBasic19a.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a> |
| R2018b  | <a   href  ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2018b%2520and%2520older%2Ftemplates%2FazuredeployWindows18b.json"   target  ="_blank"  >   <img   src  ="http://azuredeploy.net/deploybutton.png"  />   </a> | <a  href ="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmatlab-production-server-on-azure%2Fmaster%2Freleases%2FR2018b%2520and%2520older%2Ftemplates%2FazuredeployLinux18b.json"  target ="_blank" >  <img  src ="http://azuredeploy.net/deploybutton.png" />  </a> |


For more information, see [previous releases](/releases).


## What versions of MATLAB Runtime are supported?

| Release | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | MATLAB Runtime | 
|---------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| MATLAB R2018b |  | R2016a | R2016b | R2017a | R2017b | R2018a | R2018b |  |  | |
| MATLAB R2019a |  |  | R2016b | R2017a | R2017b | R2018a | R2018b | R2019a |  | |
| MATLAB R2019b |  |  |  | R2017a | R2017b | R2018a | R2018b | R2019a | R2019b | |
| MATLAB R2020a |  |  |  | | R2017b | R2018a | R2018b | R2019a | R2019b | R2020a |



## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors result from either CORS not being enabled on the server or due to the fact that the server endpoint uses a self-signed 
certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit the Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and Javascript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Or you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Create a Listener](#create-a-listener). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
Email: `cloud-support@mathworks.com`
