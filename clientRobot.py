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
from calculatorRobot import CalculatorBot

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
  reload(sys)
  sys.setdefaultencoding('utf8')
else:
  raw_input = input

class ClientBot(sleekxmpp.ClientXMPP):

  '''
  A simple SleekXMPP bot communicates with a calculator robot
  '''

  def __init__(self, jid, password, target, server, port = 5222):
    '''
    Initiates the class 
    
    Arguments:
      jid -- String: The of the jid of the robot
      password -- String: The password of the robot
      target -- String: The jid of the robot to communicate with
      server -- String: The server of the robot (eg talk.google.com)
      port -- Integer: The port of the robot (default 5222)
    '''
    self.clientServer = server
    self.port = port
    self.target = target

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
    print('Type exit to exit')
    print('Request: hello')
    self.send_presence()
    self.get_roster()
    self.sendMessage(self.target, 'hello')

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
      print('Response: ' + msg['body'])
      request = raw_input('Request: ')
      #Avoid invalid response
      while request is '':
        request = raw_input('Request: ')
      if request == 'exit':
        print('Attempt to exit.')
        self.disconnect()
      msg.reply(request).send()

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

  # Login options client
  optp.add_option('-j', '--client-jid', dest='client_jid',
                  help='JID to use for client')
  optp.add_option('-p', '--client-password', dest='client_password',
                  help='password to use for client')
  optp.add_option('-s', '--client-server', dest='client_server',
                  help='server to use for client')
  optp.add_option('-u', '--client-port', dest='client_port',
                  help='port to use for client (default 5222)')
  optp.add_option('-t', '--client-target', dest='client_target',
                  help='target for client',)

  # Login options robot
  optp.add_option('-J', '--robot-jid', dest='robot_jid',
                  help='JID to use for robot')
  optp.add_option('-P', '--robot-password', dest='robot_password',
                  help='password to use for robot')
  optp.add_option('-S', '--robot-server', dest='robot_server',
                  help='server to use for robot')
  optp.add_option('-U', '--robot-port', dest='robot_port',
                  help='port to use for robot (default 5222)')

  opts, args = optp.parse_args()
  
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')

  # Client Live Login
  if opts.client_jid is None:
      opts.client_jid = raw_input('Client Username: ')
  if opts.client_password is None:
      opts.cleint_password = getpass.getpass('Client Password: ')
  #Only request port if server is not specified
  if opts.client_server is None:
    opts.client_server = raw_input('Client Server: ')
    opts.client_port = raw_input('Client Port (default: 5222): ')
  if not opts.client_port:
    opts.client_port = 5222
  if opts.client_target is None:
    opts.client_target = raw_input('Client Target: (default robot username)')


  # Server Live Login
  if opts.robot_jid is None:
      opts.robot_jid = raw_input('Robot Username: ')
  if opts.robot_password is None:
      opts.robot_password = getpass.getpass('Robot Password: ')
  #Only request port if server is not specified
  if opts.robot_server is None:
    opts.robot_server = raw_input('Robot Server: ')
    opts.robot_port = raw_input('Robot Port (default: 5222): ')
  if not opts.robot_port:
    opts.robot_port = 5222
  
  #Default Target
  if opts.client_target is '':
    opts.client_target = opts.robot_jid

  # Create Object
  calculator = CalculatorBot(opts.robot_jid, opts.robot_password, opts.robot_server, opts.robot_port).startConnection(blocking=False)
  client = ClientBot(opts.client_jid, opts.client_password, opts.client_target, opts.client_server, opts.client_port).startConnection(blocking=True)
  calculator.disconnect()
