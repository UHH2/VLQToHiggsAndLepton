#!/usr/bin/env python

import common
import settings

import os
import time
import varial.tools
import varial.generators as gen

dirname = 'VLQ3'


def loader_hook(wrps):
    wrps = common.label_axes(wrps)
    wrps = gen.switch(
        wrps,
        lambda w: w.in_file_path[0] == 'GenHists',
        gen.gen_make_th2_projections
    )
    wrps = gen.gen_make_eff_graphs(wrps)
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


