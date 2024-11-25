#!/bin/bash

PATH=/var/www/bin:$PATH

exec 3<> /var/www/tmp/force-roster.lock
flock -x 3

todo=$(force_roster.py)

if [ "$todo" ]; then
	force_roster.py $todo
	force_stories.py $todo
fi
