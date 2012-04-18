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
import select
import socket
import datetime

# External Library Imports
#from OpenSSL import SSL
from zope.interface import Interface, implements

#   Twisted
from twisted.web import server, resource, util
from twisted.application import internet, service
from twisted.internet import protocol, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.python import components, log

# Local Imports
import config

### Information ##############################################################
__version__ = "0.0.1"
__web__ = "github.com/chetmancini"
__author__ = "Chet Mancini"
__author_email__ = "cam479 at cornell dot edu"
__licence__ = "Apache"
__warranty__ = "None"

### Globals ##################################################################
#to make the process of adding new views less static
'''VIEWS = {
    'ListValues': ListValues(),
    'AddValue': AddValue(),
    'DeleteValue': DeleteValue(),
    'ClearValues': ClearValues()
    }'''
 
### Interfaces ###############################################################

class ITimberProtocol(Interface):

    def getCount(timePeriod):
        """
        Get total log items within a given time period
        """

    def getList(key):
        """
        Get all log items based on a given key
        """

class ITimberProtocolFactory(Interface):

    def getStatic(key):
        """
        Return a deferred returning a string.
        """

    def buildProtocol(addr):
        """
        Return a protocol returning a string.
        """

class ITimberService(Interface):
    pass


class ITimberServiceFactory(Interface):
    pass

### Methods ##################################################################

def catchError(err):
    return "Internal error in server"

### Classes ##################################################################

class TimberResource(resource.Resource):
    """
    Timber Resource
    """

    def render_GET(self, request):
        return 'Welcome to the REST API'

    def render_POST(self, request):
        requestDict = request.__dict__
        content = request.content.getvalue()

    '''def getChild(self, name, request):
        if name == '':
            return self
        else:
        if name in VIEWS.keys():
            return resource.Resource.getChild(self, name, request)
        else:
            return PageNotFoundError()'''
            

class PageNotFoundError(resource.Resource):
    """
    Page not found error.
    """

    def render_GET(self, request):
        return '404 Error: Not Found.'



class TimberProtocol(protocol.Protocol):
    """
    Timber service
    """

    implements(ITimberProtocol)

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.transport.loseConnection()
        self.factory.numProtocols = self.factory.numProtocols+1 
        #self.transport.write("Welcome! There are currently %d open connections.\n" % (self.factory.numProtocols,))

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols-1

    def dataReceived(self, data):
        pass
        #self.transport.write(data)



class TimberProtocolFactory(protocol.ServerFactory):
    """
    Factory for giving back a Timber service
    """

    implements(ITimberProtocolFactory)

    protocol = TimberProtocol

    def __init__(self, fileName):
        self.file = fileName

    def buildProtocol(self, addr):
        return Timber()

    def startFactory(self):
        self.fp = open(self.file, 'a')

    def stopFactory(self):
        self.fp.close()

'''
class TimberService(service.Service):

    implements(ITimberService)

class TimberServiceFactory(service.ServiceFactory):

    implements(ITimberServiceFactory)
'''

### Main #####################################################################
if __name__ == '__main__':
    options = parse_args()

    # this variable has to be named 'application'
    application = service.Application("timber")

    # this hooks the collection we made to the application
    #serviceCollection.setServiceParent(application)


    '''application = service.Application('finger', uid=1, gid=1)
    factory = TimberFactory(moshez='Happy and well')
    internet.TCPServer(79, factory).setServiceParent(
        service.IServiceCollection(application))
    '''

    '''endpoint = TCP4ServerEndpoint(reactor, 8007)
    endpoint.listen(TimberFactory())
    reactor.run()'''

    # configuration parameters
    port = 10000
    iface = 'localhost'
    fileparam = 'aasdf.txt'

    root = resource.Resource()
    root.putChild("logger", TimberResource())

    #serviceCollection = service.MultiService()

    #timber_service = TimberService(fileparam)
    #timber_service.setServiceParent(serviceCollection)

    # the tcp service connects the factory to a listening socket. it will
    # create the listening socket when it is started
    #timber_factory = TimberFactory(timber_service)

    """    log_service = internet.TCPServer(config.DEFAULT_LOG_PORT, timber_factory, interface=iface)
    log_service.setServiceParent(serviceCollection)"""

    """    gossip_service = internet.TCPServer(config.DEFAULT_RECEIVE_PORT, factory, interface=iface)
    gossip_service.setServiceParent(serviceCollection)"""

    log_server = TCPServer(config.DEFAULT_LOG_PORT, Site(root))
    log_server.setServiceParent(application)