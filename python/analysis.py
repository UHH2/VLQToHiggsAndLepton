#!/usr/bin/env python


import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
#import sensitivity
import sframe_tools
import plot

import varial.main
import varial.tools


def mk_plot_tools():
    sframe_pat = map(lambda p: 'Main/%s/*.root' % p,
                     sframe_tools.sframe_tools.tool_paths())
    return list(
        varial.tools.ToolChainParallel(pat.split('/')[-2], plot.mk_tools(pat))
        for pat in sframe_pat
    )


tc = varial.tools.ToolChain(
    'Main',
    [
        sframe_tools.sframe_tools,
        varial.tools.ToolChainParallel(
            'Plots', lazy_eval_tools_func=mk_plot_tools),
        #sensitivity.tc,
        varial.tools.WebCreator(),
        #varial.tools.CopyTool('~/www/test'),
    ]
)


varial.settings.try_reuse_results = True
#varial.main.main(toolchain=tc)
varial.tools.Runner(tc, True)