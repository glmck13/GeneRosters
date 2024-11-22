#!/bin/bash

PATH=/var/www/bin:$PATH

exec 3<> /var/www/tmp/force-roster.lock
flock -x 3

force_stories.py
