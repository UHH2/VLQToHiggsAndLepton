#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools

dirname = 'FirstPlots_VLQToHiggsAndLepton'


def make_eff_graphs(wrps):
    token = lambda w: w.legend + ":" + "/".join(w.in_file_path)[:-4]
    subs, tots = {}, {}
    for wrp in wrps:
        yield wrp
        if wrp.name.endswith('_sub'):
            t = token(wrp)
            if t in tots:
                yield varial.operations.eff((wrp, tots.pop(t)))
            else:
                subs[t] = wrp
        elif wrp.name.endswith('_tot'):
            t = token(wrp)
            if t in subs:
                yield varial.operations.eff((subs.pop(t), wrp))
            else:
                tots[t] = wrp


def norm_histos_to_integral(wrps):
    for wrp in wrps:
        if isinstance(wrp, varial.wrappers.HistoWrapper):
            yield varial.operations.norm_to_integral(wrp)
        else:
            yield wrp


def loader_hook(wrps):
    wrps = make_eff_graphs(wrps)
    wrps = sorted(wrps, key=lambda w: w.type + ':' + w.name)
    wrps = norm_histos_to_integral(wrps)
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
