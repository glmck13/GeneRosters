#!/bin/bash

PATH=/var/www/bin:$PATH

exec 3<> /var/www/tmp/force-roster.lock
flock -x 3

likes=$(force-roster.py)

[ "$likes" ] && force-roster.py $likes
