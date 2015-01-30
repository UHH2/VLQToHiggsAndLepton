#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.analysis as ana
import varial.generators as gen
import varial.rendering as rnd
import varial.sample as smpl
import varial.settings as settings
import varial.tools

dirname = 'VLQstk'
settings.defaults_Legend['x_pos'] = 0.80
settings.defaults_Legend['label_width'] = 0.36
settings.defaults_Legend['label_height'] = 0.03
# settings.debug_mode = True
settings.box_text_size = 0.03
settings.colors = {
    'TTJets': 632, 
    'WJets': 878,
    'ZJets': 596, 
    'TpJ_TH_M800_Tlep': 870, 
    'TpJ_TH_M800_NonTlep': 434,
}

def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def loader_hook(wrps):
    wrps = gen.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path[0],
        legend=lambda w: ('100* ' if 'TpJ_TH_M' in w.sample else '') + w.sample,
        is_signal=lambda w: 'TpJ_TH_M' in w.sample,
        lumi=lambda w: 0.01 if 'TpJ_TH_M' in w.sample else 1.
    )
    wrps = gen.imap_conditional(wrps, lambda w: 'TpJ_TH_M800' in w.sample, gen.op.norm_to_lumi)
    wrps = label_axes(wrps)
    return wrps


def plotter_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
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


