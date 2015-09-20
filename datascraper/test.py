import sys
sys.dont_write_bytecode = True
import os
scriptPath = os.path.abspath(os.path.dirname(__file__))

from datascraper import Datascraper
from db.dbInitializer import DbInitializer
from db.static.idinfo import teamsNFL

import logging
logPath = os.path.join(scriptPath, 'logs/scraper.log')
logging.basicConfig(filename=logPath, level=logging.DEBUG, 
                    format='%(asctime)s %(message)s')



def main():

    dbName = 'stubhub_NFL2015.sqlite'
    # dbi = DbInitializer(dbName)
    # dbi.init_table('stats')

    for team in teamsNFL:
        ds = Datascraper(team, '2016-01-05T01:59')
        ds.writeListingsAll(mode='both', dbName='stubhub_NFL2015.sqlite')

try:
    main()
except:
    logging.exception('')