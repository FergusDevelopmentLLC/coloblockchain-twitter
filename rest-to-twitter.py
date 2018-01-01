from twitter import *
import json
import urllib2
from datetime import datetime, timedelta
import csv
import socket
import random
import logging

import private as private
import meetup_properties as meetup_properties

logging.basicConfig(filename='log/tweets.log',level=logging.DEBUG,format='%(asctime)s|%(message)s')

t = Twitter(
    auth=OAuth(
        private.twitterAuth['token'],
        private.twitterAuth['token_secret'],
        private.twitterAuth['consumer_key'],
        private.twitterAuth['consumer_secret']
        )
    )

isProduction = False
if(socket.gethostname() == private.prod_server_name):
    isProduction = True

today = datetime.today()
if(isProduction):#adjust for mountain time in production
    today = datetime.today() - timedelta(hours=7)

schedule_config = 'schedule.csv'

configs_to_execute = [] #will be populated with the rows from group-config.csv that apply to the current datetime

upcoming_meetups_url = 'http://104.236.16.91:8680/coloblockchain-meetups';
upcomingMeetups = json.load(urllib2.urlopen(upcoming_meetups_url))

def popConfigsToExecute(): #populates configs_to_execute with those that are in play

    with open(schedule_config) as csvDataFile:

        csvReader = csv.reader(csvDataFile)
        group_unique_ids = [] # ['Boulder-Blockchain','Ethereum-Denver',...]
        possible_configs_to_execute = [] # the lines from the config that are in play based on today

        next(csvReader, None)  # skip the header row in the csv

        for row in csvReader:
            if row[0] not in group_unique_ids:
                group_unique_ids.append(row[0])

            for group_id in group_unique_ids:
                for key, value in upcomingMeetups.items():
                    if value != 'No upcoming meetups scheduled.' and key == group_id and key == row[0]:
                        upcomingEventDateStart = datetime.strptime(upcomingMeetups[key]['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        days_until = upcomingEventDateStart - today
                        tweetHours = row[2].split('|');
                        isTweetHour = False

                        for tweetHour in tweetHours:
                            if(int(today.hour) == int(tweetHour)):
                                isTweetHour = True
                                break

                        if days_until.days == int(row[1]) and isTweetHour:
                            possible_configs_to_execute.append(row)

        for group_id in group_unique_ids:
            target_config = ''

            for config in possible_configs_to_execute:
                if(config[0] == group_id):
                    target_config = config
                    if(int(config[1]) < int(target_config[1])):
                        target_config = config

            if(target_config != ''):
                configs_to_execute.append(target_config)

def hashtagify(term):
    output = ''.join(x for x in term.title() if x.isalpha())
    return '#' + output[0].upper() + output[1:]

def tweetNextEventFor(group_config):
    for key, value in upcomingMeetups.items():
        if (value != 'No upcoming meetups scheduled.' and key == group_config[0]):
            upcomingEventDateStart = datetime.strptime(upcomingMeetups[key]['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
            tweetHours = group_config[2].split('|');
            for tweetHour in tweetHours:
		        #print('today.hour: ' + str(today.hour) + ' ' + 'tweetHour:' + str(tweetHour))
                if(int(today.hour) == int(tweetHour)):

                    groupname = key
                    summary = upcomingMeetups[key]['summary']

                    event_date = upcomingEventDateStart.strftime("%m/%d/%Y")
                    start_time = upcomingEventDateStart.strftime("%-I:%M")
                    upcomingEventDateStartEnd = datetime.strptime(upcomingMeetups[key]['end'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    end_time = upcomingEventDateStartEnd.strftime("%-I:%M")
                    event_datetime = event_date + ', ' + start_time + '-' + end_time + str(upcomingEventDateStartEnd.strftime("%p")).lower()

                    location = upcomingMeetups[key]['location'].split('(')[0].strip()

                    randomTerms = random.sample(set(upcomingMeetups[key]['categories']), 3)

                    if(len(randomTerms) > 0):
                        tags = hashtagify(randomTerms[0])

                    if(len(randomTerms) > 1):
                        tags = hashtagify(randomTerms[0]) + ' ' + hashtagify(randomTerms[1])

                    if(len(randomTerms) > 2):
                        tags = hashtagify(randomTerms[0]) + ' ' + hashtagify(randomTerms[1]) + ' ' + hashtagify(randomTerms[2])

                    url = upcomingMeetups[key]['url']

                    image_url = ''
                    for meetup in meetup_properties.meetups:
                        if(meetup['key'] == key):
                            image_url = meetup['image_url']

                    tweet_text = 'Next {0} #meetup. {1}. {2}. {3}. {4} {5} {6}'.format(groupname, summary, event_datetime, location, tags, url, image_url)

                    logging.debug(tweet_text)

                    print
                    print(tweet_text)

                    if (isProduction):
                        t.statuses.update(status=tweet_text)

#----------------------------------------------------------#

popConfigsToExecute()

#print(configs_to_execute)
if(len(configs_to_execute) > 0):
    for config in configs_to_execute:
        tweetNextEventFor(config)
else:
    logging.debug('no tweet')
    print('no tweet')

print("done")
