#!/bin/ksh

ETCDIR="/var/www/etc"
BINDIR="/var/www/bin"

. $BINDIR/forcenv.sh

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
	print $vars | IFS='&' read v vars
	[ "$v" ] && export ${v%%=*}="$(urlencode -d ${v#*=})"
done

echo -e "Content-Type: text/html\n"

nonce=$(od -N16 -An -w128 -tx8 </dev/urandom) nonce=${nonce// /}
#client_id=$(od -N48 -An -w128 -tx8 </dev/urandom) client_id=${client_id// /}
scopes="read"
public_key=$(urlencode "$(<$ETCDIR/discourse-public.pem)")
url="$Forum/user-api-key/new?application_name=${AppName}&client_id=${Client_Id}&scopes=${scopes}&nonce=${nonce}&public_key=${public_key}"

cat - <<-EOF
	<html>

	<head>
	<link rel="stylesheet" href="/style.min.css">
	</head>

	<body>
	<div>

	<h1>FORCE API Key Utility</h1>
	<p>
	Click <a href="$url" target="_blank">here</a> to request an API key to access the FORCE message board.
	After logging in you'll be redirected to a page that asks you to authorize access for the "mckapp" app. Click "Authorize".
	You'll then come to a page which says: <i>"We just generated a new user API key for you to use with "mckapp", please paste the following key into your application:"</i>
	Copy and paste the entire block of characters from that page into the text box below, then click "Submit".
	</p>
	<form method=POST>
	<textarea rows=4 name="response">${response}</textarea>
	<input type="submit" name="action" value="Submit">
	</form>
EOF

if [ "$response" ]; then
	apikey=$(echo "$response" | base64 -di | openssl pkeyutl -decrypt -inkey $ETCDIR/discourse-private.pem | jq .key 2>/dev/null)
	apikey=${apikey//\"/}
	if [ "$apikey" ]; then
		cat - <<-EOF
		<hr>
		<p>Your API key is: ${apikey}</p>
		<p>You can now use this to run the <a href="$Helper/force-search.cgi?apikey=${apikey}" target="_blank">FORCE Search Utility</a>. Bookmark the link to run the utility whenever you want to searh the FORCE message board.</p>
		EOF
	else
		cat - <<-EOF
		<hr>
		<p>Something failed. &#x1F641; Try again...</p>
		EOF
	fi
fi

cat - <<-EOF
	</div>
	</body>
	</html>
EOF
