#!/usr/bin/env -S PYTHONHASHSEED=0 python3

import sys, os, json, time
import requests
from forcenv_roster import *

Headers = {"User-Api-Key" : UserApiKey, "Content-Type": "application/json", "Accept" : "application/json" }

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

	try:
		Body = requests.get(Forum + "/posts/{}.json".format(Post), headers=Headers).json()
	except:
		Body = {}
	#print(Body, file=sys.stderr)

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
	for u in Table.keys():
		try:
			Body = requests.get(Forum + "/search.json?q=@{}+#{}".format(u, Slug), headers=Headers).json()
		except:
			Body = {}

		if not Body.get("topics") or len(Body["topics"]) <= 0:
			MyStory = "-"
		else:
			MyStory = "[{}]({}/t/-/{})".format(u, Forum, Body["topics"][0]["id"])

		old = Table[u].pop()
		Table[u].append(MyStory)
		if old != MyStory:
			diff = True

	if not diff:
		continue

	raw = PostBody
	raw += "|" + "|".join(TableCols) + "|\n"
	raw += "|" + "|".join(["---" for n in range(len(TableCols))]) + "|\n"
	for k, v in sorted(Table.items(), key=lambda x: x[0].casefold()):
		raw += "|@" + k + "|" + "|".join(v) + "|\n"

	print(q, raw)

	update = {}
	update["post"] = {"raw" : raw, "edit_reason" : "Reconcile MyStory links"}
	try:
		Body = requests.put(Forum + "/posts/{}.json".format(Post), headers=Headers, json=update).json()
		if "errors" in Body:
			print("Failed to update post #{}: {}".format(Post, Body["errors"][0]))
	except:
		print("Failed to update post #{}".format(Post))
