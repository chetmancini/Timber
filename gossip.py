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

# External Library Imports
from zope.interface import Interface, implements
from twisted.internet import task, reactor
from twisted.internet.protocol import 
    Protocol, ServerFactory, ReconnectingClientFactory

# Local Imports
import config
import connections
import message
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
        msg = message.buildMessage(data)
        #debug("Gossip Data Received on " + connections.getMe().getIp() 
        #+ " from " + msg.getSender().getIp())
        #if msg.isIsAliveMessage():
        #    self.transport.write(connections.getMe().getUid())
        msg.respond() # just respond polymorphically.

class GossipClientProtocol(Protocol):
    """
    Gossip client protocol
    """
    implements(IGossipClientProtocol)

    def connectionMade(self):
        debug("Huh? Client protocol connection made??")
        pass

    def connectionLost(self):
        debug("huh? client protocol connection lost??")
        pass

    def dataReceived(self, data):
        """
        Data received? this seems a little odd.
        """
        debug("huh? Client protocol data received??")
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

        #self.clients = []
        self.lc = task.LoopingCall(self.gossip)
        self.lc.start(config.GOSSIP_WAIT_SECONDS, False)
        debug("Gossip Server Factory created!", success=True)

    def gossip(self):
        """
        Gossip procedure. This is basic. Hope to improve later.
        """
        connections.connectToNeighbors()
        debug("I am now gossiping with:")

        # Get my neighbors
        recipients = connections.getNeighbors()
        for uid in recipients:
            debug("\t" + uid + "\t" + externalnode.getIp())

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


        # Send out the messages
        for msg in gossipMessages:
            msg.send()


    def clientConnectionMade(self, client):
        """
        When a node is found
        """
        #self.clients.append(client)
        debug("Receiving client " + str(client.transport.getPeer()))
        connections.foundClient(client.transport)

    def clientConnectionLost(self, client, reason):
        """
        When a node is lost.
        """
        debug("Lost client " + str(client.transport.getPeer()) + " for reason " + str(reason))
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
        debug("Client Connection failed for reason: " + reason)
        self.errback(reason)

    def clientConnectionLost(self, connector, unused_reason):
        debug("Client Connection lost!")
        self.errback(reason)

    def startedConnecting(self, connector):
        debug("Client Factory started connecting...")
        pass

    def startFactory(self):
        debug("Client Factory Started.")
        pass #good for connectiong, opening fiels, etc..

    def stopFactory(self):
        debug("Client Factory Stopped.")
        pass #good for disconnectiong databases, closing files.


### Functions ################################################################
def gossipRun():
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