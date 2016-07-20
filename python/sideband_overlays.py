import varial.util
import varial.tools
import varial.plotter

import UHH2.VLQSemiLepPreSel.common as common


plots = ['vlq_mass', 'vlq_pt', 'h_mass', 'h_pt', 'tlep_pt', 'tlep_mass']
varial.settings.colors['SignalRegion'] = 617


def rename_y_axis(wrp):
    wrp.obj.GetYaxis().SetTitle('a.u.')
    return wrp


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = common.label_axes(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps,
        legend=lambda w: w.in_file_path.split('/')[0],
        draw_option=lambda w: 'hist' if not w.is_data else 'E0X0',
    )
    wrps = varial.gen.touch_legend_color(wrps)
    # wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.category, w.sample))
    # wrps = plot.merge_samples(wrps)
    # wrps = varial.gen.attribute_printer(wrps, 'legend')
    # wrps = varial.gen.gen_norm_to_integral(wrps)
    wrps = (rename_y_axis(w) for w in wrps)
    wrps = varial.gen.switch(
        wrps,
        lambda w: not w.is_data,
        lambda wrps: varial.gen.apply_linecolor(
                         varial.gen.apply_linewidth(wrps))
    )
    wrps = varial.gen.sort(wrps)
    return wrps


def print_bkg_percentages(wrps):

    def calc_percent_and_error(th1_hist, total_int, total_int_err):
        val, err = varial.util.integral_and_error(th1_hist)
        return val / total_int, (err**2 + total_int_err**2)**.5 / total_int

    def mk_prcntgs(grp):
        h_tot = varial.op.sum(grp)
        i_tot, i_tot_err = varial.util.integral_and_error(h_tot.obj)
        return h_tot.in_file_path, list(
            (w.sample, calc_percent_and_error(w.obj, i_tot, i_tot_err))
            for w in grp
        )

    def print_prcntgs(ifp, grp):
        print "="*80
        print ifp
        for it in grp:
            print it
        print "="*80
        return ifp, grp

    wrps = (w for w in wrps if w.name == 'vlq_mass' and w.is_background)
    wrps = varial.gen.gen_norm_to_lumi(wrps)
    wrps = sorted(wrps, key=lambda w: w.sample)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    wrps = varial.gen.group(wrps, lambda w: w.in_file_path)
    wrps = (mk_prcntgs(grp) for grp in wrps)
    wrps = list(print_prcntgs(*grp) for grp in wrps)


def hook_loaded_histos_squash_mc(wrps):
    key = lambda w: w.in_file_path + '___%s' % w.is_data

    wrps = sorted(wrps, key=key)
    wrps = hook_loaded_histos(wrps)

    # print_bkg_percentages(wrps)

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

        # signal region: line histo
        sr_bkg = list(w for w in bkg if w.legend == 'SignalRegion')
        sr_bkg[0].is_pseudo_data = True
        sr_bkg[0].draw_option = sr_bkg[0].draw_option + 'E1'
        sr_bkg[0].histo.SetMarkerSize(0)

        # sideband region: stack
        sb_bkg = list(w for w in bkg if w.legend != 'SignalRegion')
        colorize_signal_region(sb_bkg[0])
        sb_bkg = [varial.op.stack(sb_bkg)]

        # if dat:
        #     dat = (w for w in dat if 'SignalRegion' not in w.in_file_path)
        #     dat = varial.gen.gen_norm_to_integral(dat)
        #     dat = list(dat)
        #     assert len(dat) == 1, dat
        # else:
        #     sb_bkg[0].is_pseudo_data = True
        yield sr_bkg + sb_bkg


def plot_setup_with_data_uncert(grps):
    for grp in grps:
        grp = list(grp)
        dat, bkg, sig = varial.gen.split_data_bkg_sig(grp)
        dat, bkg, sig = list(dat), list(bkg), list(sig)

        # signal region: line histo
        sr_bkg = list(w for w in bkg if w.legend == 'SignalRegion')
        sr_bkg[0].is_pseudo_data = True
        sr_bkg[0].draw_option = sr_bkg[0].draw_option + 'E1'
        sr_bkg[0].histo.SetMarkerSize(0)

        # data: needed for sys uncert
        dat = (w for w in dat if 'SignalRegion' not in w.in_file_path)
        dat = varial.gen.gen_norm_to_integral(dat)
        dat = list(dat)

        # sideband region: stack
        sb_bkg = list(w for w in bkg if w.legend != 'SignalRegion')
        colorize_signal_region(sb_bkg[0])
        sb_bkg = [varial.op.stack(sb_bkg)]

        dat_err = sb_bkg[0].histo.Clone()
        print '='*80
        print 'data uncerts:'
        for i in xrange(dat_err.GetNbinsX()+2):
            d_val = dat[0].histo.GetBinContent(i) or 1e10
            d_err = dat[0].histo.GetBinError(i)
            print 'i, d_val, d_err, d_err/d_val:', i, d_val, d_err, d_err/d_val
            dat_err.SetBinError(i, d_err)
        print '='*80
        sb_bkg[0].histo_sys_err = dat_err

        yield sr_bkg + sb_bkg


def multi_region_hook_sample(wrps):
    for w in wrps:
        w.legend = w.sample
        w.draw_option = 'histE0'
        w.histo.SetMarkerSize(0.)
        yield w


def multi_region_hook_region(wrps):
    for w in wrps:
        w.legend = w.in_file_path.split('/')[0]
        w.draw_option = 'histE0'
        w.histo.SetMarkerSize(0.)
        yield w


def mk_overlay_chains(loadername, add_data_uncert=False, do_standard_plotter=True):
    input_path = '../../../../Loaders/%s' % loadername

    post_build_funcs = [
        varial.rnd.mk_split_err_ratio_plot_func(poisson_errs=False,y_title='#frac{sig-ctrl}{ctrl}'),
        varial.rnd.mk_legend_func(),
    ]

    standard_plotter = varial.tools.Plotter(
        'Plotter',
        input_result_path='../HistoLoader',
        plot_grouper=varial.plotter.plot_grouper_by_name,
        plot_setup=plot_setup_with_data_uncert if add_data_uncert else plot_setup,
        canvas_post_build_funcs=post_build_funcs,
    )

    return varial.tools.ToolChainParallel(loadername, [
        varial.tools.ToolChain(
            'SideBandRegion',
            [
                varial.tools.HistoLoader(
                    input_result_path=input_path,
                    filter_keyfunc=lambda w: any(
                        t in w.in_file_path
                        for t in ['SignalRegion', 'SidebandRegion']
                    ) and (add_data_uncert or 'Run20' not in w.sample),
                ),
                varial.tools.Plotter(
                    'PlotterIndividualSamples',
                    input_result_path='../HistoLoader',
                    filter_keyfunc=lambda w: not w.is_data,
                    hook_loaded_histos=lambda ws: varial.gen.gen_add_wrp_info(
                        varial.gen.gen_copy(ws),
                        legend=lambda w: w.sample+'/'+w.in_file_path.split('/')[0]),
                    plot_grouper=varial.plotter.plot_grouper_by_name,
                    canvas_post_build_funcs=post_build_funcs,
                ),
            ] + ([standard_plotter] if do_standard_plotter else [])
        ),
        varial.tools.ToolChain(
            'MultiRegion',
            [
                varial.tools.HistoLoader(
                    input_result_path=input_path,
                    filter_keyfunc=lambda w: any(
                        t in w.in_file_path
                        for t in ['SignalRegion', 'SidebandRegion',
                                  'Fw1B0Selection', 'Fw0B0Selection']
                    ) and 'Run20' not in w.sample,
                ),
                varial.tools.Plotter(
                    'Plotter',
                    input_result_path='../HistoLoader',
                    plot_setup=lambda ws: varial.plotter.default_plot_colorizer(
                        ws, [633, 601, 417, 617]),
                    plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
                    hook_loaded_histos=multi_region_hook_sample,
                    save_name_func=lambda w: w.in_file_path.replace('/', '_'),
                    canvas_post_build_funcs=post_build_funcs,
                ),
                varial.tools.Plotter(
                    'PlotterCombineRegions',
                    input_result_path='../HistoLoader',
                    plot_setup=lambda ws: varial.plotter.default_plot_colorizer(
                        ws, [633, 601, 417, 617]),
                    plot_grouper=varial.plotter.plot_grouper_by_name,
                    hook_loaded_histos=multi_region_hook_region,
                    canvas_post_build_funcs=post_build_funcs,
                ),
            ]
        ),
    ])

def get_tc(pat):
    name = 'Sidebands' + pat
    pat = '/%s/' % pat

    good_name = lambda w: any(w.name == p for p in plots)
    good_smpl = lambda w: '_TH_' not in w.file_path
    good_chnl = lambda w: pat in w.file_path
    good_hist = lambda w: good_chnl(w) and good_name(w) and good_smpl(w)

    return varial.tools.ToolChain(
        name, [
            varial.tools.ToolChainParallel(
                'Loaders', [
                    varial.tools.HistoLoader(
                        filter_keyfunc=good_hist,
                        hook_loaded_histos=hook_loaded_histos_squash_mc,
                        name='AllSamples',
                    ),
                    varial.tools.HistoLoader(
                        filter_keyfunc=lambda w: w.sample in ('WJets', 'TTbar')
                                                 and good_hist(w),
                        hook_loaded_histos=hook_loaded_histos,
                        name='WJetsTTbar',
                    ),
                ]
            ),
            varial.tools.ToolChainParallel(
                'Plots', [
                    mk_overlay_chains('AllSamples'),
                    mk_overlay_chains('WJetsTTbar', do_standard_plotter=False),
                    # mk_overlay_chains('WJets'),
                    # mk_overlay_chains('SquashMC'),
                ]
            ),
            varial.tools.ToolChainParallel(
                'PlotsWithDataUncert', [
                    mk_overlay_chains('AllSamples', True),
                ]
            ),
        ]
    )
