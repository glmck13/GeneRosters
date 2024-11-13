#!/bin/bash

PATH=/var/www/bin:$PATH

. forcenv-roster.sh

if [ "$*" ]; then
	for gene in $*
	do
		curl -s -H "User-Api-Key: ${UserApiKey}" -H "Content-Type: application/json" --data @- "${Forum}/posts.json" <<-EOF
		{
		  "title": "${gene} mutation roster",
		  "raw": "This is the first post!",
		  "category": ${Category}
		}
		EOF
		echo; echo
	done
else
	curl -s -H "User-Api-Key: ${UserApiKey}" "${Forum}/search.json?q=roster+#${Slug}" | jq .posts[].topic_id | while read topic
	do
		echo -n "Topic=$topic, "
		curl -s -H "User-Api-Key: ${UserApiKey}" "${Forum}/t/${topic}.json" | jq '"Title=\(.title), Post=\(.post_stream.posts[0].id)"'
		sleep 3
	done
fi
