import math
import os

import UHH2.VLQSemiLepPreSel.common as common
import UHH2.VLQSemiLepPreSel.plot as plot
import varial.tools
from varial.extensions.limits import ThetaLimits
from varial.extensions.limits import theta_auto


def get_model(hist_dir):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(['TpJ_TH_M800_Tlep', 'TpJ_TH_M1200_Tlep'])
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'MC_TTJets')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.30), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'MC_WJets')
    model.add_lognormal_uncertainty('zjets_rate', math.log(1.50), 'MC_ZJets')
    model.add_lognormal_uncertainty('signal_M800_rate', math.log(1.15), 'TpJ_TH_M800_Tlep')
    model.add_lognormal_uncertainty('signal_M1200_rate', math.log(1.15), 'TpJ_TH_M1200_Tlep')
    return model


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.file_path.split('/')[-3])
    wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    wrps = plot.merge_samples(wrps)
    wrps = varial.gen.gen_norm_to_integral(wrps)
    #wrps = varial.gen.attribute_printer(wrps, 'category')
    #wrps = varial.gen.attribute_printer(wrps, 'sample')
    return wrps


def mk_sense_chain(name, cat_token):
    loader = varial.tools.HistoLoader(
        filter_keyfunc=lambda w: (w.in_file_path == 'Nm1Selection/vlq_mass'
                                  and cat_token in w.file_path),
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
        mk_sense_chain('FilteredHiggsTag', 'FilteredCat'),
        mk_sense_chain('PrunedHiggsTag', 'PrunedCat'),
    ]
)