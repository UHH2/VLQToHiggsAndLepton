
import UHH2.VLQSemiLepPreSel.common as common
from varial import plotter


filter_keyfunc = lambda w: (
	'Signal_TpB_TH_LH_M1' in w.file_path and 
	'PS_lep_' in w.in_file_path
)


def wrp_info(wrps):
	wrps = common.add_wrp_info(wrps)
	wrps = plotter.gen.gen_norm_to_integral(wrps)
	for w in wrps:
		w.sample = w.sample.replace('Signal_', '')
		w.legend = w.legend.replace('Signal_TpB_TH_',w.in_file_path[7:11] + ' ')
		yield w


pltr = plotter.Plotter(
	name='LepPlusVSLepMinus',
	filter_keyfunc=filter_keyfunc,
	hook_loaded_histos=wrp_info,
	plot_grouper=plotter.plot_grouper_by_name,
	save_name_func=plotter.save_by_name,
)
