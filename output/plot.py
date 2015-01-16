#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools

dirname = 'FirstPlots_VLQToHiggsAndLepton'


def loader_hook(wrps):
    wrps = varial.generators.gen_norm_to_integral(wrps)
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
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
