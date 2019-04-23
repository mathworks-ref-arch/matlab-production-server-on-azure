<#
    .SYNOPSIS
        This Script runs on master head node start, it is used in the ARM template tp ass around the storage account name, key
        as well as the mpsEndpoint. It saves the result to local disk and restarts the main nodeJS dashboard process running on the VM
        Used for Reference architecture 18b Update 2 (v 2.2.0)
#>

Param (
    [String]$storageAccountName,
    [String]$storageAccountKey,
    [String]$dbConnectionString,
    [String]$mpsEndPoint,
    [String]$CIDRRange,
	[String]$cloudPlatform,
	[String]$osPlatform
)

# Firewall
netsh advfirewall firewall add rule name="http" dir=in action=allow protocol=TCP localport=80



$myObj = New-Object System.Object

$myObj | Add-Member -type NoteProperty -name storageAccountName -value $storageAccountName
$myObj | Add-Member -type NoteProperty -name storageAccountKey -value $storageAccountKey
$myObj | Add-Member -type NoteProperty -name dbConnectionString -value $dbConnectionString
$myObj | Add-Member -type NoteProperty -name mpsEndPoint -value $mpsEndPoint
$myObj | Add-Member -type NoteProperty -name CIDRRange -value $CIDRRange
$myObj | Add-Member -type NoteProperty -name cloudPlatform -value $cloudPlatform
$myObj | Add-Member -type NoteProperty -name osPlatform -value $osPlatform

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False

$myContent = $myObj | ConvertTo-Json -Depth 100 
$myPath = "c:\\MathWorks\\controllerServer\\config\\dynamicOptions.json"
[System.IO.File]::WriteAllLines($myPath, $myContent, $Utf8NoBomEncoding)

# Out-File "c:\\MathWorks\\controllerServer\\config\\dynamicOptions.json" -Encoding UTF8


# restart the main process
net stop controllerServer5.exe
echo "Stopped the process successfully"
net start controllerServer5.exe
echo "Started the process successfully"

# create the File share
#$fileshareName="mps";
#$acctKey = ConvertTo-SecureString -String $storageAccountKey -AsPlainText -Force
#$credential = New-Object System.Management.Automation.PSCredential -ArgumentList "Azure\$storageAccountName", $acctKey
##New-PSDrive -Name Z -PSProvider FileSystem -Root "\\mpsstoragenew.file.core.windows.net\mohamed" -Credential $credential -Persist
#New-PSDrive -Name Z -PSProvider FileSystem -Root "\\$storageAccountName.file.core.windows.net\$fileshareName" -Credential $credential -Persist