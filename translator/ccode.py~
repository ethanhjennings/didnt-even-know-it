'''
Created on Aug 24, 2013

@author: Ethan
'''

from instructions import Instruction

cCodeFunctionMap = { 'addreg' : lambda(p): return p[1].reg + " = " + p[1].reg + " + " + p[2].reg + ";", 
                     'addnum' : lambda(p): return p[1].reg + " += " + p[1].num + ";"
}

class CCodeTranslator
    def translateInstruction(instruction):
        return cCodeFunctionMap[instruction.getOpcodeName()]
    
    def translateLabel(label):
        return label + ":"
    
    

