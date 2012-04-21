# Timber & Hiss

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
    - networkx (for visualization)

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