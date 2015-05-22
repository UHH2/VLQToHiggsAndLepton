import ROOT
ROOT.TMVA.Tools.Instance()
# prepare inputs
f_sig = ROOT.TFile('uhh2.AnalysisModuleRunner.MC.TpJ_TH_M800_Tlep.root')
f_bkg = ROOT.TFile('uhh2.AnalysisModuleRunner.MC.MC_TTJets.root')
t_sig = f_sig.Get('AnalysisTree')
t_bkg = f_bkg.Get('AnalysisTree')

variables = list(b.GetName() for b in t_bkg.GetListOfBranches())
variables.remove('weight')
variables.remove('vlq_mass')

#variables = ['n_leptons', 'n_btags', 'n_higgs_tags']
#variables = ['leading_jet_pt', 'subleading_jet_pt', 'vlq_pt', 'vlq_eta']

print variables
# prepare stuff
f_out = ROOT.TFile('TMVA.root', 'RECREATE')
factory = ROOT.TMVA.Factory(
    'TMVAClassification',
    f_out,
    '!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification'
)
for var in variables:
    typs = {int: 'I', float: 'F'}
    factory.AddVariable(var, var, 'units', typs[type(getattr(t_bkg, var))])
factory.AddSpectator('vlq_mass', 'vlq_mass', 'units')

factory.AddSignalTree(t_sig, 1.0)
factory.AddBackgroundTree(t_bkg, 1.0)
factory.SetSignalWeightExpression('weight')
factory.SetBackgroundWeightExpression('weight')
factory.PrepareTrainingAndTestTree(ROOT.TCut(''), 'SplitMode=random:!V')
factory.BookMethod(
    ROOT.TMVA.Types.kCuts,
    'Cuts',
    '!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart'
)

factory.BookMethod(
    ROOT.TMVA.Types.kCuts,
    'CutsD',
    '!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart'
)

factory.BookMethod(
    ROOT.TMVA.Types.kBDT,
    "BDT",
    "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:"
    "UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20"
)
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
f_out.Close()

