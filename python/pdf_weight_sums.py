#!/usr/bin/env python

from multiprocessing import Pool
import glob


smpls = glob.glob('/pnfs/desy.de/cms/tier2/store/user/htholen/TpB_20151125/TprimeBToTH_M-*_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_TprimeBToTH_M-*H_25ns/*/*/Ntuple_1.root')


def get_name_pnfs(smpl):
    name = smpl.split('/')[-4]  # crab_TprimeBToTH_M-700_LH_25ns
    name = name.replace('crab_', '').replace('_25ns', '')  # TprimeBToTH_M-700_LH
    name = name.replace('ToTH', '_TH')  # TprimeB_TH_M-700_LH
    name = name.replace('rime', '')  # TpB_TH_M-700_LH
    name = name.replace('M-', 'M')  # TpB_TH_M700_LH
    name = name.replace('M7', 'M07')  # TpB_TH_M0700_LH
    name = name.replace('M8', 'M08')  # TpB_TH_M0700_LH
    name = name.replace('M9', 'M09')  # TpB_TH_M0700_LH
    name_lst = name.split('_')
    name_lst = [name_lst[0], name_lst[1], name_lst[3], name_lst[2]]
    name =  '_'.join(name_lst)  # TpB_TH_LH_M0700
    name = 'Signal_' + name  # Signal_TpB_TH_LH_M0700
    return name


def handle_sample(smpl):
    name = get_name_pnfs(smpl)
    print 'working on sample:', name
    import ROOT
    f = ROOT.TFile(smpl)

    sum_events = 0.
    sum_weight = [0.]*100

    trees = (key for key in f.GetListOfKeys() if key.GetName() == 'AnalysisTree')
    trees = (key.ReadObj() for key in trees)
    events = (e for t in trees for e in t)

    for e in events:
        if not sum_events % 500:
            print 'at event:', sum_events, name
        sum_events += 1
        scale_pdf = e.genInfo.pdf_scalePDF()
        for i in xrange(100):
            sum_weight[i] += e.genInfo.systweights()[112 + i]/scale_pdf

    sum_weight = list(w / sum_events for w in sum_weight)
    return name, sum_weight


pool = Pool(24)
weight_dict = dict(pool.imap_unordered(handle_sample, smpls))
print weight_dict
with open('weight_dict', 'w') as f:
    f.write(repr(weight_dict))
