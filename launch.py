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
# launch.py                                                                  #
# Run everything                                                             #
##############################################################################

### Imports ##################################################################
# Python Library Imports
import argparse
import sys
import traceback

# External Library Imports
from twisted.internet import reactor

# Local Imports
import aggregation
import timber
import gossip
import config
import logger
import connections
from debug import debug

### Classes ##################################################################
class Args(object):
    """
    Hold arguments
    """
    pass

### Functions ################################################################
def parse_args():
    """
    Parse command line arguments
    --port
    --logport
    --interval
    --iface
    --version
    """
    arguments = Args()

    parser = argparse.ArgumentParser(
        description="--------------Timber/Hiss Settings --------------------",
        epilog="-------------------------------------------------------")

    parser.add_argument('--port', 
        default=config.DEFAULT_RECEIVE_PORT, 
        type=int,
        help='The port for the gossip system to listen on. \
            (Integer, default: %(default)s)')

    parser.add_argument('--sendport',
        default=config.DEFAULT_SEND_PORT,
        type=int,
        help='the port for the gossip system to send on \
            (Integer, default %(default)s)')

    parser.add_argument('--logport', 
        default=config.DEFAULT_LOG_PORT, 
        type=int,
        help='The port to receive log messages on. \
            (Integer, default: %(default)s)')

    parser.add_argument('--interval', 
        default=config.DEFAULT_GOSSIP_WAIT_SECONDS, 
        type=int,
        help='The interval to send gossip messages. \
            (Integer, default: %(default)s)')

    parser.add_argument('--iface', 
        default='localhost',
        help='The interface to communicate on. \
            (String, default: %(default)s)')

    parser.add_argument('--version', 
        action='version', 
        version=timber.__version__,
        help='Report system version.')

    parser.add_argument('--hissoff', 
        action='store_true',
        help='Flag. When set, will not run Hiss service')

    parser.add_argument('--timberoff', 
        action='store_true',
        help='Flag. When set, will not run Timber service.')

    parser.parse_args(namespace=arguments)
    return arguments

def applyArgs(namespace):
    """
    Apply the arguments to the config file
    """
    config.RECEIVE_PORT = namespace.port
    config.SEND_PORT = namespace.sendport
    config.LOG_PORT = namespace.logport
    config.GOSSIP_WAIT_SECONDS = namespace.interval
    config.INTERFACE = namespace.iface


### Main #####################################################################
def main():
    """
    In seperate method so it can be called from other modules.
    """
    args = parse_args()
    applyArgs(args)

    connections.init()
    aggregation.stats_init()

    if not args.timberoff:
        timber.timberRun()
        logger.loggerInit()

    if not args.hissoff:
        gossip.gossipRun()

    if args.timberoff and args.hissoff:
        debug("Nothing to run")
    else:
        reactor.run()

if __name__ == "__main__":
    main()
