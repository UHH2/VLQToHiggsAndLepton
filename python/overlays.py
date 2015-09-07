import varial.tools

import UHH2.VLQSemiLepPreSel.common as common

def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, 
        category=lambda w: w.file_path.split('/')[-3],
        legend=lambda w: w.file_path.split('/')[-3],
    )
    # wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = plot.merge_samples(wrps)
    wrps = varial.gen.attribute_printer(wrps, 'category')
    # wrps = varial.gen.attribute_printer(wrps, 'sample')
    return wrps


tc = varial.tools.ToolChainParallel(
	'PlotOverlays',
	[
		varial.tools.Plotter(
			'Nm1Selection',
		    filter_keyfunc=lambda w: (w.in_file_path == 'Nm1Selection/vlq_mass'
		    						  and 'TTbar' in w.file_path),
		    hook_loaded_histos=hook_loaded_histos,
		    plot_grouper=lambda wrps: [wrps],
	    ),
		varial.tools.Plotter(
			'NoSelection',
		    filter_keyfunc=lambda w: (w.in_file_path == 'NoSelection/vlq_mass'
		    						  and 'TTbar' in w.file_path),
		    hook_loaded_histos=hook_loaded_histos,
		    plot_grouper=lambda wrps: [wrps],
	    ),	
	],
)

