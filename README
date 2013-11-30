# Configuration #
calculatorRobot.py supports interactive login, command line arguments, or use as a imported class. Note: if not all the required command-line options are specified they will be retrieved by the interactive login.

## Interactive Login ##
    
Usage: calculatorRobot.py
    Username: 
    Password: 
    Server: 
    Port (default: 5222): 

## Command-Line Options ##
Usage: calculatorRobot.py [options]

    Options:
        -h, --help            show this help message and exit
        -q, --quiet           set logging to ERROR
        -d, --debug           set logging to DEBUG
        -v, --verbose         set logging to COMM
        -j JID, --jid=JID     JID to use
        -p PASSWORD, --password=PASSWORD
                            password to use
        -s SERVER, --server=SERVER
                            server to use
        -P PORT, --port=PORT  port to use (default 5222)

## Class ##
Use the help() function for more information.
Example:

    #!/usr/bin/python
    from jabberBot import CalculatorBot
    CalculatorBot('user@test.com', 'mypassword', 'test.com', 5222).startConnection()



# Testing #
Comprehensive function testing of the math is provided in unitTesting.py.

# Dependencies #
This software is designed to be cross platform, and therefore requires only the following two dependencies:
+ python (tested on 2.7)
+ sleekxmpp 1.0 [sleekxmpp.com] (included in the stand alone package)

# Design Notes #
mathParse.py is a library designed to create a safe eval() function for this project.

