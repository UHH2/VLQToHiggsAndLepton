import varial.tools
import varial.plotter

import UHH2.VLQSemiLepPreSel.common as common


plots = ['vlq_mass', 'vlq_pt', 'h_mass', 'h_pt', 'tlep_pt', 'tlep_mass']


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = common.label_axes(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, 
        legend=lambda w: (w.file_path.split('/')[-3][19:] or 'signal region') 
        				 if not w.is_data else 'Data',
        draw_option=lambda w: 'hist' if not w.is_data else 'E1X0',
    )
    # wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = plot.merge_samples(wrps)
    # wrps = varial.gen.attribute_printer(wrps, 'legend')
    wrps = varial.gen.gen_norm_to_integral(wrps)
    wrps = varial.gen.switch(
    	wrps,
    	lambda w: not w.is_data,
    	lambda wrps: varial.gen.apply_linecolor(
    					 varial.gen.apply_linewidth(wrps))
    )
    return wrps


def colorize_signal_region(wrp):
	wrp.obj.SetFillColor(varial.ROOT.kGray)
	wrp.obj.SetLineColor(varial.ROOT.kBlack)
	wrp.obj.SetLineWidth(1)
	return wrp


def plot_setup(grps):
	for grp in grps:
		grp = list(grp)
		dat, bkg, sig = varial.gen.split_data_bkg_sig(grp)
		dat, bkg, sig = list(dat), list(bkg), list(sig)
		signal = filter(lambda w: 'signal region' == w.legend, bkg)
		others = filter(lambda w: 'signal region' != w.legend, bkg)
		colorize_signal_region(signal[0])
		signal = [varial.op.stack(signal)]
		if dat:
			dat = [varial.op.norm_to_integral(varial.op.merge(dat))]
		yield signal + others + dat


def mk_plttr(plot_folder):
	return varial.tools.Plotter(
		plot_folder,
	    filter_keyfunc=lambda w: (
	    	w.in_file_path.startswith(plot_folder)
	      	and any(p in w.in_file_path for p in plots)
	  	),
	  	input_result_path='../HistoLoader',
	    plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
	    plot_setup=plot_setup,
	    canvas_decorators=[varial.rnd.Legend],
    )


tc = varial.tools.ToolChain(
	'PlotOverlays',
	[
		varial.tools.ToolChain(
			'StandardSideBand', 
			[
				varial.tools.HistoLoader(
				    filter_keyfunc=lambda w: (
				    	any(w.in_file_path.endswith(p) for p in plots)
				    	and 'MassPlus' not in w.file_path
					  	and 'TTbar' in w.file_path
				  	),
				  	hook_loaded_histos=hook_loaded_histos,
				),
				mk_plttr('NoSelection'),
				mk_plttr('Nm1Selection'),
			]
		),
		varial.tools.ToolChain(
			'MassPlus', 
			[
				varial.tools.HistoLoader(
				    filter_keyfunc=lambda w: (
				    	any(w.in_file_path.endswith(p) for p in plots)
				    	and ('MassPlus' in w.file_path 
				    			or 'Cat1htag/' in w.file_path)
				  		and 'TTbar' in w.file_path
				  	),
				  	hook_loaded_histos=hook_loaded_histos,
				),
				mk_plttr('NoSelection'),
				mk_plttr('Nm1Selection'),
			]
		),
		varial.tools.ToolChain(
			'CompareToDataWith0bMassPlus', 
			[
				varial.tools.HistoLoader(
				    filter_keyfunc=lambda w: (
				    	any(w.in_file_path.endswith(p) for p in plots)
				    	and (
				    		('.DATA.' in w.file_path and (
				    			'Cat1htagWith0bMassPlus/' in w.file_path
				    		))
				    	or
				    		('TTbar' in w.file_path and 'Cat1htag/' in w.file_path)
				    	)
				    	
				  	),
				  	hook_loaded_histos=hook_loaded_histos,
				),
				mk_plttr('NoSelection'),
				mk_plttr('Nm1Selection'),
			]
		),
		varial.tools.ToolChain(
			'CompareToDataWith1bMassPlus', 
			[
				varial.tools.HistoLoader(
				    filter_keyfunc=lambda w: (
				    	any(w.in_file_path.endswith(p) for p in plots)
				    	and (
				    		('.DATA.' in w.file_path and (
				    			'Cat1htagWith1bMassPlus/' in w.file_path
				    		))
				    	or
				    		('TTbar' in w.file_path and 'Cat1htag/' in w.file_path)
				    	)
				    	
				  	),
				  	hook_loaded_histos=hook_loaded_histos,
				),
				mk_plttr('NoSelection'),
				mk_plttr('Nm1Selection'),
			]
		),
	],
)

