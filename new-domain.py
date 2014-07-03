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

if not path.exists('/home/{0}/www/vhosts'.format(USERNAME)):
    makedirs('/home/{0}/www/vhosts'.format(USERNAME))

#Run new vhost: sudo python new-domain.py new-domain.test
#require test base

HOST_LOCATION = '/etc/hosts'
HOST_LINE = '127.0.0.1\t%s'
PATH_WWW_VHOSTS = '/home/{0}/www/vhosts'.format(USERNAME)
PATH_WWW_VHOSTS_PATTERN = path.join(getcwd(), 'pattern')
HOST_BASE = 'test.t'
APACHE_LOCATION = '/etc/apache2'
APACHE_SITES_AVAILABLE = 'sites-available'

NEW_HOST_NAME = argv[1]
#task1
#create new host
newHost = HOST_LINE % NEW_HOST_NAME
hostPath = HOST_LOCATION
content = None

with open(hostPath, 'r') as file: content = file.read().split('\n')

pattern = re.compile('127.*')
patternErrorCheck = re.compile(newHost.strip(), re.IGNORECASE)
mathFlag = False
lastMath = None
for no, line in enumerate(content):
    if pattern.match(line): lastMath = no
    if patternErrorCheck.match(line.strip()):
        errors = 'The host "%s" already exists.' % line
        print '\033[91m' + errors + '\033[0m'
        raise ValueError(errors)

content.insert(lastMath + 1, newHost)

with open(hostPath, 'w') as file: file.write('\n'.join(content))

#task2
#shutil.copytree(path.join(PATH_WWW_VHOSTS, HOST_BASE), path.join(PATH_WWW_VHOSTS, NEW_HOST_NAME))
newHostDir = path.join(PATH_WWW_VHOSTS, NEW_HOST_NAME)
shutil.copytree(path.join(PATH_WWW_VHOSTS_PATTERN, HOST_BASE), newHostDir)
system('sudo chown -R {0} {1}'.format(USERNAME, newHostDir))
system('sudo chgrp -R {0} {1}'.format(USERNAME, newHostDir))

#task3
#copy apache file test.t.conf to argv[1].conf
#open new file and replace test to argv[1]

apacheSitesDir = path.join(APACHE_LOCATION, APACHE_SITES_AVAILABLE)
newHostLocation = path.join(apacheSitesDir, NEW_HOST_NAME)
newHostLocationConf = newHostLocation + '.conf'
baseHostLocationConf = path.join(PATH_WWW_VHOSTS_PATTERN, APACHE_SITES_AVAILABLE, HOST_BASE) + '.conf'

shutil.copy2(baseHostLocationConf, newHostLocationConf)

content = None
with open(baseHostLocationConf, 'r') as file: content = file.read()
content = content.format(USERNAME)
content = content.replace(HOST_BASE, NEW_HOST_NAME)

with open(newHostLocationConf, 'w') as file: file.write(content)

#task4
system('sudo a2ensite {0}'.format(NEW_HOST_NAME))

#task5
system('sudo service apache2 reload')
system('sudo -k')
