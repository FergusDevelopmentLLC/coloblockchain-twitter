from twitter import *
import json
import urllib2
from pprint import pprint

import private as private

twitter = Twitter(
    auth=OAuth(
        private.twitterAuth['token'],
        private.twitterAuth['token_secret'],
        private.twitterAuth['consumer_key'],
        private.twitterAuth['consumer_secret']
        )
    )

username = 'coloblockchain'

query = twitter.friends.ids(screen_name = username)

print "found %d friends" % (len(query["ids"]))

for n in range(0, len(query["ids"]), 100):
	ids = query["ids"][n:n+100]

	subquery = twitter.users.lookup(user_id = ids)

	for u in subquery:
		print "%s|%s|%s|%s|%s|%s" % (u["name"],'https://twitter.com/' + u["screen_name"], u["location"], u["followers_count"], u["friends_count"], u["listed_count"])
