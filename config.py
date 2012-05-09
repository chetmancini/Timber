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
# config.py                                                                  #
# Holds configuration information global to the entire system                #
##############################################################################

### Imports ##################################################################


############################ Constants (edit these) ##########################
IPV6 = False
"""
Whether to use IP version 6. turn off for now.
"""

DEFAULT_SEND_PORT = 30581
DEFAULT_RECEIVE_PORT = 30081
DEFAULT_LOG_PORT = 8081
"""
Default port to receive on / send to.
Default port to communicate from / recieve from.
"""

DEFAULT_TIMESTAMP_DELAY = 300
DEFAULT_SIMULATION_DELAY = 60
DEFAULT_RETRY_DELAY = 120
DEFAULT_RETRY_ATTEMPTS = 10
DEFAULT_MAX_DISPLAY = 40
DEFAULT_GOSSIP_WAIT_SECONDS = 5
"""
Gossip settings
"""

QUEUE_PROVIDER = "RabbitMQ"

QUEUE_LOG_NAME = "timber_log"
QUEUE_COMMUNICATION_BUS_NAME = "timber_bus"
QUEUE_USERNAME = "guest"
QUEUE_PASSWORD = "guest"
QUEUE_HOST = "localhost"
QUEUE_PORT = 5672
"""
Queue connection information.
Provider choices:
'RabbitMQ' | 'SQS'
"""

GOSSIP_NEIGHBOR_STRATEGY = "default"
"""
default | random | all | single | logarithmic | constant
"""

GOSSIPTTL = 10
"""
Hops a message should live. Backup so
a message doesn't get stuck in system.
Messages will be destroyed once they hit 0.
"""

AGGREGATE_AVERAGE_REFRESH_MIN = 5
AGGREGATE_AVERAGE_REFRESH_MAX = 10
"""
When to refresh from the local node.
"""

MONGO_DB_HOST = "staff.mongohq.com"
MONGO_DB_PORT = 10005
MONGO_DB_NAME = "timber"

MONGO_DB_USER= "timber"
MONGO_DB_PASSWORD = "timber360"
"""
MongoDB login information
"""

STATS_REFRESH_INTERVAL = 5

MONGO_DB_LOG_COLLECTION = "timber_log"

MEMBERS_REFRESH_INTERVAL = 23

AWS_SECRET_KEY = "7rPpW/1gJ7gNGu6sSyLMxuhYxDPowifIeeFJy0lk"
AWS_ACCESS_KEY = "AKIAIGOASEZFJITFFO4Q"
AWS_SDB_DOMAIN_NAME = "TIMBER_NODE_LIST"
"""
Amazon Web Services Information
"""

######################## Don't edit below this line ##########################
MONGO_URI = "mongodb://" + MONGO_DB_USER + ":" + MONGO_DB_PASSWORD + "@"
MONGO_URI += MONGO_DB_HOST + ":" + str(MONGO_DB_PORT) + "/" + MONGO_DB_NAME

RECEIVE_PORT = DEFAULT_RECEIVE_PORT
SEND_PORT = DEFAULT_SEND_PORT
LOG_PORT = DEFAULT_LOG_PORT
GOSSIP_WAIT_SECONDS = DEFAULT_GOSSIP_WAIT_SECONDS

QUEUE_CREDENTIALS = {"LOGIN": QUEUE_USERNAME, 
               "PASSWORD": QUEUE_PASSWORD}


def getNextSendPort():
	global SEND_PORT
	SEND_PORT += 10
	return SEND_PORT