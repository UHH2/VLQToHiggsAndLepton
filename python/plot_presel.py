#!/usr/bin/env python

import common
import settings

import os
import time
import varial.tools
import varial.generators as gen


settings.max_open_root_files = 100
dir_input = '/nfs/dust/cms/user/tholenhe/VLQSemiLepPreSel/PHYS14-ntuple2-v2/'
dirname = 'VLQ_presel'


def loader_hook(wrps):
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common.label_axes(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    #wrps = gen.gen_make_eff_graphs(wrps)
    wrps = gen.switch(
        wrps,
        lambda w: 'TH1' in w.type,
        gen.gen_noex_norm_to_integral
    )
    return wrps


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)

p = varial.tools.mk_rootfile_plotter(
    pattern=dir_input + '*.root',
    name=dirname,
    plotter_factory=plotter_factory,
    combine_files=True,
)

if __name__ == '__main__':
    time.sleep(1)
    p.run()
    varial.tools.WebCreator().run()
    os.system('rm -r ~/www/%s' % dirname)
    os.system('mv -f %s ~/www' % dirname)


