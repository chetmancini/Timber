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
# message.py                                                                 #
# Message objects                                                            #
##############################################################################

### Imports ##################################################################
# Python Library Imports
import time
import cPickle

# External Library Imports
import zope.interface

# Local Imports
import config
import vectorClock
import connections
from debug import debug

### Message Interface ########################################################
class IMessage(zope.interface.Interface):
    """
    Interface for all messages.
    """

    def getSender():
        """
        Get the sender of a message
        """

    def getRecipients():
        """
        Get the recipient for a message.
        """

    def getPayload():
        """
        Get the message body.
        """

    def getSerialized():
        """
        Data of the payload for transfer.
        """

    def getTime():
        """
        Get the messages created time.
        """

    def send():
        """
        Send a message
        """

    def getCode():
        """
        Get the message code.
        """

    def __str__():
        """
        Messages must have a string representation
        """

### Classes of Message #######################################################
class GenericMessage(object):
    """
    Message class
    """

    zope.interface.implements(IMessage)

    def __init__(self, payload, sender=None, recipients=None):
        """
        Constructor
        """
        self._payload = payload
        self._time = time.time()
        self._code = "?"

        if sender:
            self._sender = sender
        else:
            self._sender = connections.getMe().getBaseData()
            # just assign basic node data to the sender.

        if recipients:
            self._recipients = recipients
        else:
            self._recipients = []

    def getSender(self):
        """
        Get the sender of this message. Ideally a node object.
        """
        return self._sender

    def setSender(self, sender):
        """
        Set the sender of this message with a new node object.
        """
        self._sender = sender

    def getRecipients(self):
        """
        Get the recipient for the message. Ideally a list of UID strings.
        """
        return self._recipients

    def setRecipients(self, recipients):
        """
        Set the recipients for the message
        """
        self._recipients = recipients

    def getPayload(self):
        """
        Get the message body
        """
        return self._payload

    def getSerialized(self):
        """
        get a string of the payload.
        """
        return cPickle.dumps(self)

    def getTime(self):
        """
        Get the time created
        """
        return self._time

    def send(self):
        """
        Send the message. Assume we don't have multicast, 
        so just do point to point for now.
        """
        if not self._recipients or len(self.getRecipients()) == 0:
            debug("No recipients specified.", error=True)
            raise "No recipients specified. Gossip message type" \
                + self.getCode() + "instead."

        for recipient in self.getRecipients():

            uid = recipient
            if not isinstance(recipient, str):
                # Handles exception case if this were a node instead of a UID.
                uid = recipient.getUid()

            if uid in connections.universe:
                node = connections.universe[uid]
                if not node.hasTCPConnection():
                    raise "No connection to " + node.getUid()
                else:
                    # Ok, stop messing around and send the message!
                    tcpConn = node.getTCPConnection().dispatchMessage(self)
            else:
                raise "recipient " + uid + " not found."

    def getCode(self):
        """
        Generic messages have a "?" code.
        """
        return self._code

    def compress(self):
        """
        Compress down a message for sending across the network.
        """
        del self._recipients[:]

    def __str__(self):
        """
        Get a string representation of the message
        """
        return self.getSerialized()

class VectorMessage(GenericMessage):
    """
    A message where the payload is specifically a vector clock dictionary
    (just a dictionary, not the wrapper class)
    """

    def __init__(self, vClock, sender=None, recipients=None):
        """
        Constructor
        """
        if type(vClock) is vectorClock.VectorClock:
            super(VectorMessage, self).__init__(
                vClock.getClocks(), sender, recipients)

            self._clockKey = vClock.getKey()

        else:
            super(VectorMessage, self).__init__(
                vClock, sender, recipients)

            self._clockKey = sender.getUid()

        self._code = "V"
        
    def getVectorClock(self):
        """
        Get a VectorClock object from this message.
        """
        return vectorClock.VectorClock(self._clockKey, self.getPayload())

    def respond(self):
        """
        How the systemm should respon to receiving this vector clock message.
        """
        connections.getMe().getVectorClock().receiveMessage(self)

    @staticmethod
    def createVectorClockMessage():
        me = connections.getMe()
        if me:
            return me.getVectorClock().createMessage()
        else:
            debug("me is null?")

    @staticmethod
    def isVectorMessage(msg):
        """
        Return whether the given message is a VectorMessage
        """
        return msg.getCode() == "V"

class NetworkStatusMessage(GenericMessage):
    """
    Network maintenance message. Contains information about dead nodes, 
    new nodes or whatever. This should be treated as an abstract class 
    and not implemented directly.
    """

    def __init__(self, updates, sender=None, recipients=None):
        """
        Constructor.
        """
        super(NetworkStatusMessage, self).__init__(updates, sender, recipients)
        self._code = 'S'

    def respond(self):
        """
        Don't do anything here. Let subclasses decide
        """
        pass

    @staticmethod
    def isNetworkStatusMessage(msg):
        """
        Parent for any message.
        """
        return msg.getCode() in ['S', 'A', 'D', 'G', 'AG', 'M']


class IsAliveMessage(NetworkStatusMessage):
    """
    Message to tell if another node is alive
    """

    def __init__(self, sender=None, recipients=None):
        super(IsAliveMessage, self).__init__("", sender, recipients)
        self._code = 'A'

    def respond(self):
        """
        Response to IsAliveMessage
        """
        debug('respnding to an isalive message with a memessage')
        responseMsg = MeMessage(
            connections.getMe().getUid(), 
            [self._sender.getUid()])
        responseMsg.send()

    @staticmethod
    def isIsAliveMessage(msg):
        return msg.getCode() == 'A'


class MeMessage(NetworkStatusMessage):
    """
    Message containing node information
    """
    def __init__(self, sender=None, recipients=None):
        """
        Constructor. Set the payload to be the node data of the current node.
        """
        super(MeMessage, self).__init__("", sender, recipients)
        self._code = 'M'
        self._payload = (connections.getMe()).getSerialized()

    def respond(self):
        """
        Insert the received node into this table.
        """
        try:
            nodeData = node.buildNode(self._payload)
            if nodeData.getUid() not in connections.universe:
                connections.universe[nodeData.getUid()] = nodes.ExternalNode(
                    nodeData.getIp(), 
                    config.DEFAULT_SEND_PORT, 
                    nodeData.getUid())
            connections.universe[nodeData.getUid()].knownAlive = True
            debug('reponded to a MeMessage')
        except:
            debug('failed to respond to MeMessage')

    @staticmethod
    def isMeMessage(msg):
        """
        If this message contains a payload of a single node data.
        """
        return msg.getCode() == 'M'


class GossipNetworkStatusMessage(NetworkStatusMessage):
    """
    Network maintenance message that should be gossiped around.
    """

    def __init__(self, updates, sender=None, recipients=None):
        """
        Constructor
        """
        super(GossipNetworkStatusMessage, self).__init__(
            updates, sender, recipients)

        self._gossipttl = config.GOSSIPTTL
        self._code = 'G'

    def decrementTtl(self):
        self._gossipttl -= 1

    def getTtl(self):
        return self._gossipttl

    def respond(self):
        """
        Defines how to respond when one of these messages is recieved
        No defined behavior in parent class yet.
        """
        try:
            self.decrementTtl()
            if self.getTtl() > 0:
                self._sender = connections.getMe().getBaseData()
                self._recipients = []
                # retain the same payload.
                gossip.gossipThis(self)
        except:
            debug("failed to respond to gossip network status message")

    @staticmethod
    def isGossipNetworkStatusMessage(msg):
        """
        Return if this is any type of GossipNetworkStatusMessage
        """
        return msg.getCode() in ['G', 'D', 'N']


class DeadNodeMessage(GossipNetworkStatusMessage):
    """
    Dead node message.
    Remove from connection collection and gossip.
    Payload: a uid
    """

    def __init__(self, uid, sender=None, recipients=None):
        """
        Constructor
        """
        super(DeadNodeMessage, self).__init__(uid, sender, recipients)
        self._code = "D"

    def respond(self):
        """
        Respond to a dead node.
        """
        try:
            uid = self.getPayload()
            if uid in connections.universe:
                connections.removeNode(uid)
                super.respond()
            else:
                pass #don't gossip if we've already gossipped this.
            debug("Responded to dead node message.", success=True)
        except:
            debug("failed to respond to dead node message", error=True)

    @staticmethod
    def isDeadNodeMessage(msg):
        """
        Return if this message is a dead node message
        """
        return msg.getCode() == 'D'
        

class NewNodeMessage(GossipNetworkStatusMessage):
    """
    New node message. A node has entered the system.
    """

    def __init__(self, node, sender=None, recipients=None):
        """
        Constructor
        """
        super(NewNodeMessage, self).__init__(node, sender, recipients)
        self._code = "N"

    def respond(self):
        """
        How to respond to a new node message.
        """
        try:
            (uid, ip) = self.getPayload()
            if uid not in connections.universe: 
                connections.createNode(uid, ip, connections.DEFAULT_SEND_PORT)
                super.respond()
            else:
                pass # don't need to gossip if we've already gossipped this.
            debug("Successfully responded to new node message", success=True)
        except:
            debug("Failed to respond to new node message", error=True)

    @staticmethod
    def isNewNodeMessage(msg):
        """
        Return if this message is a NewNodeMessage
        """
        return msg.getCode() == 'N'


class AggregateMessage(GossipNetworkStatusMessage):
    """
    Message that contains aggregation statistics.
    """

    def __init__(self, aggstat, sender=None, recipients=None):
        """
        Constructor. Takes a statistic name to track.
        """
        super(AggregateMessage, self).__init__(aggstat, sender, recipients)
        self._code = "AG"

    def respond(self):
        """
        Respond to an AggregateMessage
        """
        try:
            aggstat = self.getPayload()
            aggregation.STATISTICS[aggstat.getName()].reduce(aggstat)
            debug("Responded to AggregateMessage", success=True)
        except:
            debug("Did not respond to aggregation message.", error=True)

    @staticmethod
    def createAggregateMessage(agg):
        """
        Build an aggregate message for the aggregation in the param.
        """
        return AggregateMessage(agg, connections.getMe().getUid())

    @staticmethod
    def isAggregateMessage(msg):
        """
        Static method to tell whether the provided 
        message is an AggregateMessage
        """
        return msg.getCode() == "AG"



### Logging Messages #########################################################
class LogMessage(GenericMessage):
    """
    Message representing information that the application might wish to log.
    """

    def __init__(self, payload, level=None):
        """
        Constructor
        """
        super(LogMessage, self).__init__(payload)
        self._level = level

    def setLevel(self, level):
        """
        Set the level of this message
        """
        self._level = level

    def getLevel(self):
        """
        Get the level of this messsage
        """
        return self._level

    def getCode(self):
        """
        Get the code for a logging message (L)
        """
        return 'L'

    def respond(self):
        pass

    @staticmethod
    def isLogMessage(msg):
        """
        Return whether a given message is any type of LogMessage
        """
        return msg.getCode() in ['L', 'IL', 'EL']

class InternalLogMessage(LogMessage):
    """
    Interanl Log Message
    """

    def __init__(self, payload, level=None):
        """
        Constructor
        """
        super(InternalLogMessage, self).__init__(payload, level)

    def getCode(self):
        """
        Internal log message code
        """
        return 'IL'

    def respond(self):
        pass

    @staticmethod
    def isInternalLogMessage(msg):
        """
        Return whether a message is an internal logging message.
        """
        return msg.getCode() == 'IL'

class ExternalLogMessage(LogMessage):
    """
    External Log Message
    """
    def __init__(self, payload, level=-1, logType='Default'):
        """
        Constructor
        """
        super(ExternalLogMessage, self).__init__(payload, level)
        self._type = logType

    def getCode(self):
        """
        External log message code
        """
        return 'EL'

    def respond(self):
        pass

    @staticmethod
    def isExternalLogMessage(msg):
        """
        Return whether a message is an external logging message.
        """
        return msg.getCode() == 'EL'


### Message Functions ########################################################
def buildMessage(serializedMessage):
    """
    build a message from a serialized code.
    """
    return cPickle.loads(serializedMessage)