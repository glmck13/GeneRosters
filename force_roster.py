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
	TableCols.append("MyStory")

	print("Content-type: text/html\n")
	sys.stdout.flush()

	Validate = hex(abs(hash(UserName + Seed)))[2:].lower()
	#print(UserName, Token, Validate, file=sys.stderr)

	if Token != Validate:
		Body = {}
		Action = ""
	elif not Topic or not Post:
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
			row = line.split('|')
			row.pop(0)
			row.pop()
			col = len(TableCols) - len(row)
			while col > 0:
				row.append("-")
				col -= 1
			Table[row[0][1:]] = row[1:]

		TableRow = [UserName]
		TableRow.extend(Table.get(UserName, ["" for n in range(len(TableCols)-1)]))
		#print(Table, TableCols, TableRow, file=sys.stderr)

		try:
			Body = requests.get(Forum + "/search.json?q=My+Story:+@{}+#{}".format(UserName, Slug), headers=Headers).json()
		except:
			Body = {}

		if not Body.get("topics") or len(Body["topics"]) <= 0:
			Story = -1
			MyStory = "-"
		else:
			Story = Body["topics"][0]["id"]
			MyStory = "[{}]({}/t/-/{})".format(UserName, Forum, Story)

	if Action == "story":
		if Story < 0:
			Question = "Do you want to post your story?"
			Buttons = f'<a class="button" href="{Forum}/new-topic?title=My+Story:+{UserName}&category={Slug}">Yes</a> <a class="button" href="{Forum}/t/{Topic}">Not now</a>'
		else:
			Question = "Looks like you've already posted your story, thanks!  Do you want to make any updates?"
			Buttons = f'<a class="button" href="{Forum}/t/{Story}">Yes</a> <a class="button" href="{Forum}/t/{Topic}">Not now</a>'
		print(eval("f'''{}'''".format(GenericStory)))

	elif Action == "form":
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
			raw += "|@" + k + "|" + "|".join(v) + "|\n"

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

		#print('<head><meta http-equiv="refresh" content="{};URL={}/t/{}"/></head>'.format(delay, Forum, Topic))
		print('<head><meta http-equiv="refresh" content="{};URL={}{}?username={}&token={}&roster={}&action=story"/></head>'.format(delay, Helper, ScriptName, UserName, Token, Roster))
		print("</html>")

	elif Action == "error":
		print("<html><h3>Unable to access {}</h3></html>".format(Forum))

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
			print("Prefix not +/-, ignoring: {}".format(x[0]), file=sys.stderr)
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

		time.sleep(API_DELAY_SECS/4)

def do_like():
	global QueryString, Roster, UserName, Token, Action
	try:
		Body = requests.get(Forum + "/notifications.json?filter=unread", headers=Headers).json()
	except:
		Body = {}
	#print(Body, file=sys.stderr)

	clear = []
	for watch in Body.get("notifications", []):
		if watch["read"]:
			continue
		if watch["notification_type"] != NOTIFICATION_WATCH:
			continue

		print("?{}".format(watch["data"]["original_username"]))
		clear.append(watch["id"])

	for k, r in RosterData.items():
		Roster = k
		Topic = r["Topic"]
		Post = r["Post"]
		for like in Body.get("notifications", []):
			if like["read"]:
				continue
			if like["notification_type"] != NOTIFICATION_LIKE:
				continue
			if like["topic_id"] != Topic or like["data"]["original_post_id"] != Post:
				continue

			print("+{}/{}".format(Roster, like["data"]["original_username"]))
			clear.append(like["id"])

	if Dismiss:
		for id in clear:
			req = {"id": id}
			try:
				Reply = requests.put(Forum + "/notifications/mark-read.json", headers=Headers, json=req).json()
			except:
				Reply = {}
			#print(Reply, file=sys.stderr)

ScriptName = os.getenv("SCRIPT_NAME", "")
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
