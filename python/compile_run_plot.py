#! /usr/bin/env python

import os
cwd = os.getcwd()
print cwd

if not os.path.exists('../scripts/compile_run_plot.py'):
    print 'ERROR script must be executed in a dir next to "scripts". Exit.'
    exit(-1)

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
os.system('./../scripts/plot.py')
os.system('./../scripts/plot_stks.py')

