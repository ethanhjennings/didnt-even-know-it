'''
Created on Aug 15, 2013

@author: Ethan
'''
import re
import pickle
from syllables import file_paths

# load syllables from cmudict.txt
syllableCountDict = dict()

print('Opening ' + file_paths.CMU_DICT_PATH)
with open(file_paths.CMU_DICT_PATH, 'r') as f:
    print('Loading syllable information.')

    for line in f:
        sections = line.split(" ")

        # filter out words with parentheis (which are alternate
        # pronounciations) and words starting with non-letters
        if (not re.match("\w", sections[0]) or
        re.search("[\(\)]", sections[0])):
            continue

        # remove all apostrophies and hyphens from the word
        word = re.sub(r"['-]", '', sections[0])

        numSyllables = 0

        # count pronounced vowels
        for x in sections[1:]:
            if len(x) > 0 and re.search("[0-9]+", x):
                # only vowels end in numbers, so this is a vowel
                numSyllables += 1

        if numSyllables > 0:
            syllableCountDict[word.lower()] = numSyllables

print('Saving syllable information to ' + file_paths.PICKLE_DICT_PATH)

# save syllable counts to syllables.txt
with open(file_paths.PICKLE_DICT_PATH, 'wb') as f:
    pickle.dump(syllableCountDict, f)

print('Finished saving syllable information')
