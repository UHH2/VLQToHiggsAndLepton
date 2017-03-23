import glob
import ROOT
import sys
ROOT.gROOT.SetBatch(True)
ROOT.TMVA.Tools.Instance()

# prepare inputs
p = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/samples/'

f_sig = ROOT.TFile(p + 'uhh2.AnalysisModuleRunner.MC.Signal_TpB_TH_LH_M1000_0.root')
t_sig = f_sig.Get('AnalysisTree')

fs_bkg = list(ROOT.TFile(k) for t in ('*TTbar_*', '*QCD_*', '*WJets_*') for k in glob.glob(p+t))
ts_bkg = list(b.Get('AnalysisTree') for b in fs_bkg)

#variables = list(b.GetName() for b in t_bkg.GetListOfBranches())
#variables.remove('weight')
#variables.remove('vlq_mass')

#variables = ['n_leptons', 'n_btags', 'n_higgs_tags']
#variables = ['leading_jet_pt', 'subleading_jet_pt', 'vlq_pt', 'vlq_eta']
variables = [
    # 'dr_higg_top',
    'h_mass',
    'h_pt',
    'tlep_pt',
    'ST',
    #'vlq_mass',
]

print variables
# prepare stuff
f_out = ROOT.TFile('TMVA.root', 'RECREATE')
factory = ROOT.TMVA.Factory(
    'TMVAClassification',
    f_out,
    '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification'
)
for var in variables:
    typ = {int: 'I', float: 'F'}[type(getattr(t_sig, var))]
    if var.endswith('eta'):
        var = 'abs(%s)' % var
    factory.AddVariable(var, var, 'units', typ)
factory.AddSpectator('vlq_mass', 'vlq_mass', 'units')

factory.AddSignalTree(t_sig, 1.0)
factory.SetSignalWeightExpression('weight')

for t in ts_bkg:
    factory.AddBackgroundTree(t, 1.0)
factory.SetBackgroundWeightExpression('weight')
factory.PrepareTrainingAndTestTree(
    ROOT.TCut('(TwoDCut_ptrel > 40. || TwoDCut_dr > 0.4) && trigger_accept > 0.5'),
    'SplitMode=random:!V'
)

if 'Cuts' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kCuts,
        'Cuts',
        '!H:!V:FitMethod=GA:EffSel'
        #':VarProp[0]=FSmart'
        #':VarProp[1]=FSmart'
        #':VarProp[2]=FSmart'
        #':VarProp[3]=FSmart'
        #':VarProp[4]=FSmart'
        ':CutRangeMin[0]=60:CutRangeMax[0]=120:VarProp[0]=FMin'
        ':CutRangeMin[1]=200:CutRangeMax[1]=1000:VarProp[1]=FMin'
        ':CutRangeMin[2]=0:CutRangeMax[2]=1000:VarProp[2]=FMin'
        ':CutRangeMin[3]=300:CutRangeMax[3]=2000:VarProp[3]=FMin'
        #':CutRangeMin[4]=0:CutRangeMax[4]=50:VarProp[4]=FMin'
        ':SampleSize=200000'
    )

if 'CutsD' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kCuts,
        'CutsD',
        '!H:!V:FitMethod=GA:EffSel'
        ':VarTransform=Decorrelate'
        #':VarProp[0]=FSmart'
        #':VarProp[1]=FSmart'
        #':VarProp[2]=FSmart'
        #':VarProp[3]=FSmart'
        #':VarProp[4]=FSmart'
        ':CutRangeMin[0]=60:CutRangeMax[0]=120:VarProp[0]=FMin'
        ':CutRangeMin[1]=200:CutRangeMax[1]=1000:VarProp[1]=FMin'
        ':CutRangeMin[2]=0:CutRangeMax[2]=1000:VarProp[2]=FMin'
        ':CutRangeMin[3]=300:CutRangeMax[3]=2000:VarProp[3]=FMin'
        #':CutRangeMin[4]=0:CutRangeMax[4]=50:VarProp[4]=FMin'
        #':CutRangeMin[5]=0:CutRangeMax[5]=50000:VarProp[5]=FMax'
        ':SampleSize=200000'
    )

if 'CutsPCA' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kCuts,
        'CutsPCA',
        '!H:!V:FitMethod=GA:EffSel'
        ':VarTransform=PCA'
        #':VarProp[0]=FSmart'
        #':VarProp[1]=FSmart'
        #':VarProp[2]=FSmart'
        #':VarProp[3]=FSmart'
        #':VarProp[4]=FSmart'
        ':CutRangeMin[0]=60:CutRangeMax[0]=120:VarProp[0]=FMin'
        ':CutRangeMin[1]=200:CutRangeMax[1]=1000:VarProp[1]=FMin'
        ':CutRangeMin[2]=0:CutRangeMax[2]=1000:VarProp[2]=FMin'
        ':CutRangeMin[3]=300:CutRangeMax[3]=2000:VarProp[3]=FMin'
        #':CutRangeMin[4]=0:CutRangeMax[4]=50:VarProp[4]=FMin'
        #':CutRangeMin[5]=0:CutRangeMax[5]=50000:VarProp[5]=FMax'
        ':SampleSize=200000'
    )

if 'CutsSA' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kCuts,
        'CutsSA',
        '!H:!V:FitMethod=SA:EffSel'
        ':MaxCalls=150000:'
        'KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale'
        #':VarProp[0]=FSmart'
        #':VarProp[1]=FSmart'
        #':VarProp[2]=FSmart'
        #':VarProp[3]=FSmart'
        #':VarProp[4]=FSmart'
        ':CutRangeMin[0]=60:CutRangeMax[0]=120:VarProp[0]=FMin'
        ':CutRangeMin[1]=200:CutRangeMax[1]=1000:VarProp[1]=FMin'
        ':CutRangeMin[2]=0:CutRangeMax[2]=1000:VarProp[2]=FMin'
        ':CutRangeMin[3]=300:CutRangeMax[3]=2000:VarProp[3]=FMin'
        #':CutRangeMin[4]=0:CutRangeMax[4]=50:VarProp[4]=FMin'
        #':CutRangeMin[5]=0:CutRangeMax[5]=50000:VarProp[5]=FMax'
        ':SampleSize=200000'
    )

if 'BDT' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kBDT,
        'BDT',
        '!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:'
        'UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20'
    )

if 'SVM' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kSVM,
        'SVM',
        'Gamma=0.25:Tol=0.001:VarTransform=Norm'
    )

if 'GradBoost' in sys.argv:
    factory.BookMethod(
        ROOT.TMVA.Types.kBDT,
        'GradBoost',
        '!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10'
        ':UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2'
        ':IgnoreNegWeightsInTraining'
    )

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
f_out.Close()


#   root -l mvaeffs.C\(\"TMVA.root\",kTRUE,\"S/sqrt\(B\)\"\)
#
#   root -l
#   .L mvaeffs.C
#   mvaeffs("TMVA.root",kTRUE,"S/sqrt(B)")

# python -ic "import ROOT;  ROOT.TMVA.mvaeffs('TMVA.root', True, 'sqrt(2*((S+B)*TMath::Log(1+S/B)-S))')"

