import varial.tools
import os


all_methods = [
    'Cuts',
    'CutsD',
    'CutsPCA',
    'CutsSA',
    'BDT',
    # 'SVM',
    'GradBoost',
]
p='/afs/desy.de/user/t/tholenhe/xxl-af-cms/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsAndLepton/python/'


class Launcher(varial.tools.Tool):
    def run(self):
        os.system('cd '+self.cwd+'; python '+p+'tmva_script.py '+self.name+' > TMVA.out')


tc = varial.tools.ToolChainParallel(
    'TMVAParallel',
    list(Launcher(name=n) for n in all_methods)
)


if __name__ == '__main__':
    varial.tools.Runner(tc)
