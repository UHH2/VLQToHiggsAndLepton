#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.analysis as ana
import varial.generators as gen
import varial.sample as smpl
import varial.settings as settings
import varial.tools

dirname = 'VLQstk'
settings.defaults_Legend['x_pos'] = 0.83
settings.defaults_Legend['label_width'] = 0.33
# settings.debug_mode = True


def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def loader_hook(wrps):
    wrps = gen.itertools.ifilter(lambda w: 'TH1' in w.type, wrps)
    wrps = gen.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path[0],
        legend=lambda w: w.sample,
        is_signal=lambda w: w.sample == 'TpJ_TH_M800_Tlep',
    )
    wrps = label_axes(wrps)
    return wrps


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
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


