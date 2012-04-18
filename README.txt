##############################################################################
#                                                                            #
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
#    Distributed Aggregation & Logging                                       #
##############################################################################

##############################################################################
#        __  ___                                                             #
#       / / / (_)_________                                                   #
#      / /_/ / / ___/ ___/                                                   #
#     / __  / (__  |__  )                                                    #
#    /_/ /_/_/____/____/        Gossip with Python on twisted                #
#                                                                            #
##############################################################################

Version & What's New
===============================================================================
    - Version 0.0.1
    - Everything.

Dependencies
===============================================================================
### Requried Python Packages:
    - twisted (for network infrastructure)
    - pymongo (for communicating with MongoDB)
    - bson (for communicating with MongoDB)
    - kombu (talking to RabbitMQ)
    - boto (for Amazon Web Services)
    - psutil (for server statistics)

### Potential Python Packages:
    - txAWS (for AWS)
    - txRackspace (for Rackspace)
    - txCumulus (wrapper for txAWS and txRackspace)
    - txLoadBalancer (for load balancing)

Author
===============================================================================
Chet Mancini
    - cam479 at cornell dot edu
    - http://chetmancini.com

Legal
=============================================================================== 
    - License: MIT
    - Warranty: None of any kind

Instructions
===============================================================================
Execute:
    $ python launch.py

    Command line arguments:
    -h                  Print help
    --version           Print version
    --port              Hiss port
    --logport           Timber port
    --interval          Gossip interval (seconds)
    --iface             Interface (default localhost)

Installation
===============================================================================
Put files in directory

Changelog
===============================================================================
Nothing changed yet!