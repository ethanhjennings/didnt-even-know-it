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

    def boolean(self):
        if self.numVal % 2 == 0:
            return '0'
        else:
            return '1'

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
             26: '_jump_positive',
             27: '_jump_zero',
             28: '_jump_negative',
             29: '_add',
             30: '_sub',
             31: '_mul',
             32: '_div',
             33: '_mod',
             34: '_and',
             35: '_or',     
             36: '_xor',
             37: '_not',
             38: '_negate',
             }

invertedOpcodeMap = dict([[v,k] for k,v in opCodeMap.items()])

cCodeFunctionMap = {
    '_input_int':
        {1 : lambda p: 'inputInt(' + p[0].reg() + ');'},
    '_input_string': 
        {1 : lambda p: 'inputString(' + p[0].reg() + ');'},
    '_input_char':
        {1 : lambda p: 'inputChar(' +  p[0].reg() + ');'},
    '_output_int':
        {1: lambda p: 'outputIntReg(' + p[0].reg() + ',' + p[0].reg() + '->pos,0);',
         2: lambda p: 'outputIntReg(' + p[0].reg() + ',' + p[0].reg() + '->pos,' + p[1].boolean() + ');'},
    '_output_int_stack':
        {1: lambda p: 'outputIntReg(' + p[0].reg() + ',0,0);', 
         2: lambda p: 'outputIntReg(' + p[0].reg() + ',0,' + p[1].boolean() + ');'},
    '_output_char':
        {1: lambda p: 'outputStringReg(' + p[0].reg() + ',' + p[0].reg() + '->pos,0);',
         2: lambda p: 'outputStringReg(' + p[0].reg() + ',' + p[0].reg() + '->pos,' + p[1].boolean() + ');'},
    '_output_string':
        {1: lambda p: 'outputStringReg(' + p[0].reg() + ',0,0);',
         2: lambda p: ' outputStringReg(' + p[0].reg() + ',0,' + p[1].boolean() + ');'},
    '_load_immediate_int':
        {2: lambda p: 'assignReg(' + p[0].reg() + ',' +  str(p[1].num()) + ');'},
    '_load_immediate_char':
        {2: lambda p: 'assignReg(' + p[0].reg() + ',' +  p[1].word()[0] + ');'},
    '_load_immediate_string':
        {2: lambda p: 'assignReg(' + p[0].reg() + ',' + p[1].string() + ');'},
    '_assign_top':
        {2: lambda p: 'assignReg(' + p[0].reg() + ',peekReg(' + p[1].reg() + '));'},
    '_assign_stack':
        {2: lambda p: 'assignStack(' + p[0].reg() + ',' + p[1].reg() + ');'},
    '_push':
        {2: lambda p: ('pushReg(' + p[0].reg() + ',' + 'peekReg(' + p[1].reg() + '));'),
         3: lambda p: ('pushReg(' + p[0].reg() + ',' + 'peekReg(' + p[1].reg() + ')); assignReg(' + 
                        p[2].reg() + ',' + p[0].reg() + '->pos + 1);')},
    '_pop':
        {1: lambda p: 'popReg(' + p[0].reg() + ');',
         2: lambda p: 'assignReg(' + p[1].reg() + ',peekReg(' + p[0].reg() +')); popReg('+ p[0].reg() + ');',
         3: lambda p: ('assignReg(' + p[1].reg() + ',peekReg(' + p[0].reg() +')); popReg('+ p[0].reg() + ');' + 
            ' assignReg(' + p[2].reg() + ',' + p[0].reg() + '->pos + 1);')},
    '_clear_stack':
        {1: lambda p: 'freeReg(' + p[0].reg() + '); ' + p[0].reg() + ' = createReg(0);'},
    '_get_stack_size':
        {2: lambda p: 'assignReg(' + p[0].reg() + ',' + p[1].reg() + '->pos + 1);'},
    '_jump':
        {1: lambda p: 'goto ' + p[0].label() + ';'},
    '_jump_equal':
        {1: lambda p: ('if (peekReg(' + p[0].reg() + ') == ' +
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_not_equal':
        {3: lambda p: ('if (peekReg(' + p[0].reg() + ') != '
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_less':
        {3: lambda p: ('if (peekReg(' + p[0].reg() + ') < ' +
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_less_or_equal':
        {3: lambda p: ('if (peekReg(' + p[0].reg() + ') <= ' +
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_greater':
        {3: lambda p: ('if (peekReg(' + p[0].reg() + ') > ' +
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_greater_or_equal':
        {3: lambda p: ('if (peekReg(' + p[0].reg() + ') >= ' +
            'peekReg(' + p[1].reg() + ')) goto ' + p[2].label() + ';')},
    '_jump_stack_equal':
        {3: lambda p: ('if (stackEqual(' + p[0].reg() + ',' + p[1].reg() + '))' + 
            ' goto ' + p[2].label() + ';')},
    '_jump_stack_not_equal':
        {3: lambda p: ('if (!stackEqual(' + p[0].reg() + ',' + p[1].reg() + '))' +
            ' goto ' + p[2].label() + ';')},
    '_jump_zero':
        {2: lambda p: ('if(peekReg(' + p[0].reg() + ') == 0) ' +
            'goto ' + p[1].label() + ';')},
    '_jump_positive':
        {2: lambda p: ('if(peekReg(' + p[0].reg() + ') > 0) ' +
            'goto ' + p[1].label() + ';')},
    '_jump_negative':
        {2: lambda p: ('if(peekReg(' + p[0].reg() + ') < 0) ' +
            'goto ' + p[1].label() + ';')}
    }

def translateInstruction(opcode, parameters, line, lineNum):
    
    if opcode not in opCodeMap:
        raise TranslatorSyntaxError(lineNum, "Opcode '" + str(opcode) + "' is not known.\nFull line:\n" +line.data.strip())

    operation = opCodeMap[opcode]

    overloadedOperatorDict = cCodeFunctionMap[operation]

    if len(parameters) not in overloadedOperatorDict:
        raise TranslatorSyntaxError(lineNum, "for operation " + operation + " (" + "opcode " + str(opcode) + ") - given " + str(len(parameters)) + " parameters but expected " + str(overloadedOperatorDict.keys()) + "\nFull line:\n" + line.data.strip())

    return overloadedOperatorDict[len(parameters)](parameters)

def isInstruction(ins):
    return ins in invertedOpcodeMap

# returns None if command is not known
def getOpcodeFromIns(ins):
    return invertedOpcodeMap[ins]
