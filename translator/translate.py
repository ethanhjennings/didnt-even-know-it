'''
Created on Sep 1, 2013

@author: Ethan
'''
#!/usr/bin/env python

import re
from collections import namedtuple

from syllables import SyllableCounter
import translator.instructions as instructions


INDENT = "    "
DBL_INDENT = "        "

# split apart poem into stanzas
def _splitIntoStanzas(lines):
    LineTuple = namedtuple('LineTuple', 'data, num')
    
    stanzas = list()
    currentStanza = list()
    wasLastLineEmpty = True
    
    for lineNum, lineData in enumerate(lines):
        if len(lineData.strip()) == 0:
            wasLastLineEmpty = True
            if len(currentStanza) > 0:
                stanzas.append(currentStanza)
                currentStanza = list()
        else:
            if wasLastLineEmpty:
                wasLastLineEmpty = False
            currentStanza.append(LineTuple(lineData, lineNum))

    # treat the eof as a stanza seperator
    if len(currentStanza) > 0:
        stanzas.append(currentStanza)
        
    return stanzas


# generate label for one stanza
def _generateStanzaLabel(stanzaNumber):
    return "l" + str(stanzaNumber)

def _generateReg(regNumber):
    return "r" + str(regNumber)

# generate labels for all the stanzas
def _generateLabelDict(stanzas):
    labelDict = dict()
    for stanzaNum, stanza in enumerate(stanzas): 
        # extract the first word form the first line of the stanza
        firstLine = stanza[0]
        firstWord = firstLine.data[re.search("[\s,.:]", firstLine.data).start():].lower()
        labelDict[firstWord] = _generateStanzaLabel(stanzaNum)
    return labelDict

# Check if a string is an int
def _isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def translatePoem(lines):
    
    syllableCounter = SyllableCounter()
    
    outputCode = list()

    stanzas = _splitIntoStanzas(lines)
    
    # maps register to its current type
    registerSet = set()

    # ignore first stanza (reserved for title/author etc.)
    stanzas = stanzas[1:]

    labelDict = _generateLabelDict(stanzas)
    
    outputCode.append('#include "stdio.h"')
    outputCode.append("")
    outputCode.append("int main()")
    outputCode.append("{")

    for stanzaNum, stanza in enumerate(stanzas):
        outputCode.append(INDENT + _generateStanzaLabel(stanzaNum) + ": ;")
        for line in stanza:
            # split up line by punctuation into segments.
            segments = re.split("[^\w\s]+", line.data)

            params = list()

            for segment in segments:
                # split segment into individual words
                if len(segment.strip()) == 0:
                    continue
                words = re.split("(?:(?:\W-\W)|[^\w-])+", segment.strip())

                numVal = 0
                
                if _isNumber(words[0]):
                    # if the first word is just a raw number, then let's use it 
                    # directly
                    numVal = int(words[0])
                else:
                    for pos, word in enumerate(words):
                        if not syllableCounter.countSyllables(word).val % 2 == 0:
                            numVal += 2 ** (len(words) - (pos + 1))

                label = ''
                if words[0].lower() in labelDict:
                    label = labelDict[words[0].lower()]
                else:
                    label = _generateStanzaLabel(numVal)

                regVal = _generateReg(numVal)

                # callback that will be called every time a register is accessed
                def registerCallback(regNum, regVal):
                    if not regNum in registerSet:
                        # new register, so we need to add an int define
                        registerSet.add(regNum)
                        outputCode.append(DBL_INDENT + "int " + regVal + ";")

                params.append(instructions.Parameter(numVal, regVal, label,
                                                     registerCallback))

            outputCode.append(DBL_INDENT + 
                instructions.translateInstruction(
                    params[0].num(),
                    params[1:],
                    line.num))

    outputCode.append("}")

    return outputCode


    
