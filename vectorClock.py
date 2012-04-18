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
# vectorClock.py                                                             #
# Implements vector clocks using Lamport's logical clocks                    #
##############################################################################

### Imports ##################################################################

# Local Imports
import config
import connections
import message

### Classes ##################################################################
class VectorClock:
    """
    Basic Vector Clock algorithm implementation for single-threaded web apps.
    """

    def __init__(self, key=None, initialClocks=None, externKeys=None):
        """
        Constructor
        """
        if initialClocks:
            self._clocks = initialClocks
        else:
            self._clocks = {}
            if externKeys:
                for externKey in externKeys:
                    self._clocks[externKey] = 0
        if key:
            self._key = key
        else:
            self._key = connections.getMe().getUid()

        if self._key not in self._clocks:
            self._clocks[self._key] = 0

    def incrementClock(self):
        """
        Increment this node's logical clock.
        """
        self._clocks[self._key] += 1

    def handleEvent(self, message):
        """
        handle an event. Increment this logical clock and return the value.
        """
        self.incrementClock()
        return self._clocks[self._key]

    def createMessage(self):
        """
        Send a message from this machine. returns the message to send.
        """
        self.incrementClock()
        return message.VectorMessage(self._clocks)

    def mergeClock(self, otherclock):
        """
        Merge another clock into this one.
        """
        if otherclock is VectorClock:
            otherclock = otherclock.getClocks()
        for key in otherclock:
            if key in self._clocks:
                self._clocks[key] = max(otherclock[key], self._clocks[key])
            else:
                self._clocks[key] = otherclock[key] 
                #automatically adds new key


    def receiveMessage(self, vectorMessage):
        """
        Receive a message and update this clock.
        """
        assert(vectorMessage is VectorMessage)
        self.incrementClock()
        self.mergeClock(vectorMessage.getPayload())

    def cameBefore(self, otherclock):
        """
        Return if this clock logically came before another.
        """
        oneStrictlySmall = False
        for key in otherclock:
            if self._clocks[key] > otherclock[key]:
                return False
            elif self._clocks[key] < otherclock[key]:
                oneStrictlySmall = True
        return oneStrictlySmall

    def cameAfter(self, otherclock):
        """
        Return if this clock logically came after another.
        """
        oneStrictlyLarger = False
        for key in otherclock:
            if self._clocks[key] < otherclock[key]:
                return False
            elif self._clocks[key] > otherclock[key]:
                oneStrictlyLarger = True
        return oneStrictlyLarger

    def getClocks(self):
        """
        Get the dictionary of clocks. (vector clock)
        """
        return self._clocks

    def getKey(self):
        """
        get the key of this vector clock. I assumed it would be the key of the
        current system, but that might not be the case for merges.
        """
        return self._key

    def sendMesage(self):
        msg = message.VectorMessage(self, connections.getMe(), connections.neighbors)
        msg.send()
