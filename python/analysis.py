#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import os


dir_name = 'VLQ2HT'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
input_pat = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/samples/uhh2*.root'

varial.settings.my_lh_signals = [
    'Signal_TpB_TH_LH_M0700',
    'Signal_TpB_TH_LH_M1200',
    'Signal_TpB_TH_LH_M1700',
]
varial.settings.my_rh_signals = [
    'Signal_TpB_TH_RH_M0700',
    'Signal_TpB_TH_RH_M1300',
    'Signal_TpB_TH_RH_M1700',
]


# these imports might need the settings above
import sideband_overlays
import lep_plus_minus
#import sframe_tools
import tree_project
import sensitivity
import tex_content
import plot


hadd = Hadd(
    input_pat, 
    [
        'uhh2.AnalysisModuleRunner.DATA.Run2015D', 
        'uhh2.AnalysisModuleRunner.MC.TTbar',
        'uhh2.AnalysisModuleRunner.MC.WJets',
        'uhh2.AnalysisModuleRunner.MC.DYJets',
        'uhh2.AnalysisModuleRunner.MC.QCD',
        'uhh2.AnalysisModuleRunner.MC.SingleT',
    ], 
    add_aliases_to_analysis=False,
    samplename_func=common.get_samplename
)


tc = varial.tools.ToolChain(
    dir_name,
    [
        # varial.extensions.make.Make([
        #     uhh_base + 'core',
        #     uhh_base + 'common',
        #     uhh_base + 'VLQSemiLepPreSel',
        #     uhh_base + 'VLQToHiggsAndLepton',
        # ]),
        # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        # sframe_tools.sframe_tools,
        
        varial.tools.ToolChain(
            'Inputs', [
                tree_project.mk_tp(input_pat),
                hadd,
            ]
        ),
        varial.tools.ToolChainParallel(
            'Histograms', [
                plot.mk_toolchain('Selections', '%s/Inputs/TreeProjector/*.root' % dir_name),
                plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name, cutflow=True),
                sideband_overlays.tc,
                lep_plus_minus.pltr,
                sensitivity.tc,
            ]
        ),

        # varial.tools.PrintToolTree(),
        varial.tools.WebCreator(),
        tex_content.tc,
        varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
    ]
)


varial.settings.try_reuse_results = True
# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
import varial.main
varial.main.main(toolchain=tc)
