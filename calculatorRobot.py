#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
  SleekXMPP: The Sleek XMPP Library
  Copyright (C) 2010  Nathanael C. Fritz
  This file is part of SleekXMPP.

  See the file LICENSE for copying permission.
'''

import sys
import sleekxmpp
import logging
from optparse import OptionParser
import getpass
from mathParser import MathParser

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
  reload(sys)
  sys.setdefaultencoding('utf8')
else:
  raw_input = input

class CalculatorBot(sleekxmpp.ClientXMPP):
  mathParser = MathParser()

  '''
  A simple SleekXMPP bot that preforms basic mathematical calculations
  '''

  def __init__(self, jid, password, server, port = 5222):
    '''
    Initiates the class 
    
    Arguments:
      jid -- String: The of the jid of the robot
      password -- String: The password of the robot
      server -- String: The server of the robot (eg talk.google.com)
      port -- Integer: The port of the robot (default 5222)
    '''
    self.clientServer = server
    self.port = port

    # Sends initilization to parent class
    sleekxmpp.ClientXMPP.__init__(self, jid, password)

    # Define Handelers
    self.add_event_handler('session_start', self.start)
    self.add_event_handler('message', self.message)

  def start(self, event):
    '''
    Uses the API to handle presence and roster

    Arguments:
      event -- An empty dictionary. The session_start
           event does not provide any additional
           data.
    '''
    self.send_presence()
    self.get_roster()

  def message(self, msg):
    '''
    Process incoming message stanzas.

    Arguments:
      msg -- The received message stanza. See the documentation
           for stanza objects and the Message stanza to see
           how it may be used.
    '''
    # Check Message Type
    if msg['type'] in ('chat', 'normal'):
      # Check for keywords before parsing
      if msg['body'].upper().strip() == 'HELLO':
        msg.reply('world').send()
      elif msg['body'].upper().strip() == 'AUTHOR':
        msg.reply('Daniel Morrison').send()
      elif msg['body'].upper().strip() == 'HELP':
        help='''\
          # Commands: #
          + Help: Prints this screen
          + Author: Prints the author's name
          + Hello: Prints world
          # Setting Variables: #
          > Variables must be set one at a time using the following syntax 
          > Note: variables are case sensitive
          + Request: foo = 4+4
          + Response: foo is set to 8
          # Answer Variable #
          + Request: 4+4
          + Response: 8
          + Request: ans + 2 
          + Response: 10
          # Math: #
          > Supports the following operators using the PEMDAS order of operations.
          + Parentheses: () 
          + Exponents: ^
          + Multiplication: *
          + Division: /
          + Addition: +
          + Subtraction: -
          '''
        msg.reply(help).send()
      # Handle non keywords expressions
      else:
        msg.reply(self.mathParser.eval(msg['body'], str(msg['from']))).send()


  def startConnection(self, blocking=True):
    # Connect to the XMPP server and start processing XMPP stanzas.
    if self.connect((self.clientServer, self.port)):
      self.use_signals()
      self.process(block=blocking)
    else:
      print('Unable to connect.')
    return self

if __name__ == '__main__':
  optp = OptionParser()
  
  # Output verbosity options.
  optp.add_option('-q', '--quiet', help='set logging to ERROR',
                  action='store_const', dest='loglevel',
                  const=logging.ERROR, default=logging.INFO)
  optp.add_option('-d', '--debug', help='set logging to DEBUG',
                  action='store_const', dest='loglevel',
                  const=logging.DEBUG, default=logging.INFO)
  optp.add_option('-v', '--verbose', help='set logging to COMM',
                  action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

  # Login options
  optp.add_option('-j', '--jid', dest='jid',
                  help='JID to use')
  optp.add_option('-p', '--password', dest='password',
                  help='password to use')
  optp.add_option('-s', '--server', dest='server',
                  help='server to use')
  optp.add_option('-u', '--port', dest='port',
                  help='port to use (default 5222)')

  opts, args = optp.parse_args()
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  if opts.jid is None:
      opts.jid = raw_input('Username: ')
  if opts.password is None:
      opts.password = getpass.getpass('Password: ')
  #Only request port if server is not specified
  if opts.server is None:
    opts.server = raw_input('Server: ')
    opts.port = raw_input('Port (default: 5222): ')
  if not opts.port:
    opts.port = 5222
  
  # Create Object
  xmpp = CalculatorBot(opts.jid, opts.password, opts.server, opts.port).startConnection()

