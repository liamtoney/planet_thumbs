#!/bin/bash

# Check for correct number of input arguments
if [ $# -ne 3 ]; then
  echo "You must provide exactly three arguments!"
  exit 1
fi

# Make shortcut for repeated curl args
curl_auth () { curl -L -H "Authorization: api-key $PL_API_KEY" $*; }

# Build URL for asset
asset_url="https://api.planet.com/data/v1/item-types/$2/items/$1/assets/"

# Activate asset
curl_auth -s -X POST `curl_auth -s $asset_url | jq -r .$3._links.activate`

# Check asset status
status=`curl_auth -s $asset_url | jq -r .$3.status`

# Attempt to download asset
if [ "$status" = "active" ]; then
  curl_auth `curl_auth -s $asset_url | jq -r .$3.location` > $1_$2_$3.tif
else  # Either the asset is being activated, or it's null (likely doesn't exist)
  echo $status
fi
