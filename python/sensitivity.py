import common

import varial.tools


tc = varial.tools.ToolChain(
    "Sensitivity",
    [
        varial.tools.HistoLoader(
            filter_keyfunc=lambda w: w.in_file_path == 'SanityCheckEvent/HT',
            hook_loaded_histos=lambda w: common.merge_decay_channels(common.add_wrp_info(w)),
        ),
        varial.tools.Plotter(
            #plot_grouper=lambda w: (w,),
            save_name_func=lambda w: w._renderers[0].legend,
        )
    ]
)
