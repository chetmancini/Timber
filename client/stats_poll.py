##############################################################################
#        __  ___                                                             #
#       / / / (_)_________                                                   #
#      / /_/ / / ___/ ___/                                                   #
#     / __  / (__  |__  )                                                    #
#    /_/ /_/_/____/____/        Gossip with Python on Twisted                #
#                                                                            #
##############################################################################


### Imports ##################################################################
import os
import sys
import argparse
import json
import time
import twisted.internet.protocol
import twisted.internet.reactor
import twisted.web.client
import twisted.web.http_headers

### Constants ################################################################
STATISTICS = []

### Arguments ################################################################
 
### Classes ##################################################################
class Args(object):
    """
    Holds arguments
    """
    pass

### Functions ################################################################
def parse_args():
    """
    Parse command line arguments
    """
    arguments = Args()
    parser = argparse.ArgumentParser(
        description="------------Timber/Hiss Settings ----------------",
        epilog="-------------------------------------------------")

    parser.add_argument('--stat',
        default='all',
        type=str.
        help='which statistic to poll')

    parser.add_argument('--infinity', 
        default=True, 
        type=bool, 
        help='Run forever')

    parser.add_argument('--delay',
        default=10,
        type=int,
        help='time between requests')

    parser.add_argument('--host',
        default='127.0.0.1',
        type=str,
        help='host address')

    parser.add_argument('--port',
        default='8080',
        type=int,
        help='host port')

    parser.parse_args(namespace=arguments)
    return arguments

def poll(name, host='127.0.0.1', port=8080):
    """
    Poll for a specific statistic.
    """
    content = { 'stat': name }
    data = json.loads(content)
    agent = twisted.web.client.Agent(reactor)

    d = agent.request(
        'GET',
        'http://' + host + ":" + str(port) + "/stat",
        twisted.web.http_headers.Headers({'User-Agent': ['Twisted Web Client Example'],
                 'Content-Type': ['text/json']}),
        data)

    def cbResponse(ignored):
        print 'Response received'
    d.addCallback(cbResponse)

    def cbShutdown(ignored):
        reactor.stop()
    d.addBoth(cbShutdown)

    twisted.internet.reactor.run()


### Main #####################################################################
if __name__ == "__main__":
    """
    Main
    """
    args = parse_args()

    while True:

        if args.stat == 'all':
            for stat in STATISTICS:
                poll(stat)
        elif args.stat == 'input':
            stat = raw_input(
                "Enter a stat to poll. Choices: " + "|".join(STATISTICS))
            poll(stat)
        else:
            poll(args.stat)


        if not args.infinity:
            break

        time.sleep(args.delay)


