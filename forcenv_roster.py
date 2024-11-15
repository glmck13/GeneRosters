Seed = ""
Dismiss = True
Forum = "https://discourse.mckblog.net"
Helper = "https://forceapps.mckblog.net"
AppName = "forceapps"
Client_Id=""
UserApiKey = ""

RosterVars = {
	"Roster": {"name": "roster", "default": ""},
	"UserName": {"name": "username", "default": ""},
	"Token": {"name": "token", "default": ""},
	"Action": {"name": "action", "default": ""},
}

GenericVars = {
	"BirthYear": {"name": "birthyear", "default": "-", "col": True},
	"Gender": {"name": "gender", "default": "-", "col": True},
	"Trans": {"name": "trans", "default": "-", "col": True},
	"Race": {"name": "race", "default": "-", "col": True},
	"Cancers": {"name": "cancers", "default": "", "col": True},
	"Remove": {"name": "remove", "default": "", "col": False},
}

GenericForm = '''
	<b>In what year were you born?</b>
		<select id="birthyear" name="birthyear">
		<option value="-">Prefer not to enter</option>
		</select>
	<br><br><b>What is your gender?</b>
		<select id="gender" name="gender">
		<option value="-">Prefer not to enter</option>
		<option value="Female">Female</option>
		<option value="Male">Male</option>
		<option value="Non-binary">Non-binary</option>
		</select>
	<br><br><b>Are you transgender?</b>
		<select id="trans" name="trans">
		<option value="-">Prefer not to enter</option>
		<option value="No">No</option>
		<option value="Yes">Yes</option>
		</select>
	<br><br><b>Which of these best describes your race/ethnicity? (select as many that apply)</b>
		<select id="race" name="race" multiple>
		<option value="-">Prefer not to enter</option>
		<option value="AI/AN">American Indian, Alaska native or First Nations</option>
		<option value="Ashkenazi">Ashkenazi</option>
		<option value="Asian">Asian or Asian American</option>
		<option value="Black">Black or African-American</option>
		<option value="Hispanic">Hispanic or Latino</option>
		<option value="NHPI">Native Hawaiian or Pacific Islander</option>
		<option value="White">White</option>
		<option value="Other">Other</option>
		</select>
	<br><br><b>If you would like to share your cancer history, enter your cancer type(s) and your age at diagnosis:</b>
		<input type="text" id="cancers" name="cancers" value="{Cancers}">
	<br><br><label>
		<input type="checkbox" id="remove" name="remove">
		<span class="checkable">Please remove me from the list, thanks</span>
	</label>
	<br><br><input type="submit" name="action" value="Submit">
	<input type="hidden" name="username" value="{UserName}">
	<input type="hidden" name="token" value="{Token}">
	<input type="hidden" name="roster" value="{Roster}">
'''

GenericScript = '''
	function createYearPicker(id, startYear, endYear) {{
		const select = document.getElementById(id);
		for (let year = startYear; year <= endYear; year++) {{
			const option = document.createElement("option");
			option.value = year;
			option.text = year;
			select.appendChild(option);
		}}
	}}
	createYearPicker("birthyear", 1940, 2010);
	var x = document.getElementById("birthyear");
	for (i = 0; i < x.options.length; i++) {{
		if ("{BirthYear}" == x.options[i].value) {{
			x.options[i].selected = true;
		}}
	}}
	var x = document.getElementById("gender");
	for (i = 0; i < x.options.length; i++) {{
		if ("{Gender}" == x.options[i].value) {{
			x.options[i].selected = true;
		}}
	}}
	var x = document.getElementById("trans");
	for (i = 0; i < x.options.length; i++) {{
		if ("{Trans}" == x.options[i].value) {{
			x.options[i].selected = true;
		}}
	}}
	var x = document.getElementById("race");
	for (i = 0; i < x.options.length; i++) {{
		if ("{Race}".split(',').includes(x.options[i].value)) {{
			x.options[i].selected = true;
		}}
	}}
'''

RosterData = {
	"lynch": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"Lynch syndrome roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your Lynch info",
		"MsgBody": 	"Use [this link]({}) to update or delete your Lynch entry. Thanks again for sharing your info with the group.",
		"FormVars": {
			"Mutation": {"name": "mutation", "default": "-", "col": True},
			"BirthYear": {"name": "birthyear", "default": "-", "col": True},
			"Gender": {"name": "gender", "default": "-", "col": True},
			"Trans": {"name": "trans", "default": "-", "col": True},
			"Race": {"name": "race", "default": "-", "col": True},
			"Cancers": {"name": "cancers", "default": "", "col": True},
			"Remove": {"name": "remove", "default": "", "col": False},
		},
		"FormText": 	'<html><head><title>Lynch Syndrome Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update Lynch entry for: {UserName}</h1><form method="post">' + '''
		<b>Which specific gene mutation do you have?</b>
			<select id="mutation" name="mutation">
			<option value="-">Select one</option>
			<option value="MLH1">MLH1</option>
			<option value="MSH2">MSH2</option>
			<option value="MSH6">MSH6</option>
			<option value="PMS2">PMS2</option>
			<option value="EPCAM">EPCAM</option>
			</select>
		<br><br>
		''' + GenericForm + '</form></div><script>' + GenericScript + '''
			var x = document.getElementById("mutation");
			for (i = 0; i < x.options.length; i++) {{
				//if ("{Mutation}".split(',').includes(x.options[i].value)) {{
				if ("{Mutation}" == x.options[i].value) {{
					x.options[i].selected = true;
				}}
			}}
		''' + '</script></body></html>'
	},

	"brca1": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"BRCA1 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your BRCA1 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your BRCA1 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>BRCA1 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update BRCA1 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"brca2": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"BRCA2 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your BRCA2 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your BRCA2 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>BRCA2 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update BRCA2 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"bard1": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"BARD1 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your BARD1 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your BARD1 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>BARD1 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update BARD1 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"brip1": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"BRIP1 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your BRIP1 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your BRIP1 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>BRIP1 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update BRIP1 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"apc": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"APC mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your APC info",
		"MsgBody": 	"Use [this link]({}) to update or delete your APC entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>APC Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update APC entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"atm": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"ATM mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your ATM info",
		"MsgBody": 	"Use [this link]({}) to update or delete your ATM entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>ATM Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update ATM entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"tp53": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"TP53 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your TP53 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your TP53 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>TP53 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update TP53 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"rad51c": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"RAD51C mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your RAD51C info",
		"MsgBody": 	"Use [this link]({}) to update or delete your RAD51C entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>RAD51C Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update RAD51C entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"rad51d": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"RAD51D mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your RAD51D info",
		"MsgBody": 	"Use [this link]({}) to update or delete your RAD51D entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>RAD51D Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update RAD51D entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"mutyh": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"MUTYH mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your MUTYH info",
		"MsgBody": 	"Use [this link]({}) to update or delete your MUTYH entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>MUTYH Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update MUTYH entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"hoxb13": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"HOXB13 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your HOXB13 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your HOXB13 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>HOXB13 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update HOXB13 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"pten": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"PTEN mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your PTEN info",
		"MsgBody": 	"Use [this link]({}) to update or delete your PTEN entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>PTEN Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update PTEN entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"palb2": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"PALB2 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your PALB2 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your PALB2 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>PALB2 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update PALB2 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"stk11": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"STK11 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your STK11 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your STK11 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>STK11 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update STK11 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"nbn": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"NBN mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your NBN info",
		"MsgBody": 	"Use [this link]({}) to update or delete your NBN entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>NBN Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update NBN entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"cdk4": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"CDK4 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your CDK4 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your CDK4 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>CDK4 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update CDK4 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"cdkn2a": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"CDKN2A mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your CDKN2A info",
		"MsgBody": 	"Use [this link]({}) to update or delete your CDKN2A entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>CDKN2A Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update CDKN2A entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"cdh1": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"CDH1 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your CDH1 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your CDH1 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>CDH1 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update CDH1 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},

	"chek2": {
		"Topic":	0,
		"Post": 	0,
		"PostSubj": 	"CHEK2 mutation roster",
		"PostBody": 	"To be included in this roster, simply click the 'Like' :heart: button on this post. Later you'll be sent a link to populate the other fields in the table if you want.  You can update or delete your info at any time. Feel free to message @moderators if you have any questions or concerns. Thanks for participating!\n",
		"MsgSubj": 	"Link to edit your CHEK2 info",
		"MsgBody": 	"Use [this link]({}) to update or delete your CHEK2 entry. Thanks again for sharing your info with the group.",
		"FormVars":	GenericVars,
		"FormText": 	'<html><head><title>CHEK2 Mutation Roster</title><link rel="stylesheet" href="/style.min.css"></head><body style="background-color: whitesmoke;"><div class="two-third"><h1>Update CHEK2 entry for: {UserName}</h1><form method="post">' + GenericForm + '</form></div><script>' + GenericScript + '</script></body></html>'
	},
}
