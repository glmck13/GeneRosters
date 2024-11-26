#!/usr/bin/env python3

import sys, os, json, time
import requests
from forcenv import *
from urllib.parse import parse_qs, quote

Method = os.getenv("REQUEST_METHOD", "")
if Method == "GET":
	QueryString = os.getenv("QUERY_STRING", "")
elif Method == "POST":
	QueryString = sys.stdin.read()
else:
	QueryString = ""

Fields = parse_qs(QueryString)
Keywords = Fields.get("keywords", [""])[0]
Username = Fields.get("username", [""])[0]
ApiKey = Fields.get("apikey", [""])[0]
Action = Fields.get("action", [""])[0]
Headers = {"User-Api-Key" : ApiKey, "Accept" : "application/json" }

print("Content-Type: text/html\n")

print('''<html>

	<head>
	<link rel="stylesheet" href="/style.min.css">
	</head>

	<body>
''', end='')

print('''
	<h1>Search FORCE Message Board</h1>
	<div class="half">
	<form method=POST>
	<input type=text name=keywords placeholder="Look for keywords..." value="{Keywords}">
	<input type=text name=username placeholder="Filter by user..." value="{Username}">
	<input type=text name=apikey placeholder="API key" value="{ApiKey}">
	<br>(<i>If you don't have an API key, click <a href={Helper}/force-apikey.cgi>here</a> to get one</i>)<br>
	<input type=submit name=action value="Submit">
	</form>
	</div>
	<hr>
'''.format(Keywords=Keywords, Username=Username, ApiKey=ApiKey, Helper=Helper), end='')

Search = ""
if Keywords:
	Search += Keywords.strip()
if Username:
	Search += " @" + Username.strip()
if Search:
	Search = quote(Search)

if Action == "Submit" and Search and ApiKey:

	post_hits = {}
	topic_hits = {}
	topic_ids = {}
	topics = {}

	#print("<pre>")

	page = 1
	while True:
		q = Search
		if page > 1:
			q += '&page={}'.format(page)
		page += 1

		#print(Forum + "/search.json?q=" + q)
		try:
			Body = requests.get(Forum + "/search.json?q=" + q, headers=Headers).json()
		except:
			Body = {}

		if not Body or not Body.get("topics"):
			break

		for t in Body["topics"]:
			t["username"] = ""
			t["blurb"] = ""
			topics[t["id"]] = t

		for p in Body["posts"]:
			y, m, d = [int(k) for k in p["created_at"].split("T")[0].split("-")]
			m -= 1
			u = p["username"]
			b = p["blurb"].encode('ascii', 'ignore').decode().replace('"', '')
			t = p["topic_id"]
			topics[t]["username"] = u
			topics[t]["blurb"] = b
			x = topics[t]["title"].encode('ascii', 'ignore').decode().replace('"', '')
			topics[t]["title"] = x

			if y not in post_hits:
				post_hits[y] = [0 for k in range(0,12)]
			post_hits[y][m] += topics[t]["posts_count"]

			if y not in topic_hits:
				topic_hits[y] = [0 for k in range(0,12)]
			topic_hits[y][m] += 1

			if y not in topic_ids:
				topic_ids[y] = [[] for k in range(0,12)]
			topic_ids[y][m].append(t)

		if not Body.get("grouped_search_result", {}).get("more_full_page_results"):
			break

	#print("</pre>")

	print('<div class="flex two"><div style="overflow:auto; height:500px;">', end='')

	for y in sorted(topic_hits.keys(), reverse=True):
		print('<canvas id="hits{}"></canvas>'.format(y), end='')

	print('</div><div id="preview"><h3>Topics:</h3></div></div>')

	print('''
		<script>
		var preview = document.getElementById("preview");
		</script>
	''', end='')

	print('''
		<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	''', end='')

	for y in sorted(topic_hits.keys(), reverse=True):
		print('''
		<script>
		const ctx_hits{Year} = document.getElementById('hits{Year}');
		var hits{Year} = new Chart(ctx_hits{Year}, {{
			data: {{
	      			labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				datasets: [
				{{
					type: 'bar',
					label: '# of Posts',
					data: [{Posts}]
				}},
				{{
					type: 'line',
					label: '# of Topics',
					data: [{Topics}]
				}}
				]
			}},
			options: {{
				scales: {{ y: {{ beginAtZero: true }} }},
				plugins: {{ title: {{ display: true, text: 'Matches in {Year}', font: {{ size: 18 }} }} }}
			}}
		}});
		ctx_hits{Year}.onclick = function(e) {{
			var bar = hits{Year}.getElementsAtEventForMode(e, "nearest", {{ intersect: true }}, true);
			if (!bar.length) return;
			var m = bar[0].index;
			var label = hits{Year}.data.labels[m];
			switch (m) {{'''.format(Year=y, Posts=','.join([str(x) for x in post_hits[y]]), Topics=','.join([str(x) for x in topic_hits[y]]), end=''))

		for m in range(0,12):
			if not topic_hits[y][m]:
				continue
			print('''
			case {Month}:
				preview.innerHTML = "<h3>Topics "+label+"-{Year}:</h3>'''.format(Year=y, Month=m), end='')

			for k in topic_ids[y][m]:
				t = topics[k]
				link = Forum + "/t/-/{}".format(k)
				link = "<a href={} target=_blank>{}</a>".format(link, link)
				print('<b>Topic</b>: {Topic}<br><b>Posts</b>: {Count}<br><b>Contributor</b>: {User}<br><b>Blurb</b>: {Blurb}<br><b>Link</b>: {Link}<br><br>'.format(
					Topic=t["title"], Count=t["posts_count"], User=t["username"], Blurb=t["blurb"], Link=link), end='')

			print('''";
			break;
			''')

		print('''
			}
		}
		</script>
		''', end='')

print('''
	</body>
</html>''')
