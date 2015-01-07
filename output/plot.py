#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()

import os
import time
import varial.tools as t

dirname = 'FirstPlots_VLQToHiggsAndLepton'

p = t.mk_plotter_chain(name=dirname)
time.sleep(1)
p.run()
t.WebCreator().run()
os.system('rm -r ~/www/%s' % dirname)
os.system('mv -f %s ~/www' % dirname)
