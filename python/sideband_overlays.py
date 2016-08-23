import UHH2.VLQSemiLepPreSel.common as common
import varial.plotter
import varial.tools
import varial.util


plots = ['vlq_mass', 'vlq_pt', 'h_mass', 'h_pt', 'tlep_pt', 'tlep_mass']
varial.settings.colors['SignalRegion'] = 617


def rename_y_axis(wrp):
    wrp.obj.GetYaxis().SetTitle('a.u.')
    return wrp


def set_uncertainty_on_vlq_mass(wrps):
    # bins (6, 7, 24, 25) get double uncertainty
    for w in wrps:
        if w.name == 'vlq_mass':
            # w.histo.SetBinContent(5, 0.)
            # w.histo.SetBinError(5, 0.)
            for i in (6, 7, 24, 25):
                w.histo.SetBinError(i, 2 * w.histo.GetBinError(i))
        yield w


def hook_loaded_histos(wrps):
    wrps = set_uncertainty_on_vlq_mass(wrps)
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


class Chi2Test(varial.tools.Tool):
    def run(self):
        wrps = self.lookup_result('../HistoLoader')
        assert wrps, str(wrps)
        wrps = list(w for w in wrps if w.name == 'vlq_mass')
        assert len(wrps) == 2, str(wrps)
        a, b = wrps
        chi2 = b.histo.Chi2Test(a.histo, 'WW')
        self.result = varial.wrp.Wrapper(chi2=chi2)


class Chi2Collector(varial.tools.Tool):
    def run(self):
        sys_names = varial.ana.lookup_children_names('..')
        sys_names.remove(self.name)
        assert sys_names, str(sys_names)
        chi2_vals = dict(
            (sys, round(self.lookup_result('../%s/Chi2Test'%sys).chi2, 2))
            for sys in sys_names
        )
        self.result = varial.wrp.Wrapper(**chi2_vals)


def mk_overlay_chain(name, input_pat, hlh=hook_loaded_histos_squash_mc):

    # keyfunc
    good_name = lambda w: any(w.name == p for p in plots)
    good_smpl = lambda w: '_TH_' not in w.file_path and 'Run2015' not in w.file_path
    good_regn = lambda w: any(
        t in w.in_file_path
        for t in ['SignalRegion', 'SidebandRegion']
    )
    good_hist = lambda w: good_name(w) and good_smpl(w) and good_regn(w)

    post_build_funcs = [
        varial.rnd.mk_split_err_ratio_plot_func(
            poisson_errs=False,
            y_title='#frac{sig-ctrl}{ctrl}'
        ),
        varial.rnd.mk_legend_func(),
    ]

    return varial.tools.ToolChain(
        name,
        [
            varial.tools.HistoLoader(
                pattern=input_pat,
                filter_keyfunc=good_hist,
                hook_loaded_histos=hlh,
            ),
            varial.tools.Plotter(
                'Plotter',
                input_result_path='../HistoLoader',
                plot_grouper=varial.plotter.plot_grouper_by_name,
                plot_setup=plot_setup,
                canvas_post_build_funcs=post_build_funcs,
            ),
            Chi2Test(),
        ]
    )


def get_xsec_sys(input_pat):
    bkgs = list(varial.settings.stacking_order)
    percent_errs = {
        'TTbar':        0.2,  # 0.08,    # 0.15,  # 0.05650
        'SingleT':      0.2,  # 0.2,     # 0.15,  # 0.04166
        'QCD':          0.5,  # 0.3,
        'DYJets':       0.2,  # 0.2,     # 0.15,  # 0.01728
        'WJets':        0.2,  # 0.06,    # 0.15,  # 0.03759
    }

    def mk_hook_ld_hist_renorm(bkg, factor):
        scale_factor = percent_errs[bkg]*factor + 1

        def scale_bkg(wrps):
            for w in wrps:
                if w.sample == bkg:
                    w.histo.Scale(scale_factor)
                yield w

        def new_hook(wrps):
            wrps = scale_bkg(wrps)
            wrps = hook_loaded_histos_squash_mc(wrps)
            return wrps

        return new_hook

    return list(
        mk_overlay_chain(
            b + ('__plus' if fctr>0 else '__minus'),
            input_pat,
            hlh=mk_hook_ld_hist_renorm(b, fctr)
        )
        for b in bkgs
        for fctr in (+1., -1.)
    )


def get_sys(sys_name, input_pat):
    input_pat += '/SysTreeProjectors/%s/*.root' % sys_name
    return mk_overlay_chain(sys_name, input_pat)


def get_tc(base_path):
    name = 'Sidebands' + ('El' if base_path.endswith('/El') else 'Mu')

    return varial.tools.ToolChain(
        name,
        [
            mk_overlay_chain('Nominal', base_path+'/TreeProjector/*.root'),
            get_sys('b_tag_bc__minus', base_path),
            get_sys('b_tag_bc__plus', base_path),
            get_sys('b_tag_udsg__minus', base_path),
            get_sys('b_tag_udsg__plus', base_path),
            get_sys('JES__minus', base_path),
            get_sys('JES__plus', base_path),
            get_sys('JER__minus', base_path),
            get_sys('JER__plus', base_path),
        ] + get_xsec_sys(base_path+'/TreeProjector/*.root') + [
            Chi2Collector()
        ]
    )
