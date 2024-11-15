# GeneRosters
Code to create gene mutation rosters for a Discourse site  

## Architecture
<img width=600 src=https://github.com/glmck13/GeneRosters/blob/main/arch.png>  

The Ubuntu host functions as an application server in the architecture, providing two main functions:
+ servicing web requests from users to update roster entries  
+ polling the main Discourse platform for LIKEs, and updating roster topics/posts in response to LIKEs and user web requests.  All of the interaction with the Discourse server is accomplished using the Discourse API.

## Discourse server config

### Create Category
+ Create a category named "Gene Mutation Rosters" or something similar on the Discourse server to store the rosters. Be sure to check "Allow unlimited owner edits on first post" under Settings so rosters can be updated indefinitely.
+ Next, click on the category name in your browser.  It will be formatted as https://sitename/c/slug/id.  Make a note of the _slug_ and _id_, since you'll need to save these later within the forcenv file on the app server.

## Ubuntu server config

### Install Apache
+ If it's not configured already, install an Apache web server on your Ubuntu host and enable the SSL and CGI modules:
```
apt install apache2
a2enmod ssl cgid
a2dissite 000-default
a2ensite default-ssl
sed -i -e "s/^#\([[:space:]]*AddHandler[[:space:]]*cgi-script[[:space:]]*\.cgi\)$/\1/" /etc/apache2/mods-available/mime.conf
sed -i -e "s/^\([[:space:]]*Options Indexes FollowSymLinks\)$/\1 ExecCGI/" /etc/apache2/apache2.conf
```
+ Install your SSL certificate and private key files under /etc/ssl/certs and /etc/ssl/private respectively, and edit SSLCertificateFile and SSLCertificateKeyFile in /etc/apache2/default-ssl.conf accordingly.  Restart the apache server (systemctl restart apache2) and make sure you can access the site.

### Install application files
+ We’ll be installing application-related files under www-data, so edit /etc/passwd to change the login shell for www-data from /usr/sbin/nologin to /bin/bash.  Become www-data by executing by executing: sudo su – www-data
+ mkdir bin and tmp directories under /var/www, download all the .sh, .py, and .txt files from this repository into /var/www/bin, and make the .sh and .py files executable: chmod +x *.sh *.py
+ Next, create a CGI link under /var/www/html to service user forms:
```
cd /var/www/html; mkdir cgi; cd cgi
ln -s ../../bin/force-roster.sh force-roster.cgi
```

### Generate User API Key to interact with Discourse
+ Choose an account on your Discourse platform to function as a roster custodian.  This can be any account on Discourse, and does not require Discourse administrator or moderator privileges.  Next, run the $HOME/bin/forceapps.sh script, open the link it generates, authorize access for "forceapps" under your Discourse account, then copy the string returned by Discourse and paste it back into the forceapps.sh script.  If all goes well, the script will output a Client_Id and UserApiKey on the next lines.
+ Poplate the Client_id and UserApiKey variables within $HOME/bin/forcenv-roster.sh and $HOME/bin/forcenv_roster.py using the values output by the script.
+ Populate the Slug and Category variables within $HOME/bin/forcenv-roster.sh using the values for _slug_ and _id_ obtained earlier.

### Create rosters
+ Create Discourse topics for all the gene rosters, and afterwards, tweak the topic names in Discourse as desired (e.g. add back the "syndrome" names):
```
cd $HOME/bin; ./force-topics.sh $(cut -f1 -d' ' genes.txt)
```
+ Retrieve Discourse numerical ids for all the topics and posts:
```
cd $HOME/bin; ./force-topics.sh
```
 + Edit $HOME/bin/forcenv_roster.py to fill in values for RosterData[]["Topic"] and RosterData[]["Post"] based on the above.

### Format the initial roster posts and validate user forms
+ The roster posts created above are simply dummy entries; they don't yet contain any user tables.  We'll format the posts by creating an initial entry for the account selected as the roster custodian (replace "custodian" in the following command with the actual account name):
```
cd $HOME/bin; ./force-roster.sh $(cut -f1 -d' ' genes.txt | sed -e "s?\(.*\)?+\L\1/custodian?g")
```
+ When a roster entry gets created, the software sends a Discourse message to the impacted user containing a link to edit/delete their entry.  Access these roster messages and try out the links to verify everything functions properly.  Once finished, go ahead and delete the custodian entries on each roster (again, replace "custodian" in the following command with the actual account name):
```
cd $HOME/bin; ./force-roster.sh $(cut -f1 -d' ' genes.txt | sed -e "s?\(.*\)?-\L\1/custodian?g")
```

### Create a cron entry for www-data to poll for LIKEs every 5 minutes
+ Append the following entry to the crontab for www-data:
```
*/5 * * * * $HOME/bin/force-rosterpoll.sh >>/tmp/force-roster.log 2>&1
```
