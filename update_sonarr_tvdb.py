#!/usr/bin/env python
# coding: utf-8
# Calls Sonarr/Nzbdrone's Command/Rescan endpoint for a given TVDB ID

# To debug, uncomment the print statement
def debug_print(msg):
	#print >> sys.stderr, msg
	pass

def error_print(msg):
	print >> sys.stderr, msg

try:
	import urllib2
	import json
	import sys
except ImportError as e:
	error_print("Unable to import dependencies! %r" % e)
	sys.exit(1)
debug_print("Import finished.")

# Variables
try:
	API_ENDPOINT = sys.argv[1]
	API_KEY = sys.argv[2]
	TVDBID = sys.argv[3]
except IndexError as e:
	debug_print("Usage: %s <API endpoint> <API key> <TVDB ID>")
	sys.exit(1)

debug_print("API Endpoint: %s\nAPI Key: %s\nTVDB ID: %s" % (API_ENDPOINT, API_KEY, TVDBID))

# Build the request with all the desired headers
sonarrseriesreq = urllib2.Request(url = "%s/Series" % API_ENDPOINT,
                                  headers = {'User-Agent':"Sonarr Series to ID Python-urllib/%s" % urllib2.__version__,
                                             'X-Api-Key':API_KEY,
                                             'Content-Type':'application/json'},
                                  unverifiable = True)
debug_print("Request built for %s" % sonarrseriesreq.get_full_url())

# Attempt to fetch the series list from the Sonarr API
try:
	seriesjson = urllib2.urlopen(sonarrseriesreq)
	debug_print("Request made.\nFinal URL: %s\nResponse code: %s\nInfo:%s" % (seriesjson.geturl(),
                                                                               seriesjson.getcode(),
                                                                               seriesjson.info()))
	json_string = seriesjson.read()
	debug_print("Series data fetched.")
	seriesjson.close()
except urllib2.URLError as e:
	error_print("urllib2.URLError while contacting Sonarr API. %r" % e)
	sys.exit(1)
except urllib2.HTTPError as e:
	error_print("urllib2.HTTPError while contacting Sonarr API. %r" % e)
	sys.exit(1)

debug_print("Server Response/JSON: %s" % json_string)
try:
	parsed_json = json.loads(json_string)
except ValueError as e:
	error_print("Invalid JSON received from the Sonarr API! %r" % e)
	sys.exit(1)
debug_print("Parsed JSON: %r" % parsed_json)

SHOW_ID = -1
for show in parsed_json:
	debug_print("Title: %s  TVDB: %s" % (show['title'], show["tvdbId"]))
	if str(show["tvdbId"]) == TVDBID:
		SHOW_ID = int(show["id"])
		break

if SHOW_ID >= 0:
  api_data = {'name': 'RescanSeries', 'seriesId': SHOW_ID}
  # Build the request with all the desired headers
  sonarrrescanreq = urllib2.Request(url = "%s/Command" % API_ENDPOINT,
                                    headers = {'User-Agent':"Sonarr Series to ID Python-urllib/%s" % urllib2.__version__,
                                               'X-Api-Key':API_KEY,
                                               'Content-Type':'application/json'},
                                    data = str(api_data),
                                    unverifiable = True)
  debug_print("Request built for %s" % sonarrrescanreq.get_full_url())
  
  # Attempt to fetch the series list from the Sonarr API
  try:
  	sonarrrescan = urllib2.urlopen(sonarrrescanreq)
  	debug_print("Request made.\nFinal URL: %s\nResponse code: %s\nInfo:%s" % (sonarrrescan.geturl(),
                                                                              sonarrrescan.getcode(),
                                                                              sonarrrescan.info()))
  	debug_print("API Response: %s" % sonarrrescan.read())
  	sonarrrescan.close()
  except urllib2.URLError as e:
  	error_print("urllib2.URLError while contacting Sonarr API. %r" % e)
  	sys.exit(1)
  except urllib2.HTTPError as e:
  	error_print("urllib2.HTTPError while contacting Sonarr API. %r" % e)
  	sys.exit(1)
else:
  error_print("Unable to find a Sonarr series ID for TVDB ID %s" % TVDBID)
  sys.exit(1)

# All done!
debug_print("Complete!")
sys.exit(0)



"""
Example JSON for /api/Series
[
  {
    "title": "2 Broke Girls",
    "alternateTitles": [],
    "sortTitle": "2 broke girls",
    "seasonCount": 4,
    "episodeCount": 0,
    "episodeFileCount": 0,
    "sizeOnDisk": 0,
    "status": "continuing",
    "overview": "A lot of girls move to New York City to \"make it\". Max and Caroline are just trying to make their rent. In this fun, outrageous comedy series, two girls from very different backgrounds – Max, poor from birth, and Caroline, born wealthy but down on her luck – wind up as waitresses in the same colorful Brooklyn diner and strike up an unlikely friendship that could lead to a successful business venture. All they need to do is come up with $250,000 in start-up expenses. \"2 Broke Girls\" infuses the classic comedy with something new, current and young, proving life can be fun – even if you’re broke.",
    "nextAiring": "2015-05-05T00:00:00Z",
    "network": "CBS",
    "airTime": "20:00",
    "images": [
      {
        "coverType": "fanart",
        "url": "/MediaCover/1/fanart.jpg?lastWrite=635642964090000000"
      },
      {
        "coverType": "banner",
        "url": "/MediaCover/1/banner.jpg?lastWrite=635642964090000000"
      },
      {
        "coverType": "poster",
        "url": "/MediaCover/1/poster.jpg?lastWrite=635647720380000000"
      }
    ],
    "seasons": [
      {
        "seasonNumber": 0,
        "monitored": false
      },
      {
        "seasonNumber": 1,
        "monitored": false
      },
      {
        "seasonNumber": 2,
        "monitored": false
      },
      {
        "seasonNumber": 3,
        "monitored": false
      },
      {
        "seasonNumber": 4,
        "monitored": true
      }
    ],
    "year": 2011,
    "path": "/path/to/2 Broke Girls",
    "profileId": 1,
    "seasonFolder": true,
    "monitored": true,
    "useSceneNumbering": false,
    "runtime": 30,
    "tvdbId": 248741,
    "tvRageId": 28416,
    "firstAired": "2011-09-19T07:00:00Z",
    "lastInfoSync": "2015-04-29T23:37:20.900855Z",
    "seriesType": "standard",
    "cleanTitle": "2brokegirls",
    "imdbId": "tt1845307",
    "titleSlug": "2-broke-girls",
    "certification": "TV-14",
    "genres": [
      "Comedy"
    ],
    "tags": [],
    "added": "2015-04-10T20:59:43.931289Z",
    "qualityProfileId": 1,
    "id": 1
  },
  {etc}
]
"""
