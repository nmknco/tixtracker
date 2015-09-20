import requests
from datetime import datetime
from time import sleep
import json
import sqlite3
from contextlib import closing

import os
scriptPath = os.path.abspath(os.path.dirname(__file__))

import logging
logPath = os.path.join(scriptPath, 'logs/scraper.log')
logging.basicConfig(filename=logPath, level=logging.DEBUG, 
                    format='%(asctime)s %(message)s')

from db.static.idinfo import venues




class Datascraper:
# Getting listings for HOME game only
    def __init__(self, teamname, dateTo):
        logging.info("Creating scraper for %s" % teamname)
        print "Creating scraper for %s" % teamname 

        self.team = teamname
        self.id = venues[teamname]['id']
        self.venueId = venues[teamname]['venueId']

        self.appToken = 'JW5_w_v4k9FLlPdYEHPEPR78pMoa'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'application/json',
            'Authorization': 'Bearer ' + self.appToken
        }
        self.dateTo = dateTo
        # stubhub str format: '2015-10-05T00:59'

        self.events = self.getEvents()

    def requestJson(self, url):
        print "Requesting " + url
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
                    logging.exception(str(e))
                    raise
                logging.exception(str(e))
                loggin.info("Going to retry in %d seconds..." % retrydelay)
                print "Going to retry in %d seconds..." % retrydelay
                sleep(retrydelay)
                retrydelay += 5
                retrycount += 1
                continue
        return rd


    def getEvents(self):
    # Search and return a list of Event objects
        logging.info("Getting events list for %s" % self.team)
        print "Getting events list for %s" % self.team
        
        time = datetime.now()
        dateFrom = time.strftime('%Y-%m-%dT%H:%M')
        dateTo = self.dateTo
        url = 'https://api.stubhub.com/search/catalog/events/v2'
        url = url + '?performerId=%d' % self.id
        url = url + '&sort=dateLocal asc'
        url = url + '&date=%s TO %s' % (dateFrom, dateTo)
        url = url + '&limit=200'

        response_dict = self.requestJson(url)
        events = []
        if response_dict['numFound']:
            for d in response_dict['events']:
                e = Event(d)
                if e.isGame():
                    events.append(e)
        return events

    def getEventIds(self):
    # return a list of ids
        eventIds = []
        for e in self.events:
            eventIds.append(e.getId())
        return eventIds

    # def writeEventsAll(self):
    # # write events info into database
    # # In principle this should only be called once 
    # # to write all events in a season
    #     for e in self.events:
    #         e.writeDb()

    def getListings(self, eventId):
    # return data form a single event as a Listings object 
        logging.info("Getting listings for event %s" % eventId)
        time = datetime.now()
        rows = 2500

        url0 = 'https://api.stubhub.com/search/inventory/v1'
        url0 = url0 + '?eventId=%d&rows=' % eventId
        url = url0 + str(rows)
        response_dict = self.requestJson(url)
        numOfLis = response_dict['totalListings']

        if numOfLis > rows:
            time = datetime.now()
            url = url0 + str(numOfLis)
            response_dict = self.requestJson(url)
        return Listings(eventId, time, response_dict)

    def writeListingsAll(self, mode='both', dbName=''):
    # mode = file | db | both
        eventIds = self.getEventIds()
        for eid in eventIds:
            lis = self.getListings(eid)
            if mode in ['file', 'both']:
                lis.writeFile()
            if mode in ['db', 'both']:
                lis.writeDb(dbName)
            sleep(6)
        logging.info("writeListingsAll finished")


class Event:
    def __init__(self, data):
    # data is in dict form
        self.data = data

    def getId(self):
        return self.data['id']

    def isGame(self):
        # check if is normal game or other events (season tickets etc.)
        if self.data['attributes'][0]['value'] == self.data['attributes'][1]['value']:
            return False
        if "Season" in self.data['title']:
            return False
        return True        

    # def writeDb(self):
    # # write event info (venues, performers) into db for query by eventId
    # # mind that key event info may change (e.g. time)
    #     db = 'db/stubhub.sqlite'
    #     pass

class Listings:
    def __init__(self, eventId, time, data):
    # data is in dict form
    # This can be constructed both from api directly or from file
        self.eventId = eventId
        self.time = time
        self.data = data
        self.stats = self.getStats()

    def getStats(self):
    # return stats of all the zones listed, as a dict keyed by zoneId
        stats = {}
        for lis in self.data['listing']:
            zoneId = lis['zoneId']
            if zoneId == None:
                continue
            if not (zoneId in stats):
                stats[zoneId] = {
                        'zoneName': lis['zoneName'],
                        'lowPrice': lis['currentPrice']['amount'],
                        'numOfLis': 1,
                        'numOfTix': lis['quantity']
                    }
            else:
                stats[zoneId]['numOfLis'] += 1
                stats[zoneId]['numOfTix'] += lis['quantity']
        return stats

    def writeDb(self, dbName):
    # write zone price stats into the low price tracking database
        if self.stats != {}:

            dbPath = os.path.join(scriptPath, 'db', dbName)
            query = 'INSERT INTO stats VALUES'
            query += '(?,?,?,?,?,?,?)'

            timeStr = self.time.strftime("%Y-%m-%d %H:%M:%S")

            logging.info("Writing into db, eventId = %s" % self.eventId)
            for zoneId, stat in self.stats.iteritems():
                values = (self.eventId, timeStr, zoneId, stat['zoneName'],
                    stat['numOfLis'], stat['numOfTix'], stat['lowPrice']
                    )
                with closing(sqlite3.connect(dbPath)) as conn:
                    conn.cursor().execute(query, values)
                    conn.commit()

    def writeFile(self):
    # write raw listings data into disk file
        timeStr = self.time.strftime('%Y-%m-%d %H-%M-%S')
        fileName = '%s-%s.txt' % (self.eventId, timeStr)
        fielPath = os.path.join(scriptPath, 'datafile', fileName)
        with open(fielPath, 'w') as f:
            logging.info("Writing to file")
            f.write(json.dumps(self.data))

