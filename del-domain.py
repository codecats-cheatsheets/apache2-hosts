# -*- coding: utf-8 -*-
from os import remove, removedirs, rmdir, system, path, getcwd, \
    makedirs, rename, geteuid, execlpe, environ, execlpe, getenv, \
    walk
from sys import argv, stderr, exit, executable
import shutil
import re
from getpass import getuser
import zipfile

def zipdir(dir_path, zip, root_dir):
    for root, dirs, files in walk(dir_path):
        for file in files:
            map_path = path.join(root.replace(root_dir, ''), file)
            zip.write(path.join(root, file), map_path)

if __name__ == '__main__':
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
        exit('Script need domain name and no root permissions: example python del-domain.py foo.t')

    HOST_LOCATION = '/etc/hosts'
    HOST_LINE = '127.0.0.1\t%s'
    PATH_WWW_VHOSTS = '/home/{0}/www/vhosts'.format(USERNAME)
    PATH_WWW_VHOSTS_PATTERN = path.join(getcwd(), 'pattern')
    HOST_BASE = 'test.t'
    APACHE_LOCATION = '/etc/apache2'
    APACHE_SITES_AVAILABLE = 'sites-available'

    DEL_HOST_NAME = argv[1]

    #task1
    #disable 'conf'
    system('sudo a2dissite {0}'.format(DEL_HOST_NAME))
    remove(path.join(APACHE_LOCATION, APACHE_SITES_AVAILABLE, '{0}.conf'.format(DEL_HOST_NAME)))

    #task2
    #remove etc/hosts line argv[1]
    newHost = HOST_LINE % DEL_HOST_NAME
    hostPath = HOST_LOCATION
    content = None
    with open(hostPath, 'r') as file: content = file.read().split('\n')

    patternToDelete = re.compile(newHost.strip(), re.IGNORECASE)

    for no, line in enumerate(content):
        if patternToDelete.match(line.strip()):
            content.remove(line)

    with open(hostPath, 'w') as file: file.write('\n'.join(content))

    #task3
    #zip or tar vhosts tree, remove original structure
    #creat path to place zip and dir in the same root
    to_zip = '{0}/{1}'.format(PATH_WWW_VHOSTS, DEL_HOST_NAME)

    if not path.exists(to_zip):
        raise ValueError('Vhost directory not exists.')

    zipf = zipfile.ZipFile(to_zip + '.zip', 'w')
    zipdir(to_zip, zipf, PATH_WWW_VHOSTS)
    zipf.close()
    shutil.rmtree(to_zip)


    #task4
    #reload apache2 service
    system('sudo service apache2 reload')
    system('sudo -k')