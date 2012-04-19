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
import nodes

############################ Constants (edit these) ##########################
IPV6 = False
"""
Whether to use IP version 6. turn off for now.
"""

DOORNODE_IP = '192.168.0.1'
DOORNODE_PORT = 8080
"""
New nodes communicate with a doorway node. This information goes here.
"""

DEFAULT_SEND_PORT = 30480
DEFAULT_RECEIVE_PORT = 30481
DEFAULT_LOG_PORT = 8080
"""
Default port to receive on / send to.
Default port to communicate from / recieve from.
"""

DEFAULT_TIMESTAMP_DELAY = 300
DEFAULT_SIMULATION_DELAY = 60
DEFAULT_RETRY_DELAY = 120
DEFAULT_RETRY_ATTEMPTS = 10
DEFAULT_MAX_DISPLAY = 40
DEFAULT_GOSSIP_WAIT_SECONDS = 10
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

GOSSIPTTL = 10
"""
Hops a message should live. Backup so
a message doesn't get stuck in system.
Messages will be destroyed once they hit 0.
"""

MONGO_DB_NAME = "timber"
MONGO_DB_USER= "timber"
MONGO_DB_PASSWORD = "timber360"
"""
MongoDB login information
"""

MONGO_DB_HOST = "127.0.0.1"
MONGO_DB_PORT = 10001
"""
Hostname of the Mongo server/cluster. Default: localhost
"""

MONGO_DB_LOG_COLLECTION = "timber_log"

MEMBERS_REFRESH_INTERVAL = 15

AWS_SECRET_KEY = "7rPpW/1gJ7gNGu6sSyLMxuhYxDPowifIeeFJy0lk"
AWS_ACCESS_KEY = "AKIAIGOASEZFJITFFO4Q"
AWS_SDB_DOMAIN_NAME = "TIMBER_NODE_LIST"
"""
Amazon Web Services Information
"""

######################## Don't edit below this line ##########################
DOORNODE = nodes.DoorNode(DOORNODE_IP, DOORNODE_PORT)

MONGO_URI = "mongodb://" + MONGO_DB_USER + ":" + MONGO_DB_PASSWORD + "@"
MONGO_URI += MONGO_DB_HOST + ":" + str(MONGO_DB_PORT) + "/" + MONGO_DB_NAME

RECEIVE_PORT = DEFAULT_RECEIVE_PORT
LOG_PORT = DEFAULT_LOG_PORT
GOSSIP_WAIT_SECONDS = DEFAULT_GOSSIP_WAIT_SECONDS

QUEUE_CREDENTIALS = {"LOGIN": QUEUE_USERNAME, 
               "PASSWORD": QUEUE_PASSWORD}