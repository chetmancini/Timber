##############################################################################
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
##############################################################################

#----------------------------------------------------------------------------#
#   Name:       Timber                                                       #
#   Description: A cloud based logging/analytics system                      #
#                built on top of RabbitMQ and MongoDB                        #
#   Web:            github.com/chetmancini                                   #
#   Author:         Chet Mancini                                             #
#   Email:          cam479 at cornell dot edu                                #
#   Version:    0.0.1                                                        #
#   License:    MIT                                                          #
#   Warranty:   None of any kind                                             #
#                                                                            #
#   Dependencies: RabbitMQ, MongoDB                                          #
#----------------------------------------------------------------------------#

### Imports ##################################################################
#   Python Standard Library
import logger
import sys
import json
import errno
import optparse
import select
import socket
import datetime

# External Library Imports
from zope.interface import Interface, implements

from twisted.web import server, resource, util
from twisted.application import internet, service
from twisted.internet import protocol, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.python import components, log

# Local Imports
import config
import me
import stats
import message
import message_queue
import aggregation
from timber_exceptions import GeneralError, ConnectionError
from debug import debug


### Application ##############################################################
__name__ = "Timber/Hiss"
__summary__ = "Gossip on Twisted in Python"
__version__ = "0.0.1"
__web__ = "github.com/chetmancini"
__author__ = "Chet Mancini"
__author_email__ = "cam479 at cornell dot edu"
__licence__ = "Apache"
__warranty__ = "None"

### Methods ##################################################################

def catchError(err):
    return "Internal error in server"

def getHead():
    return """
    <div style='font-family:sans-serif;'>
    <h1>Timber API Access</h1>
    """

def getFoot():
    return """
    </div>
    """

### Classes ##################################################################

class TimberRootResource(resource.Resource):
    """
    Timber root resource
    """

    def render_GET(self, request):
        """
        get response method for the root resource
        localhost:8000/
        """
        debug("GET request received at Root on " + \
            me.getMe().getIp(), info=True, threshold=3)
        return 'Welcome to the REST API'

    def getChild(self, name, request):
        """
        We overrite the get child function so that we can handle invalid
        requests
        """
        if name == '':
            return self
        else:
            if name in APIS.keys():
                return resource.Resource.getChild(self, name, request)
            else:
                return PageNotFoundError()


class TimberLoggingResource(resource.Resource):
    """
    Timber Logging Resource
    """

    def render_GET(self, request):
        """
        Receive GET request on the logging api. Just tell em they've arrived.
        """
        debug("received GET request on logging resource")
        description = "Welcome to the Timber REST API. Use POST to log data."
        description += "JSON Format:{'level': INTEGER,'message': STRING,"
        description += "'type': STRING}"
        return description

    """
    def render_POST(self, request):
        requestDict = request.__dict__
        requestArgs = request.args
        #content = request.content.getvalue() ? not sure if this is right.
        rawcontent = request.content.read()
        content = json.loads(rawcontent)
        debug("received content:" + content)
        try:
            logMessage = content['message']
            logLevel = content['level']
            logType = content['type']
            msg = message.ExternalLogMessage(logMessage, logLevel, logType)
            logger.logMessage(msg)
        except:
            debug('Problem logging', error=True)
            return "There was a problem logging the message"
        return "Message Logged!"
    """

    def render_POST(self, request):
        """
        Handle post request
        """
        """
        args = request.args
        print args
        logMessage = args['message'][0] if 'message' in args else None
        logLevel = args['level'][0] if 'level' in args else None
        logType = args['type'][0] if 'type' in args else None
        """
        stringcontent = request.content.read()
        if len(stringcontent) > 0:
            debug("received: " + stringcontent, info=True)
            
        content = json.loads(stringcontent)

        logMessage = content['message']
        logLevel = content['level']
        logType = content['type']
        try:
            if logMessage:
                msg = message.ExternalLogMessage(logMessage, logLevel, logType)
                me.getMe().getVectorClock().handleEvent(msg)
                message_queue.put(msg)
                return "Success"
            else:
                return "Null message"
        except Exception as e:
            debug(e, error=True)
            return "Error"



class TimberStatsResource(resource.Resource):
    """
    Resource for getting server stats.
    """

    def render_GET(self, request):
        """
        Get statistics for this node and the system
        """
        debug("Recevied GET on stat resouce")
        requestDict = request.__dict__
        requestArgs = request.args

        if 'name' in requestArgs:
            name = requestArgs['name'][0]
            if name == 'all':
                aggDict = {}
                for name in aggregation.STATISTICS:
                    aggDict[name] = aggregation.getAggregation(name)
                return json.dumps(aggDict)
            elif name in aggregation.STATISTICS:
                aggDict = aggregation.getAggregation(name)
                debug("Sent Stat response for " + name, 
                    success=True, threshold=2)
                return json.dumps(aggDict)
            else:
                return "Not a valid statistic name. Try: '" + \
                    + "' | '".join(aggregation.STATISTICS.keys()) + "'"
        else:
            ret = getHead()
            ret += "<p>Set a 'name' GET parameter to:</p><ul>"
            for key in aggregation.STATISTICS:
                ret += "<li><a href='?name="+key+"'>"+key+"</a></li>"
            ret += "</ul>"
            ret += getFoot()
            return ret

    def render_POST(self, request):
        """
        Post data to statistics. Not currently supported.
        """
        debug("Invalid stats POST access", info=True)
        ret = getHead()
        ret += "<p>POST access not provided.</p>"
        ret += "<p>Set a 'name' GET parameter to:</p><ul>"
        for key in aggregation.STATISTICS:
            ret += "<li><a href='?name="+key+"'>"+key+"</a></li>"
        ret += "</ul>" + getFoot()
        return ret


class PageNotFoundError(resource.Resource):
    """
    Page not found error.
    """

    def render_GET(self, request):
        """
        Render page not found for GET requests
        """
        debug("404 error")
        return '404 Error: Not Found.'

    def render_POST(self, request):
        """
        Render page not found for POST requests
        """
        debug("POST to page not found? wtf.")
        return '404 Error: Not found.'

### Globals ##################################################################

APIS = {
    'logger': TimberLoggingResource(),
    'stats': TimberStatsResource(),
    }

### Main #####################################################################

def timberRun():
    """
    Run the Timber API on the reactor.
    """
    root = TimberRootResource()
    root.putChild("logger", TimberLoggingResource())
    root.putChild("stats", TimberStatsResource())

    timber_factory = server.Site(root)

    debug("Launching Timber listener on port " \
        + str(config.LOG_PORT) + ".", info=True)
    
    reactor.listenTCP(config.LOG_PORT, timber_factory)


if __name__ == "__main__":
    """
    This allows one to run the Timber API without running other services
    (like gossip) for testing.
    """
    timberRun()
    reactor.run()