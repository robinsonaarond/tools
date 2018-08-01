#! /usr/bin/python
import urllib2, base64
import json
import datetime
import time
from dateutil import tz
from socket import socket

#curl -u$API_KEY: https://api.deadmanssnitch.com/v1/snitches

api_key = ""
api_url = "https://api.deadmanssnitch.com"

# Globals
CARBON_SERVER = ''
CARBON_PORT = 2003

# Open socket at the first, so we can reuse it
sock = socket()
sock.connect((CARBON_SERVER, CARBON_PORT))
stats = []

# Man, curl is simpler ;)
req = urllib2.Request(api_url+'/v1/snitches')
base64string = base64.encodestring('%s:' % api_key).replace('\n', '')
req.add_header("Authorization", "Basic %s" % base64string)
snitches = json.loads(urllib2.urlopen(req).read())

# Get SSv2 snitches
snitch_list = []
for snitch in snitches:
    if all( i in snitch["tags"] for i in [ "prod", "SSv2" ]):
        # Get notes field for each snitch
        if snitch['checked_in_at']:
            dte = datetime.datetime.strptime(snitch['checked_in_at'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
            interval = snitch['interval']
            stats.append("central.prod.dms.ssv2.%s.checked_in_at 1 %d" % (snitch['name'], time.mktime(dte.timetuple())))

sock.sendall('\n'.join(stats))
