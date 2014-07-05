#!/bin/bash
if [ -d "/home/$USER/www/vhosts/$1.t/htdocs/Symfony" ]; then
	cd /home/$USER/www/vhosts/$1.t/htdocs/Symfony
else 
	cd /home/$USER/www/vhosts/$1.t/htdocs
fi
