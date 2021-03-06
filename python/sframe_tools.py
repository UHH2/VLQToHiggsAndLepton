
import time
import os

from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
import varial.tools
import plot


disable_plots = True
n_wrkrs = 1


sframe_cfg = os.getenv('CMSSW_BASE') + \
             '/src/UHH2/VLQToHiggsAndLepton/config/VLQToHiggsAndLepton.xml'

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
        add_aliases_to_analysis=False,
    )

    hadd = Hadd('../SFrame/uhh2*', [
        'uhh2.AnalysisModuleRunner.DATA.Run2015D', 
        'uhh2.AnalysisModuleRunner.MC.WJets',
        'uhh2.AnalysisModuleRunner.MC.DYJets',
        'uhh2.AnalysisModuleRunner.MC.QCD',
        'uhh2.AnalysisModuleRunner.MC.SingleT',
    ])

    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lambda: plot.mk_tools(
            '%s/../Hadd/uhh*.root' % varial.analysis.cwd)
    )

    tc = varial.tools.ToolChain(
        catname,
        [sframe, hadd] if disable_plots else [sframe, hadd, plots]
    )
    return tc


def mk_merged_cat_plots(toolname, input_categories):
    def lazy_eval_func():
        # wait a bit, so that sframe tools can start working
        time.sleep(5)

        # wait for all sframe results to be available
        sframe_paths = map(
            lambda s: '%s../../%s/' % (varial.analysis.cwd, s),
            input_categories
        )
        while not all((
            os.path.exists(p + 'Hadd/Hadd (result available).log') and 
            os.path.exists(p + 'SFrame/SFrame (result available).log')
        ) for p in sframe_paths):
            #print 'Im here: ', varial.analysis.cwd
            #print 'Im checking: ', sframe_paths[0]
            time.sleep(2.)

        # make plotters and go
        input_pats = list(p + 'Hadd/uhh*.root' for p in sframe_paths )
        return [
            plot.cutflow_tables.mk_cutflow_chain(
                input_pats, plot.loader_hook_cat_merging),
            varial.tools.mk_rootfile_plotter(
                pattern=input_pats,
                name='VLQ2HT_stack',
                plotter_factory=plot.plotter_factory_stack_cat_merging,
                combine_files=True,
                auto_legend=False,
            )
        ]
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lazy_eval_func
    )
    tc = varial.tools.ToolChain(
        toolname,
        [] if disable_plots else [plots]
    )
    return tc


sframe_tools = varial.tools.ToolChainParallel(
    'EventLoopAndPlots',
    [
        mk_sframe_and_plot_tools('MakeFlatTuple'),
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htag'),
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagMassSB'),
#        mk_merged_cat_plots(
#            'AK8SoftDropCatAll',
#            [
#                'AK8SoftDropCat1htag',
#                'AK8SoftDropCat1htagMassSB',
#            ]
#        ),
#
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith1b'),
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith1bMassSB'),
#        mk_merged_cat_plots(
#            'AK8SoftDropCatAllWith1b',
#            [
#                'AK8SoftDropCat1htagWith1b',
#                'AK8SoftDropCat1htagWith1bMassSB',
#            ]
#        ),
#
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith0b'),
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith0bMassSB'),
#        mk_merged_cat_plots(
#            'AK8SoftDropCatAllAll',
#            [
#                'AK8SoftDropCat1htag',
#                'AK8SoftDropCat1htagMassSB',
#                'AK8SoftDropCat1htagWith1b',
#                'AK8SoftDropCat1htagWith1bMassSB',
#                'AK8SoftDropCat1htagWith0b',
#                'AK8SoftDropCat1htagWith0bMassSB',
#            ]
#        ),
#
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith1bMassPlus'),
#        mk_sframe_and_plot_tools('AK8SoftDropCat1htagWith0bMassPlus'),
    ],
    n_workers=n_wrkrs,
)
