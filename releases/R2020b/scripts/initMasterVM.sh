#!/bin/bash

WORKSPACE=/opt/mathworks

# $0 is the file name

storageAccountName="$1"
storageAccountKey="$2"
dbConnectionString="$3"
mpsEndpoint="$4"
CIDRRange="$5"
cloudPlatform="$6"
osPlatform="$7"
ikey="$8"
resourceGroup="$9"
subscriptionID="${10}"
userName="${11}"
passWord="${12}"
test="${13}"
redisName="${14}"
gatewayPrivateIP="${15}"
offerType="${16}"

echo $storageAccountName
echo $storageAccountKey
echo $dbConnectionString
echo $mpsEndpoint
echo $CIDRRange
echo $cloudPlatform
echo $osPlatform
echo $ikey
echo $resourceGroup
echo $subscriptionID
echo $userName
echo $redisName
# echo $passWord
echo $gatewayPrivateIP
echo $offerType

JSONCMD='
{
	"storageAccountName": "'"$storageAccountName"'",
	"storageAccountKey": "'"$storageAccountKey"'",
	"test": "'"$test"'",
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
    "offerType": "'"$offerType"'"
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
# should we do sudo here
systemctl restart refarchcontroller

echo "Restarted daemon successfully!"


# chown to this user /opt/mathworks 
# Clear history
history -c

echo "Cleared History!"
# File Location
#https://mwstorage24.blob.core.windows.net/azuretemplates/initVm.sh