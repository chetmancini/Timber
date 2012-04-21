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
import Queue
import sys
import traceback

# External Library Imports
from zope.interface import Interface, implements
from twisted.internet import task, reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import ReconnectingClientFactory

# Local Imports
import config
import connections
import message
import aggregation
import group_membership
from timber_exceptions import GeneralError, ConnectionError
from debug import debug

### Globals ##################################################################

gossipqueue = Queue.Queue()

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
        self.factory.clientConnectionMade(self)

    def connectionLost(self, reason):
        """
        Callback called when a connection is lost.
        """
        self.factory.clientConnectionLost(self, reason)

    def dataReceived(self, data):
        """
        When gossip data is received.
        """
        debug("Raw data received", info=True)
        msg = message.buildMessage(data)

        msg.respond() # just respond polymorphically.

class GossipClientProtocol(Protocol):
    """
    Gossip client protocol
    """
    implements(IGossipClientProtocol)

    def connectionMade(self):
        debug("Client protocol connection made", info=True)
        pass

    def connectionLost(self):
        debug("Client protocol connection lost", error=True)
        pass

    def dataReceived(self, data):
        """
        Data received? this seems a little odd.
        """
        debug("Client protocol data received?", strange=True)
        msg = message.buildMessage(data)
        msg.respond()



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
        self.membersLoop.start(group_membership.getRandomWaitTimeSecs(), False)

        # Run gossip on a timer.
        self.gossipLoop = task.LoopingCall(self.gossip)
        self.gossipLoop.start(config.GOSSIP_WAIT_SECONDS, False)

        debug("Gossip Server Factory created!", success=True)

    def gossip(self):
        """
        Gossip procedure. This is basic. Hope to improve later.
        """
        connections.connectToNeighbors()

        # Get my neighbors
        recipients = connections.getNeighbors()

        if len(recipients) > 0:
            debug("I am now gossiping with:")
            for uid in recipients:
                debug("\t" + uid + "\t" + externalnode.getIp())
        else:
            debug("No neighbors to gossip with this interval.", error=True)
            return

        # Put all messages in a list.
        gossipMessages = []

        # Get a vector clock message
        vcMessage = message.VectorMessage.createVectorClockMessage()
        vcMessage.setRecipients(recipients)
        gossipMessages.append(vcMessage)

        # Put in each aggreggation
        for agg in aggregation.STATISTICS:
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
                debug("message sent", success=True)
            except ConnectionError as ce:
                debug(ce.__str__(), error=True)
            except GeneralError as ge:
                debug(ge.__str__(), error=True)


    def clientConnectionMade(self, client):
        """
        When a node is found
        """
        debug("Receiving client " + str(client.transport.getPeer()), 
            info=True)

        connections.foundClient(client.transport)

    def clientConnectionLost(self, client, reason):
        """
        When a node is lost.
        """
        debug("Lost client " + str(client.transport.getPeer()) + \
            " for reason " + str(reason), info=True)

        connections.lostClient(client.transport)


class GossipClientFactory(ReconnectingClientFactory):
    """
    Factory for gossip clients
    """

    implements(IGossipServerFactory)

    protocol = GossipClientProtocol

    def __init__(self, callback, errback):
        debug("client factory init")
        self.callback = callback
        self.errback = errback

    def clientConnectionFailed(self, connector, reason):
        debug("Client Connection failed for reason: " + reason, info=True)
        self.errback(reason)

    def clientConnectionLost(self, connector, unused_reason):
        debug("Client Connection lost!", info=True)
        self.errback(reason)

    def startedConnecting(self, connector):
        debug("Client Factory started connecting...", info=True)
        pass

    def startFactory(self):
        debug("Client Factory Started.", info=True)
        pass #good for connectiong, opening fiels, etc..

    def stopFactory(self):
        debug("Client Factory Stopped.", info=True)
        pass #good for disconnectiong databases, closing files.


### Functions ################################################################
def gossipRun():

    debug("Launching Hiss Listener on port " + \
        str(config.RECEIVE_PORT) + ".", info=True)

    gossipServerFactory = GossipServerFactory()
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
        return gossipqueue.get()
    else:
        return None


### Main #####################################################################
if __name__ == "__main__":
    """
    This allows one to run gossip directly without other APIs
    """
    gossipRun()
    reactor.run()