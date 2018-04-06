#!/usr/bin/env python

##################################### definition of UserConfig item changes ###

sys_uncerts = {
    # 'name' : {'item name': 'item value', ...},
    'jec_up'         : {'jecsmear_direction':'up'},
    'jec_down'       : {'jecsmear_direction':'down'},
    'jer_up'         : {'jersmear_direction':'up'},
    'jer_down'       : {'jersmear_direction':'down'},
    'SCALE_upup'     : {'ScaleVariationMuR':'up','ScaleVariationMuF':'up'},
    'SCALE_upnone'   : {'ScaleVariationMuR':'up','ScaleVariationMuF':'none'},
    'SCALE_noneup'   : {'ScaleVariationMuR':'none','ScaleVariationMuF':'up'},
    'SCALE_nonedown' : {'ScaleVariationMuR':'none','ScaleVariationMuF':'down'},
    'SCALE_downnone' : {'ScaleVariationMuR':'down','ScaleVariationMuF':'none'},
    'SCALE_downdown' : {'ScaleVariationMuR':'down','ScaleVariationMuF':'down'},
    # 'jer_jec_up'    : {'jersmear_direction':'up','jecsmear_direction':'up'},
    # 'jer_jec_down'  : {'jersmear_direction':'down','jecsmear_direction':'down'},
}
start_all_parallel = True

############################################################### script code ###
import varial
import sys
import os


if len(sys.argv) != 2:
    print 'Plz. give me da name of da sframe-config! ... dude!'
    exit(-1)


def set_uncert_func(uncert_name):
    uncert = sys_uncerts[uncert_name]
    def do_set_uncert(element_tree):
        cycle = element_tree.getroot().find('Cycle')
        user_config = cycle.find('UserConfig')
        output_dir = cycle.get('OutputDirectory')
        cycle.set('OutputDirectory', os.path.join(output_dir, uncert_name))

        for name, value in uncert.iteritems():
            uc_item = list(i for i in user_config if i.get('Name') == name)
            assert uc_item, 'could not find item with name: %s' % name
            uc_item[0].set('Value', value)

    return do_set_uncert


from varial.extensions.sframe import SFrame
from varial import tools
if start_all_parallel:
    ToolChain = tools.ToolChainParallel
else:
    ToolChain = tools.ToolChain


class MySFrameBatch(SFrame):

    def configure(self):
        self.xml_doctype = self.xml_doctype + """
<!--
   <ConfigParse NEventsBreak="100000" FileSplit="0" AutoResubmit="0" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="svenja.schumann@desy.de" Notification="as" Workdir="workdir"/>
-->
"""
        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt


sframe_tools = ToolChain(
    'SFrameUncerts',
    list(
        MySFrameBatch(
            cfg_filename=sys.argv[1],
            xml_tree_callback=set_uncert_func(uncert),
            name='SFrame_' + uncert,
            halt_on_exception=False,
        ) 
        for uncert in sys_uncerts
    )
)


if __name__ == '__main__':
    varial.tools.Runner(sframe_tools)
