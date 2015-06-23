
import time
import os

from varial.extensions.sframeproxy import SFrame
import varial.tools
import plot


sframe_cfg = '/afs/desy.de/user/t/tholenhe/xxl-af-cms/' \
             'CMSSW_7_2_1_patch1/src/UHH2/VLQToHiggsAndLepton/' \
             'config/VLQToHiggsAndLepton.xml'


def set_category_func(catname):
    def do_set_cat(element_tree):
        user_config = element_tree.getroot().find('Cycle').find('UserConfig')
        for item in user_config:
            if item.get('Name') == 'category':
                item.set('Value', catname)
                break
    return do_set_cat


def mk_sframe_and_plot_tools(catname):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=set_category_func(catname),
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lambda: plot.mk_tools(
            '%s/../SFrame/*.root' % varial.analysis.cwd)
    )
    tc = varial.tools.ToolChain(
        catname,
        [sframe, plots]
    )
    return tc


def mk_merged_cat_plots(toolname, input_categories):
    def lazy_eval_func():
        # wait a bit, so that sframe tools can start working
        time.sleep(5)

        # wait for all sframe results to be available
        sframe_paths = map(
            lambda s: '%s../../%s/SFrame/' % (varial.analysis.cwd, s),
            input_categories
        )
        while not all(os.path.exists(p + 'SFrame (result available).log')
                      for p in sframe_paths):
            #print 'Im here: ', varial.analysis.cwd
            #print 'Im checking: ', sframe_paths[0]
            time.sleep(2.)

        # make plotters and go
        input_pats = list(p + '*.root' for p in sframe_paths )
        return [
            plot.cutflow_tables.mk_cutflow_chain(
                input_pats, plot.loader_hook_cat_merging),
            varial.tools.mk_rootfile_plotter(
                pattern=input_pats,
                name='VLQ2HT_stack',
                plotter_factory=plot.plotter_factory_stack_cat_merging,
                combine_files=True,
            )
        ]
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lazy_eval_func
    )
    tc = varial.tools.ToolChain(
        toolname,
        [plots]
    )
    return tc


sframe_tools = varial.tools.ToolChainParallel(
    'EventLoopAndPlots',
    [
        mk_sframe_and_plot_tools('FilteredCat1htag'),
        mk_sframe_and_plot_tools('FilteredCat0h2btag'),
        mk_sframe_and_plot_tools('FilteredCat0h1btag'),
        mk_sframe_and_plot_tools('PrunedCat1htag'),
        mk_sframe_and_plot_tools('PrunedCat0h2btag'),
        mk_sframe_and_plot_tools('PrunedCat0h1btag'),
        mk_merged_cat_plots(
            'FilteredAll',
            ['FilteredCat1htag', 'FilteredCat0h2btag', 'FilteredCat0h1btag']
        ),
        mk_merged_cat_plots(
            'PrunedAll',
            ['PrunedCat1htag', 'PrunedCat0h2btag', 'PrunedCat0h1btag']
        ),
    ]
)
