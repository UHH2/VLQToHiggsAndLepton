import varial.tools
import varial.plotter

import UHH2.VLQSemiLepPreSel.common as common


plots = ['vlq_mass', 'vlq_pt', 'h_mass', 'h_pt', 'tlep_pt', 'tlep_mass']


def rename_y_axis(wrp):
	wrp.obj.GetYaxis().SetTitle('a.u.')
	return wrp


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = common.label_axes(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, 
        legend=lambda w: w.in_file_path.split('/')[0],
        draw_option=lambda w: 'hist' if not w.is_data else 'E1X0',
    )
    wrps = varial.gen.touch_legend_color(wrps)
    # wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = plot.merge_samples(wrps)
    # wrps = varial.gen.attribute_printer(wrps, 'legend')
    wrps = varial.gen.gen_norm_to_integral(wrps)
    wrps = (rename_y_axis(w) for w in wrps)
    wrps = varial.gen.switch(
    	wrps,
    	lambda w: not w.is_data,
    	lambda wrps: varial.gen.apply_linecolor(
    					 varial.gen.apply_linewidth(wrps))
    )
    wrps = varial.gen.sort(wrps)
    return wrps


def hook_loaded_histos_squash_mc(wrps):
	key=lambda w: w.in_file_path + '___%s' % w.is_data

	wrps = sorted(wrps, key=key)
	wrps = hook_loaded_histos(wrps)

	vlq_masses = filter(lambda w: w.name=='vlq_mass' and w.is_background, wrps)
	categories = set(w.in_file_path for w in vlq_masses)
	for cat in categories:
		print '='*20
		print cat
		vlq_masses_cat = filter(lambda w: w.in_file_path == cat, vlq_masses)
		total_int = sum(1./w.lumi for w in vlq_masses_cat)
		for w in vlq_masses_cat:
			inte = 1./w.lumi
			print 'fraction of %20s: %8.2f / %8.2f = %5.3f' % (
									w.sample, inte, total_int, inte/total_int)
	
	wrps = varial.gen.group(wrps, key)
	wrps = varial.gen.gen_merge(wrps)
	wrps = varial.gen.gen_norm_to_integral(wrps)
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
		signal = filter(lambda w: 'SignalRegion' == w.legend, bkg)
		others = filter(lambda w: 'SignalRegion' != w.legend, bkg)
		colorize_signal_region(signal[0])
		signal = [varial.op.stack(signal)]
		others[0].is_pseudo_data = True
		if dat:
			dat = [varial.op.norm_to_integral(varial.op.merge(dat))]
		yield signal + others + dat


def mk_plttr(plot_folder):
	return varial.tools.Plotter(
		plot_folder,
		#filter_keyfunc=lambda w: any(
		#	t in w.in_file_path for t in [
		#	    'SignalRegion/', 'SidebandTest',
		#	]
		#),
	  	input_result_path='../HistoLoader',
	    plot_grouper=varial.plotter.plot_grouper_by_name,
	    plot_setup=plot_setup,
	    # canvas_decorators=[varial.rnd.Legend],
    )


def mk_overlay_chains(samplename):
	input_path = '../../../../Loaders/%s' % samplename
	return varial.tools.ToolChainParallel(samplename, [
		varial.tools.ToolChain(
			'SideBandRegion', 
			[
				varial.tools.HistoLoader(
					input_result_path=input_path,
				    filter_keyfunc=lambda w: any(
				    	t in w.in_file_path for t in [
				    	    'SignalRegion', 'SidebandRegion',
				    	],
				  	) and not 'Run20' in w.file_path,
				),
				mk_plttr('Plotter'),
			]
		),
		#varial.tools.ToolChain(
		#	'MassPlus', 
		#	[
		#		varial.tools.HistoLoader(
		#			input_result_path=input_path,
		#		    filter_keyfunc=lambda w: (
		#		    	('MassPlus' in w.file_path 
		#		    			or 'Cat1htag/' in w.file_path)
		#		    	and not '.DATA.' in w.file_path
		#		  	),
		#		),
		#		mk_plttr('NoSelection'),
		#		mk_plttr('Nm1Selection'),
		#	]
		#),
		#varial.tools.ToolChain(
		#	'CompareToDataWith0bMassPlus', 
		#	[
		#		varial.tools.HistoLoader(
		#			input_result_path=input_path,
		#		    filter_keyfunc=lambda w: (
		#		    	(
		#		    		('.DATA.' in w.file_path and (
		#		    			'Cat1htagWith0bMassPlus/' in w.file_path
		#		    		))
		#		    	or
		#		    		('Cat1htag/' in w.file_path)
		#		    	)
		#		  	),
		#		),
		#		mk_plttr('NoSelection'),
		#		mk_plttr('Nm1Selection'),
		#	]
		#),
		#varial.tools.ToolChain(
		#	'CompareToDataWith1bMassPlus', 
		#	[
		#		varial.tools.HistoLoader(
		#			input_result_path=input_path,
		#		    filter_keyfunc=lambda w: (
		#		    	(
		#		    		('.DATA.' in w.file_path and (
		#		    			'Cat1htagWith1bMassPlus/' in w.file_path
		#		    		))
		#		    	or
		#		    		('Cat1htag/' in w.file_path)
		#		    	)
		#		    	
		#		  	),
		#		  	
		#		),
		#		mk_plttr('NoSelection'),
		#		mk_plttr('Nm1Selection'),
		#	]
		#),
	])

good_name = lambda w: any(w.name == p for p in plots)
good_smpl = lambda w: not '_TH_' in w.file_path
good_hist = lambda w: good_name(w) and good_smpl(w)

tc = varial.tools.ToolChain(
	'Sidebands', [
		varial.tools.ToolChainParallel(
			'Loaders', [
				varial.tools.HistoLoader(
				    filter_keyfunc=good_hist,
		            hook_loaded_histos=hook_loaded_histos_squash_mc,
		            name='AllSamples',
				),
			]
		),
		varial.tools.ToolChainParallel(
			'Plots', [
			    mk_overlay_chains('AllSamples'),
	    		# mk_overlay_chains('WJets'),
	    		# mk_overlay_chains('SquashMC'),
			]
		)
	]
)
