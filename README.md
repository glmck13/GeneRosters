# GeneRosters
Code to create gene mutation rosters for a Discourse site  

## Architecture
<img width=600 src=https://github.com/glmck13/GeneRosters/blob/main/arch.png>  

The Ubuntu server functions as an application server in the architecture, providing two main functions:
+ servicing web requests from users to update roster entries  
+ polling the main Discourse platform for LIKEs, and updating roster topics/posts in response to  LIKEs and user web requests.
All of the interaction with the Discourse server is accomplished using the Discourse API.

## Discourse server config
### Create Category
+ All of the rosters will be stored under their own category, so create a category named "Gene Mutation Rosters" or something similar on the Discourse server. Be sure to check "Allow unlimited owner edits on first post" under "Settings" so rosters can be updated indefinitely.
+ Next, click on the category name in your browser.  It will be formatted as https://sitename/c/slug/id.  Make a note of the _slug_ and _id_, since you'll need these later to enter into the Python setup file on the app server.

## Ubuntu server config
### Install Apache
+ If it's not there already, install an Apache web server on your Ubuntu host.  Turn on SSL support and enable CGI processing:
```
apt install apache2
a2enmod ssl cgid
a2dissite 000-default
a2ensite default-ssl
sed -i -e "s/^#\([[:space:]]*AddHandler[[:space:]]*cgi-script[[:space:]]*\.cgi\)$/\1/" /etc/apache2/mods-available/mime.conf
sed -i -e "s/^\([[:space:]]*Options Indexes FollowSymLinks\)$/\1 ExecCGI/" /etc/apache2/apache2.conf
```
+ Install your SSL certificate and private key files in appropriate directories (e.g. /etc/ssl/certs and /etc/ssl/private), and edit /etc/apache2/default-ssl.conf to specify these locations.  Restart the apache server and make sure you can access the site:
```
systemctl restart apache2
```
### Install application files
+ We’ll be installing application-related files under www-data, so edit /etc/passwd to change the login shell for www-data from /usr/sbin/nologin to /bin/bash.  Become www-data by executing:
```
sudo su – www-data
```
+ While running as www-data mkdir bin and tmp directories under /var/www, then download all the .sh and .py files from this repository into /var/www/bin, and make them executable, i.e. chmod +x *
+ Next, create a CGI link under /var/www/html to process user forms:
```
cd /var/www/html
mkdir cgi; cd cgi
ln -s ../../bin/force-roster.sh force-roster.cgi
```
### Generate User API Key
+ Pick a Discourse account to administer the rosters.  This can be any account on Discourse, and does not require administrator or moderator privileges.  Next, run the /var/www/bin/forceapps.sh script, open the link it generates, authorize access for "forceapps" under your Discourse account, then copy the string returned by Discourse and paste it back into the forceapps.sh script.  If all goes well, the script will output your API key on the next line.
