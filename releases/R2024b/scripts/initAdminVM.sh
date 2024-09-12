#!/bin/bash

WORKSPACE=/opt/mathworks

LOG_DIR=/var/log/custom_script
LOG_FILE=$LOG_DIR/custom_script.log

# Create log directory and file
sudo mkdir -p $LOG_DIR
sudo touch $LOG_FILE
sudo chmod 666 $LOG_FILE

# $0 is the file name

storageAccountName="$1"
dbConnectionString="$2"
mpsEndpoint="$3"
CIDRRange="$4"
cloudPlatform="$5"
osPlatform="$6"
ikey="$7"
resourceGroup="$8"
subscriptionID="$9"
userName="${10}"
passWord="${11}"
redisName="${12}"
gatewayPrivateIP="${13}"
offerType="${14}"

azEnvironment=$(sudo curl -s -H Metadata:true --noproxy "*" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" | jq -r '.compute.azEnvironment')

echo "$storageAccountName"
echo "$dbConnectionString"
echo "$mpsEndpoint"
echo "$CIDRRange"
echo "$cloudPlatform"
echo "$osPlatform"
echo "$ikey"
echo "$resourceGroup"
echo "$subscriptionID"
echo "$userName"
echo "$redisName"
echo "$gatewayPrivateIP"
echo "$offerType"
echo "$azEnvironment"

JSONCMD='
{
	"storageAccountName": "'"$storageAccountName"'",
	"dbConnectionString": "'"$dbConnectionString"'",
	"mpsEndPoint": "'"$mpsEndpoint"'",
	"CIDRRange": "'"$CIDRRange"'",
	"cloudPlatform": "'"$cloudPlatform"'",
	"osPlatform": "'"$osPlatform"'",
	"ikey": "'"$ikey"'",
	"resourceGroup": "'"$resourceGroup"'",
	"subscriptionID": "'"$subscriptionID"'",
	"redisCacheName": "'"$redisName"'",
	"gatewayPrivateIP": "'"$gatewayPrivateIP"'",
  "offerType": "'"$offerType"'",
  "azEnvironment": "'"$azEnvironment"'"
}
'

destination=$WORKSPACE/controller/dynamicOptions.json
rm $destination

echo $JSONCMD >> $destination

echo "Written Config File successfully"

cd $WORKSPACE/cloud/main
node $WORKSPACE/cloud/main/server/hash_pw.js "${userName}" "${passWord}" "${passWord}"

echo "Written sudo passwd successfully"

cp ./.shadow ./bin/.

echo "Copied shadow file"

# Update package lists and log errors
sudo apt-get update 2>> $LOG_FILE
if [ $? -ne 0 ]; then
  echo "apt update failed. Check the log file at $LOG_FILE" | tee -a $LOG_FILE
fi

# Install openssh-server and log errors
sudo apt-get install -y openssh-server 2>> $LOG_FILE
if [ $? -ne 0 ]; then
  echo "apt install failed. Check the log file at $LOG_FILE" | tee -a $LOG_FILE
fi

systemctl restart refarchcontroller

echo "Restarted daemon successfully!"


# chown to this user /opt/mathworks 
# Clear history
history -c

echo "Cleared History!"
# File Location
#https://mwstorage24.blob.core.windows.net/azuretemplates/initVm.sh