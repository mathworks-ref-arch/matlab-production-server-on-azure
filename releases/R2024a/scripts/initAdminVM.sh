#!/bin/bash

WORKSPACE=/opt/mathworks

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

systemctl restart refarchcontroller

echo "Restarted daemon successfully!"


# chown to this user /opt/mathworks 
# Clear history
history -c

echo "Cleared History!"
# File Location
#https://mwstorage24.blob.core.windows.net/azuretemplates/initVm.sh