'''
Created on Aug 30, 2013

@author: Ethan
'''


class TranslatorSyntaxError(Exception):
    message = ""
    line = -1

    def __init__(self, line, message):
        self.message = message
        self.line = line

    def __str__(self):
        return "Syntax Error on line " + str(self.line) + ": " + self.message
