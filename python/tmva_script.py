import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TMVA.Tools.Instance()

# prepare inputs
p = 'VLQ2HT/EventLoopAndPlots/FilteredCat1htag/SFrame/'
f_sig = ROOT.TFile(p + 'uhh2.AnalysisModuleRunner.MC.TpJ_TH_M800_Tlep.root')
f_bkg = ROOT.TFile(p + 'uhh2.AnalysisModuleRunner.MC.MC_TTJets.root')
t_sig = f_sig.Get('AnalysisTree')
t_bkg = f_bkg.Get('AnalysisTree')

#variables = list(b.GetName() for b in t_bkg.GetListOfBranches())
#variables.remove('weight')
#variables.remove('vlq_mass')

#variables = ['n_leptons', 'n_btags', 'n_higgs_tags']
#variables = ['leading_jet_pt', 'subleading_jet_pt', 'vlq_pt', 'vlq_eta']
variables = [
    'dr_higg_top',
    'h_mass',
    'h_pt',
    'tlep_pt',
    'abs_largest_jet_eta',
    'event_chi2',
    'vlq_mass',
    #'n_leading_btags',
    #'n_fwd_jets',
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
    typ = {int: 'I', float: 'F'}[type(getattr(t_bkg, var))]
    if var.endswith('eta'):
        var = 'abs(%s)' % var
    factory.AddVariable(var, var, 'units', typ)
factory.AddSpectator('vlq_mass', 'vlq_mass', 'units')

factory.AddSignalTree(t_sig, 1.0)
factory.AddBackgroundTree(t_bkg, 1.0)
factory.SetSignalWeightExpression('weight')
factory.SetBackgroundWeightExpression('weight')
factory.PrepareTrainingAndTestTree(ROOT.TCut(''), 'SplitMode=random:!V')
factory.BookMethod(
    ROOT.TMVA.Types.kCuts,
    'Cuts',
    '!H:!V:FitMethod=GA:EffSel'
    ':VarProp[0]=FSmart'
    ':VarProp[2]=FSmart'
    ':VarProp[3]=FSmart'
    ':VarProp[4]=FSmart'
    ':VarProp[5]=FSmart'
    #':CutRangeMin[0]=0:CutRangeMax[0]=50:VarProp[0]=FMin'
    #':CutRangeMin[1]=0:CutRangeMax[1]=50'
    #':CutRangeMin[2]=0:CutRangeMax[2]=50000:VarProp[2]=FMin'
    #':CutRangeMin[3]=0:CutRangeMax[3]=50:VarProp[3]=FMin'
    #':CutRangeMin[4]=0:CutRangeMax[4]=50:VarProp[4]=FMin'
    #':CutRangeMin[5]=0:CutRangeMax[5]=50000:VarProp[5]=FMax'
    #':SampleSize=200000'
)

#factory.BookMethod(
#    ROOT.TMVA.Types.kBDT,
#    'BDT',
#    '!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:'
#    'UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20'
#)
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
f_out.Close()

