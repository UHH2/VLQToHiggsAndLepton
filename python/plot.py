#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
from UHH2.VLQSemiLepPreSel.plot import loader_hook

import varial.generators as gen
import varial.history
import varial.tools
import itertools
import time


# varial.settings.debug_mode = True
input_pat = './uhh2.*.root'


@varial.history.track_history
def vlq2ht_plot_preproc(w):
    if w.legend.endswith('_0'):
        w.legend = w.legend[:-2]
    if w.is_signal:
        if 'SignalRegion' in w.in_file_path:
            w.legend += ' (1pb)'
        else:
            w.lumi /= 20.
            w.legend += ' (20pb)'
            w = varial.op.norm_to_lumi(w)
    return w


def add_jet_eta_hists(wrps):
    return varial.gen.gen_make_eff_graphs(
        wrps,
        'fwd_jet_eta',
        'ak4_jet_eta',
        'full_jet_eta',
        True,
        lambda w, l: w.in_file_path[:-l]+'__'+w.sample+'__'+w.sys_info,
        varial.op.merge
    )


def loader_hook_sig_scale(wrps, rebin_max_bins):
    wrps = loader_hook(wrps, rebin_max_bins)
    wrps = (vlq2ht_plot_preproc(w) for w in wrps)
    wrps = add_jet_eta_hists(wrps)

    # filter signals that are not for plotting
    wrps = itertools.ifilter(lambda w: 'Signal_' not in w.sample, wrps)
    return wrps


def plotter_factory_stack_sig_scale(**kws):
    rebin_max_bins = kws.pop('rebin_max_bins', 40)
    kws['hook_loaded_histos'] = lambda ws: loader_hook_sig_scale(ws, rebin_max_bins)
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    return varial.tools.Plotter(**kws)


def loader_hook_cat_merging(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = (vlq2ht_plot_preproc(w) for w in wrps)
    group_key = lambda w: w.in_file_path + '__' + w.sample
    wrps = sorted(wrps, key=group_key)
    wrps = gen.group(wrps, key_func=group_key)
    wrps = gen.gen_merge(wrps)
    wrps = common.label_axes(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps


def plotter_factory_stack_cat_merging(**kws):
    kws['hook_loaded_histos'] = loader_hook_cat_merging
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    return varial.tools.Plotter(**kws)


def mk_tools(input_pattern=None, **args):
    if not input_pattern:
        input_pattern = input_pat

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=input_pattern,
            name='Stacks',
            plotter_factory=plotter_factory_stack_sig_scale,
            combine_files=True,
            auto_legend=False,
            hook_canvas_post_build=varial.gen.add_sample_integrals,
            **args
        ),

        #varial.tools.mk_rootfile_plotter(
        #    pattern=input_pat,
        #    name='VLQ2HT_no_signal',
        #    plotter_factory=plotter_factory,
        #    combine_files=True,
        #    auto_legend=False,
        #    filter_keyfunc=lambda w: not common.is_signal(w.file_path)
        #),
    ]


def mk_toolchain(name, input_pattern, **args):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=lambda: mk_tools(input_pattern, **args),
    )


def mk_cutflowchain(name, input_pattern, filter_keyfunc=None):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=lambda: [
            cutflow_tables.mk_cutflow_chain(
                input_pattern, loader_hook, filter_keyfunc)]
    )


if __name__ == '__main__':
    all_tools = mk_tools()
    tc = varial.tools.ToolChainParallel(
        'VLQ2HT', all_tools
    )

    time.sleep(1)
    varial.tools.Runner(tc)
    varial.tools.WebCreator().run()
    print 'done.'
