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


@varial.history.track_history
def scale_mc_down_to_1p266invfb(w):
    if not w.is_data:
        w.lumi /= 6./10.
        w = varial.op.norm_to_lumi(w)
    return w


def loader_hook_sig_scale(wrps):
    wrps = loader_hook(wrps)
    wrps = (vlq2ht_plot_preproc(w) for w in wrps)
    # wrps = (scale_mc_down_to_1p266invfb(w) for w in wrps)

    # filter signals that are not for plotting
    wrps = itertools.ifilter(lambda w: 'Signal_' not in w.sample, wrps)
    return wrps


def plotter_factory_stack_sigx10(**kws):
    kws['hook_loaded_histos'] = loader_hook_sig_scale
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

    rm_uncerts = ('HT__', 'jet_pt__')

    if 'filter_keyfunc' in args:
        fk = args['filter_keyfunc']
        args['filter_keyfunc'] = lambda w: (
            not any(t in w.file_path for t in rm_uncerts)
            and fk(w)
        )
    else:
        args['filter_keyfunc'] = lambda w: (
            not any(t in w.file_path for t in rm_uncerts)
        )

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=input_pattern,
            name='Stacks',
            plotter_factory=plotter_factory_stack_sigx10,
            combine_files=True,
            auto_legend=False,
            hook_canvas_post_build=varial.gen.add_sample_integrals,
            **args
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
