import varial.extensions.tex

# base path
p_base = 'VLQ2HT/Outputs/'
ext = '.pdf'
target_ext = '.pdf'
varial.settings.rootfile_postfixes += ['.pdf']


######################################################## AutoContentObjects ###
def get4obj(chan):
    histos = 'pt_lin', 'eta_lin', 'phi_lin', 'number_lin'
    jet_histos = 'pt_jet_lin', 'eta_jet_lin', 'phi_jet_lin', 'number_lin'
    p = p_base + 'SFramePlots/Stacks/' + chan + 'Chan/'
    return {
        chan+'_muons'     : map((p+'SanityCheckMu/{}'+ext).format, histos),
        chan+'_electrons' : map((p+'SanityCheckEle/{}'+ext).format, histos),
        chan+'_jets'      : map((p+'SanityCheckJets/{}'+ext).format, jet_histos),
        chan+'_fwd_jets'  : map((p+'SanityCheckFwdJets/{}'+ext).format, jet_histos),
        chan+'_ak8_jets'  : map((p+'SanityCheckAK8Jets/{}'+ext).format, histos),
        chan+'_higg_jets' : map((p+'HiggsJetsAfterSel/{}'+ext).format, histos),
        chan+'_jet_pts'   : map((p+'SanityCheckJets/{}'+ext).format, 
            ('pt_1_lin', 'pt_2_lin', 'pt_3_lin', 'pt_4_lin', )
        ),
        chan+'_event'     : map((p+'SanityCheckEvent/{}'+ext).format, 
            ('N_PrimVertices_lin', 'N_TrueInteractions_lin', 'ST_lin', 'MET_lin', )
        ),
    }.items()

AutoContentObjects = varial.extensions.tex.TexContent(
    dict(get4obj('Mu') + get4obj('El')),
    include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
    name='AutoContentObjects',
)


##################################################### AutoContentTopHiggVlq ###
def get4thv(chan):
    p = p_base + 'SFramePlots/Stacks/' + chan + 'Chan/Nm1Selection/'
    return {
        chan+'_Nm1Sel_tlep': (
            p + 'tlep_eta_lin' + ext,
            p + 'tlep_pt_lin' + ext,
            p + 'tlep_mass_lin' + ext,
        ),
        chan+'_Nm1Sel_higg': (
            p + 'h_eta_lin' + ext,
            p + 'h_pt_lin' + ext,
            p + 'h_mass_lin' + ext,
        ),
        chan+'_Nm1Sel_vlq': (
            p + 'vlq_eta_lin' + ext,
            p + 'vlq_pt_lin' + ext,
            p + 'vlq_mass_lin' + ext,
        ),
    }.items()

AutoContentTopHiggVlq = varial.extensions.tex.TexContent(
    dict(get4thv('Mu') + get4thv('El')),
    include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
    name='AutoContentTopHiggVlq',
)


###################################################### AutoContentSelection ###
p_nm1 = p_base + 'SFramePlots/Stacks/%sChan/Nm1Selection/'

def get4sel(chan):
    p = p_nm1 % chan
    return {
        chan+'_twoDeeCut': (
            p + 'TwoDCut_QCD_lin' + ext,
            p + 'TwoDCut_TpB_TH_1200_lin' + ext,
        ),
        chan+'_firstblock': (            
            p + 'leading_jet_pt_lin' + ext,
            p + 'subleading_jet_pt_lin' + ext,
            p + 'primary_lepton_pt_lin' + ext,
            p + 'ST_lin' + ext,
        ),
        chan+'_secondblock': (
            p + 'event_chi2_log' + ext,
            p + 'dr_higg_top_lin' + ext,
            p + 'tlep_pt_lin' + ext,
            p + 'h_mass_lin' + ext,
        ),
    }.items()

img_2d_px = {
    'twoDeeCut_px': (
        (p_nm1 % 'El') + 'TwoDCut_px_log' + ext,
        (p_nm1 % 'Mu') + 'TwoDCut_px_log' + ext,
    ),
}.items()

def get4cf(chan):
    p = p_base + 'SFrameCutflow' + chan + '/CutflowTools/'
    return {
        chan+'_cutflow_tabular.tex':
            p + 'CutflowTableTex/cutflow_tabular.tex',
        chan+'_cutflow_stack'+target_ext:
            p + 'CutflowStack/cutflow_log'+ext,
    }.items()

AutoContentSelection = varial.extensions.tex.TexContent(
    dict(get4sel('Mu') + get4sel('El') + img_2d_px),
    dict(get4cf('Mu') + get4cf('El')),
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentSelection',
)


####################################################### AutoContentSideband ###
def get4sb(chan):
    p_sel = p_base + 'Selections' + chan + '/Stacks/'
    p_baseline = p_sel + 'BaseLineSelection/'

    return {
        chan+'_variables': (
            p_baseline+'n_fwd_jets_lin'+ext,
            p_baseline+'h_n_subjet_btags_lin'+ext,
            p_base+'Sidebands'+chan+'/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin'+ext,
        ),
        chan+'_comparison': (
            p_sel+'SidebandRegion/vlq_mass_lin'+ext,
            p_sel+'SignalRegion/vlq_mass_lin'+ext,
        ),
    }.items()

AutoContentSideband = varial.extensions.tex.TexContent(
    dict(get4sb('Mu') + get4sb('El')),
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentSideband',
)


######################################################### AutoContentLimits ###
p_lim = p_base + 'Limits/DataBackground/'
img_lim = {
    'El_limits': (
        p_lim+'PostFit/SignalRegion__el_lin'+ext,
        p_lim+'Theta/ThetaLimitsEl/plots/limit_band_plot-log-bayesian.png',
    ),
    'Mu_limits': (
        p_lim+'PostFit/SignalRegion__mu_lin'+ext,
        p_lim+'Theta/ThetaLimitsMu/plots/limit_band_plot-log-bayesian.png',
    ),
    'Comb_limits': (
        p_lim+'Theta/ThetaLimits/plots/limit_band_plot-log-bayesian.png',
    ),
    'pulls': (
        p_lim+'PostFitPulls/ThetaLimits/cnv_post_fit_Signal_TpB_TH_LH_M1000.pdf',
    ),
}

lim_tabs = {
    'sysrate_tables_el.tex': p_lim+'Theta/ThetaLimits/sysrate_tables_el.tex',
    'sysrate_tables_mu.tex': p_lim+'Theta/ThetaLimits/sysrate_tables_mu.tex',
}

AutoContentLimits = varial.extensions.tex.TexContent(
    img_lim,
    lim_tabs,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentLimits',
)


############################################################ AutoContentPAS ###
pas_block = {
    'selection_block': (
        p_base + 'SFramePlots/Stacks/ElChan/SanityCheckEle/pt_lin.pdf',
        p_base + 'SFramePlots/Stacks/MuChan/SanityCheckMu/pt_lin.pdf',
        p_base + 'SFramePlots/Stacks/ElChan/Nm1Selection/ST_lin.pdf',
        p_base + 'SFramePlots/Stacks/MuChan/Nm1Selection/h_mass_lin.pdf',
    ),   
}

pas_single = {
    'tlep_mass_lin.pdf': p_base + 'SFramePlots/Stacks/MuChan/Nm1Selection/tlep_mass_lin.pdf',
    'tlep_pt_lin.pdf': p_base + 'SFramePlots/Stacks/MuChan/Nm1Selection/tlep_pt_lin.pdf',
    'SignalRegion__el_lin.pdf': p_base + 'Limits/SignalRegionOnly/PreFit/SignalRegion__el_lin.pdf',
    'SignalRegion__mu_lin.pdf': p_base + 'Limits/SignalRegionOnly/PreFit/SignalRegion__mu_lin.pdf',
    'SignalRegion_bkg__el_lin.pdf': p_base + 'Limits/DataBackground/PostFit/SignalRegion__el_lin.pdf',
    'SignalRegion_bkg__mu_lin.pdf': p_base + 'Limits/DataBackground/PostFit/SignalRegion__mu_lin.pdf',
    'Sideband__el_lin.pdf': p_base + 'SelectionsEl/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband__mu_lin.pdf': p_base + 'SelectionsMu/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__el.pdf': p_base+'SidebandsEl/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__mu.pdf': p_base+'SidebandsMu/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin.pdf',
    'limits.png': p_lim+'Theta/ThetaLimits/plots/limit_band_plot-log-bayesian.png',
}.items()
AutoContentPAS_img = varial.extensions.tex.TexContent(
    pas_block,
    dict(pas_single + lim_tabs.items()),
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='img',
)


###############################################################################


################################################################# toolchain ###
tc = varial.tools.ToolChainParallel(
    'Tex', 
    [
        AutoContentTopHiggVlq,
        AutoContentObjects,
        AutoContentSideband,
        AutoContentSelection,
        AutoContentLimits,
        AutoContentPAS_img,
    ]
)
