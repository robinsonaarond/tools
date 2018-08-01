#! /usr/bin/python
import urllib2, base64
import json
import datetime
import time
from dateutil import tz

#curl -u$API_KEY: https://api.deadmanssnitch.com/v1/snitches

api_key = ""
api_url = "https://api.deadmanssnitch.com"

# Man, curl is simpler ;)
req = urllib2.Request(api_url+'/v1/snitches')
base64string = base64.encodestring('%s:' % api_key).replace('\n', '')
req.add_header("Authorization", "Basic %s" % base64string)
snitches = json.loads(urllib2.urlopen(req).read())

# Get <TAG> snitches
snitch_list = []
for snitch in snitches:
    if all( i in snitch["tags"] for i in [ "<TAG1>", "<TAG2>" ]):
        # Get notes field for each snitch
        r2 = urllib2.Request(api_url+snitch['href'])
        r2.add_header("Authorization", "Basic %s" % base64string)
        snitch_props = json.loads(urllib2.urlopen(r2).read())
        if snitch['checked_in_at']:
            dte = datetime.datetime.strptime(snitch['checked_in_at'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
            hours_ago = float("{0:.2f}".format((time.time() - time.mktime(dte.timetuple())) / 60 / 60))
            snitch_list.append([snitch['name'], snitch['status'], snitch['type']['interval'], "%s (%s hours ago)" % (dte,hours_ago), snitch_props['notes']])
        else:
            snitch_list.append([snitch['name'], snitch['status'], snitch['type']['interval'], "Not checked in. (0 hours ago)", snitch_props['notes']])

# Generate some HTML
html = []

for snitch in snitch_list:
    hours = float(snitch[3].split("(")[1].split(" ")[0])
    snitch_data = (snitch[0],snitch[4],snitch[1],snitch[2],snitch[3])

    if snitch[2] == "weekly":
        max_hours = 168.00
    elif snitch[2] == "hourly":
        max_hours = 1.00
    else:
        max_hours = 24.00

    if snitch[1] == "healthy" and hours < max_hours:
        html.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % snitch_data)
    elif snitch[1] == "healthy" and hours > max_hours:
        html.insert(0,"<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td bgcolor='#DD0000'>%s</td></tr>" % snitch_data)
    elif snitch[1] != "healthy" and hours < max_hours:
        html.insert(0,"<tr><td>%s</td><td>%s</td><td bgcolor='#DD0000'>%s</td><td>%s</td><td>%s</td></tr>" % snitch_data)
    else:
        html.insert(0,"<tr><td>%s</td><td>%s</td><td bgcolor='#DD0000'>%s</td><td>%s</td><td bgcolor='#DD0000'>%s</td></tr>" % snitch_data)

html.insert(0,"""
    <html>
      <head>
        <link rel='stylesheet' type='text/css' href='http://maxcdn.bootstrapcdn.com/bootswatch/3.3.6/cyborg/bootstrap.min.css'>
        <meta http-equiv="refresh" content="60">
      </head>
      <body>
        <h3 align="center"><b>DMS Sitesync Alerts</b></h3>
        <table id='sitesync' class='table table-condensed' width='100%'>
          <tr>
            <th>NAME</th>
            <th>NOTES</th>
            <th>STATUS</th>
            <th>INTERVAL</th>
            <th>CHECKED IN</th>
          </tr>
    """)
html.append("</table>Page last updated: %s" % time.strftime("%x %X"))
# New JS to hide healthy rows.  Makes for a cleaner view on the TV
html.append("""<script>
    url = new URL(window.location.href);

    if (url.searchParams.get('hidehealthy')) {
        var table = document.getElementById("sitesync");
        for (var i = 0, row; row = table.rows[i]; i++) {
            if (row.cells[4].bgColor.indexOf("#DD0000") < 0) {
                if (row.cells[0].innerHTML != "NAME") {
                    table.deleteRow(i);
                    i -= 1;
                }
            }
        }
    }

</script>
""")
html.append("</body></html>")
print '\n'.join(html)
