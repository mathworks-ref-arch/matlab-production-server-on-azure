## Release Notes for MATLAB Production Server on Microsoft Azure

### R2025a
- You can assign a private IP for the Network License Manager VM. Previously, you could only assign the Network License Manager VM a public IP address.
- You can allow a range of IP addresses to access the Network License Manager dashboard.
- The **Assign Public IP Address to VM Hosting MATLAB Production Server** entry of the deployment template now controls access to the storage account. For details, see the **Assign Public IP Address to VM Hosting MATLAB Production Server** entry in the [Configure Cloud Resources](/releases/R2025a/README.md#step-2-configure-cloud-resources) step of the deployment process.
    - If you assign a public IP address to the VM hosting MATLAB Production Server, then public network access to the storage account is enabled only from selected virtual networks and IP addresses. Previously, public network access was enabled from all networks.
    - If you assign a private IP address to the VM hosting MATLAB Production Server, then public network access to the storage account is disabled. You must use a bastion host or jump box VM to connect to the storage account. Previously, storage account access was enabled from all networks.
- If you deploy using an existing virtual network, you must manually add a private or service endpoint to the virtual network before deploying MATLAB Production Server in order to create and access the storage account. For details, see [Create Endpoint in Virtual Network](/releases/R2025a/README.md#create-endpoint-in-virtual-network).