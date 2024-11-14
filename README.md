# GeneRosters
Code to create gene mutation rosters for a Discourse site  
## Architecture
<img width=600 src=https://github.com/glmck13/GeneRosters/blob/main/arch.png>  

The Ubuntu server functions as an application server in the architecture, providing two main functions:
+ servicing web requests from users to update roster entries  
+ polling the main Discourse platform for LIKEs, and updating roster topics/posts in response to  LIKEs and user web requests.
All of the interaction with the Discourse server is accomplished using the Discourse API.

## Ubuntu Installation
+ Install the Apache web server with SSL support, and enable CGI processing:
```
apt install apache2
a2enmod ssl cgid
a2dissite 000-default
a2ensite default-ssl
sed -i -e "s/^#\([[:space:]]*AddHandler[[:space:]]*cgi-script[[:space:]]*\.cgi\)$/\1/" /etc/apache2/mods-available/mime.conf
sed -i -e "s/^\([[:space:]]*Options Indexes FollowSymLinks\)$/\1 ExecCGI/" /etc/apache2/apache2.conf
```
* Install your SSL certificate and private key files in an appropriate directory, and edit default-ssl.conf to specify these locations.  Restart the apache server and make sure you can access the site:
```
systemctl restart apache2
```
+ We’ll be installing application-related files under www-data, so edit /etc/passwd to change the login shell for www-data from /usr/sbin/nologin to /bin/bash.  Become www-data by executing:
```
sudo su – www-data
```
+ While running as www-data:
```
cd /var/www
mkdir bin tmp
```
Afterwards, download the .sh and .py files from this repository into /var/www/bin, and make them executable (chmod +x *)
+ Create a CGI link under /var/www/html to process user forms:
```
cd /var/www/html
mkdir cgi
cd cgi
ln -s ../../bin/force-roster.sh force-roster.cgi
```
