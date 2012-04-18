##############################################################################
#                                                                            #
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
#----------------------------------------------------------------------------#
# persist.py                                                                 #
# contains all the stuff for persistant storage                              #
##############################################################################


### Imports ###################################################################
# Python Library Imports
import time
import datetime

# External Library Imports
import bson
import pymongo.connection
import pymongo.database
import pymongo.collection

# Local Imports
import config
from debug import debug


### Script  ###################################################################
mongoConnection = pymongo.connection.Connection(
    config.MONGO_DB_HOST, 
    config.MONGO_DB_PORT)

if mongoConnection:
     debug("PyMongo Established connection", success=True)

mongoDatabase = pymongo.database.Database(
    mongoConnection, 
    config.MONGO_DB_NAME)

if mongoDatabase:
    debug("PyMongo Initialized DB", success=True)

    mongoDatabase.authenticate(
        config.MONGO_DB_USER, 
        config.MONGO_DB_PASSWORD)

    debug("PyMongo database authenticated.", success=True)


try:
    validation_data = mongoDatabase.validate_collection(
        config.MONGO_DB_LOG_COLLECTION)

    debug("PyMongo validating database collection")
except:
    database.create_collection(
        config.MONGO_DB_LOG_COLLECTION)

    debug("PyMongo could not find collection. Creating collection.")

mongoCollection = pymongo.collection.Collection(
    mongoDatabase, 
    config.MONGO_DB_LOG_COLLECTION)

if mongoCollection:
    debug("PyMongo: Database collection set up successfully.", success=True)
else:
    debug("PyMongo: Database collection initialization failed.", error=True)


### Access Functions  ########################################################
def insert(items):
    """
    Insert one or more items into the collection.
    """
    global mongoCollection
    mongoCollection.insert(items)


def find(searchDict):
    """
    Return a message
    """
    return mongoCollection.find(searchDict)


def insertMessage(message):
    """
    Insert a message into the collection.
    """
    value = {
        "payload": message.getPayload(),
        "time": message.getTime(),
        "code": message.getCode
        }
    insert(value)

def findMessages(searchDict):
    """
    Find messages in the collection.
    """
    return mongoCollection.find(searchDict)

def log(typ, msg, ordered=True):
    """
    Log a received piece of data from the api.
    Can be ordered or not. 
    """
    try:
        item = {"type":typ,"message":msg,"time":time.time()}
        if ordered:
            item["machine"] = connections.me.getUid()
            item["clock"] = connections.me.getVectorClock().getClocks()
        insert(item)
        debug("logged item", success=True)
    except:
        debug("did not log message (ordered:" + str(ordered) + ")", error=True)
          

