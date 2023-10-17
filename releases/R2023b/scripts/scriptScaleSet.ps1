<#
    .SYNOPSIS
        This Script runs on MPS instances
#>

# Param (
#     [Parameter(Mandatory=$False)][string]$SERVER_MODE
# )

# disable automatic updates
Echo "disabling automatic updates"
$service = Get-WmiObject Win32_Service -Filter 'Name="wuauserv"'
if ($service)
{
	if ($service.StartMode -ne "Disabled")
	{
		$result = $service.ChangeStartMode("Disabled").ReturnValue
		if($result)
		{
			Echo "Failed to disable the 'wuauserv' service. The return value was $result."
		}
		else {Echo "Success to disable the 'wuauserv' service."}
			
		if ($service.State -eq "Running")
		{
			$result = $service.StopService().ReturnValue
			if ($result)
			{
				Echo "Failed to stop the 'wuauserv' service. The return value was $result."
			}
			else {Echo "Success to stop the 'wuauserv' service."}
		}
	}
	else {Echo "The 'wuauserv' service is already disabled."}
}
else {Echo "Failed to retrieve the service 'wuauserv'."}

#Disable Automatic Windows Updates
Set-ItemProperty -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU -Name AUOptions -Value 1

# exclude .ctf file from windows defender scanning
#Add-MpPreference -ExclusionExtension ".ctf"

#Get-ChildItem "C:\Program Files\MATLAB\MATLAB Runtime\" -Directory | 
#    ForEach-Object {
#		Echo ($_.FullName + '\bin\win64\extractCTF.exe')
#        Add-MpPreference -ExclusionProcess ($_.FullName + '\bin\win64\extractCTF.exe')
#    }

Stop-Service -Name Spooler -Force

Set-Service -Name Spooler -StartupType Disabled

# Execute reboot required for domain join
#Restart-Computer