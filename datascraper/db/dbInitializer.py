import os
scriptPath = os.path.abspath(os.path.dirname(__file__))

import sqlite3
from contextlib import closing

import requests
from time import sleep

from static.idinfo import venues


class DbInitializer:
    def __init__(self, dbName):
        self.db = os.path.join(scriptPath, dbName)

        self.appToken = 'JW5_w_v4k9FLlPdYEHPEPR78pMoa'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'application/json',
            'Authorization': 'Bearer ' + self.appToken
        }

    def init_table(self, tableName):
        schemaPath = os.path.join(scriptPath, 'schema_%s.sql'%tableName)
        with closing(sqlite3.connect(self.db)) as conn:
            with open(schemaPath, 'r') as f:
                conn.cursor().executescript(f.read())
            conn.commit() 
                     
    def init_alltables(self):
        for tableName in ('events', 'venues', 'stats'):
            self.init_table(tableName)     

    def requestJson(self, url):
        retrydelay = 5
        retrycount = 0
        maxretry = 10
        while True:
            try:
                r = requests.get(url, headers=self.headers)
                rd = r.json()
                break
            except ValueError as e:
                if retrycount > maxretry:
                    raise
                print e
                print "Going to retry in %d seconds..." % retrydelay
                sleep(retrydelay)
                retrydelay += 5
                retrycount += 1
                continue
        return rd


    def write_venue(self, team):

        print "Writing venue data for %s" % team

        venueId = venues[team]['venueId']
        url = 'https://api.stubhub.com/catalog/venues/v2/%s' % venueId

        rd = self.requestJson(url)

        addr = rd['address']

        query = 'INSERT INTO venues VALUES'
        query += '(?,?,?,?,?,?,?,?,?,?,?)'
        values = (venueId, addr['address1'], rd['name'], addr['city'], 
                    addr['state'], addr['zipCode'], addr['country'], 
                    rd['latitude'], rd['longitude'], rd['timezone'], 
                    rd['url']
                )

        with closing(sqlite3.connect(self.db)) as conn:
            try:
                conn.cursor().execute(query, values)
                conn.commit()
            except(sqlite3.IntegrityError):
                pass

    def write_allvenues(self, teamList):
        for team in teamList:
            self.write_venue(team)
            sleep(5)

    def write_events(self, team, dateFrom, dateTo):
        # stubhub str format: '2015-10-05T00:59'
        # there is some wierd behavior that leads to incomplete reuslts
        # leave enough space at the end: use time like 00:59

        print "Writing events data for %s" % team

        teamId = venues[team]['id']
        url = 'https://api.stubhub.com/search/catalog/events/v2'
        url = url + '?performerId=%d' % teamId
        url = url + '&sort=dateLocal asc'
        url = url + '&date=%s TO %s' % (dateFrom, dateTo)
        url = url + '&limit=200' # necessary for complete results

        rd = self.requestJson(url)

        for event in rd['events']:
            # Getting rid of none-game events (like season tickets)
            if event['attributes'][0]['value'] == event['attributes'][1]['value']:
                continue
            if "Season" in event['title']:
                continue

            query = 'INSERT INTO events VALUES'
            query += '(?,?,?,?,?,?,?,?,?)'
            values = (event['id'], event['venue']['id'], 
                event['attributes'][0]['value'], event['attributes'][1]['value'],
                teamId, event['dateLocal'], event['dateUTC'], event['title'],
                event['eventInfoUrl']
                )

            with closing(sqlite3.connect(self.db)) as conn:
                try:
                    conn.cursor().execute(query, values)
                    conn.commit()
                except(sqlite3.IntegrityError):
                    pass


    def write_allevents(self, teamList, dateFrom, dateTo):
        for team in teamList:
            self.write_events(team, dateFrom, dateTo)
            sleep(5)