# MATLAB Production Server on Microsoft Azure

# Requirements

Before starting, you need the following:

-   A MATLAB® Production Server™ license that meets the following conditions:
    - Linked to a [MathWorks Account](https://www.mathworks.com/mwaccount/).
    - Concurrent license type. To check your license type, see [MathWorks License Center](https://www.mathworks.com/licensecenter/). 
    - Configured to use a network license manager on the virtual network. By default, the deployment of MATLAB Production Server includes a network license manager, but you can also use an existing license manager. In either case, activate or move the license after deployment. For details, see [Configure MATLAB Production Server License for Use on the Cloud](https://www.mathworks.com/help/mps/server/configure-matlab-production-server-license-for-use-on-the-cloud.html).   
-   A Microsoft Azure™ account.

If you do not have a license, please contact your MathWorks representative [here](https://www.mathworks.com/company/aboutus/contact_us/contact_sales.html) or [request a trial license](https://www.mathworks.com/campaigns/products/trials.html?prodcode=PR).

# Costs
You are responsible for the cost of the Azure services used when you create cloud resources using this guide. Resource settings, such as instance type, affect
the cost of deployment. For cost estimates, see the pricing pages for each Azure
service you are using. Prices are subject to change.


# Introduction 
Use this guide to automate the process of running MATLAB
Production Server on Azure using your Azure account. The automation is
accomplished using an Azure Resource Manager (ARM) template. The template is a JSON
file that defines the resources needed to deploy and manage MATLAB Production
Server on Azure. Once deployed, you can manage the server using the
MATLAB Production Server Dashboard&mdash;a web-based interface to
configure and manage server instances on the cloud. For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).
For information about the architecture of this solution, see [Architecture and Resources](#architecture-and-resources).

# Deploy Reference Architecture for Your Release
To deploy the reference architecture, select your MATLAB Production Server release from the table and follow the instructions to deploy the server using the provided template. A deployment of MATLAB Production Server supports MATLAB Runtime versions up to six releases back.
| Release | Supported MATLAB Runtime Versions |
| ------- | --------------------------------- |
| [R2025a](releases/R2025a/README.md) | R2025a, R2024b, R2024a, R2023b, R2023a, R2022b |
| [R2024b](releases/R2024b/README.md) | R2024b, R2024a, R2023b, R2023a, R2022b, R2022a |
| [R2024a](releases/R2024a/README.md) | R2024a, R2023b, R2023a, R2022b, R2022a, R2021b |
| [R2023b](releases/R2023b/README.md) | R2023b, R2023a, R2022b, R2022a, R2021b, R2021a |
| [R2023a](releases/R2023a/README.md) | R2023a, R2022b, R2022a, R2021b, R2021a, R2020b |
| [R2022b](releases/R2022b/README.md) | R2022b, R2022a, R2021b, R2021a, R2020b, R2020a |

> **Note**: MathWorks provides templates for only the six most recent releases of MATLAB Production Server. Earlier templates are removed and are no longer supported.
# Architecture and Resources
Deploying this reference architecture will create several resources in your
resource group.

*Architecture on Azure*

![Cluster Architecture](/releases/R2023a/images/mps-ref-arch-azure-architecture-diagram.jpg?raw=true)

## Resources
### Matlab Production Server Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                            |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Virtual network | `mps-network` | 1 | Provide support and security to the operation of MATLAB Production Server. |
| Storage account                                                            | `serverlog<uniqueID>`   | 1                  | Storage account where the deployable archives (CTF files) created by MATLAB® Compiler SDK™ will be stored. The deployable archives (CTF files) will be stored in a file share.                                                                                                                           |
| Application Insights |  `logs-apmservice` | 1 | Enables storing and viewing of all logs associated with deployment. |
| Log analytics workspace | `logs-workspace` | 1 | Workspace that contains data collected from various sources. |

### Virtual Machine Scale Set Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                            |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Virtual machine scale set                                                  | `vmss<uniqueID>`        | 1                   | Manages the number of identical VMs to be deployed. Each VM runs an instance of MATLAB Production Server which in turn runs multiple MATLAB workers.                                                                                                                                                                               |
| Application gateway                                                        | `vmss<uniqueID>-agw`    | 1                   | Provides routing and load balancing service to MATLAB Production Server instances. The MATLAB Production Server dashboard retrieves the HTTP/HTTPS endpoint for making requests to the server from the application gateway resource.<p>**NOTE**: Provides HTTPS endpoint to the server for making requests.</p>                                                                                           |
| Virtual network                                                           | `vmss<uniqueID>-vnet`   | 1                   | Enables resources to communicate with each other.                                                                                                                                                                                                                                                                                  |
|Network security group | `vmss<uniqueID>-rdp-nsg` | 1 | Filter network traffic to and from virtual machine scale set in an Azure virtual network. |
|Public IP address | `Vmss<uniqueID>-pip` | 1 | Provide public IP address to virtual machine scale set. |

### Admin Dashboard Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                            |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MATLAB Production Server dashboard virtual machine | `admindashboard`           | 1                   | Virtual machine (VM) that hosts the MATLAB Production Server dashboard. Use the dashboard to: <ul><li>Get HTTP/HTTPS endpoint to make requests</li><li> Upload applications (CTF files) to the server</li><li> Manage server configurations</li></ul><p>For more information, see [Manage MATLAB Production Server Using the Dashboard](https://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html).   |
| MATLAB Production Server dashboard public IP                           | `admindashboard-public-ip` | 1                   | Public IP address to connect to MATLAB Production Server dashboard.<p>**NOTE**: Provides HTTPS endpoint to the dashboard for managing server instances.</p>                                                                                                                                                                                                                                                            |
| Disk | `admindashboard_OsDisk_<uniqueID>` | 1 | Operating system disk attached to admin dashboard. |
| Network interface	| `admindashboard-nic` | 1	| Provide network interface for admin dashboard. |

### Redis Resources
| Resource Name                                                              | Resource Name in Azure  | Number of Resources | Description                                                                                                            |
|----------------------------------------------------------------------------|-------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Azure Cache for Redis |  `vmss<uniqueID>redis` | 1 | Enables caching of data between calls to MATLAB code running on a server instance. |
| Network interface	| `redisPrivateEndpoint.nic.<uniqueID>` | 1 | Provide network interface for Redis private endpoint. |
|Private DNS zone | `privatelink.redis.cache.windows.net` | 1 | Provide DNS resolution for the private endpoint of Redis cache.|
| Private endpoint | `redisPrivateEndpoint` | 1 | Private endpoint for Redis.|

**Note**: Some or all of these resources will get created depending on inputs provided to the deployment template. For example, Redis may or may not get created.

# FAQ

## How do I deploy to an existing virtual network?
>**Note:** Your existing virtual network must have at least two available subnets for deployment. 

### Create Service Endpoint in Virtual Network (Since R2025a)
Starting in R2025a, If you are using an existing virtual network and assign a public IP address to the VM hosting MATLAB Production Server, then you must manually add a service endpoint to the virtual network *before* deploying MATLAB Production Server in order to create and access the storage account. Service Endpoints enable private IP addresses in the VNet to reach the endpoint of an Azure service without needing a public IP address on the VNet. For more details, see [Virtual Network service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview).

You can check if such an endpoint already exists by navigating to the Azure Portal, selecting your virtual network, and clicking **Service endpoints**. If no such endpoint is present, follow these steps:
1. In the Azure Portal, click **Resource groups** and select the virtual network for this deployment.
1. In the left navigation menu, expand the **Settings** category and click **Service endpoints**.
1. Click **Add** to add the new endpoint. It must have the following parameters:

    <table>
      <tr><td><b>Service</b></td><td>Microsoft.Storage</td></tr>
      <tr><td><b>Subnet</b></td><td>Name of subnet in which the storage account will be deployed</td></tr>      
    </table>

For more information on creating endpoints, see [Create and associate service endpoint policies](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoint-policies).

### Deploy to Existing Virtual Network
To deploy MATLAB Production Server to an existing virtual network, set the **Deploy to New or Existing Virtual Network** parameter to `existing`.

Set the following parameter values in the template based on your existing virtual network. 

| Parameter Name          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Virtual Network Name** |  Specify the name of your existing virtual network or use the default value.   |
| **Virtual Network CIDR Range** |  Specify the IP address range of the virtual network in CIDR notation or use the default value. |
| **Subnet 1 CIDR Range** |  Specify the IP address range of the first subnet in CIDR notation or use the default value. The first subnet hosts the dashboard and other resources. | 
| **Subnet 2 CIDR Range** | Specify the IP address range of the second subnet in CIDR notation or use the default value. The second subnet hosts the application gateway. |
| **Available Subnet 2 IP Address** |   Specify an unused IP address from Subnet 2 or use the default value. This IP address serves as the private IP of the application gateway. |
| **Resource Group Name Of Virtual Network** |   Specify the resource group name of the virtual network or use the default value.    |

### Ports to Open in Existing Virtual Network
If you are deploying to an existing virtual network, open these ports in your network:
| Port | Description |
| ------------------|---------------------------------------------------------------------------------------------------------------- |
| `443` | Required for communicating with the dashboard |
| `8000`, `8004`, `8080`, `9090`, `9910` | Required for communication between the dashboard, MATLAB Production Server workers, and various microservices within the virtual network. These ports do not need to be open to the Internet. | 
| `27000` | Required for communication between the Network License Manager and the workers. | 
| `65200`, `65535` | Required for the Azure application gateway health check to work. These ports need to be accessible over the Internet. For more information, see [MSDN Community](https://social.msdn.microsoft.com/Forums/azure/en-US/96a77f18-3b71-45d2-a213-c4ba63fd4e63/internal-application-gateway-backend-health-is-unkown?forum=WAVirtualMachinesVirtualNetwork). | 
| `22`, `3389` | (Optional) Enables Remote Desktop functionality, which can be used for troubleshooting and debugging. |
<br>
You can close ports 22 and 3389 after deployment.

## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors occur either when CORS is not enabled on the server or when the server endpoint uses a self-signed certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and JavaScript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Alternatively, you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate to Application Gateway](https://www.mathworks.com/help/mps/server/configure-azure-resources-reference-architecture.html#mw_6ae700e7-b895-4e90-b0fb-7292e905656e_sep_mw_1fd15ea2-d161-4694-963d-41a81fc773bf). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
