#!/usr/bin/env python

'''
Created on Aug 24, 2013

@author: Ethan
'''

from translator.exceptions import TranslatorSyntaxError

class Parameter:
    def __init__(self, numVal, regVal, labelVal, registerCallback):
        self.numVal = numVal
        self.regVal = regVal
        self.labelVal = labelVal
        self.registerCallback = registerCallback

    def reg(self):
        self.registerCallback(self.numVal, self.regVal)
        return self.regVal

    def num(self):
        return self.numVal

    def label(self):
        return self.labelVal

opCodeMap = {0: 'add',
             1: 'load_immediate',
             2: 'unconditional_jump',
             3: 'input_num',
             4: 'output_num',
             5: 'output_newline',
             6: 'jump_equal',
             7: 'jump_not_equal',
             8: 'jump_less',
             9: 'jump_less_or_equal',
             10: 'jump_greater',
             11: 'jump_greator_or_equal',
             }

cCodeFunctionMap = {'add':
                        lambda p: p[0].reg() + " += " + p[1].reg() + ";",
                    'load_immediate': 
                        lambda p: p[0].reg() + " = " + str(p[1].num()) + ";",
                    'unconditional_jump':
                        lambda p: "goto " + p[0].label() + ";",
                    'input_num':
                        lambda p: 'scanf("%d",&' + p[0].reg() + ');',
                    'output_num':
                        lambda p: 'printf("%d",' + p[0].reg() + ');',
                    'output_newline':
                        lambda p: 'printf("\\n");',
                    'jump_equal':
                        lambda p: 'if (' + p[0].reg() + ' == ' + p[1].reg() + ')'
                            ' goto ' + p[2].label() + ";",
                    'jump_less':
                        lambda p: 'if (' + p[0].reg() + ' < ' + p[1].reg() + ')'
                            ' goto ' + p[2].label() + ";",
                   }

numArgumentsMap = {'add': 2,
                   'load_immediate': 2,
                   'unconditional_jump': 1,
                   'input_num': 1,
                   'output_num': 1,
                   'output_newline': 0,
                   'jump_equal': 3,
                   'jump_less': 3,
                   }


def translateInstruction(opcode, parameters, lineNum):

    if not opcode in opCodeMap:
        raise TranslatorSyntaxError(lineNum, "Opcode '" + str(opcode) + "' is not known.")

    operation = opCodeMap[opcode]

    if not numArgumentsMap[operation] == len(parameters):
        raise TranslatorSyntaxError(lineNum, "for operation " + operation + " (" + "opcode " + str(opcode) + ") - given " + str(len(parameters)) + " parameters but expected " + str(numArgumentsMap[operation]))

    return cCodeFunctionMap[operation](parameters)
