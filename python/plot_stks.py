#!/usr/bin/env python

import common
import settings

import os
import time
import varial.generators as gen
import varial.rendering as rnd
import varial.tools


dirname = 'VLQstk'


def loader_hook(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = gen.imap_conditional(wrps, lambda w: 'TpJ_TH_M800' in w.sample, gen.op.norm_to_lumi)
    wrps = common.label_axes(wrps)
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

if __name__ == '__main__':
    time.sleep(1)
    p.run()
    varial.tools.WebCreator().run()
    os.system('rm -r ~/www/%s' % dirname)
    os.system('mv -f %s ~/www' % dirname)


