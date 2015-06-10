
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


sframe_tools = varial.tools.ToolChainParallel(
    'EventLoopAndPlots',
    [
        mk_sframe_and_plot_tools('FilteredCat1htag'),
        mk_sframe_and_plot_tools('FilteredCat0h2btag'),
        mk_sframe_and_plot_tools('FilteredCat0h1btag'),
        mk_sframe_and_plot_tools('PrunedCat1htag'),
        mk_sframe_and_plot_tools('PrunedCat0h2btag'),
        mk_sframe_and_plot_tools('PrunedCat0h1btag'),
    ]
)