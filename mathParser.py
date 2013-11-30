#!/usr/bin/python
# mathParser.py
import re

class MathParser:
  '''
  A safe eval() function for basic mathmatical calculations
  '''
  # dictionary containing variables in the following format variables[jid][variable]
  variables = {}
  
  # Evaluate
  def eval(self, expr, usr='default'):
    '''
    Evaluates a mathematical expression and returns a string.

    Arguments:
      expr -- String: The expression to be evaluated
      usr -- The namespace in which the variables are stored
    '''
    # Remove spaces before begining
    expr = expr.replace(' ','')

    try:
      if '=' in expr:
        # Handle Assignment
        terms = expr.split('=',1)
        if '=' in terms:
          raise SyntaxError('One assignment per message')
        if not terms[0].isalpha():
          raise SyntaxError('Alphanumeric variable names only')
        queue = self.infix_to_prefix(terms[1])
        response = self.process_queue(queue, usr)

        try:
          self.variables[usr][terms[0]] = response
        except:
          self.variables[usr] = {}
          self.variables[usr][terms[0]] = response
        return terms[0] + ' is set to ' + ('%f' % response).rstrip('0').rstrip('.')
      
      # Queue and return expression
      queue = self.infix_to_prefix(expr)
      return ('%f' % self.process_queue(queue, usr)).rstrip('0').rstrip('.')
    
    # Graceful Error Handeling
    except SyntaxError as e: return 'Syntax Error: ' + str(e)
    except KeyError as e: return 'Unknown Variable: ' + str(e)
    except OverflowError: return 'Overflow: Number too large'
    except Exception as e: return 'Unknown Error: ' + str(e)

  # Shunting Yard Algorithm
  def infix_to_prefix(self, expr):
    '''
    Converts an infix expression to a postfix queue

    Arguments:
      expr -- String: The mathematical function to be queued
    '''
    stack = []
    queue = []
    
    # Remove spaces before begining
    expr = expr.replace(' ','')
    # Alter string to list of tokens
    expr = list(re.findall('(^[-\+][\w\d\.]+|(?<![\(\)\^\*/\+-])[-\+]|[-\+]*[\w\d\.]+|[\(\)\^\*/\+]|.)', expr))
    
    # Pops items off the list till completed
    while expr:
      token = expr.pop(0)
      # If token is float append it to queue
      try:
        token = Operator(token)
        #Handle special ^ case
        if stack and str(token) is '^' and str(stack[-1]) is '^':
          stack.append(token)
          continue
        # If there is an operator at the top of the stack
        # If the operator is less than o2
        while stack and stack[-1] is not '(' and token <= stack[-1]:
          queue.append(stack.pop())
          continue
        stack.append(token)
      except ValueError:
        #Parentheses
        if token is '(':
          stack.append(token)
          continue
        if token is ')':
          try:
            token = stack.pop()
            while token is not '(':
              queue.append(token)
              token = stack.pop()
            continue
          except IndexError: raise SyntaxError('Unmatched Parentheses')
        #Variables and Floats   
        queue.append(token)
    while stack:
      queue.append(stack.pop())
      if queue[-1] is '(':
        raise SyntaxError('Unmatched Parentheses')
    return queue

  #Process the queue
  def process_queue(self, queue, usr='default'):
    '''
    Process a postfix queue and return a float result

    Arguments:
      queue -- A stack of numbers, variables, and operators
      usr -- The variable namespace
    '''
    stack = []
    while queue:
      token = queue.pop(0)
      if isinstance(token, Operator):
        try: stack.append(token(stack.pop(-2),stack.pop()))
        except IndexError: raise SyntaxError('At ' + str(token))
      else:
        try: token = float(token)
        except ValueError:
          try: token = self.variables[usr][token]
          except KeyError: raise KeyError(str(token))
        stack.append(token)
    try:
      self.variables[usr]['ans'] = stack[0]
    except:
      self.variables[usr] = {}
      self.variables[usr]['ans'] = stack[0]
    return stack[0]

class Operator:
  '''
  Makes an operator object for supported operators
  '''
  def __init__(self, operator, function, precedence):
    self.operator = operator
    self.function = function
    self.precedence = precedence

  def __init__(self, operator):
    self.operator = operator

    if operator is '^':
      self.function = (lambda x, y: x ** y)
      self.precedence = 4
    elif operator is '*':
      self.function = (lambda x, y: x * y)
      self.precedence = 3
    elif operator is '/':
      self.function = (lambda x, y: x / y)
      self.precedence = 3
    elif operator is '+':
      self.function = (lambda x, y: x + y)
      self.precedence = 2
    elif operator is '-':
      self.function = (lambda x, y: x - y)
      self.precedence = 2
    else:
      raise ValueError('No such operator: ' + str(operator))

  def __cmp__(self,other):
    return self.precedence - other.precedence

  def __str__(self):
    return self.operator

  def __call__(self, x, y):
    return self.function(x,y)

  def __repr__(self):
    return str(self)