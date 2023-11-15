#!/usr/bin/env python3

# Written by Toby Creek, distributed under the MIT License
# Basic operability check of HomeAssistant via the haobserver on port 4357
# This was written to help in monitoring HAOS as basic access to the operating system
# is frought with peril.

from bs4 import BeautifulSoup
import socket
import requests
import sys

if len(sys.argv) == 1:
  print('USAGE: ' + sys.argv[0] + ' hostname [local]',file=sys.stderr)
  exit(1)

# Verify host specification
try:
  socket.getaddrinfo(sys.argv[1],"8123")
except:
  print('Invalid host specification (name or IP)',file=sys.stderr)
  exit(1);

if len(sys.argv) > 2 and sys.argv[2] == 'local':
  print('<<<local>>>')
else:
  print('<<<check_mk>>>')
  print('Version: 1.0')
  print('AgentOS: HomeAssistant')
  print('<<<local>>>')

try:
  response=requests.get('http://' + sys.argv[1] + ':4357/')
  soup=BeautifulSoup(response.text.replace('\r','').replace('\n','').replace('\t',''), "html.parser")
  table = soup.find('table')
  statrows = table.find_all('tr')
except:
  print('Unable to collect data from HAobserver',file=sys.stderr)
  exit(1)

for row in statrows:
  #print(row)
  service=row.find('td', {'class': []}).contents[0].string.strip().replace(':','')
  try:
    status=row.find('td', {'class': ['connected','disconnected']})
    if status.attrs['class'][0] == 'connected':
      # OK
      code='0'
      perf=' connected=1 '
    if status.attrs['class'][0] == 'disconnected':
      # CRIT
      code='2'
      perf=' connected=0 '
    nicestatus=status.contents[0].string.strip()
  except:
    # Unknown
    code='3'
    nicestatus="Unknown"
    perf=' - '
  print(code + ' ' + service + perf + service + ' reports ' + nicestatus)
exit(0)
