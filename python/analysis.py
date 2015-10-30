#!/usr/bin/env python


import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
#import sframe_tools
import sideband_overlays
import tree_project
import sensitivity
import tex_content
import plot

from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.extensions.git
import varial.tools
import os


dir_name = 'VLQ2HT'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
input_pat = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/samples/uhh2*.root'

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
        # varial.extensions.git.GitAdder(),
        # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        # sframe_tools.sframe_tools,
        
        varial.tools.ToolChainParallel(
            'Inputs', [
                tree_project.mk_tp(input_pat),
                hadd,
            ]
        ),
        varial.tools.ToolChainParallel(
            'Histograms', [
                plot.mk_toolchain('Selections', '%s/Inputs/TreeProjector/*.root' % dir_name),
                plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name),
                sideband_overlays.tc,
                sensitivity.tc,
            ]
        ),

        # varial.tools.PrintToolTree(),
        varial.tools.WebCreator(),
        # tex_content.tex_content,
        varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
        # varial.extensions.git.GitTagger(commit_prefix='VLQ2HT'),
    ]
)


varial.settings.try_reuse_results = True
# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
import varial.main
varial.main.main(toolchain=tc)
