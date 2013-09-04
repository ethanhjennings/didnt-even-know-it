didnt-even-know-it (WIP)
==================

Translator for an esoteric programming language where programs are made from poems

Note: currently only limited instructions and integer registers are supported, 
and no plain English poem examples have been written yet.

To see progress so far try running: (you need python 3+)
`python translate_poem.py sample_poems/test.poem -c output.c -o output`


This will compile and run the poem "test.poem" (which currently is not actually a poem, 
but just bare bones number opcodes and parameters). Type in a number and it should count 
up to that number.
