#!/bin/bash

#DISCOURSE_SERVER="https://messageboard.facingourrisk.org"
#DISCOURSE_SERVER="https://try.discourse.org"
DISCOURSE_SERVER="https://discourse.mckblog.net"
APPLICATION_NAME="forceapps"
PRIVATE_KEY_FILE=/tmp/discourse-private.pem
PUBLIC_KEY_FILE=/tmp/discourse-public.pem

openssl genrsa -out $PRIVATE_KEY_FILE
openssl rsa -in $PRIVATE_KEY_FILE -pubout > $PUBLIC_KEY_FILE

nonce=$(od -N16 -An -w128 -tx8 </dev/urandom) nonce=${nonce// /}
client_id=$(od -N48 -An -w128 -tx8 </dev/urandom) client_id=${client_id// /}
application_name=$APPLICATION_NAME
scopes="read,write"
public_key=$(urlencode "$(<$PUBLIC_KEY_FILE)")

url="$DISCOURSE_SERVER/user-api-key/new?application_name=${application_name}&client_id=${client_id}&scopes=${scopes}&nonce=${nonce}&public_key=${public_key}"

echo -e "$url\n"
echo -n "Enter Discourse response: "; read response

echo
echo Client_Id=\"${client_id}\"
echo -n UserApiKey=
echo "$response" | base64 -di | openssl pkeyutl -decrypt -inkey $PRIVATE_KEY_FILE | jq .key

rm -f $PRIVATE_KEY_FILE $PUBLIC_KEY_FILE
