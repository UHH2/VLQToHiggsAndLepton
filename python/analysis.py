#!/usr/bin/env python


import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as common
import sframe_tools
import overlays
# import sensitivity
import tex_content

import varial.extensions.make
import varial.extensions.git
import varial.tools
import os


dir_name = 'VLQ2HT'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'


tc = varial.tools.ToolChain(
    dir_name,
    [
        varial.extensions.make.Make([
            uhh_base + 'core',
            uhh_base + 'common',
            uhh_base + 'VLQSemiLepPreSel',
            uhh_base + 'VLQToHiggsAndLepton',
        ]),
        # varial.extensions.git.GitAdder(),
        # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        sframe_tools.sframe_tools,
        overlays.tc,
        # sensitivity.tc,
        # varial.tools.PrintToolTree(),
        varial.tools.WebCreator(),
        # tex_content.tex_content,
        # varial.tools.CopyTool('~/www/test'),
        # varial.extensions.git.GitTagger(commit_prefix='VLQ2HT'),
    ]
)


# varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
import varial.main
#varial.main.main(toolchain=tc, try_reuse_results=True)
