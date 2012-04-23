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
# gossip.py                                                                  #
# Gossip channels                                                            #
##############################################################################
#        __  ___                                                             #
#       / / / (_)_________                                                   #
#      / /_/ / / ___/ ___/                                                   #
#     / __  / (__  |__  )                                                    #
#    /_/ /_/_/____/____/        Gossip with Python on Twisted                #
#                                                                            #
##############################################################################

### Imports ##################################################################
# Python Libary Imports
import sys
import traceback
import random
try:
    from Queue import Queue, Empty
except ImportError: #Hack for Python2to3
    from queue import Queue, Empty

# External Library Imports
from zope.interface import Interface, implements
from twisted.internet import task, reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import ReconnectingClientFactory

# Local Imports
import me
import config
import connections
import message
import aggregation
import group_membership
from timber_exceptions import GeneralError, ConnectionError
from debug import debug

### Globals ##################################################################

gossipqueue = Queue()

### Interfaces ###############################################################
class IGossipServerProtocol(Interface):
    """
    GossipServerProtocol Interface
    """

class IGossipClientProtocol(Interface):
    """
    GossipClientProtocol Interface
    """

class IGossipServerFactory(Interface):
    """
    GossipServerFactory Interface
    """

class IGossipClientFactory(Interface):
    """
    GossipClientFactory Interface
    """

### Classes ##################################################################

class GossipServerProtocol(Protocol):
    """
    Gossip server protocol
    """

    implements(IGossipServerProtocol)

    def connectionMade(self):
        """
        Callback called once a connection is made with a client.
        """
        debug("Server protocol connection made!", success=True)
        self.factory.clientConnectionMade(self)

        # Send a response
        #response = message.MeMessage()
        #response.send(self.transport)
        self.transport.write(me.getUid())

    def connectionLost(self, reason):
        """
        Callback called when a connection is lost.
        Pretty much just ignore. client connection losses
        more important.
        """
        self.factory.clientConnectionLost(self, reason)

    def dataReceived(self, data):
        """
        When gossip data is received.
        """
        debug("DATA RECEIVED BOOYAH!", success=True)
        if len(data) == 32:
            connections.assignTransport(data, self.transport)
        else:
            try:
                msg = message.buildMessage(data)
                msg.respond() # just respond polymorphically.
            except:
                debug(data, error=True)

class GossipClientProtocol(Protocol):
    """
    Gossip client protocol
    """
    implements(IGossipClientProtocol)

    def connectionMade(self):
        """
        Callback when a connection is made.
        """
        debug("Client Protocol connection made", success=True)
        connections.clientConnectionMade(self.transport)

        ### Send a message to respond.
        #response = message.MeMessage()
        #response.send(self.transport)
        self.transport.write(me.getUid())

    def connectionLost(self):
        """
        Callback when a connection is lost.
        """
        debug("Client Protocol connection lost", error=True)
        connections.clientConnectionLost(self.transport.addr)


    def dataReceived(self, data):
        """
        Data received? this seems a little odd.
        """
        debug("DATA RECEIVED...ON CLIENT?", strange=True)
        if len(data) == 32:
            connections.assignTransport(data, self.transport)
        else:
            try:
                msg = message.buildMessage(data)
                msg.respond()
            except:
                debug("data: " + data, error=True)


class GossipServerFactory(ServerFactory):
    """
    Gossip Factory
    """

    implements(IGossipServerFactory)

    protocol = GossipServerProtocol
    """
    This factory will create gossip protocol objects on connections.
    """

    def __init__(self):
        """
        Factory Constructor
        """
        # We want to run members refresh every once in awhile
        self.membersLoop = task.LoopingCall(connections.maintainMembers)
        self.membersLoop.start(group_membership.getRandomWaitTimeSecs(), True)

        debug("Gossip Server Factory created!", success=True)


    def clientConnectionMade(self, client):
        """
        When a node is found
        """
        debug("Server: Receiving client " + str(client.transport.getPeer()), 
            success=True)

        connections.foundClientAsServer(client.transport)

    def clientConnectionLost(self, client, reason):
        """
        When a node is lost.
        """
        debug("Server: Lost client " + str(client.transport.getPeer()) + \
            " for reason " + str(reason), error=True)

        connections.lostClientAsServer(client.transport)

    def startFactory(self):
        pass

    def stopFactory(self):
        pass


class GossipClientFactory(ReconnectingClientFactory):
    """
    Factory for gossip clients
    """

    implements(IGossipServerFactory)

    protocol = GossipClientProtocol

    def __init__(self, callback=None, errback=None):
        """
        Constructor.
        """
        debug("Client Factory Init", info=True)
        # Run gossip on a timer.
        self.gossipLoop = task.LoopingCall(self.gossip)
        self.gossipLoop.start(config.GOSSIP_WAIT_SECONDS, False)

        self.callback = callback
        self.errback = errback

    def clientConnectionFailed(self, connector, reason):
        """
        Callback when the client connection fails.
        """
        debug("Client Connection failed for reason: " + reason, info=True)
        if self.errback:
            self.errback(reason)

    def clientConnectionLost(self, connector, unused_reason):
        """
        Callback for when the client connection is lost.
        """
        debug("Client Connection lost!", info=True)
        if self.errback:
            self.errback(reason)

    def startedConnecting(self, connector):
        """
        Called when a connection is starting
        """
        debug("Client Factory started connecting...", info=True)

    def startFactory(self):
        """
        Called when the factory is started
        """
        debug("Client Factory Started...", info=True)
        pass #good for connectiong, opening fiels, etc..

    def stopFactory(self):
        """
        Called when the factory is stopped.
        """
        debug("Client Factory Stopped...", info=True)
        pass #good for disconnectiong databases, closing files.


    def gossip(self):
        """
        Gossip procedure. This is basic. Hope to improve later.
        """
        if connections.connectToNeighbors():
            debug("Connections in process. deferred gossip", info=True)
            return

        # Get my neighbors
        recipients = connections.getNeighbors()

        if len(recipients) > 0:
            debug("I am now gossiping with:", info=True)
            for uid in recipients:
                externalnode = connections.lookupNode(uid)
                debug("-----[ " + externalnode.getShortUid() + " ]" + \
                    "--" + str(externalnode.getIp()) + ":" + \
                    str(externalnode.getPort()), info=True)
        else:
            debug("No neighbors to gossip with this interval.", error=True)
            return

        # Put all messages in a list.
        gossipMessages = []

        # Get a vector clock message
        vcMessage = message.VectorMessage.createVectorClockMessage()
        vcMessage.setRecipients(recipients)
        gossipMessages.append(vcMessage)

        # Put in each aggreggation. Tae out for now.
        """
        for aggName in aggregation.STATISTICS:
            agg = aggregation.STATISTICS[aggName]
            aggMessage = message.AggregateMessage.createAggregateMessage(agg)
            aggMessage.setRecipients(recipients)
            gossipMessages.append(aggMessage)
        """
        agg = random.choice(aggregation.STATISTICS.values())      
        aggMessage = message.AggregateMessage.createAggregateMessage(agg)
        aggMessage.setRecipients(recipients)
        gossipMessages.append(aggMessage)

        # Get a network message
        gossipmsg = gossipPrepare()
        while gossipmsg:
            gossipmsg.setRecipients(recipients)
            toAppend = copy.deepcopy(gossipmsg)
            gossipMessages.append(toAppend)
            gossipmsg = gossipPrepare()

        debug("There are " \
            + str(len(gossipMessages)) + " to send.", threshold=2, info=True)

        # Send out the messages
        for msg in gossipMessages:
            try:
                msg.send()
            except ConnectionError as ce:
                debug(ce.__str__(), error=True)
            except GeneralError as ge:
                debug(ge.__str__(), error=True)


### Factories ################################################################
gossipServerFactory = None
gossipClientFactory = None

### Functions ################################################################
def gossipClientConnect(host, port):
    """
    connect as a client. returns a connector
    """
    connector = reactor.connectTCP(host, port, gossipClientFactory)
    debug("Reactor is connecting to " + host + ":" + str(port), 
        info=True)
    return connector

def gossipRun():
    """
    Execute the gossip logic.
    """
    global gossipClientFactory
    global gossipServerFactory

    gossipServerFactory = GossipServerFactory()
    gossipClientFactory = GossipClientFactory()

    debug("Launching Hiss Listener on port " + \
        str(config.RECEIVE_PORT) + ".", info=True)

    reactor.listenTCP(config.RECEIVE_PORT, gossipServerFactory)

def gossipThis(msg):
    """
    Receive a gossiped Message from another node.
    """
    global gossipqueue

    debug("Received Gossip message: " + msg.__class__.__name__ + 
        " from " + msg.getSender() + " (" + msg.getCode() + ")", success=True)

    gossipqueue.put_nowait(msg)

def gossipPrepare():
    """
    Get the next Message object to gossip to friends
    """
    if not gossipqueue.empty():
        return gossipqueue.get_nowait()
    else:
        return None


### Main #####################################################################
if __name__ == "__main__":
    """
    This allows one to run gossip directly without other APIs
    """
    gossipRun()
    reactor.run()