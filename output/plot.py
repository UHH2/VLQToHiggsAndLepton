#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()

import os
import time
import varial.tools

dirname = 'FirstPlots_VLQToHiggsAndLepton'


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = varial.generators.gen_norm_to_integral
    return varial.tools.Plotter(**kws)

p = varial.tools.mk_rootfile_plotter(
    name=dirname,
    plotter_factory=plotter_factory,
    combine_files=True
)
time.sleep(1)
p.run()
varial.tools.WebCreator().run()
os.system('rm -r ~/www/%s' % dirname)
os.system('mv -f %s ~/www' % dirname)
