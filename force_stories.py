#!/usr/bin/env -S PYTHONHASHSEED=0 python3

import sys, os, json, time
import requests
from forcenv_roster import *

API_MAX_PER_MINUTE = 15
Headers = {"User-Api-Key" : UserApiKey, "Content-Type": "application/json", "Accept" : "application/json" }

api_count = 0

for q, r in RosterData.items():

	Table = {}
	TableCols = ["UserName"]
	Topic = r["Topic"]
	Post = r["Post"]
	PostSubj = r["PostSubj"]
	PostBody = r["PostBody"]
	FormText = r["FormText"]
	for k, v in r["FormVars"].items():
		if v["col"]:
			TableCols.append(k)
	TableCols.append("MyStory")

	api_count += 1
	if (api_count % API_MAX_PER_MINUTE) == 0:
		time.sleep(10)
	try:
		Body = requests.get(Forum + "/posts/{}.json".format(Post), headers=Headers).json()
	except:
		continue

	skip = 2
	for line in Body.get("raw", "").split('\n'):
		if not len(line):
			continue
		if line[0] != '|':
			continue
		skip -= 1
		if skip >= 0:
			continue
		row = line.split('|')
		row.pop(0)
		row.pop()
		col = len(TableCols) - len(row)
		while col > 0:
			row.append("-")
			col -= 1
		Table[row[0][1:]] = row[1:]

	diff = False
	skip = False
	for u in Table.keys():
		api_count += 1
		if (api_count % API_MAX_PER_MINUTE) == 0:
			time.sleep(10)
		try:
			Body = requests.get(Forum + "/search.json?q=My+Story:+@{}+#{}".format(u, Slug), headers=Headers).json()
		except:
			skip = True
			break

		if not Body.get("topics") or len(Body["topics"]) <= 0:
			MyStory = "-"
		else:
			MyStory = "[{}]({}/t/-/{})".format(u, Forum, Body["topics"][0]["id"])

		old = Table[u].pop()
		Table[u].append(MyStory)
		if old != MyStory:
			diff = True

	if skip or not diff:
		continue

	raw = PostBody
	raw += "|" + "|".join(TableCols) + "|\n"
	raw += "|" + "|".join(["---" for n in range(len(TableCols))]) + "|\n"
	for k, v in sorted(Table.items(), key=lambda x: x[0].casefold()):
		raw += "|@" + k + "|" + "|".join(v) + "|\n"

	print(raw)

	update = {}
	update["post"] = {"raw" : raw, "edit_reason" : "Reconcile MyStory links"}

	api_count += 1
	if (api_count % API_MAX_PER_MINUTE) == 0:
		time.sleep(10)
	try:
		Body = requests.put(Forum + "/posts/{}.json".format(Post), headers=Headers, json=update).json()
	except:
		continue
