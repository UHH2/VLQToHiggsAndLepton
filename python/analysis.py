#!/usr/bin/env python


import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
#import sensitivity
import sframe_tools
import plot

import varial.tools
import os


dir_name = 'VLQ2HT'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'


def mk_plot_tools():
    sframe_pat = map(lambda p: '%s/%s/*.root' % (dir_name, p),
                     sframe_tools.sframe_tools.tool_paths())
    return list(
        varial.tools.ToolChainParallel(pat.split('/')[-2], plot.mk_tools(pat))
        for pat in sframe_pat
    )


tc = varial.tools.ToolChain(
    dir_name,
    [
        varial.tools.CompileTool([
            uhh_base + 'core',
            uhh_base + 'common',
            uhh_base + 'VLQSemiLepPreSel',
            uhh_base + 'VLQToHiggsAndLepton',
        ]),
        sframe_tools.sframe_tools,
        varial.tools.ToolChainParallel(
            'Plots', lazy_eval_tools_func=mk_plot_tools),
        #sensitivity.tc,
        varial.tools.WebCreator(),
        #varial.tools.CopyTool('~/www/test'),
    ]
)


varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
varial.tools.Runner(tc, True)