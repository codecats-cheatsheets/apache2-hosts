# -*- coding: utf-8 -*-
from os import remove, removedirs, rmdir, system, path, getcwd, makedirs, rename, geteuid, execlpe, environ, execlpe, getenv
from sys import argv, stderr, exit, executable
import shutil
import re
from getpass import getuser

system('sudo -k')

USERNAME = getuser()
#check if root
if geteuid() != 0:
    argv.append(USERNAME)
    args = ['sudo', executable] + argv + [environ]
    # the next line replaces the currently-running process with the sudo
    execlpe('sudo', *args)

USERNAME = argv[len(argv) - 1]
if len(argv) <= 2:
    exit('Script need new domain name and no root permissions: example python new-domain.py foo.t')

HOST_LOCATION = '/etc/hosts'
HOST_LINE = '127.0.0.1\t%s'
PATH_WWW_VHOSTS = '/home/{0}/www/vhosts'.format(USERNAME)
PATH_WWW_VHOSTS_PATTERN = path.join(getcwd(), 'pattern')
HOST_BASE = 'test.t'
APACHE_LOCATION = '/etc/apache2'
APACHE_SITES_AVAILABLE = 'sites-available'

NEW_HOST_NAME = argv[1]

#task1
#check if vhost 'conf' is enabled, disable it, and remove
system('sudo a2dissite {0}'.format(NEW_HOST_NAME))

#task2
#remove etc/hosts line argv[1]

#task3
#zip or tar vhosts tree, remove original structure

#task4
#reload apache2 service
