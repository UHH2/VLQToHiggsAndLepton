import varial.extensions.tex

# base path
p = 'VLQ2HT/Histograms/'
ext = '.png'
target_ext = '.png'


######################################################## AutoContentObjects ###
p_ana = p + 'SFramePlots/VLQ2HT_stack/'
histos = 'pt_lin', 'eta_lin', 'phi_lin', 'number_lin'
jet_histos = 'pt_jet_lin', 'eta_jet_lin', 'phi_jet_lin', 'number_lin'

images = {
    'muons'     : map((p_ana+'SanityCheckMu/{}'+ext).format, histos),
    'electrons' : map((p_ana+'SanityCheckEle/{}'+ext).format, histos),
    'jets'      : map((p_ana+'SanityCheckJets/{}'+ext).format, jet_histos),
    'fwd_jets'  : map((p_ana+'SanityCheckFwdJets/{}'+ext).format, jet_histos),
    'ak8_jets'  : map((p_ana+'SanityCheckAK8Jets/{}'+ext).format, histos),
    'higg_jets' : map((p_ana+'HiggsJetsAfterSel/{}'+ext).format, histos),
    'jet_pts'   : map((p_ana+'SanityCheckJets/{}'+ext).format, 
        ('pt_1_lin', 'pt_2_lin', 'pt_3_lin', 'pt_4_lin', )
    ),
    'event'     : map((p_ana+'SanityCheckEvent/{}'+ext).format, 
        ('N_PrimVertices_lin', 'N_TrueInteractions_lin', 'ST_lin', 'MET_lin', )
    ),
}
AutoContentObjects = varial.extensions.tex.TexContent(
    images,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentObjects',
)


##################################################### AutoContentTopHiggVlq ###
p_nm1sel = p + 'SFramePlots/VLQ2HT_stack/Nm1Selection/'
images = {
    'p_Nm1Sel_tlep': (
        p_nm1sel + 'tlep_eta_lin' + ext,
        p_nm1sel + 'tlep_pt_lin' + ext,
        p_nm1sel + 'tlep_mass_lin' + ext,
    ),
    'p_Nm1Sel_higg': (
        p_nm1sel + 'h_eta_lin' + ext,
        p_nm1sel + 'h_pt_lin' + ext,
        p_nm1sel + 'h_mass_lin' + ext,
    ),
    'p_Nm1Sel_vlq': (
        p_nm1sel + 'vlq_eta_lin' + ext,
        p_nm1sel + 'vlq_pt_lin' + ext,
        p_nm1sel + 'vlq_mass_lin' + ext,
    ),
}
AutoContentTopHiggVlq = varial.extensions.tex.TexContent(
    images,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentTopHiggVlq',
)


###################################################### AutoContentSelection ###
p_cutflow = p + 'SFramePlots/CutflowTools/'
images = {
    'twoDeeCut': (
        p_nm1sel + 'TwoDCut_QCD_lin' + ext,
        p_nm1sel + 'TwoDCut_TpB_TH_1200_0_lin' + ext,
    ),
    'firstblock': (
        p_nm1sel + 'trigger_accept_lin' + ext,
        p_nm1sel + 'primary_lepton_pt_lin' + ext,
        p_nm1sel + 'leading_jet_pt_lin' + ext,
        p_nm1sel + 'ST_lin' + ext,
    ),
    'secondblock': (
        p_nm1sel + 'event_chi2_lin' + ext,
        p_nm1sel + 'dr_higg_top_lin' + ext,
        p_nm1sel + 'tlep_pt_lin' + ext,
        p_nm1sel + 'h_mass_lin' + ext,
    ),
}
plain_files = {
    'p_cutflow_tabular.tex':
        p_cutflow + 'CutflowTableTex/cutflow_tabular.tex',
    'p_cutflow_stack'+target_ext:
        p_cutflow + 'CutflowStack/cutflow_lin'+ext,
}
AutoContentSelection = varial.extensions.tex.TexContent(
    images,
    plain_files,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentSelection',
)


####################################################### AutoContentSideband ###
p_sel = p + 'Selections/VLQ2HT_stack/'
p_baseline = p_sel + 'BaseLineSelection/'
images = {
    'variables': (
        p_baseline+'n_fwd_jets_lin'+ext,
        p_baseline+'h_n_subjet_btags_lin'+ext,
        p_baseline+'tlep_mass_lin'+ext,
        p+'Sidebands/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin'+ext,
    ),
    'comparison': (
        p_sel+'SidebandRegion/vlq_mass_lin'+ext,
        p_sel+'SignalRegion/vlq_mass_lin'+ext,
    ),
}
AutoContentSideband = varial.extensions.tex.TexContent(
    images,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentSideband',
)


######################################################### AutoContentLimits ###
p_lim = p + 'Limits/DataBackground/'
images = {
    'limits': (
        p_lim+'Plotter/SignalRegion_lin'+ext,
        p_lim+'ThetaLimits/plots/limit_band_plot-log-acls'+ext,
    ),
}
AutoContentLimits = varial.extensions.tex.TexContent(
    images,
    include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
    name='AutoContentLimits',
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
    ]
)
