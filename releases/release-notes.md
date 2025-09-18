## Release Notes for MATLAB Production Server on Microsoft Azure

### R2025b
- You can now deploy MATLAB Production Server R2025b using the Microsoft Azure reference architecture.

### R2025a
- You can now deploy MATLAB Production Server R2025a using the Microsoft Azure reference architecture.
- The **Assign Public IP Address to VM Hosting MATLAB Production Server** parameter of the deployment template now controls access to the storage account. For details, see the **Assign Public IP Address to VM Hosting MATLAB Production Server** parameter in the [Configure Cloud Resources](/releases/R2025a/README.md#step-2-configure-cloud-resources) step of the deployment process.
    - If you assign a public IP address to the VM hosting MATLAB Production Server, then public network access to the storage account is enabled only from selected virtual networks and IP addresses. Previously, public network access was enabled from all networks.
    - If you assign a private IP address to the VM hosting MATLAB Production Server, then public network access to the storage account is disabled. You must use a bastion host or jump box VM to connect to the storage account. Previously, storage account access was enabled from all networks.
- If you deploy using an existing virtual network and assign a public IP address to the VM hosting MATLAB Production Server, you must manually add a service endpoint to the virtual network before deploying MATLAB Production Server in order to create and access the storage account. For details, see [How do I deploy to an existing virtual network?](/README.md#how-do-i-deploy-to-an-existing-virtual-network)
- You can now specify a range of IP addresses for the **Allow Connections From** parameter with a comma-separated list.

### R2024b
- You can now deploy MATLAB Production Server R2024b using the Microsoft Azure reference architecture.
- You can assign a private IP address for the Network License Manager VM. Previously, you could only assign the Network License Manager VM a public IP address.
- You can allow a range of IP addresses to access the Network License Manager dashboard.