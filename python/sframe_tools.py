
from varial.extensions.sframeproxy import SFrameProcess
import varial.tools


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


sframe_tools = varial.tools.ToolChain(
    'SFrame',
    [
        SFrameProcess(
            cfg_filename=sframe_cfg,
            xml_tree_callback=set_category_func('1htag'),
            name='Cat1htag',
        )
    ]
)