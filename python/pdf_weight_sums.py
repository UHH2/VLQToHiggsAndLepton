#!/usr/bin/env python

from multiprocessing import Pool
import itertools
import glob
import os


# smpls = glob.glob('/pnfs/desy.de/cms/tier2/store/user/htholen/TpB_20151125/TprimeBToTH_M-*_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_TprimeBToTH_M-*H_25ns/*/*/Ntuple_*.root')
# out_name = 'weight_dict_TpB'

smpls = glob.glob('/nfs/dust/cms/user/tholenhe/grid_control_new/gc-output/RunII-ntuple-25ns-v1.2/signals/MC_TpT_TH_*_Ntuple.root')
out_name = 'weight_dict_TpT'

def get_name_pnfs(name):
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


def get_name_nfs(name):
    name = name.replace('MC_', 'Signal_') # MC_TpT_TH_LH_M1600
    return name


def get_name(smpl):
    if smpl.startswith('/nfs/'):
        return get_name_nfs(get_basename(smpl))
    elif smpl.startswith('/pnfs/'):
        return get_name_pnfs(get_basename(smpl))
    raise RuntimeError('Bad sample: ' + smpl)


def get_basename(filename):
    if filename.startswith('/pnfs/'):       # use crab-project name
        return filename.split('/')[-4]

    # remove jobnumber and 'Ntuple' and make a set
    filename = os.path.splitext(filename)[0]
    filename = os.path.basename(filename)
    tokens = filename.split('_')
    if tokens[-1] == 'Ntuple':              # grid control
        tokens = tokens[:-2]
    else:                                   # sframe batch
        tokens = tokens[:-1]
    basename = '_'.join(tokens)
    return basename


def handle_sample(smpl_grp):
    name = get_name(smpl_grp[0])
    print 'working on sample:', name
    import ROOT

    sum_events = 0.
    sum_weight = [0.]*100

    files = (ROOT.TFile(s) for s in smpl_grp)
    trees = (f.Get('AnalysisTree') for f in files)
    events = (e for t in trees for e in t)

    for e in events:
        if not sum_events % 10000:
            print 'at event:', sum_events, name
        sum_events += 1
        scale_pdf = e.genInfo.pdf_scalePDF()
        for i in xrange(100):
            sum_weight[i] += e.genInfo.systweights()[112 + i]/scale_pdf

    sum_weight = list(w / sum_events for w in sum_weight)
    print '='*15, 'TOTAL EVENTS:', sum_events, name
    return name, sum_weight


smpls = sorted(smpls)
smpl_grps = list(list(g) for _, g in itertools.groupby(smpls, get_basename))


pool = Pool(24)
weight_dict = dict(pool.imap_unordered(handle_sample, smpl_grps))
print weight_dict
with open(out_name, 'w') as f:
    f.write(repr(weight_dict))
