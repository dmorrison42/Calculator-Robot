# Configuration #
calculatorRobot.py supports interactive login, command line arguments, or use as a imported class. Note: if not all the required command-line options are specified they will be retrieved by the interactive login. 

Note: Running python programs is a system specific task, but can generally be accomplished by running python [filename]

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
        -U PORT, --port=PORT  port to use (default 5222)

## Class ##
Use the help() function for more information.
Example:

    #!/usr/bin/python
    from jabberBot import CalculatorBot
    CalculatorBot('user@test.com', 'mypassword', 'test.com', 5222).startConnection()

# Testing #
Comprehensive function testing of the math parser is provided in unitTesting.py.

    Usage: unitTesting.py 

    Response: 
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in [number]s

    OK


# Manual Testing Client #
Note non specified arguments will be requested via the interactive login

    Usage: clientRobot.py [options]

    Options:
      -h, --help            show this help message and exit
      -q, --quiet           set logging to ERROR
      -d, --debug           set logging to DEBUG
      -v, --verbose         set logging to COMM
      -j CLIENT_JID, --client-jid=CLIENT_JID
                            JID to use for client
      -p CLIENT_PASSWORD, --client-password=CLIENT_PASSWORD
                            password to use for client
      -s CLIENT_SERVER, --client-server=CLIENT_SERVER
                            server to use for client
      -u CLIENT_PORT, --client-port=CLIENT_PORT
                            port to use for client (default 5222)
      -t CLIENT_TARGET, --client-target=CLIENT_TARGET
                            target for client
      -J ROBOT_JID, --robot-jid=ROBOT_JID
                            JID to use for robot
      -P ROBOT_PASSWORD, --robot-password=ROBOT_PASSWORD
                            password to use for robot
      -S ROBOT_SERVER, --robot-server=ROBOT_SERVER
                            server to use for robot
      -U ROBOT_PORT, --robot-port=ROBOT_PORT
                            port to use for robot (default 5222)

# Dependencies #
This software is designed to be cross platform, and therefore requires only the following two dependencies:

+ [python](http://python.org/) (tested with python 2.7.5 and 3.3.3 on Windows, OSX, and Linux)
+ [sleekxmpp 1.0](http://sleekxmpp.com) (included in the stand alone package)
+ [xmpp](http://xmpp.org/) (tested with Google Talk and FaceBook)

# Design Notes #
mathParse.py is a library designed to create a safe eval() function for this project.
