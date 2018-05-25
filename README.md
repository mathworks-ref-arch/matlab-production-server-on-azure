# MATLAB Production Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/support/cloud/configure-matlab-production-server-licensing-on-the-cloud.html). In order to configure the license in the cloud, you will need the MAC address of the license server on the cloud. You can get the license server MAC address only after deploying the solution to the cloud. For more information, see [Get License Server MAC Address](/doc/cloudConsoleDoc.md#get-license-server-mac-address).   
-   MATLAB® Production Server™ software. 
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
MATLAB Production Server Cloud Console&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [MATLAB Production Server Cloud Console User's Guide](doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources). 

# Deployment Steps

## Step 1. Launch the Template
Click the **Deploy to Azure** button to deploy resources on
    Azure. This will open the Azure Portal in your web browser.

| Windows Server 2016 VM                                                                                                                                                                                                                            | Ubuntu 16.04 VM                                                                                                                                                                                                                                   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href="https://portal.azure.com/#create/Microsoft.Template/urihttps%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmps-on-azure%2Fmaster%2FazuredeployWindows.json" target="_blank"> <img src="http://azuredeploy.net/deploybutton.png"/> </a>  <p>MATLAB Release: R2018a </p>| <a href="https://portal.azure.com/#create/Microsoft.Template/urihttps%3A%2F%2Fraw.githubusercontent.com%2Fmathworks-ref-arch%2Fmps-on-azure%2Fmaster%2FazuredeployLinux.json" target="_blank"> <img src="http://azuredeploy.net/deploybutton.png"/> </a><p> MATLAB Release: R2018a </p>|

**Note**: Creating resources on Azure can take at least 30 minutes.

## Step 2. Configure Cloud Resources
Provide values for parameters in the custom deployment template on the Azure Portal :

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Subscription**            | Choose an Azure subscription to use for purchasing resources.<p><em>Example:</em> VERTHAM Dev</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Resource group**          | Choose a name for the resource group that will hold the resources. It is recommended you create a new resource group for each deployment. This allows all resources in a group to be deleted simultaneously. <p><em>Example:</em> Saveros</p>                                                                                                                                                                                                                                                                       |
| **Location**                | Choose the region to start resources in. Ensure that you select a location which supports your requested instance types. To check which services are supported in each location, see [Azure Region Services](<https://azure.microsoft.com/en-gb/regions/services/>). We recommend you use East US or East US 2. <p><em>Example:</em> East US</p>                                                                                                                                                                                                                          |
| **Server VM Instance Size** | Specify the size of the VM you plan on using for deployment. Each MATLAB Production Server instance runs on a VM and each instance will run multiple workers. We recommend you choose a VM size where the number of cores on your VM match the number of MATLAB workers per VM you plan on using. The template defaults to: Standard_D4s_v3. This configuration has 4 vCPUs and 16 GiB of Memory. For more information, see Azure [documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-general). <p><em>Example:</em> Standard_D4s_v3</p> |
| **Instance Count**          | Number of VMs to run MATLAB Production Server instances. Each MATLAB Production Server instance runs on a VM and each instance will run multiple workers. The maximum number of MATLAB Production Server instances is limited to 24. This means only a maximum of 24 VMs can be provisioned. Therefore, your instance count cannot exceed 24. <p><em>Example:</em> 6</p><p>If you have a standard 24 worker MATLAB Production Server license and select Standard_D4s_v3 VM (4 cores) as the Server VM Instance Size, you will need 6 VMs to fully utilize the workers in your license. Therefore, your instance count will be 6.</p><p>You can always under provision the number of VMs. In which case you may end up using fewer workers than you are licensed for.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Admin Username**          | Specify the admin user name for all VMs. This will be username to log in to the MATLAB Production Server Cloud Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Admin Password**          | Specify the admin password for all VMs. This will be the password to log in to the MATLAB Production Server Cloud Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

<br />

Click **Purchase** to begin the deployment. This can take up to 40 minutes.

## Step 3. Connect to the Cloud Console
>   **Note:** Complete these steps only after your resource group has been successfully created.

> **Note:** The Internet Explorer web browser is not supported for interacting with the cloud console. 

1.  In the Azure Portal, on the navigation panel on the left, click **Resource
    groups**. This will display all your resource groups.

2.  Select the resource group you created for this deployment from the list. This
    will display the Azure blade of the selected resource group with its own
    navigation panel on the left.

3.  Select the resource labeled **servermachine-public-ip**. This resource
    contains the public IP address to the MATLAB Production Server Cloud
    Console.

4.  Copy the IP address from the IP address field.

5.  In your browser, connect to the cloud console using the IP address and the default port of `9000`. 

>   *Example:*

>   https://<span></span>11.22.135.137:9000


You will now be connected to the MATLAB Production Server Cloud Console.

## Step 4. Log in to the Cloud Console
Use the admin username and password you created in [Step.2](#step-2-configure-cloud-resources) while configuring your
resources to log in to the MATLAB Production Server Cloud Console. The cloud console provides a web-based interface to
configure and manage server instances on the cloud. For more information on how to use the cloud console, see [MATLAB Production Server Cloud Console User's Guide](/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide). 
 
![MATLAB Production Server Cloud Console](/pics/cloudConsoleLogin.png?raw=true)
> **Accept Terms and Conditions**: Access to and use of the MATLAB Production Server Cloud Console is governed by license terms in the file `C:\MathWorks\Cloud Console License.txt` (Linux: `/MathWorks/Cloud Console License.txt`) available on the `servermachine` in the resource group for this solution. 

>**Note**: The cloud console uses a self-signed certificate which can be changed. For information on changing the self-signed certificates, see [Change Self-signed Certificates](/doc/cloudConsoleDoc.md#change-self-signed-certificates).

## Step 5. Upload the License File
> **Note**: You will need a fixed MAC address to get a license file from the MathWorks License Center. For more information, see [Configure MATLAB Production Server Licensing on the Cloud](https://www.mathworks.com/support/cloud/configure-matlab-production-server-licensing-on-the-cloud.html).

1.  In the cloud console, click **Administration** \> **Manage License**.

2.  Click **Browse License File**, select the license file you want to upload,
    and click **Open**.

3.  Click **Upload**.


You are now ready to use MATLAB Production Server on Azure. 

To run applications on MATLAB Production Server, you will need to create applications using MATLAB Compiler SDK. For more information, see [Deployable Archive Creation](https://www.mathworks.com/help/mps/deployable-archive-creation.html) in the MATLAB Production Server product documentation.

# Additional Information 

## Delete Your Resource Group
> **Note**: Your license file is tied to your MAC address. If you delete your
resource group to delete your cluster, you will need to get a new license file.
You are limited to changing your MAC address 4 times per year.

You can remove the resource group and all associated cluster resources when you
are done with them. Note that there is no undo.

1.  Login to the Azure Portal.
2.  Select the resource group containing your cluster resources.
3.  Select the **Delete resource group** icon to destroy all resources deployed
    in this group.
4.  You will be prompted to enter the name of the resource group to confirm the
    deletion.

## Security 
When you run MATLAB Production Server on the cloud you get two HTTPS endpoints that use self-signed certificates. 

1. A HTTPS endpoint to the application gateway that connects the server instances. This endpoint is displayed in the home page of the cloud console and is used to make requests to the server.

1. A HTTPS endpoint to the cloud console. This endpoint is used to connect to the cloud console.

For information on changing the self-signed certificates, see [Change Self-signed Certificates](/doc/cloudConsoleDoc.md#change-self-signed-certificates). 

# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.


![Cluster Architecture](/pics/FinalArchitecture60.png?raw=true)

*Architecture on Azure*

### Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MATLAB Production Server Cloud Console and License Manager virtual machine | `servermachine`           | 1                   | Virtual machine(VM) that hosts the MATLAB Production Server Cloud Console and license manager. Use the cloud console to: <ul><li> Upload your license file and start using the server</li><li>Get HTTP/HTTPS endpoint to make requests</li><li> Upload applications (.ctf files) to the server</li><li> Manage server configurations</li><li> Manage the HTTPS certificate</li></ul><p>For more information, see [MATLAB Production Server Cloud Console User's Guide](/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide).   |
| MATLAB Production Server Cloud Console public IP                           | `servermachine-public-ip` | 1                   | Public IP address to connect to MATLAB Production Server Cloud Console.<p>**NOTE**: Provides HTTPS endpoint to the cloud console for managing server instances.</p>                                                                                                                                                                                                                                                            |
| Virtual machine scale set                                                  | `vmss<uniqueID>`        | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Application gateway                                                        | `vmss<uniqueID>-agw`    | 1                   | Provides routing and load balancing service to MATLAB Production Server instances. The MATLAB Production Server Cloud Console retrieves the HTTP/HTTPS endpoint for making requests to the server from the application gateway resource.<p>**NOTE**: Provides HTTPS endpoint to the server for making requests.</p>                                                                                           |
| Storage account                                                            | `serverlog<uniqueID>`   | NA                  | User provided storage account where logs for the reference architecture are stored. The server logs are stored in an Azure Table.                                                                                                                                                                                                  |
| Virtual network                                                            | `vmss<uniqueID>-vnet`   | 1                   | Enables resources to communicate with each other.                                                                                                                                                                                                                                                                                  |

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: 
https://www.mathworks.com/cloud/enhancement-request.html

# Technical Support
Email: `cloud-support@mathworks.com`

