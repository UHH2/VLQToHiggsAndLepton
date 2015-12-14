from varial.extensions.limits import ThetaLimits, theta_auto
import UHH2.VLQSemiLepPreSel.common as common
import varial.tools
import math


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


def add_region_and_category(wrps):
    return varial.gen.gen_add_wrp_info(
        wrps, 
        region=lambda w: w.in_file_path.split('/')[0],
        category=lambda w: 'mu',
    )


def hook_loaded_histos(wrps):
    wrps = common.add_wrp_info(wrps)
    wrps = add_region_and_category(wrps)
    wrps = sorted(wrps, key=lambda w: '%s__%s' % (w.region, w.sample))
    # wrps = varial.gen.attribute_printer(wrps, 'region')
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
    model.add_lognormal_uncertainty('bkg_rate', math.log(2.), 'Bkg')
    # for s in varial.settings.my_lh_signals:
    #     model.add_lognormal_uncertainty(s+'_rate', math.log(1.15), s)
    return model


def hook_loaded_histos_data_bkg(wrps):
    wrps = hook_loaded_histos(wrps)
    wrps = (w for w in wrps if not w.is_background)
    wrps = list(w for w in wrps if not (
                                w.is_signal and w.region == 'SidebandRegion'))

    sigs = list(w for w in wrps if w.sample.startswith('Signal_'))
    sr, = list(w for w in wrps if w.is_data and w.region == 'SignalRegion')
    sb, = list(w for w in wrps if w.is_data and w.region == 'SidebandRegion')

    # re-interpret sideband histogram for fitting
    scale_factor = sr.obj.Integral() / sb.obj.Integral()
    sb = varial.op.prod([sb, varial.wrp.FloatWrapper(scale_factor)])
    sb.sample = 'Bkg'
    sb.legend = 'Sideband'
    sb.region = 'SignalRegion'
    sb.is_data = False
    sb.lumi = sr.lumi

    return sigs + [sb, sr]


def hook_sys(wrps):

    # assign information to wrappers: region, sys_type
    wrps = hook_loaded_histos(wrps)
    wrps = varial.gen.gen_add_wrp_info(
        wrps,
        sys_type=lambda w: w.file_path.split('/')[-2],
    )

    # group by sys_type, then apply original hook within every systematic
    keyfunc = lambda w: w.sys_type
    wrps = sorted(wrps, key=keyfunc)
    grps = varial.generators.group(wrps, keyfunc)
    wrps = (w for g in grps for w in hook_loaded_histos_data_bkg(g))

    # create closure-uncertainty
    mcs = varial.gen.dir_content('VLQ2HT/Inputs/TreeProjector/*.root')
    mcs = add_region_and_category(mcs)
    mcs = (w for w in mcs if w.region in ['SignalRegion', 'SidebandRegion'])
    mcs = (w for w in mcs if w.name == 'vlq_mass')
    mcs = varial.gen.load(mcs)
    mcs = (w for w in mcs if w.is_background)
    mcs = varial.gen.sort_group_merge(mcs, lambda w: w.region)
    mcs = dict((w.region, w) for w in mcs)
    assert len(mcs) == 2, 'need one for SignalRegion and one for SidebandRegion'
    ratio = varial.op.div((mcs['SignalRegion'], mcs['SidebandRegion']))
    bkg = list(
        w 
        for w in varial.ana.lookup_result('../HistoLoader') 
        if w.sample == 'Bkg'
    )[0]
    closure_ncrt_p = varial.op.prod((bkg, ratio))
    closure_ncrt_p.region = 'SidebandRegion'
    closure_ncrt_p.sys_type = 'closure_uncert__plus'
    closure_ncrt_m = varial.op.copy(bkg)
    closure_ncrt_m.region = 'SidebandRegion'
    closure_ncrt_m.sys_type = 'closure_uncert__minus'
    closure_ncrt = [closure_ncrt_p, closure_ncrt_m]

    # append closure uncert
    wrps = (w for grp in (wrps, closure_ncrt) for w in grp)
    return wrps


########################################################### make toolchains ###
def mk_sense_chain(name, 
                   cat_tokens, 
                   hook=hook_loaded_histos, 
                   model=get_model, 
                   sys_pat=None):
    loader = varial.tools.HistoLoader(
        filter_keyfunc=lambda w: (
            w.name == 'vlq_mass'
            and ('_TH_' not in w.file_path 
                    or any(s in w.file_path for s in varial.settings.my_lh_signals))
            and any(t in w.in_file_path for t in cat_tokens)
        ),
        hook_loaded_histos=hook,
    )
    plotter = varial.tools.Plotter(
        input_result_path='../HistoLoader',
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: w.region),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: w.region
    )
    limits = ThetaLimits(
        model_func=model,
        cat_key=lambda w: w.category,
        sys_key=lambda w: w.sys_type,
    )

    if sys_pat:
        sys_loader = varial.tools.HistoLoader(
            pattern=sys_pat,
            hook_loaded_histos=hook_sys,
            name='HistoLoaderSys',
        )
        tools = [loader, sys_loader, plotter, limits]
    else:
        tools = [loader, plotter, limits]

    return varial.tools.ToolChain(name, tools)


tc = varial.tools.ToolChainParallel(
    'Limits', [
        mk_sense_chain('SignalRegionOnly', ['SignalRegion']),
        # mk_sense_chain('SignalRegionAndSideband', ['SignalRegion', 'SidebandRegion']),
        mk_sense_chain(
            'DataBackground', 
            ['SignalRegion', 'SidebandRegion'], 
            hook_loaded_histos_data_bkg, 
            get_model_data_bkg, 
            'VLQ2HT/Inputs/SysTreeProjectors/*/*.root'
        ),
    ]
)
