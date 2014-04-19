from os import remove, removedirs, rmdir, system, path
from sys import argv
import shutil
import re

#Run new vhost: sudo python new-domain.py new-domain.test
#require test base

HOST_LOCATION = '/etc/hosts'
HOST_LINE = '127.0.0.1\t%s'
PATH_WWW_VHOSTS = '/home/t/www/vhosts'
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
shutil.copytree(path.join(PATH_WWW_VHOSTS, HOST_BASE), path.join(PATH_WWW_VHOSTS, NEW_HOST_NAME))

#task3
#copy apache file test.t.conf to argv[1].conf
#open new file and replace test to argv[1]
apacheSitesDir = path.join(APACHE_LOCATION, APACHE_SITES_AVAILABLE)
newHostLocation = path.join(apacheSitesDir, NEW_HOST_NAME)
newHostLocationConf = newHostLocation + '.conf'
baseHostLocationConf = path.join(apacheSitesDir, HOST_BASE) + '.conf'
shutil.copy2(baseHostLocationConf, newHostLocationConf)

content = None
with open(baseHostLocationConf, 'r') as file: content = file.read()
content = content.replace(HOST_BASE, NEW_HOST_NAME)
print content
with open(newHostLocationConf, 'w') as file: file.write(content)

#task4
system('sudo a2ensite ' + NEW_HOST_NAME)

#task5
system('sudo service apache2 reload')
