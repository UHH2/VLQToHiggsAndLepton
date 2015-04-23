#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
from UHH2.VLQSemiLepPreSel.plot import *

import time
import varial.tools
import varial.generators as gen


# varial.settings.debug_mode = True
dir_input = './'



#def loader_hook(wrps):
#    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
#    wrps = common.label_axes(wrps)
#    wrps = gen.switch(
#        wrps,
#        lambda w: w.in_file_path.split('/')[0] == 'GenHists',
#        gen.gen_make_th2_projections
#    )
#    wrps = gen.gen_make_eff_graphs(wrps)
#    wrps = gen.switch(
#        wrps,
#        lambda w: 'TH1' in w.type,
#        gen.gen_noex_norm_to_integral
#    )
#    return wrps


def loader_hook_split_bkg(wrps):
    #wrps = common.yield_n_objs(wrps, 20)
    #wrps = apply_match_eff(wrps)
    wrps = common.add_wrp_info(wrps)
    #wrps = merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-5)
    wrps = common.label_axes(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    #wrps = gen.gen_make_eff_graphs(wrps)
    return wrps


def plotter_factory_split_bkg(**kws):
    kws['hook_loaded_histos'] = loader_hook_split_bkg
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)


if __name__ == '__main__':
    p1 = varial.tools.mk_rootfile_plotter(
        pattern=dir_input + '*.root',
        name='VLQ2HT_stack',
        plotter_factory=plotter_factory_stack,
        combine_files=True,
    )

    p2 = varial.tools.mk_rootfile_plotter(
        pattern=dir_input + '*.root',
        name='VLQ2HT_norm',
        plotter_factory=plotter_factory_norm,
        combine_files=True,
    )

    p3 = varial.tools.mk_rootfile_plotter(
        pattern=dir_input + '*.root',
        name='VLQ2HT_norm_no_signal',
        plotter_factory=plotter_factory,
        combine_files=True,
        filter_keyfunc=lambda w: common.is_signal(w.file_path)
    )

    p4 = varial.tools.mk_rootfile_plotter(
        pattern=dir_input + '*.root',
        name='VLQ2HT_norm_split_bkg',
        plotter_factory=plotter_factory_split_bkg,
        combine_files=True,
        filter_keyfunc=lambda w: common.is_signal(w.file_path)
    )

    tc_inner = varial.tools.ToolChainParallel(
        'VLQ2HT', [
            p1.tool_chain[0],
            p2.tool_chain[0],
            p3.tool_chain[0],
            p4.tool_chain[0],
        ]
    )
    tc = varial.tools.ToolChain(
        'host_toolchain', [tc_inner]
    )

    time.sleep(1)
    tc.run()
    varial.tools.WebCreator().run()
    print 'done.'
