# This scrapes and records tickets data of whole league (one time only)
# takes command line argument: league, mode
# league = 'NFL2015Reg' |
# mode = 'db' | 'file' | 'both'

import sys
sys.dont_write_bytecode = True
import os
scriptPath = os.path.abspath(os.path.dirname(__file__))

from datascraper import Datascraper
from db.dbInitializer import DbInitializer
from db.static.idinfo import *

import logging
logPath = os.path.join(scriptPath, 'logs/scraper.log')
logging.basicConfig(filename=logPath, level=logging.DEBUG, 
                    format='%(asctime)s %(message)s')


def main(league, mode):

    if (league not in ('NFL2015Reg',)) or (
            mode not in ('db', 'file', 'both')):

        logging.error("Invalid arguments (\'%s\', \'%s\'')" % (league, mode))
        print "Invalid arguments (\'%s\', \'%s\'')" % (league, mode)
        return

    if league == 'NFL2015Reg':
        dbName = 'stubhub_NFL2015.sqlite'
        teamList = teamsNFL
        dateTo = '2016-01-05T01:59'
        # dbi = DbInitializer(dbName)
        # dbi.init_table('stats')

    for team in teamList:
        ds = Datascraper(team, dateTo)
        ds.writeListingsAll(mode=mode, dbName=dbName)

try:
    main(sys.argv[1], sys.argv[2])
except:
    logging.exception('')
    raise