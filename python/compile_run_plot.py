#! /usr/bin/env python

import os
cwd = os.getcwd()
print cwd

if not os.path.exists('../python/compile_run_plot.py'):
    print 'ERROR script must be executed in a dir next to "python". Exit.'
    exit(-1)

# compile common
os.chdir('../../common')
if os.system('make -j 9'):
    print 'ERROR compiling common package. Exit.'
    exit(-1)
os.chdir(cwd)

# compile VLQSemiLepPreSel
os.chdir('../../VLQSemiLepPreSel')
if os.system('make -j 9'):
    print 'ERROR compiling VLQSemiLepPreSel package. Exit.'
    exit(-1)
os.chdir(cwd)

# compile own analysis
os.chdir('../')
if os.system('make -j 9'):
    print 'ERROR compiling own analysis. Exit.'
    exit(-1)
os.chdir(cwd)

# run sframe
if os.system('sframe_main ../config/VLQToHiggsAndLepton.xml'):
    print 'ERROR exiting!'
    exit(-1)

# plot
os.system('./../python/plot.py')
#os.system('./../python/copy_www.py')

