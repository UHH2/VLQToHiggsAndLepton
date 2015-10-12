#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
from UHH2.VLQSemiLepPreSel.plot import *

import varial.generators as gen
import varial.history
import varial.tools
import time
import os


# varial.settings.max_num_processes = 1
# varial.settings.debug_mode = True
input_pat = './uhh2.*.root'


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


@varial.history.track_history
def scale_signal(w):
    if w.is_signal:
        w.lumi /= 20.
        w = varial.op.norm_to_lumi(w)
    return w


def loader_hook_sigx10(wrps):
    wrps = loader_hook(wrps)
    wrps = (scale_signal(w) for w in wrps)
    return wrps


def plotter_factory_stack_sigx10(**kws):
    kws['hook_loaded_histos'] = loader_hook_sigx10
    kws['save_lin_log_scale'] = True
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    return varial.tools.Plotter(**kws)


def loader_hook_cat_merging(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = (scale_signal(w) for w in wrps)
    group_key = lambda w: w.in_file_path + '__' + w.sample
    wrps = sorted(wrps, key=group_key)
    wrps = gen.group(wrps, key_func=group_key)
    wrps = gen.gen_merge(wrps)
    wrps = merge_samples(wrps)
    wrps = common.label_axes(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps


def plotter_factory_stack_cat_merging(**kws):
    kws['hook_loaded_histos'] = loader_hook_cat_merging
    kws['save_lin_log_scale'] = True
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    return varial.tools.Plotter(**kws)


def mk_tools(input_pattern=None):
    if not input_pattern:
        input_pattern = input_pat

    return [
        cutflow_tables.mk_cutflow_chain(input_pattern, loader_hook),

        varial.tools.mk_rootfile_plotter(
            pattern=input_pattern,
            name='VLQ2HT_stack',
            plotter_factory=plotter_factory_stack_sigx10,
            combine_files=True,
            auto_legend=False,
        ),

        # TODO for norm: set backgrounds line width to 2
        # TODO for norm: make data black!
        #varial.tools.mk_rootfile_plotter(
        #    pattern=input_pattern,
        #    name='VLQ2HT_norm',
        #    plotter_factory=plotter_factory_norm,
        #    combine_files=True,
        #    auto_legend=False,
        #),

        #varial.tools.mk_rootfile_plotter(
        #    pattern=input_pat,
        #    name='VLQ2HT_no_signal',
        #    plotter_factory=plotter_factory,
        #    combine_files=True,
        #    auto_legend=False,
        #    filter_keyfunc=lambda w: not common.is_signal(w.file_path)
        #),

        #varial.tools.mk_rootfile_plotter(
        #    pattern=input_pat,
        #    name='VLQ2HT_norm_split_bkg',
        #    plotter_factory=plotter_factory_split_bkg,
        #    combine_files=True,
        #    auto_legend=False,
        #    filter_keyfunc=lambda w: not common.is_signal(w.file_path)
        #),
    ]


if __name__ == '__main__':
    all_tools = mk_tools()
    tc = varial.tools.ToolChainParallel(
        'VLQ2HT', all_tools
    )

    time.sleep(1)
    varial.tools.Runner(tc)
    varial.tools.WebCreator().run()
    print 'done.'
