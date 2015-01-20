#! /usr/bin/env python

import os
os.system('pwd')

# compile
os.chdir('..')
if os.system('make'):
    print 'ERROR compiling own analysis. Exit.'
    exit(-1)

os.chdir('../common')
if os.system('make'):
    print 'ERROR compiling common package. Exit.'
    exit(-1)

# run sframe
os.chdir('../VLQToHiggsAndLepton/output')
if os.system('sframe_main ../config/VLQToHiggsAndLepton.xml'):
    print 'ERROR exiting!'
    exit(-1)

# plot
os.system('./plot.py')
