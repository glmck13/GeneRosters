#!/usr/bin/env -S PYTHONHASHSEED=0 python3

import sys, os, json, time
import requests
from forcenv_roster import *
from urllib.parse import parse_qs

def do_edit():
	global QueryString, Roster, UserName, Token, Action, TableRow
	#print(QueryString, file=sys.stderr)

	Fields = parse_qs(QueryString)
	for k, v in RosterVars.items():
		exec('global {}; {} = ",".join(Fields.get("{}", ["{}"]))'.format(k, k, v["name"], v["default"]))
	Action = Action.lower()

	Table = {}
	TableCols = ["UserName"]
	r = RosterData.get(Roster)
	if r:
		Topic = r["Topic"]
		Post = r["Post"]
		PostSubj = r["PostSubj"]
		PostBody = r["PostBody"]
		FormText = r["FormText"]
		for k, v in r["FormVars"].items():
			if v["col"]:
				TableCols.append(k)
			exec('global {}; {} = ",".join(Fields.get("{}", ["{}"]))'.format(k, k, v["name"], v["default"]))
			#print("{} = {}".format(k, eval(k)), file=sys.stderr)
	else:
		Token = ""

	print("Content-type: text/html\n")
	sys.stdout.flush()

	Validate = hex(abs(hash(UserName + Seed)))[2:].lower()
	#print(UserName, Token, Validate, file=sys.stderr)

	if Token != Validate:
		Body = {}
		Action = ""
	else:
		try:
			Body = requests.get(Forum + "/posts/{}.json".format(Post), headers=Headers).json()
		except:
			Body = {}
			Action = "error"
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
		row = []
		for col in line.split('|'):
			row.append(col.strip())
		row.pop(0)
		row.pop()
		Table[row[0]] = row[1:]

	TableRow = [UserName]
	TableRow.extend(Table.get(UserName, ["" for n in range(len(TableCols)-1)]))
	#print(TableCols, TableRow, file=sys.stderr)

	if Action == "form":
		exec('global {}; {} = TableRow[1:]'.format(','.join(TableCols[1:]), ','.join(TableCols[1:])))
		print(eval("f'''{}'''".format(FormText)))

	elif Action == "submit":
		print("<html>")
		exec('global TableRow; TableRow = [{}]'.format(','.join(TableCols)))
		if not Remove:
			Table[UserName] = TableRow[1:]
		elif UserName in Table:
			Table.pop(UserName)

		delay = 0

		raw = PostBody
		raw += "|" + "|".join(TableCols) + "|\n"
		raw += "|" + "|".join(["---" for n in range(len(TableCols))]) + "|\n"
		for k, v in sorted(Table.items(), key=lambda x: x[0].casefold()):
			raw += "|" + k + "|" + "|".join(v) + "|\n"

		update = {}
		update["post"] = {"raw" : raw, "edit_reason" : "Updated by {}".format(UserName)}
		try:
			Body = requests.put(Forum + "/posts/{}.json".format(Post), headers=Headers, json=update).json()
			#print(Body, file=sys.stderr)
			if "errors" in Body:
				print("<h3>Failed to update post #{}: {}</h3>".format(Post, Body["errors"][0]))
				delay = 5
		except:
			print("<h3>Failed to update post #{}</h3>".format(Post))
			delay = 5

		print('<head><meta http-equiv="refresh" content="{};URL={}/t/{}"/></head>'.format(delay, Forum, Topic))
		print("</html>")

	elif Action == "error":
		print("<html>")
		print("<h3>Unable to access {}</h3>".format(Forum))
		print("</html>")

def do_addrmv():
	global QueryString, Roster, UserName, Token, Action
	for x in sys.argv[1:]:

		x = x.split("/")
		x.append("")
		u = x[1]
		if len(x[0]) > 0:
			c = x[0][0]
			r = x[0][1:]
		else:
			c = "?"
			r = "?"

		if c not in ("+", "-"):
			print("Need to specify +/-: {}".format(x[0]), file=sys.stderr)
			continue

		if not RosterData.get(r):
			print("Roster '{}' not found!".format(r), file=sys.stderr)
			continue

		if not u:
			print("No user!", file=sys.stderr)
			continue

		try:
			Reply = requests.get(Forum + "/u/{}.json".format(u), headers=Headers).json()
		except:
			Reply = {}
		#print(Reply, file=sys.stderr)

		if Reply.get("user", {}).get("username", "") != u:
			print("User '{}' not found!".format(u), file=sys.stderr)
			continue

		Roster = r
		UserName = u
		Token = hex(abs(hash(UserName + Seed)))[2:].lower()
		q = "username={}&token={}&roster={}".format(UserName, Token, Roster)

		QueryString = q + "&action=submit"
		if c == "-":
			QueryString += "&remove=on"

		do_edit()

		if c == "+":
			r = RosterData[r]
			MsgSubj = r["MsgSubj"]
			MsgBody = r["MsgBody"]

			url = "{}/cgi/force-roster.cgi?".format(Helper) + q + "&action=form"
			message = {}
			message["title"] = MsgSubj
			message["raw"] = MsgBody.format(url)
			message["target_recipients"] = UserName
			message["archetype"] = "private_message"
			print(message["raw"], file=sys.stderr)
			try:
				Reply = requests.post(Forum + "/posts.json", headers=Headers, json=message).json()
			except:
				Reply = {}
			#print(Reply, file=sys.stderr)

		time.sleep(15)

def do_like():
	global QueryString, Roster, UserName, Token, Action
	try:
		Body = requests.get(Forum + "/notifications.json?filter=unread", headers=Headers).json()
	except:
		Body = {}
	#print(Body, file=sys.stderr)

	for k, r in RosterData.items():
		Roster = k
		Topic = r["Topic"]
		Post = r["Post"]
		for like in Body.get("notifications", []):

			if like["topic_id"] != Topic:
				continue

			if like["data"]["original_post_id"] != Post:
				continue

			if like["read"]:
				continue

			print("+{}/{}".format(Roster, like["data"]["original_username"]))

			if not Dismiss:
				continue

			clear = {}
			clear["id"] = like["id"]
			try:
				Reply = requests.put(Forum + "/notifications/mark-read.json", headers=Headers, json=clear).json()
			except:
				Reply = {}
			#print(Reply, file=sys.stderr)

Method = os.getenv("REQUEST_METHOD", "")
if Method == "GET":
	QueryString = os.getenv("QUERY_STRING", "")
elif Method == "POST":
	QueryString = sys.stdin.read()
else:
	QueryString = ""

Headers = {"User-Api-Key" : UserApiKey, "Content-Type": "application/json", "Accept" : "application/json" }

Roster = ""
UserName = ""
Token = ""
Action = ""
TableRow = []

if len(sys.argv) > 1:
	do_addrmv()
elif Method:
	do_edit()
else:
	do_like()
