# MATLAB Production Server Cloud Console User's Guide

1. [Get Information About Server Instances](#get-information-about-server-instances)
1. [Get HTTPS End Point](#get-https-end-point)
1. [Upload a MATLAB Application Created with MATLAB Compiler SDK](#upload-a-matlab-application-created-with-matlab-compiler-sdk)
1. [Edit the Server Configuration](#edit-the-server-configuration)
1. [Edit the Azure Cache for Redis Configuration](#edit-the-azure-cache-for-redis-configuration)
1. [Get License Server MAC Address](#get-license-server-mac-address)
1. [Upload a License File](#upload-a-license-file)
1. [Upload an HTTPS Certificate](#upload-an-https-certificate)
1. [Setup Authentication Using Azure Active Directory](#setup-authentication-using-azure-active-directory)
1. [View Logs](#view-logs)
1. [Change the Number of Virtual Machines](#change-the-number-of-virtual-machines)
1. [Change Self-signed Certificates](#change-self-signed-certificates)

## Get Information About Server Instances
To get information about server instances:
- On the cloud console navigation menu, click **Home**.

![Cloud Console Home](/releases/R2019a/images/cloudConsoleHome.png)

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Get HTTPS End Point
To get the HTTPS end point:
1. On the cloud console navigation menu, click **Home**. 
1. Copy the parameter value listed next to **HTTPS Server Endpoint**.

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Upload a MATLAB Application Created with MATLAB Compiler SDK
To upload an application:
1. On the cloud console navigation menu, click **Applications**. 
1. Click **+Upload Application**.
1. Click **Browse CTF File**, select the file, and click **Upload**.

For information on how to create an application, see [Package Deployable Archives
with Production Server Compiler App](https://www.mathworks.com/help/mps/ml_code/create-a-deployable-ctf-archive-with-the-library-compiler-app.html) in the MATLAB® Compiler SDK™ documentation.
  
[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Edit the Server Configuration
To edit the server configuration:
1. On the cloud console navigation menu, select **Administration** > **Server Configuration**. 
1. Find the server property you want to change and enter the appropriate value. For
a list of server properties and values, see [Server Properties](http://www.mathworks.com/help/mps/propertylist.html).

>**NOTE**: To assign a value to a property that has been commented out, remove the #
symbol and assign a value.

*Example*: Enabling CORS:

`--cors-allowed-origins http://www.w3.org, https://www.apache.org`

>**NOTE**: When setting the `num-workers` property in the server configuration you need to carefully consider your cluster setup. Each virtual machine in the cluster runs an instance of MATLAB Production Server and each instance runs multiple MATLAB workers. MathWorks recommends 1 core per MATLAB worker. For example, a `Standard_D4s_v3` **Server VM Instance Size** has 4 cores; therefore, we recommend you set `num-workers` be no more than 4 per instance.<p>`--num-workers 4`</p> 

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Edit the Azure Cache for Redis Configuration
To edit the Azure Cache for Redis configuration:
- On the cloud console navigation menu, select **Administration** > **Persistence Configuration**.

The cache configuration is specified in JSON format as follows: 
```
{
  "Connections": {
    "<connection_name>": {
      "Provider": "Redis",
      "Host": "<hostname>",
      "Port": <port_number>,
      "Key": <access_key>
    }
  }
}
```
Specify the `<connection_name>`, `<hostname>`, `<port_number>`, and `<access_key>` values in the configuration.

| Value                             | Description                                                |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<connection_name>`               | <p>Specify a name for the connection to the persistence service. This name may be used in MATLAB code to pass data to the cache.</p>                                                          |
| `<hostname>`  and `<port_number>` | <p>Specify the host name and port number for the Azure Cache for Redis from the Azure portal. The port number has to be a non-SSL port. To retrieve the host name and port number:</p><ul><li>Log in to your Azure portal and select the resource group associated with this deployment.</li><li>Select the *Azure Cache for Redis*  resource within the resource group. This resource usually has the name `vmss<uniqueID>redis`.</li><li>Select **Overview** and copy the values listed under **Host name** and under **Ports**.</li></ul><p>*Note*: You can also use an Azure Cache for Redis that was created independently of this deployment. The steps to retreive the host name and port number remain the same.</p> |
| `<access_key>`                    | <p>To retrieve an access key to connect to an Azure Redis Cache resource:</p><ul><li>Log in to your Azure portal and select the resource group associated with this deployment.</li><li>Select the *Azure Cache for Redis*  resource within the resource group. This resource usually has the name `vmss<uniqueID>redis`.</li><li>Select **Overview** and under **Keys** click **Show access keys**.</li><li>In the resulting blade, copy the access key string listed under **Primary**.</li></ul>                                                          |

For more information, see [Use a Data Cache to Persist Data](https://www.mathworks.com/help/mps/ml_code/use-a-data-cache-to-persist-data.html).

[Back to Top](releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Get License Server MAC Address
>**NOTE**: You can get the license server MAC address only after deploying the solution to the cloud. For information on deploying the solution, see [Deployment Steps](/README.md#deployment-steps).

1. Click **Administration** > **License**.
1. Copy the license server MAC address displayed at the top.

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Upload a License File
To upload a license file:
1. On the cloud console navigation menu, select **Administration** > **License**.
1. Click **Browse License File** and select a file. 
1. Click **Upload**.

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Upload an HTTPS Certificate
> **NOTE**: When you upload a new certificate, you will lose all pending requests.

To upload an HTTPS certificate:
1. On the cloud console navigation menu, select **Administration** > **HTTPS Certificate**.
1. Click **Browse Certificate...** and select a certificate file. Only `.pfx` files are supported.
1. Enter the certificate password in the **Certificate Password** field.
1. Click **Upload**.

The server will automatically restart after uploading a certificate. You will
need to log out and log back in.

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Setup Authentication Using Azure Active Directory
You can use Azure Active Directory (Azure AD) to provide an identity to each user. To use Azure AD you will need to specify an:
* Access Control Configuration File
* Access Control Policy File

<table>
  <tr>
    <th>Sample Access Control Configuration File</th>
  </tr>
  <tr>
    <td><pre>{<br>  "tenantId": "54ss4lk1-8428-7256-5fvh-d5785gfhkjh6",<br>  "serverAppId": "j21n12bg-3758-3r78-v25j-35yj4c47vhmt",<br>  "jwksUri": "https://login.microsoftonline.com/common/discovery/keys",<br>  "issuerBaseUri": "https://sts.windows.net/",<br>  "jwksTimeOut": 120<br>}</pre></td>
  </tr>
</table>

<table>
  <tr>
    <th>Sample Access Control Policy File</th>
  </tr>
  <tr>
    <td><pre>{<br>  "version": "1.0.0",<br>  "policy" : [<br>    {<br>      "id": "policy1",<br>      "description": "MPS Access Control policy for XYZ Corp.",<br>      "rule": [<br>        {<br>          "id": "rule1",<br>          "description": "group A can execute ctf magic",<br>          "subject": { "groups": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"] },<br>          "resource": { "ctf": ["magic"] },<br>          "action": ["execute"]<br>        },<br>        {<br>          "id": "rule2",<br>          "description": "group A and group B can execute ctf monteCarlo and fastFourier",<br>          "subject": { "groups": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"]  },<br>          "resource": { "ctf": ["monteCarlo", "fastFourier"] },<br>          "action": ["execute"]<br>        },<br>        {<br>          "id": "rule3",<br>          "description": "QE group C can execute any ctf starts with test",<br>          "subject": { "groups": ["cccccccc-cccc-cccc-cccc-cccccccccccc"] },<br>          "resource": { "ctf": ["test*"] },<br>          "action": ["execute"] <br>        }<br>      ]<br>    }<br>  ]<br>}<br></pre></td>
  </tr>
</table>

For more information, see [Access Control](https://www.mathworks.com/help/mps/server/access_control.html).&nbsp;

After you enter the details of each file and click **Save and Apply Configuration**, you will need to edit the [Server Configuration](#edit-the-server-configuration) and enable the option `access-control-provider`.

[Back to Top](releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## View Logs
Logs are stored in your Azure storage account and can be viewed using the Azure Storage Explorer. To view server logs:

1. Download and install the Microsoft Azure Storage Explorer.
2. Sign-on using your Azure account.
3. Expand the storage account associated with your selected Azure subscription. The storage account name is diplayed in the View Logs section of the cloud console. 
4. Expand Tables and view: MasterController, mpsInstances, mpsNative
    - `MasterController`: Log of user logins, deployed archives (.ctf files), certificate changes, and user interface actions.
    - `mpsInstances`: Log of orchestrator code for server virtual machines.
    - `mpsNative`: Log of activity generated by the server instance.

[Back to Top](/releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Change the Number of Virtual Machines
You cannot change the number of virtual machines (VMs) from the cloud console.
To change the number of VMs:

1. Log in to the Azure Portal
1. Change the number of virtual machines in the virtual machine scale set resource (`vmss<uniqueID>`).

![Scaling](/releases/R2019a/images/azureScaling.png)

If you have a standard 24 worker MATLAB Production Server license and select `Standard_D4s_v3 VM` as the **Server VM Instance Size** during setup, you will need 6 VMs to fully utilize the workers in your license.

The Azure Resource Manager (ARM) template by default has the `overprovision`
property set to `true`. This means Azure will provision more virtual machines than
necessary for a brief period to buffer against any machines that may fail. Once
all virtual machines are healthy, Azure will scale down to the number of virtual
machines you specified. For more information, see [Azure Virtual Machine Scale Sets FAQs](https://releases/R2019a/docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq).

[Back to Top](releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

## Change Self-signed Certificates
You can change the self-signed certificate to:
- The HTTPS endpoint to the application gateway. This endpoint is used to make requests to the server. 
- The HTTPS endpoint to the cloud console. This endpoint is used to connect to the cloud console. 

To change the self-signed certificate used to connect to the cloud console, see [Upload an HTTPS Certificate](#upload-an-https-certificate).

To change the self-signed certificate to the application gateway you need to complete a twostep process in the Azure Portal.

1.  Create a listener

2.  Add a rule
 
> NOTE: The application gateway HTTPS endpoint is used to make requests to the server. 

[Back to Top](releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)

### Create a Listener
<ol>
<li>In the resource group for the solution, select the application gateway
    resource with the name <code>vmss&lt;uniqueID&gt;-agw</code>.</li>

<li>Select <strong>Listeners</strong> from the navigation panel on the left and click
    <strong>+Basic</strong> at the top of the expanded panel.</li>

<li>Enter parameter values:

<table>
<tbody>
<tr>
<td width="312">
<p><strong>Name</strong></p>
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
<p>Leave as is.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Frontend port</p>
</td>
<td width="312">
<p>Select <strong>+New</strong>.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Name</p>
</td>
<td width="312">
<p>Enter a name for the port.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Port</p>
</td>
<td width="312">
<p>Any free port between 8001 - 10000.</p>
</td>
</tr>
</tbody>
</table>

<li>Flip the tab to HTTPS.</li>

<li>In the <strong>Certificate</strong> dropdown menu, select <strong>+New</strong>.</li>

<li>Upload a PFX certificate, give it a name, and create a password.
    Click <strong>OK</strong>.</li>
</ol>


### Add a Rule
<ol>
<li>In the resource group for the solution, select the application gateway resource with the name <code>vmss&lt;uniqueID&gt;-agw</code>.</li>
<li>Select <strong>Rules</strong> from the navigation panel on the left and click <strong>+Basic</strong> at the top of the expanded panel.</li>
<li>Enter parameter values:</li>
</ol>
<table>
<tbody>
<tr>
<td width="312">
<p><strong>Name</strong></p>
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
<p>Enter a name for the rule.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Listener</p>
</td>
<td width="312">
<p>Select the listener you created.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Configure redirection</p>
</td>
<td width="312">
<p>Check box if appropriate.</p>
</td>
</tr>
<tr>
<td width="312">
<p>Backend pool</p>
</td>
<td width="312">
<p>Select appropriate value.</p>
</td>
</tr>
<tr>
<td width="312">
<p>HTTP setting</p>
</td>
<td width="312">
<p>Select appropriate value.</p>
</td>
</tr>
</tbody>
</table>
<p>Click <strong>OK</strong>.</p>


[Back to Top](releases/R2019a/doc/cloudConsoleDoc.md#matlab-production-server-cloud-console-users-guide) | [Back to Main](/README.md#matlab-production-server-on-azure)
