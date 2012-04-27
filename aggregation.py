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
# Aggregation.py                                                             #
#----------------------------------------------------------------------------#

### Imports ##################################################################
# Python Library imports
import time
import copy

# External library imports
import psutil
import zope.interface

# Local imports
import me
import logger
import stats

### Interfaces ###############################################################
class IAggregator(zope.interface.Interface):
    """
    IAggregation
    """

    def reduce(other):
        """
        Reduce from another object value.
        """

    def getValue():
        """
        Get the value of this aggregator
        """

    def getLocalValue():
        """
        Get the local value of the stat at this node.
        """

    def getStatistic():
        """
        Get this as a dictionary.
        """

class INamedAggregator(zope.interface.Interface):
    """
    Interface for aggregators with name.
    """

    def getName():
        """
        Get the name of this aggregator
        """

    def reduce(other):
        """
        Reduce from another object value.
        """

    def getValue():
        """
        get the value of this aggregator
        """

    def getLocalValue():
        """
        Get the local value of this stat at this node.
        """

    def getStatistic():
        """
        Get this as a dictionary.
        """

### Classes ##################################################################
class Aggregator(object):
    """
    ValueAggegation. Do not instanciate
    """

    zope.interface.implements(IAggregator)

    def __init__(self, statistic=None):
        """
        Constructor
        """
        self._key = me.getMe().getUid()
        self._statistic_function = statistic
        if statistic:
            self._value = self._statistic_function()
        else:
            self._value = None

    def getKey(self):
        """
        Return the key of the aggregation. This is usually a node's UID.
        """
        return self._key

    def getValue(self):
        """
        Return the value of the aggregation. 
        This is the value associated with that UID.
        """
        return self._value

    def reduce(self, other):
        """
        Reduce from another object value. 
        For example it might keep a Max by comparing
        successive reduced values.
        """
        pass #retain by default. subclass and override to implement.

    def refresh(self):
        """
        Refresh statistic from the current node to keep it updated.
        """
        tojoin = Aggregator(self.getName(), self._statistic_function)
        self.reduce(tojoin)

    def getLocalValue(self):
        """
        Get the local value of at this node of the given
        statistic.
        """
        return self._statistic_function()

    def getStatistic(self):
        """
        Get this stat as a dictionary.
        """
        toReturn = {}
        toReturn['key'] = self._key
        toReturn['value'] = self._value
        return toReturn

class NamedAggregator(Aggregator):
    """
    An aggregator with a name
    """
    zope.interface.implements(INamedAggregator)

    def __init__(self, name, statistic=None):
        """
        Constructor
        """
        super(NamedAggregator, self).__init__(statistic)
        self._name = name

    def getName(self):
        """
        Get the name
        """
        return self._name

    def getStatistic(self):
        """
        Get as a dictionary
        """
        toReturn = super.getStatistic()
        toReturn['name'] = self._name
        return toReturn


class MinAggregator(NamedAggregator):
    """
    Aggregator that keeps a reference to the minimum
    """

    def __init__(self, name, statistic=None):
        """
        Constructor
        """
        super(MinAggregator, self).__init__(name, statistic)

    def reduce(self, other):
        """
        Reduce to keep a minimum value and its key
        """
        if self.getName() == other.getName():
            if other.getValue() < self.getValue():
                self._value = other.getValue()
                self._key = other.getKey()
            return self.getValue()
        else:
            error = "Cannot reduce different aggregators: (" + self.getName()
            error += ", " + other.getName() + ")"
            raise error

class MaxAggregator(NamedAggregator):
    """
    Aggregator that keeps a reference to the maximum value.
    """

    def __init__(self, name, statistic=None):
        """
        Constructor for MaxAggregator
        """
        super(MaxAggregator, self).__init__(name, statistic)

    def reduce(self, other):
        """
        Combine to keep a maximum value and its key
        """
        if self.getName() == other.getName():
            if other.getValue > self.getValue():
                self._value = other.getValue()
                self._key = other.getKey()
            return self.getValue()
        else:
            error = "Cannot reduce different aggregators: (" + self.getName()
            error += ", " + other.getName() + ")"
            raise error


class MinMaxAggregator(object):
    """
    MinMaxAggregator is a wrapper class for two related values
    so that min and max of the same statistic can be more easily
    tracked.
    """

    zope.interface.implements(INamedAggregator)

    def __init__(self, name, statistic):
        """
        Constructor
        """
        self._max = MaxAggregator(name, statistic)
        self._min = MinAggregator(name, statistic)
        self._name = name
        self._statistic_function = statistic

    def getName(self):
        """
        Get the name of the statistic that MinMaxAggregator holds.
        """
        return self._name

    def getMaxAggregator(self):
        """
        Getter for the max
        """
        return self._max

    def getMinAggregator(self):
        """
        Getter for the min
        """
        return self._min

    def reduce(self, other):
        """
        Combine the two.
        """
        assert other.__class__.__name__ == "MinMaxAggregator"
        self._max.reduce(other.getMaxAggregator())
        self._min.reduce(other.getMinAggregator())

    def refresh(self):
        """
        Refresh from local node.
        """
        self._max.refresh()
        self._min.refresh()

    def getValue(self):
        """
        Get the value of this aggregator (do nothing).
        """
        return None

    def getStatistic(self):
        toReturn = {}
        toReturn['min'] = self.getMinAggregator().getStatistic()
        toReturn['min'] = self.getMaxAggregator().getStatistic()
        return toReturn

    def localValue(self):
        """
        Return the statistic local to this node.
        """
        return self._statistic_function()


class UpdateAggregator(NamedAggregator):
    """
    Update a value based on vector clock
    """

    def __init__(self, name, statistic, vectorClock=None):
        """
        Constructor
        """
        super(UpdateAggregator, self).__init__(name, statistic)
        if vectorClock:
            self._vectorClock = copy.deepcopy(vectorClock)
        else:
            self._vectorClock = copy.deepcopy(
                me.getMe().getVectorClock())


    def getVectorClock(self):
        """
        Get the vector clock
        """Looping
        return self._vectorClock

    def setVectorClock(self, vectorClock):
        """
        Set the vector clock
        """
        self._vectorClock = copy.deepcopy(vectorClock)

    def reduce(self, other):
        """
        Only merge in value if other came later.
        """
        if self.getVectorClock().cameBefore(other.getVectorClock()):
            self._key = other.getKey()
            self._value = other.getValue()
            self.getVectorClock().mergeClocks(other)
        else:
            pass #irrelevant.

    def refresh(self):
        """
        Refresh value from the statistic function.
        (only if the current vector clock is late)
        """
        if me.getMe().getVectorClock().cameAfter(
            self.getVectorClock()):
            self._key = me.getMe().getUid()
            self._value = self._statistic_function()
        else:
            pass # not relevant


### Globals ##################################################################

STATISTICS = {}
"""
These are stats we would like to be accessible in the system
"""

### Functions ################################################################

def stats_init():
    global STATISTICS

    DISK_AVAILABLE = MinMaxAggregator(
        'diskavailable', stats.disk_free)

    NETWORK_LOAD = MinMaxAggregator(
        'networkload', stats.network_load_single_stat)

    DISK_LOAD = MinMaxAggregator(
        'diskload', stats.disk_load_single_stat)

    CPU_LOAD = MinMaxAggregator(
        'cpuload', stats.cpu_utilization)

    CPU_COUNT = MinMaxAggregator(
        'cpucount', stats.cpu_count)

    PMEM_AVAILABLE = MinMaxAggregator(
        'pmemavailable', stats.physical_mem_free)

    NODE_COUNT = UpdateAggregator(
        'nodecount', stats.timber_node_count)

    LOG_COUNT = UpdateAggregator(
        'logcount', logger.logCount)

    STATISTICS = {
        'diskavailable': DISK_AVAILABLE, 
        'networkload': NETWORK_LOAD, 
        'diskload': DISK_LOAD,
        'cpuload': CPU_LOAD,
        'cpucount': CPU_COUNT,
        'pmemavailable': PMEM_AVAILABLE, 
        'nodecount': NODE_COUNT, 
        'logcount':LOG_COUNT
        }

def getAggregation(name, local=False, minOnly=False, maxOnly=False):
    """
    Get aggregation.
    """
    toReturn = STATISTICS[name].getStatistic()
    if local:
        return STATISTICS[name].getLocalValue()
    elif minOnly and "min" in toReturn:
        return toReturn["min"]
    elif maxOnly and "max" in toReturn:
        return toReturn["max"]
    else:
        return toReturn

def refreshAll():
    """
    Refresh all the statistics.
    """
    for name in STATISTICS:
        STATISTICS[name].refresh()