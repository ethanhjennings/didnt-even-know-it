'''
Created on Aug 15, 2013

@author: Ethan Jennings
'''

import re
import collections
import pickle
import syllables.digthedoug
from syllables import file_paths

class SyllableCounter:
    syllableCountDict = dict()

    def __init__(self):
        with open(file_paths.PICKLE_DICT_PATH, "rb") as f:
            self.syllableCountDict = pickle.load(f)

    def countSyllables(self, word):
        word = word.lower()
        SyllableCountVal = collections.namedtuple("SyllableCountVal",
                                                  ['syllable_count',
                                                  'was_in_dictionary'])
        if word in self.syllableCountDict:
            return SyllableCountVal(self.syllableCountDict[word], True)
        else:
            return SyllableCountVal(
                                    syllables.digthedoug.CountSyllables(word, False),
                                    False)
