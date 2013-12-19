#!/usr/bin/python
# mathParser.py
import re

class MathParser:
    '''
    A safe eval() function for basic mathematical calculations
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

        try:
            # Handle Assignment
            if '=' in expr:
                # Remove spaces
                expr = re.sub('\s','',expr)
                # Divide into expression and assignment
                terms = expr.split('=',1)
                if '=' in terms:
                    raise SyntaxError('One assignment per message')
                if not terms[0].isalpha():
                    raise SyntaxError('Alphanumeric variable names only')
                queue = self.infix_to_postfix(terms[1])
                response = self.process_queue(queue, usr)
                #Ensure variable gets saved in namespace
                try:
                    self.variables[usr][terms[0]] = response
                except:
                    self.variables[usr] = {}
                    self.variables[usr][terms[0]] = response
                return terms[0] + ' is set to ' + ('%f' % response).rstrip('0').rstrip('.')

            # Queue and return expression
            queue = self.infix_to_postfix(expr)
            return ('%f' % self.process_queue(queue, usr)).rstrip('0').rstrip('.')

        # Graceful Error Handling
        except SyntaxError as e: return 'Syntax Error: ' + str(e)
        except KeyError as e: 
            error = str(e)[1:-1]
            if len(error) == 1 and not error.isalpha():
                return 'Unknown Symbol: ' + str(e)
            return 'Unknown Variable: ' + str(e)

        except OverflowError: return 'Overflow: Number too large'
        except ZeroDivisionError: return 'Cannot divide by zero'
        except Exception as e: return 'Unknown Error: ' + str(e)

    # Shunting Yard Algorithm
    def infix_to_postfix(self, expr):
        '''
        Converts an infix expression to a postfix queue

        Arguments:
            expr -- String: The mathematical function to be queued
        '''
        stack = []
        queue = []

        # Alter string to list of tokens
        expr = list(re.findall('((?<=[\w\d\.])[-\+]|[-\+]*[\w\d\.]+|\S)', expr))
        # Pops items off the list till completed
        while expr:
            token = expr.pop(0)
            # If token is float append it to queue
            try:
                token = Operator(token)
                # If there is an operator at the top of the stack
                # If the operator is less than o2
                while stack and stack[-1] is not '(' and token <= stack[-1]:
                    queue.append(stack.pop())
                    continue
                stack.append(token)
            except ValueError:
                # Parentheses
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
                # Variables and Floats
                queue.append(token)
        while stack:
            queue.append(stack.pop())
            if queue[-1] is '(':
                raise SyntaxError('Unmatched Parentheses')
        return queue

    # Process the queue
    def process_queue(self, queue, usr='default'):
        '''
        Process a postfix queue and return a float result

        Arguments:
            queue -- A stack of numbers, variables, and operators
            usr -- The variable namespace
        '''
        stack = []
        while queue:
            # Get next element in queue
            token = queue.pop(0)
            # If it is a variable, process it
            if isinstance(token, Operator):
                try: stack.append(token(stack.pop(-2),stack.pop()))
                except IndexError: raise SyntaxError('At ' + str(token))
            else:
                try: token = float(token)
                except ValueError:
                    try: token = self.variables[usr][token]
                    except KeyError: raise KeyError(str(token))
                stack.append(token)

        #Ensure Variable Saving
        try:
            self.variables[usr]['ans'] = stack[0]
        except:
            self.variables[usr] = {}
            self.variables[usr]['ans'] = stack[0]
        if len(stack) is not 1:
            raise SyntaxError('Missing operator')
        return stack[0]

class Operator:
    '''
    Makes an operator object for supported operators

    To add supported operators see __init__
    '''

    operators = {
        '^': {'function': (lambda x, y: x ** y), 'precedence': 4,
                    'associativity': 'right'},
        '*': {'function': (lambda x, y: x * y), 'precedence': 3},
        '/': {'function': (lambda x, y: x / y), 'precedence': 3},
        '+': {'function': (lambda x, y: x + y), 'precedence': 2},
        '-': {'function': (lambda x, y: x - y), 'precedence': 2}
    }

    def __init__(self, operator):
        '''
        Creates an operator object for supported operators

        Arguments:
            operator -- char one of the predefined operators
            operator -- a dictionary containing keys for char function and precedence
                                    {'char':'%', 'function':(lambda x, y: x % y), 'precedence': 3}
        '''
        try:
            self.operator = self.operators[operator]
            self.operator['char'] = operator
        except KeyError:
            raise ValueError('No such operator: ' + str(operator))
        except TypeError:
            self.operators[operator.pop('char')] = operator
            self.operator = operator

    def __cmp__(self,other):
        try:
            if self.operator['associativity'] == 'right':
                return self.operator['precedence'] - other.operator['precedence'] + 1
        except KeyError:
            return self.operator['precedence'] - other.operator['precedence']

    def __str__(self):
        return self.operator['char']

    def __call__(self, x, y):
        return self.operator['function'](x,y)

    def __repr__(self):
        return str(self)
