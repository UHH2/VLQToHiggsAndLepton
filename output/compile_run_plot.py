#! /usr/bin/env python

import os
os.chdir('..')
os.system('pwd')

# compile
if os.system('make'):
    print 'ERROR exiting!'
    exit(-1)

# run sframe
os.chdir('output')
if os.system('sframe_main ../config/VLQToHiggsAndLepton.xml'):
    print 'ERROR exiting!'
    exit(-1)

# plot
os.system('./plot.py')
