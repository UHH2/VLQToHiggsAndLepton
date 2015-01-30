#! /usr/bin/env python

import os
cwd = os.getcwd()
print cwd

# compile
os.chdir('../../common')
if os.system('make -j 9'):
    print 'ERROR compiling common package. Exit.'
    exit(-1)

os.chdir(cwd)
os.chdir('../')
if os.system('make -j 9'):
    print 'ERROR compiling own analysis. Exit.'
    exit(-1)

# run sframe
os.chdir(cwd)
if os.system('sframe_main ../config/VLQToHiggsAndLepton.xml'):
    print 'ERROR exiting!'
    exit(-1)

# plot
os.system('./plot.py')
os.system('./plot_stks.py')

