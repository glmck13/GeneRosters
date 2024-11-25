#!/usr/bin/env python3

import sys, os, json, time
import requests
from forcenv import *
from urllib.parse import parse_qs
from pprint import pprint

#PERIODS = ["all", "yearly", "quarterly", "monthly", "weekly", "daily"]
PERIODS = ["daily"]

Headers = {"User-Api-Key" : UserApiKey, "Content-Type": "application/json", "Accept" : "application/json" }

api_count = 0
header_row = []

for p in PERIODS:

	next = "/directory_items?period={}&order=days_visited".format(p)
	done = False

	while not done:
		try:
			Body = requests.get(Forum + next, headers=Headers).json()
			api_count += 1
			#print(api_count, file=sys.stderr)
			if (api_count % API_MAX_PER_MINUTE) == 0:
				time.sleep(API_DELAY_SECS)
		except:
			Body = {}

		if not Body:
			done = True
			break

		#print(Body, file=sys.stderr)

		stats = Body.get("directory_items", [])

		if len(stats) <= 0:
			break

		if not header_row:
			s = stats.pop(0)
			header_row = [k for k in s.keys()]
			header_row.append("period")
			print(','.join(header_row))

		for s in stats:
			if not s["days_visited"]:
				done = True
				break
			s["user"] = s["user"]["username"]
			s["period"] = p
			print(','.join(str(s.get(k, 0)) for k in header_row))

		#pprint(Body["meta"])

		next = Body.get("meta", {}).get("load_more_directory_items", "")
		if not next:
			done = True
