#!/bin/bash
if [ -d "/home/s/www/vhosts/$1.t/htdocs/Symfony" ]; then
	cd /home/s/www/vhosts/$1.t/htdocs/Symfony
else 
	cd /home/s/www/vhosts/$1.t/htdocs
fi
