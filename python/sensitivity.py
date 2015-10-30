import math
import os

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.plot as plot
import varial.tools
from varial.extensions.limits import ThetaLimits, theta_auto


def get_model(hist_dir):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(['TpB_TH_700', 'TpB_TH_1700'])
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.30), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'WJets')
    model.add_lognormal_uncertainty('dyjets_rate', math.log(1.50), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(1.50), 'SingleT')
    model.add_lognormal_uncertainty('signal_700_rate', math.log(1.15), 'TpB_TH_700')
    model.add_lognormal_uncertainty('signal_1700_rate', math.log(1.15), 'TpB_TH_1700')
    return model


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.in_file_path.split('/')[0])
    wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = varial.gen.attribute_printer(wrps, 'category')
    # wrps = varial.gen.attribute_printer(wrps, 'sample')
    return wrps


def mk_sense_chain(name, cat_tokens):
    loader = varial.tools.HistoLoader(
        filter_keyfunc=lambda w: (w.name == 'vlq_mass'
                                  and any(t in w.in_file_path for t in cat_tokens)),
        hook_loaded_histos=hook_loaded_histos,
    )
    plotter = varial.tools.Plotter(
        input_result_path='../HistoLoader',
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: w.category),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: w.category
    )
    limits = ThetaLimits(
        model_func=get_model,
        cat_key=lambda w: w.category,
    )
    tc = varial.tools.ToolChain(name, [loader, plotter, limits])
    return tc


tc = varial.tools.ToolChain(  # Parallel(
    'Limits', [
        mk_sense_chain('SignalRegionOnly', ['SignalRegion']),
        mk_sense_chain('SignalRegionAndSideband', ['SignalRegion', 'SidebandTest']),
    ]
)