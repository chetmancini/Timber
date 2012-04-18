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
#   Installation Instructions:                                               #
#       Lorem ipsum                                                          #
#                                                                            #
##############################################################################

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
from debug import debug
import connections

### Methods ##################################################################

def catchError(err):
    return "Internal error in server"

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
        debug("GET request received at Root on " + connnections.getMe().getIp())
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

    def render_POST(self, request):
        """
        Receive POST request on the logger. This is the main logging api.

        JSON Format:
        {
            'level': INTEGER
            'message': STRING
            'type': STRING
        }
        
        """
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
            debug('problem logging')
            return "There was a problem logging the message"
        return "Message Logged!"


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
        # TODO implement this!

    def render_POST(self, request):
        """
        Post data to statistics. Not currently supported.
        """
        debug("Invalid stats POST access")
        return "Sorry, POST access not provided"


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

def timberSimpleRun():
    """
    Run the Timber API on the reactor.
    """
    root = TimberRootResource()
    root.putChild("logger", TimberLoggingResource())
    root.putChild("stats", TimberStatsResource())

    timber_factory = server.Site(root)

    reactor.listenTCP(config.LOG_PORT, timber_factory)


if __name__ == "__main__":
    """
    This allows one to run the Timber API without running other services
    (like gossip) for testing.
    """
    timberSimpleRun()
    reactor.run()