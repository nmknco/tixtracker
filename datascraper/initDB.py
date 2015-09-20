import sys
sys.dont_write_bytecode = True
import os
scriptPath = os.path.abspath(os.path.dirname(__file__))

from db.dbInitializer import DbInitializer
from db.static.idinfo import teamsNFL


def initDB(league):
    
    if league == 'NFL2015Reg':
        dbName = 'stubhub_NFL2015.sqlite'
        dbi = DbInitializer(dbName)
        dbi.init_alltables()
        dbi.write_allevents(teamsNFL, '2015-09-06T23:59', '2016-01-05T01:59')
        dbi.write_allevents(teamsNFL, '2015-09-07T01:59', '2016-01-05T01:59')
        dbi.write_allvenues(teamsNFL)
        return

    print "Invalid league name."

if __name__ == '__main__':

    league = raw_input("Please enter the leauge to initialize: ")
    initDB(league)