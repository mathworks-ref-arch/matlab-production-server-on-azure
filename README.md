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
| [R2024a](releases/R2024a/README.md) | R2024a, R2023b, R2023a, R2022b, R2022a, R2021b |
| [R2023b](releases/R2023b/README.md) | R2023b, R2023a, R2022b, R2022a, R2021b, R2021a |
| [R2023a](releases/R2023a/README.md) | R2023a, R2022b, R2022a, R2021b, R2021a, R2020b |
| [R2022b](releases/R2022b/README.md) | R2022b, R2022a, R2021b, R2021a, R2020b, R2020a |
| [R2022a](releases/R2022a/README.md) | R2022a, R2021b, R2021a, R2020b, R2020a, R2019b |
| [R2021b](releases/R2021b/README.md) | R2021b, R2021a, R2020b, R2020a, R2019b, R2019a |

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

## Why do requests to the server fail with errors such as “untrusted certificate” or “security exception”?  

These errors occur either when CORS is not enabled on the server or when the server endpoint uses a self-signed certificate. 

If you are making an AJAX request to the server, make sure that CORS is enabled in the server configuration. You can enable CORS by editing the property `--cors-allowed-origins` in the config file. For more information, see [Edit Server Configuration](http://www.mathworks.com/help/mps/server/use-matlab-production-server-cloud-dashboard-on-azure-reference-architecture.html#mw_d9c9b367-376f-4b31-a97e-ed894abfcbbe).

Also, some HTTP libraries and JavaScript AJAX calls will reject a request originating from a server that uses a self-signed certificate. You may need to manually override the default security behavior of the client application. Alternatively, you can add a new 
HTTP/HTTPS endpoint to the application gateway. For more information, see [Change SSL Certificate to Application Gateway](https://www.mathworks.com/help/mps/server/configure-azure-resources-reference-architecture.html#mw_6ae700e7-b895-4e90-b0fb-7292e905656e_sep_mw_1fd15ea2-d161-4694-963d-41a81fc773bf). 

# Enhancement Request
Provide suggestions for additional features or capabilities using the following link: https://www.mathworks.com/solutions/cloud.html

# Technical Support
If you require assistance or have a request for additional features or capabilities, please contact [MathWorks Technical Support](https://www.mathworks.com/support/contact_us.html).
