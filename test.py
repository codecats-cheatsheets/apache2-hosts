# -*- coding: utf-8 -*-
import re

hostPath = '/etc/hosts'
HOST_LINE = '127.0.0.1\t%s'
DEL_HOST_NAME = 'zadanie'
newHost = HOST_LINE % DEL_HOST_NAME
content = None

with open(hostPath, 'r') as file: content = file.read().split('\n')

pattern = re.compile('127.*')
patternToDelete = re.compile(newHost.strip(), re.IGNORECASE)

for no, line in enumerate(content):
    if patternToDelete.match(line.strip()):
        content.remove(line)

with open(hostPath, 'w') as file: file.write('\n'.join(content))
