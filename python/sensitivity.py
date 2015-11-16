import math
import os

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.plot as plot
import varial.tools
from varial.extensions.limits import ThetaLimits, theta_auto


################################################ fitting with MC background ###
def get_model(hist_dir):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(varial.settings.my_lh_signals)
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.30), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'WJets')
    model.add_lognormal_uncertainty('dyjets_rate', math.log(1.50), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(1.50), 'SingleT')
    for s in varial.settings.my_lh_signals:
        model.add_lognormal_uncertainty(s+'_rate', math.log(1.15), s)
    return model


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.in_file_path.split('/')[0])
    wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = varial.gen.attribute_printer(wrps, 'category')
    # wrps = varial.gen.attribute_printer(wrps, 'sample')
    return wrps


############################################## fitting with DATA background ###
def get_model_data_bkg(hist_dir):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(varial.settings.my_lh_signals)
    model.add_lognormal_uncertainty('bkg_rate', math.log(1.15), 'Bkg')
    for s in varial.settings.my_lh_signals:
        model.add_lognormal_uncertainty(s+'_rate', math.log(1.15), s)
    return model


def hook_loaded_histos_data_bkg(wrps):
    wrps = hook_loaded_histos(wrps)
    wrps = filter(lambda w: not w.is_background, wrps)
    wrps = filter(lambda w: not (w.is_signal and w.category == 'SidebandTest'), wrps)
    signals = filter(lambda w: w.is_signal, wrps)
    sr, = filter(lambda w: w.is_data and w.category == 'SignalRegion', wrps)
    sb, = filter(lambda w: w.is_data and w.category == 'SidebandTest', wrps)

    # re-interpret sideband histogram for fitting
    scale_factor = sr.obj.Integral() / sb.obj.Integral()
    sb = varial.op.prod([sb, varial.wrp.FloatWrapper(scale_factor)])
    sb.sample = 'Bkg'
    sb.legend = 'Sideband'
    sb.category = 'SignalRegion'
    sb.is_data = False
    sb.lumi = sr.lumi

    return signals + [sb, sr]


########################################################### make toolchains ###
def mk_sense_chain(name, cat_tokens, hook=hook_loaded_histos, model=get_model):
    loader = varial.tools.HistoLoader(
        filter_keyfunc=lambda w: (
            w.name == 'vlq_mass'
            and (not '_TH_' in w.file_path 
                    or any(s in w.file_path for s in varial.settings.my_lh_signals))
            and any(t in w.in_file_path for t in cat_tokens)
        ),
        hook_loaded_histos=hook,
    )
    plotter = varial.tools.Plotter(
        input_result_path='../HistoLoader',
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: w.category),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: w.category
    )
    limits = ThetaLimits(
        model_func=model,
        cat_key=lambda w: w.category,
    )
    tc = varial.tools.ToolChain(name, [loader, plotter, limits])
    return tc


tc = varial.tools.ToolChainParallel(
    'Limits', [
        mk_sense_chain('SignalRegionOnly', ['SignalRegion']),
        mk_sense_chain('SignalRegionAndSideband', ['SignalRegion', 'SidebandTest']),
        mk_sense_chain('DataBackground', ['SignalRegion', 'SidebandTest'], 
            hook_loaded_histos_data_bkg, get_model_data_bkg),
    ]
)
