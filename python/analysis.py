#!/usr/bin/env python

print 'importing modules.'
import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import os
ToolChain = varial.tools.ToolChain
ToolChainParallel = varial.tools.ToolChainParallel


# varial.rnd.default_decorators += [
#     varial.rnd.TitleBox(text='2.3 fb^{-1} (13 TeV)')
# ]
varial.settings.defaults_BottomPlot['poisson_errs'] = True
varial.settings.defaults_Legend['text_size'] = 0.035
varial.ROOT.gStyle.SetPadTopMargin(0.1)
varial.settings.canvas_size_x = 600
varial.settings.canvas_size_y = 500

dir_name = 'VLQ2HT_full_baseline'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
# input_pat = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/samples_74X/uhh2*.root'
input_pat = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/samples_full_baseline/uhh2*.root'

varial.settings.my_lh_signals = [
    'Signal_TpB_TH_LH_M0700',
    'Signal_TpB_TH_LH_M0800',
    'Signal_TpB_TH_LH_M0900',
    'Signal_TpB_TH_LH_M1000',
    'Signal_TpB_TH_LH_M1100',
    'Signal_TpB_TH_LH_M1200',
    # 'Signal_TpB_TH_LH_M1300',
    'Signal_TpB_TH_LH_M1400',
    'Signal_TpB_TH_LH_M1500',
    # 'Signal_TpB_TH_LH_M1600',
    'Signal_TpB_TH_LH_M1700',
    'Signal_TpB_TH_LH_M1800',
]
varial.settings.my_rh_signals = [
    'Signal_TpB_TH_RH_M0700',
    'Signal_TpB_TH_RH_M0800',
    'Signal_TpB_TH_RH_M0900',
    'Signal_TpB_TH_RH_M1000',
    'Signal_TpB_TH_RH_M1100',
    'Signal_TpB_TH_RH_M1200',
    'Signal_TpB_TH_RH_M1300',
    'Signal_TpB_TH_RH_M1400',
    'Signal_TpB_TH_RH_M1500',
    'Signal_TpB_TH_RH_M1600',
    'Signal_TpB_TH_RH_M1700',
    'Signal_TpB_TH_RH_M1800',
]
varial.settings.tpt_lh_signals = [
    'Signal_TpT_TH_LH_M0700',
    'Signal_TpT_TH_LH_M0800',
    'Signal_TpT_TH_LH_M0900',
    'Signal_TpT_TH_LH_M1000',
    'Signal_TpT_TH_LH_M1100',
    'Signal_TpT_TH_LH_M1200',
    'Signal_TpT_TH_LH_M1300',
    'Signal_TpT_TH_LH_M1500',
    'Signal_TpT_TH_LH_M1600',
    'Signal_TpT_TH_LH_M1700',
    'Signal_TpT_TH_LH_M1800',
]
varial.settings.tpt_rh_signals = [
    'Signal_TpT_TH_RH_M0700',
    'Signal_TpT_TH_RH_M0800',
    'Signal_TpT_TH_RH_M0900',
    'Signal_TpT_TH_RH_M1000',
    'Signal_TpT_TH_RH_M1100',
    'Signal_TpT_TH_RH_M1200',
    'Signal_TpT_TH_RH_M1300',
    'Signal_TpT_TH_RH_M1400',
    'Signal_TpT_TH_RH_M1500',
    'Signal_TpT_TH_RH_M1600',
    'Signal_TpT_TH_RH_M1700',
    'Signal_TpT_TH_RH_M1800',
]
varial.settings.all_signals = (
    varial.settings.my_lh_signals +
    varial.settings.my_rh_signals +
    varial.settings.tpt_lh_signals +
    varial.settings.tpt_rh_signals
)


varial.settings.defaults_BottomPlot['force_y_range'] = True

varial.settings.pretty_names.update({
     'no sel._tex':                 r'no sel.',
     'trigger_accept_tex':          r'trigger',
     '2D cut_tex':                  r'2D-iso',
     'primary_lepton_pt_tex':       r'lep. \pt',
     'leading_jet_pt_tex':          r'1st jet \pt',
     'subleading_jet_pt_tex':       r'2nd jet \pt',
     'ST_tex':                      r'ST',
     'event_chi2_tex':              r'$\chi^2$',
     'dr_higg_top_tex':             r'$\Delta R(H, t)$',
     'tlep_pt_tex':                 r't \pt',
     'h_mass_tex':                  r'$M(H)$',
     '1000 X output/input_tex':     r'$\epsilon$ * 1000',
})


# these imports might need the settings above
import sideband_overlays
import lep_plus_minus
# import sframe_tools
import tree_project
import yields_n_eff
import sensitivity
import tex_content
import fit_w_peak
import plot

print 'setting up tools.'
hadd = Hadd(
    input_pat,
    [
        'uhh2.AnalysisModuleRunner.DATA.Run2015D',
        'uhh2.AnalysisModuleRunner.MC.TTbar',
        'uhh2.AnalysisModuleRunner.MC.WJets',
        'uhh2.AnalysisModuleRunner.MC.DYJets',
        'uhh2.AnalysisModuleRunner.MC.QCD',
        'uhh2.AnalysisModuleRunner.MC.SingleT',
        'uhh2.AnalysisModuleRunner.MC.TpB_TH_0700',
        'uhh2.AnalysisModuleRunner.MC.TpB_TH_1200',
        'uhh2.AnalysisModuleRunner.MC.TpB_TH_1700',
    ] + list(
        'uhh2.AnalysisModuleRunner.MC.Signal_TpB_TH_LH_M' + num
        for num in ('0700', '1200', '1700')
    ) + list(
        'uhh2.AnalysisModuleRunner.MC.Signal_TpB_TH_RH_M' + num
        for num in ('0700', '1300', '1700')
    ),
    cmd='hadd -f -v 1 -T',
    add_aliases_to_analysis=False,
    samplename_func=common.get_samplename,
)

post_build_funcs_only_legend = [
    varial.rnd.mk_legend_func(),
]

tc = ToolChain(dir_name, [
    # varial.extensions.make.Make([
    #     uhh_base + 'core',
    #     uhh_base + 'common',
    #     uhh_base + 'VLQSemiLepPreSel',
    #     uhh_base + 'VLQToHiggsAndLepton',
    # ]),
    # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
    # sframe_tools.sframe_tools,

    ToolChainParallel('Inputs', [
#         ToolChainParallel('El', [
#             tree_project.mk_tp(input_pat, ['trigger_accept_el > 0.5']),
#             tree_project.mk_sys_tps(['trigger_accept_el > 0.5']),
#         ], n_workers=1),
#         ToolChainParallel('Mu', [
#             tree_project.mk_tp(input_pat, ['trigger_accept_mu > 0.5']),
#             tree_project.mk_sys_tps(['trigger_accept_mu > 0.5']),
#         ], n_workers=1),
        hadd,
    ], n_workers=1),

    ] + ([
    ToolChainParallel('Outputs', [
        # plot.mk_toolchain('SelectionsFwdEl', '%s/Inputs/El/TreeProjector/*.root'%dir_name,
        #     filter_keyfunc=lambda w: 'FwdSelection' in w.in_file_path),  #, keep_content_as_result=True),
        # plot.mk_toolchain('SelectionsFwdMu', '%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
        #     filter_keyfunc=lambda w: 'FwdSelection' in w.in_file_path),  #, keep_content_as_result=True),
        # plot.mk_toolchain('SelectionsFwdComb', '%s/Inputs/*/TreeProjector/*.root'%dir_name,
        #    filter_keyfunc=lambda w: 'FwdSelection' in w.in_file_path),  #, keep_content_as_result=True),
#         plot.mk_toolchain('SelectionsEl', ['%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/El/SysTreeProjectors/*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsMu', ['%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/Mu/SysTreeProjectors/*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsElNoFwdSys',
#             [
#                 '%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                 '%s/Inputs/El/SysTreeProjectors/*/*.root'%dir_name
#             ],
#             filter_keyfunc=lambda w: 'rate_fwdjet__' not in w.file_path,
#         ),
#         plot.mk_toolchain('SelectionsMuNoFwdSys',
#             [
#                 '%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                 '%s/Inputs/Mu/SysTreeProjectors/*/*.root'%dir_name
#             ],
#             filter_keyfunc=lambda w: 'rate_fwdjet__' not in w.file_path,
#         ),
#         plot.mk_toolchain('SelectionsElNoData',
#             [
#                 '%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                 '%s/Inputs/El/SysTreeProjectors/*/*.root'%dir_name
#             ],
#             filter_keyfunc=lambda w: 'Run2015' not in w.file_path,
#             canvas_post_build_funcs=post_build_funcs_only_legend,
#         ),
#         plot.mk_toolchain('SelectionsMuNoData',
#             [
#                 '%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                 '%s/Inputs/Mu/SysTreeProjectors/*/*.root'%dir_name
#             ],
#             filter_keyfunc=lambda w: 'Run2015' not in w.file_path,
#             canvas_post_build_funcs=post_build_funcs_only_legend,
#         ),
#         plot.mk_toolchain('SelectionsElJetPT', ['%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/El/SysTreeProjectors/jet_pt__*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsMuJetPT', ['%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/Mu/SysTreeProjectors/jet_pt__*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsElJERC', ['%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/El/SysTreeProjectors/JE*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsMuJERC', ['%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/Mu/SysTreeProjectors/JE*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsElbtag', ['%s/Inputs/El/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/El/SysTreeProjectors/b_tag_*/*.root'%dir_name]),
#         plot.mk_toolchain('SelectionsMubtag', ['%s/Inputs/Mu/TreeProjector/*.root'%dir_name,
#                                               '%s/Inputs/Mu/SysTreeProjectors/b_tag_*/*.root'%dir_name]),
        plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name),
        plot.mk_cutflowchain('SFrameCutflowEl', '%s/Inputs/Hadd/*.root' % dir_name, lambda w: 'ElChan/' in w.in_file_path),
        plot.mk_cutflowchain('SFrameCutflowMu', '%s/Inputs/Hadd/*.root' % dir_name, lambda w: 'MuChan/' in w.in_file_path),
#         sideband_overlays.get_tc('%s/Inputs/El'%dir_name),
#         sideband_overlays.get_tc('%s/Inputs/Mu'%dir_name),
        # fit_w_peak.WPeakFitter(),
        # fit_w_peak.tc_sys_comp,
        # lep_plus_minus.pltr,
#         sensitivity.get_tc('LimitsTpBLH', varial.settings.my_lh_signals),
#         sensitivity.get_tc('LimitsTpBRH', varial.settings.my_rh_signals),
#         sensitivity.get_tc('LimitsTpTLH', varial.settings.tpt_lh_signals),
#         sensitivity.get_tc('LimitsTpTRH', varial.settings.tpt_rh_signals),
    ]),
#     sensitivity.PValueCollector(),
#     sensitivity.BetaSignalCollector(),
#     yields_n_eff.EffNumTable(),
#     yields_n_eff.SigEffGraph(),
#     yields_n_eff.sig_eff_grph_pltr,
    # varial.tools.PrintToolTree(),
    varial.tools.WebCreator(),
#     tex_content.tc,
#     varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
    ] if True else []) + [
])

print 'starting.'

varial.settings.try_reuse_results = True
import varial.main
varial.main.main(toolchain=tc)
