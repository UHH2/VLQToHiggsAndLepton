import UHH2.VLQSemiLepPreSel.common as common
import varial.extensions.limits as limits
import varial.tools
import itertools
import cPickle
import ROOT
import math


ele_bins = [0., 400., 560., 640., 720., 800., 880., 960., 1040., 1120.,
            1200., 1280., 1360., 1440., 1600., 1760., 2000]

mu_bins = [0., 360., 480., 560., 640., 720., 800., 880., 960., 1040., 1120.,
           1200., 1280., 1360., 1440., 1520., 1600., 1680., 1840., 2000.]

theory_masses = [700, 800, 900, 1000, 1100, 1200,
                 1300, 1400, 1500, 1600, 1700, 1800,]

theory_xsec_tpb = [5.820, 3.860, 2.720, 1.950, 1.350, 0.982,
                   0.716, 0.540, 0.408, 0.305, 0.230, 0.174,]
theory_xsec_tpb = list(v/4. for v in theory_xsec_tpb)  # branching to tH in 50/25/25

theory_xsec_tpt = [0.745, 0.532, 0.388, 0.285, 0.212, 0.159,
                   0.120, 0.0917, 0.0706, 0.0541, 0.0420, 0.0324,]
theory_xsec_tpt = list(v/2. for v in theory_xsec_tpt)  # branching to tH in 0/50/50


def add_th_curve(grps):
    return limits.add_th_curve(
        grps,
        theory_masses,
        theory_xsec_tpb if 'LimitsTpB' in varial.analysis.cwd else theory_xsec_tpt
    )


limits.tex_table_mod_list.insert(
    0,
    ('Signal_TpB_TH_LH_', ' '),  # remove lengthy part of name
)
limits.tex_table_mod_list.insert(
    0,
    ('process / nuisance parameter', ' '),  # shorten table...
)


################################################ fitting with MC background ###
def get_model(hist_dir, signals):
    model = limits.theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True,
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(signals)
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.30), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'WJets')
    model.add_lognormal_uncertainty('dyjets_rate', math.log(1.50), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(1.50), 'SingleT')
    # for s signals:
    #     model.add_lognormal_uncertainty(s+'_rate', math.log(1.15), s)
    return model


def add_region_and_category(wrps):
    return varial.gen.gen_add_wrp_info(
        wrps,
        region=lambda w: w.in_file_path.split('/')[0],
        category=lambda w: 'mu' if '/Mu/' in w.file_path else 'el',
    )


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = add_region_and_category(wrps)
    wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.region, w.category))
    # wrps = varial.gen.attribute_printer(wrps, 'region')
    # wrps = varial.gen.attribute_printer(wrps, 'sample')
    return wrps


def rebin_for_bb(wrps, norm_by_bin_width=False):
    for w in wrps:
        if w.category == 'el':
            w = varial.op.rebin(w, ele_bins, norm_by_bin_width)
        elif w.category == 'mu':
            w = varial.op.rebin(w, mu_bins, norm_by_bin_width)
        yield w


############################################## fitting with DATA background ###
def get_model_data_bkg(hist_dir, signals):
    model = limits.theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties=True,
    )
    model.fill_histogram_zerobins()
    model.set_signal_processes(signals)
    model.add_lognormal_uncertainty('bkg_rate', math.log(2.), 'Bkg')

    for s in signals:
        model.add_lognormal_uncertainty('fwd_jet_eff', math.log(1.15), s)

    for s in signals:
        model.add_lognormal_uncertainty(
            'lepton_iso_and_trigger', math.log(1.05), s)

    return model


class SigInjModel(object):
    def __init__(self, injected_signal, signal_strength, n_toys=1000):
        self.injected_signal = injected_signal
        self.signal_strength = signal_strength
        self.n_toys = n_toys
        self.data = None

    def get_model_data_bkg(self, hist_dir, signals):
        model_toys = get_model_data_bkg(hist_dir, signals)
        model_toys = limits.theta_auto.get_bootstrapped_model(model_toys)
        self.data = limits.theta_auto.make_data(
            model_toys,
            'toys:%s'%self.signal_strength,
            n=self.n_toys,
            signal_process_groups={self.injected_signal: [self.injected_signal]},
        )
        return get_model_data_bkg(hist_dir, signals)

    def limit_func(self, model):
        return limits.theta_auto.asymptotic_cls_limits(
            model,
            input=self.data[self.injected_signal],
            n=self.n_toys,
        )

    def pvalue_func(self, model):
        res = limits.theta_auto.zvalue_approx(
            model,
            input=self.data[self.injected_signal],
            n=self.n_toys,
        )
        return res

    def postfit_func(self, model):
        res = limits.theta_auto.mle(
            model,
            input=self.data[self.injected_signal],
            n=self.n_toys,
        )
        import numpy
        for pf_vals in res.itervalues():
            del pf_vals['__nll']
            for key in pf_vals:
                vals = list(a for a, _ in pf_vals[key])
                errs = list(b for _, b in pf_vals[key])
                weis = list(1/b for b in errs)
                wei_mean = numpy.average(vals, weights=weis)
                mean_err = numpy.average(errs)
                pf_vals[key] = ((wei_mean, mean_err),)

        return res


def hook_loaded_histos_data_bkg(wrps):
    wrps = hook_loaded_histos(wrps)
    wrps = (w for w in wrps if not w.is_background)
    wrps = list(w for w in wrps if not (w.is_signal and w.region == 'SidebandRegion'))

    sigs = list(w for w in wrps if w.sample.startswith('Signal_'))
    sr = (w for w in wrps if w.is_data and w.region == 'SignalRegion')
    sr = sorted(sr, key=lambda w: w.category)
    sb = list(w for w in wrps if w.is_data and w.region == 'SidebandRegion')
    sb = sorted(sb, key=lambda w: w.category)

    def scale_bkg(sr_, sb_):
        scale_factor = sr_.obj.Integral() / sb_.obj.Integral()
        sb_ = varial.op.prod([sb_, varial.wrp.FloatWrapper(scale_factor)])
        sb_.sample = 'Bkg'
        sb_.legend = 'Bkg. estimate'
        sb_.region = 'SignalRegion'
        sb_.is_data = False
        sb_.lumi = sr_.lumi
        return sb_

    sb = list(
        scale_bkg(*sr_sb) for sr_sb in zip(sr, sb)
    )

    return sorted(sigs + sb + sr, key=lambda w: '%s__%s' % (w.region, w.category))


def hook_sys(wrps):

    # assign information to wrappers: region, sys_type
    wrps = hook_loaded_histos(wrps)
    wrps = varial.gen.gen_add_wrp_info(
        wrps,
        sys_type=lambda w: w.file_path.split('/')[-2],
    )
    wrps = (w for w in wrps if not (w.category == 'el' and 'muon' in w.sys_type))

    # group by sys_type, then apply original hook within every systematic
    keyfunc = lambda w: w.sys_type
    wrps = sorted(wrps, key=keyfunc)
    grps = varial.generators.group(wrps, keyfunc)
    wrps = (w for g in grps for w in hook_loaded_histos_data_bkg(g))

    # # create closure-uncertainty
    # mcs = varial.analysis.fs_aliases
    # mcs = add_region_and_category(mcs)
    # mcs = (w for w in mcs if w.region in ['SignalRegion', 'SidebandRegion'])
    # mcs = (w for w in mcs if w.name == 'vlq_mass')
    # mcs = varial.gen.load(mcs)
    # mcs = (w for w in mcs if w.is_background)
    # mcs = list(varial.gen.sort_group_merge(mcs, lambda w: '%s__%s' % (w.region, w.category)))

    # def mk_closure_uncert(mcs):
    #     bkg, = list(
    #         w
    #         for w in varial.ana.lookup_result('../HistoLoader')
    #         if w.sample == 'Bkg' and w.category == mcs[0].category
    #     )
    #     mcs = dict((w.region, w) for w in mcs)
    #     assert len(mcs) == 2, 'need one for SignalRegion and one for SidebandRegion'
    #     ratio = varial.op.div((
    #         varial.op.norm_to_integral(mcs['SignalRegion']),
    #         varial.op.norm_to_integral(mcs['SidebandRegion'])
    #     ))

    #     closure_ncrt_p = varial.op.prod((bkg, ratio))
    #     closure_ncrt_p.region = 'SidebandRegion'
    #     closure_ncrt_p.sys_type = 'bkg_shape__plus'
    #     closure_ncrt_m = varial.op.copy(bkg)
    #     closure_ncrt_m.region = 'SidebandRegion'
    #     closure_ncrt_m.sys_type = 'bkg_shape__minus'
    #     return [closure_ncrt_p, closure_ncrt_m]

    # closure_ncrt = list(
    #     ncrt
    #     for cat in ['el', 'mu']
    #     for ncrt in mk_closure_uncert(
    #         list(m for m in mcs if cat == m.category)
    #     )
    # )

    # # append closure uncert
    # wrps = (w for grp in (wrps, closure_ncrt) for w in grp)

    return wrps


def scale_bkg_postfit(wrps, theta_res_path):
    theta_res = varial.ana.lookup_result(theta_res_path)
    try:
        r, _ = theta_res.postfit_vals['Signal_TpB_TH_LH_M1000']['bkg_rate'][0]
    except KeyError:
        r = 0

    for w in wrps:
        if w.sample == 'Bkg':
            w.sample = 'BkgPostFit'
            w.legend = 'Bkg. post-fit'
            w.histo.Scale(1+r)
        yield w


def make_combo(wrps):
    wrps = list(wrps)
    copies = (varial.op.copy(w) for w in wrps)
    copies = varial.gen.sort_group_merge(copies, lambda w: w.sample + '__' + w.sys_info)
    copies = varial.gen.gen_add_wrp_info(copies, category=lambda w: 'comb')
    for coll in (wrps, copies):
        for w in coll:
            yield w


def put_uncert_title(canvas_builders):
    for cnv in canvas_builders:
        for entry in cnv.legend.GetListOfPrimitives():
            if entry.GetLabel() == 'Stat. uncert. MC':
                entry.SetLabel('Stat. uncert. Bkg')
        yield cnv


def canvas_hook_integrals(cnvs):
    cnvs = varial.gen.add_sample_integrals(cnvs)
    cnvs = put_uncert_title(cnvs)

    ntgrls = varial.wrp.Wrapper(name='integrals')
    for c in cnvs:
        cat = c.renderers[0].category
        ints = list((k.replace('(700', '(0700'), v)
                    for k, v in c.renderers[0].all_info().iteritems()
                    if 'Integral___' in k and 'rightarrow' in k)
        for k, v in ints:
            if len(v) == 4:
                vals = v[0], v[1], v[3]
            else:
                vals = v[0], v[1], 0.
            setattr(ntgrls, '_' + cat + k,
                r'& $%5.1f\;\pm%5.1f$(stat.)$\;\pm%5.1f$(syst.)' % vals)
        yield c

    varial.diskio.write(ntgrls)


class PValueCollector(varial.tools.Tool):
    def run(self):
        tokens = ['TpBLH', 'TpBRH', 'TpTLH', 'TpTRH']
        res = (                                     # fetch theta results
            self.lookup_result(
                '../Outputs/Limits%s/DataBackground/Theta/ThetaLimits' % t)
            for t in tokens
        )
        res = (w.p_vals for w in res)               # pull out p_vals
        res = (                                     # find signal with min p-val
            min(
                ((sig, z_dict['p'])
                 for sig, z_dict in p_vals.iteritems()),
                key=lambda tpl: tpl[1]
            )
            for p_vals in res
        )
        wrp = varial.wrp.Wrapper()                  # put it all in a wrapper
        for tok, min_p in itertools.izip(tokens, res):
            setattr(wrp, tok, min_p)
        self.result = wrp


class BetaSignalCollector(varial.tools.Tool):
    def run(self):
        p_tpblh = '../Outputs/LimitsTpBLH'
        res = varial.analysis.lookup_children_names(p_tpblh)
        res = (                                     # fetch names / result wrps
            (
                toolname.split('SigInj')[1],
                self.lookup_result(p_tpblh+'/'+toolname+'/Theta/ThetaLimits')
            )
            for toolname in res
            if 'SigInj' in toolname
        )
        res = (                                     # pull out postfit_vals
            (signalname, w.postfit_vals[signalname])
            for signalname, w in res
        )
        res = (                                     # pull out beta_signal
            (signalname, pf_vals['beta_signal'])
            for signalname, pf_vals in res
        )
        wrp = varial.wrp.Wrapper()                  # put it all in a wrapper
        for signalname, beta_signal in res:
            setattr(wrp, signalname, beta_signal)
        self.result = wrp


class EffNumTable(varial.tools.Tool):
    def run(self):
        def get_line_info(info):
            return sorted(
                (k.replace('(700', '(0700'), v)
                for k, v in info.iteritems()
                if k.startswith('Integral___T_')
            )

        def get_fmt(line_tuple, f):
            f /= 100.
            name, nums = line_tuple
            if len(nums) == 4:
                i, st, _, sy = nums
                st, sy = max(st, 0.01), max(sy, 0.01)
            else:
                (i, st), sy = nums, 0.
            num = r'& $%5.1f \pm %4.1f \pm %4.1f$ ' % (i, st, sy)
            eff = r'& $%2.2f \pm %2.2f \pm %2.2f$ ' % (i/f, st/f, sy/f)
            return ('%50s'%name) + num + eff

        res = ['TpBLH', 'TpBRH', 'TpTLH', 'TpTRH']
        res = (
            './VLQ2HT/Outputs/Limits%s/DataBackground/PostFit/_varial_infodata.pkl' % tok
            for tok in res
        )
        res = (cPickle.load(open(fname)) for fname in res)
        res = (
            sorted(
                (name, info)
                for name, info in pkldata.iteritems()
                if name.endswith('el') or name.endswith('mu')
            )
            for pkldata in res
        )
        res = ((item[0][1], item[1][1]) for item in res)  # drop name
        res = (                                    # pull integrals out of wrps
            line_tuple
            for w_el, w_mu in res
            for line_tuple in zip(get_line_info(w_el), get_line_info(w_mu))
        )
        res = (
            get_fmt(line_el, 2318.-93.) + get_fmt(line_mu, 2318.)
            for line_el, line_mu in res
        )
        res = '\n'.join(res)
        with open(self.cwd+'table_content.tex', 'w') as f:
            f.write(res)


class CouplingLimit(varial.tools.Tool):
    def run(self):
        def mk_coupling_graph(wrp):
            wrp = varial.op.copy(wrp)
            g = wrp.graph
            n_points = len(theory_masses)
            for i in xrange(n_points):
                x, y = ROOT.Double(), ROOT.Double()
                g.GetPoint(i, x, y)
                if x == 0:
                    continue
                th_y = th_vals[theory_masses.index(int(x))]
                g.SetPoint(i, x, (y/th_y)**.5)

            if 'std. deviation' in wrp.legend:
                for i in xrange(n_points):
                    j = i + n_points
                    g.GetPoint(j, x, y)
                    if x == 0.:
                        continue
                    th_y = th_vals[theory_masses.index(int(x))]
                    g.SetPoint(j, x, (y/th_y)**.5)

            g.GetXaxis().SetTitle(x_title)
            g.GetYaxis().SetTitle(y_title)
            # g.GetYaxis().SetRangeUser(0.1, 2.5 if is_tpb else 5.0)
            # g.SetMinimum(0.1)
            # g.SetMaximum()
            wrp.val_y_min = 0.1
            wrp.val_y_max = 4.5 if is_tpb else 7.0

            return wrp

        is_tpb = 'LimitsTpB' in self.cwd
        x_title = 'T quark mass / GeV'
        prodchan = 'bW' if is_tpb else 'tZ'
        handness = 'L' if 'LH/Dat' in self.cwd else 'R'
        y_title = '|c^{%s}_{%s}|' % (prodchan, handness)
        th_vals = theory_xsec_tpb if is_tpb else theory_xsec_tpt
        gs = self.lookup_result('../LimitGraphs')
        gs = (mk_coupling_graph(g) for g in gs)
        self.result = varial.wrp.WrapperWrapper(list(gs))


########################################################### make toolchains ###
def mk_sense_chain(name,
                   cat_tokens,
                   signals,
                   hook=hook_loaded_histos,
                   model=get_model,
                   sys_pat=None,
                   filter_keyfunc=None,
                   asymptotic=False,
                   sig_inj_tuple=None):

    def loader_keyfunc(w):
        res = (w.name == 'vlq_mass'
            and ('_TH_' not in w.file_path or any(s in w.file_path for s in signals))
            and any(t in w.in_file_path for t in cat_tokens)
            and (not filter_keyfunc or filter_keyfunc(w))
        )
        return res

    hl = varial.tools.HistoLoader(
        filter_keyfunc=loader_keyfunc,
        hook_loaded_histos=hook,
    )

    limit_tools = [
        limits.ThetaLimits(
            input_path='../../HistoLoader',
            input_path_sys='../../HistoLoaderSys',
            model_func=lambda d: model(d, signals),
            cat_key=lambda w: w.category,
            sys_key=lambda w: w.sys_type,
            hook_loaded_histos=rebin_for_bb,
            asymptotic=asymptotic,
            pvalue_func=lambda m: limits.theta_auto.zvalue_approx(m, input='data', n=1)
        ),
        limits.ThetaLimits(
            input_path='../../HistoLoader',
            input_path_sys='../../HistoLoaderSys',
            model_func=lambda d: model(d, signals),
            cat_key=lambda w: w.category,
            sys_key=lambda w: w.sys_type,
            filter_keyfunc=lambda w: w.category == 'el',
            hook_loaded_histos=rebin_for_bb,
            asymptotic=asymptotic,
            postfit_func=lambda _: {},
            name='ThetaLimitsEl',
        ),
        limits.ThetaLimits(
            input_path='../../HistoLoader',
            input_path_sys='../../HistoLoaderSys',
            model_func=lambda d: model(d, signals),
            cat_key=lambda w: w.category,
            sys_key=lambda w: w.sys_type,
            filter_keyfunc=lambda w: w.category == 'mu',
            hook_loaded_histos=rebin_for_bb,
            asymptotic=asymptotic,
            postfit_func=lambda _: {},
            name='ThetaLimitsMu',
        ),
    ]

    if sig_inj_tuple:
        limit_tools = limit_tools[:1]  # only channel combination
        for lt in limit_tools:
            model = SigInjModel(*sig_inj_tuple)
            lt._sig_inj_model = model
            lt.model_func = lambda d: model.get_model_data_bkg(d, signals)
            lt.limit_func = lambda m: model.limit_func(m)
            lt.pvalue_func = lambda m: model.pvalue_func(m)
            lt.postfit_func = lambda m: model.postfit_func(m)

    limit_toolchain = varial.tools.ToolChainParallel('Theta', limit_tools)
    postfit_toolchain = varial.tools.ToolChainParallel('PostFitPulls', list(
        limits.ThetaPostFitPlot(
            '../../%s/%s' % (limit_toolchain.name, t.name),
            name=t.name,
        ) for t in limit_toolchain.tool_chain
    ))

    plotter_prefit = varial.tools.Plotter(
        filter_keyfunc=lambda w: '700' in w.sample
                                 or '1200' in w.sample
                                 or not w.is_signal,
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: '%s__%s' % (w.region, w.category)),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: '%s__%s' % (w.region, w.category),
        hook_canvas_post_build=canvas_hook_integrals,
        hook_loaded_histos=make_combo,
        name='PreFit',
    )

    def postfit_grouper(wrps):
        key = lambda w: '%s__%s' % (w.region, w.category)
        wrps = sorted(wrps, key=key)
        wrps = varial.gen.group(wrps, key)
        return wrps

    postfit_input = ['../HistoLoader', '../HistoLoaderSys'] if sys_pat else '../HistoLoader'

    plotter_postfit = varial.tools.Plotter(
        input_result_path=postfit_input,
        filter_keyfunc=lambda w: '700' in w.sample
                                 or '1200' in w.sample
                                 or not w.is_signal,
        plot_grouper=postfit_grouper,
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: '%s__%s' % (w.region, w.category),
        hook_canvas_post_build=canvas_hook_integrals,
        hook_loaded_histos=lambda ws: make_combo(scale_bkg_postfit(
            ws, '../%s/ThetaLimits' % limit_toolchain.name)),
        name='PostFit',
    )

    plotter_postfit_bins = varial.tools.Plotter(
        input_result_path=postfit_input,
        filter_keyfunc=lambda w: '700' in w.sample
                                 or '1200' in w.sample
                                 or not w.is_signal,
        plot_grouper=postfit_grouper,
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: '%s__%s' % (w.region, w.category),
        hook_canvas_post_build=canvas_hook_integrals,
        hook_loaded_histos=lambda ws: rebin_for_bb(make_combo(scale_bkg_postfit(
            ws, '../%s/ThetaLimits' % limit_toolchain.name)), True),
        name='PostFitBins',
    )

    limit_graph = limits.LimitGraphs(
        '../Theta/ThetaLimits', True, True, True,
        axis_labels = ('T mass / GeV', '#sigma #times BR(T->tH) / pb')
    )

    limit_graph_plot = varial.tools.Plotter(
        input_result_path='../LimitGraphs',
        plot_grouper=lambda ws: [ws],
        plot_setup=add_th_curve,
        name='LimitGraphsPlot',
    )

    limit_graph_plot_exp = varial.tools.Plotter(
        input_result_path='../LimitGraphs',
        plot_grouper=lambda ws: [ws],
        plot_setup=lambda ws: ws,
        filter_keyfunc=lambda w: w.legend != 'Obs 95% CL ',
        name='ExpLimitGraphsPlot',
    )

    coupling_limit = CouplingLimit()

    coupling_limit_plot = varial.tools.Plotter(
        input_result_path='../CouplingLimit',
        plot_grouper=lambda ws: [ws],
        plot_setup=lambda ws: ws,
        name='CouplingLimitPlot',
    )

    return varial.tools.ToolChain(name, [
            hl,
        ] + ([
            varial.tools.HistoLoader(
                pattern=sys_pat,
                filter_keyfunc=loader_keyfunc,
                hook_loaded_histos=hook_sys,
                name='HistoLoaderSys',
            )
        ] if sys_pat else []) + [
            limit_toolchain,
            postfit_toolchain,
            plotter_prefit,
            plotter_postfit,
            plotter_postfit_bins,
            limit_graph,
            limit_graph_plot,
            limit_graph_plot_exp,
            coupling_limit,
            coupling_limit_plot,
        ]
    )


def get_tc(name, signals):

    def filter_keyfunc_no_rate(w):
        return 'rate__' not in w.file_path

    def filter_keyfunc_no_rate_no_ht(w):
        return filter_keyfunc_no_rate(w) and 'HT__' not in w.file_path

    def filter_keyfunc_no_rate_no_jetpt(w):
        return filter_keyfunc_no_rate(w) and 'jet_pt__' not in w.file_path

    def filter_keyfunc_no_rate_no_jetpt_no_ht(w):
        return filter_keyfunc_no_rate_no_ht(w) and filter_keyfunc_no_rate_no_jetpt(w)

    sense_chains = [
        mk_sense_chain(
            'SignalRegionOnly',
            ['SignalRegion'],
            signals,
            asymptotic=True,
        ),
        mk_sense_chain(
            'DataBackground',
            ['SignalRegion', 'SidebandRegion'],
            signals,
            hook_loaded_histos_data_bkg,
            get_model_data_bkg,
            'VLQ2HT/Inputs/*/SysTreeProjectors/*/*.root',
            filter_keyfunc=filter_keyfunc_no_rate_no_jetpt_no_ht,
        ),
        mk_sense_chain(
            'DataBackgroundWithJetPtSys',
            ['SignalRegion', 'SidebandRegion'],
            signals,
            hook_loaded_histos_data_bkg,
            get_model_data_bkg,
            'VLQ2HT/Inputs/*/SysTreeProjectors/*/*.root',
            filter_keyfunc=filter_keyfunc_no_rate_no_ht,
        ),
        mk_sense_chain(
            'DataBackgroundWithHTSys',
            ['SignalRegion', 'SidebandRegion'],
            signals,
            hook_loaded_histos_data_bkg,
            get_model_data_bkg,
            'VLQ2HT/Inputs/*/SysTreeProjectors/*/*.root',
            filter_keyfunc=filter_keyfunc_no_rate_no_jetpt,
        ),
    ] + (list(
        mk_sense_chain(
            'DataBackgroundSigInj' + sig_inj[0],
            ['SignalRegion', 'SidebandRegion'],
            signals,
            hook_loaded_histos_data_bkg,
            get_model_data_bkg,
            sig_inj_tuple=sig_inj,
        )
        for sig_inj in (
            (signals[0], '4.0'),
            (signals[1], '3.0'),
            (signals[2], '2.0'),
            (signals[3], '1.0'),
            (signals[4], '1.0'),
            (signals[5], '1.0'),
            (signals[-3], '1.0'),
            (signals[-1], '1.0'),
        )
    ) if name == 'LimitsTpBLH' else [])

    return varial.tools.ToolChainParallel(name, sense_chains)
