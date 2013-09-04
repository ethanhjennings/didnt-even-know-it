#!/usr/bin/env python

'''
Created on Aug 24, 2013

@author: Ethan
'''

from translator.exceptions import TranslatorSyntaxError

class Parameter:
    def __init__(self, numVal, regVal, labelVal, stringVal,  wordVal, registerCallback):
        self.numVal = numVal
        self.regVal = regVal
        self.labelVal = labelVal
        self.stringVal = stringVal
        self.wordVal = wordVal
        self.registerCallback = registerCallback

    def reg(self):
        self.registerCallback(self.numVal, self.regVal)
        return self.regVal

    def num(self):
        return self.numVal

    def label(self):
        return self.labelVal

    def word(self):
        return self.wordVal

    def string(self):
        return self.stringVal

opCodeMap = {
             0: '_input_int',
             1: '_input_string',
             2: '_input_char',
             3: '_output_int',
             4: '_output_int_stack',
             5: '_output_char',
             6: '_output_string',
             7: '_load_immediate_int',
             8: '_load_immediate_string',
             9: '_load_immediate_word',
             10: '_load_immediate_char',
             11: '_assign_top',
             12: '_assign_stack',
             13: '_push',
             14: '_pop',
             15: '_clear_stack',
             16: '_get_stack_size',
             17: '_jump',
             18: '_jump_equal',
             19: '_jump_not_equal',
             20: '_jump_less',
             21: '_jump_less_or_equal',
             22: '_jump_greater',
             23: '_jump_greater_or_equal',
             24: '_jump_stack_equal',
             25: '_jump_stack_not_equal',
             26: '_add',
             27: '_sub',
             28: '_mul',
             29: '_div',
             30: '_mod',
             31: '_and',
             32: '_or',            
             33: '_xor',
             34: '_not',
             }

invertedOpcodeMap = dict([[v,k] for k,v in opCodeMap.items()])

cCodeFunctionMap = {'_input_int':
                        lambda p: 'inputInt(' + p[0].reg() + ');',
                    '_input_string':
                        lambda p: 'inputString(' + p[0].reg() + ');',
                    '_input_char':
                        lambda p: 'inputChar(' +  p[0].reg() + ');',
                    '_output_int':
                        lambda p: 'outputIntReg(' + p[0].reg() + ',' + p[0].reg() + '->pos - 1);',
                    '_output_int_stack':
                        lambda p: 'outputIntReg(' + p[0].reg() + ',0);',
                    '_output_char':
                        lambda p: 'outputStringReg(' + p[0].reg() + ',' + p[0].reg() + '->pos - 1);',
                    '_output_string':
                        lambda p: 'outputStringReg(' + p[0].reg() + ',0);',
                    '_load_immediate_int':
                        lambda p: 'assignReg(' + p[0].reg() + ',' +  str(p[1].num()) + ');',
                    '_load_immediate_char':
                        lambda p: 'assignReg(' + p[0].reg() + ',' +  p[1].word()[0] + ');',
                    '_load_immediate_string':
                        lambda p: 'assignReg(' + p[0].reg() + ',' + p[1].string() + ');',
                    }

numArgumentsMap = {
                    '_input_int' : 1,
                    '_input_string' : 1,
                    '_input_char' : 1,
                    '_output_int' : 1,
                    '_output_int_stack' : 1,
                    '_output_char' : 1,
                    '_output_string' : 1,
                    '_load_immediate_int' : 2,
                    '_load_immediate_string' : 2,
                    '_load_immediate_word' : 2,
                    '_load_immediate_char' : 2
                   }


def translateInstruction(opcode, parameters, lineNum):
    
    if opcode not in opCodeMap:
        raise TranslatorSyntaxError(lineNum, "Opcode '" + str(opcode) + "' is not known.")

    operation = opCodeMap[opcode]

    if not numArgumentsMap[operation] == len(parameters):
        raise TranslatorSyntaxError(lineNum, "for operation " + operation + " (" + "opcode " + str(opcode) + ") - given " + str(len(parameters)) + " parameters but expected " + str(numArgumentsMap[operation]))

    return cCodeFunctionMap[operation](parameters)

def isInstruction(ins):
    return ins in invertedOpcodeMap

# returns None if command is not known
def getOpcodeFromIns(ins):
    return invertedOpcodeMap[ins]
