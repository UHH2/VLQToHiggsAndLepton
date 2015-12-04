#!/usr/bin/env python

from varial.extensions.treeprojector import TreeProjector, SGETreeProjector
import varial.tools
import plot

import glob


histo_names_args = {
    'event_chi2':        ('event chi2',                                    100, 0, 200   ),
    'dr_higg_top':       ('#DeltaR(H, t)',                                 50, 0, 5      ),
    'h_pt':              (';Higgs candidate p_{T};events / 40 GeV',        25, 0, 1000   ),
    'tlep_pt':           (';lept. top p_{T};events / 20 GeV',              50, 0, 1000   ),
    'h_mass':            (';Higgs candidate mass;events / 10 GeV',         25, 50, 300   ),
    'h_n_subjet_btags':  ('N_{H-jet subjet b-tags}',                        5, -.5, 4.5 ),
    'n_leading_btags':   ('N_{b-tag leading}',                             11, -.5, 10.5 ),
    'abs_largest_jet_eta': ('most forward jet #eta',                       50, 0., 5.    ),
    'n_btags':           ('N_{b-tag}',                                     11, -.5, 10.5 ),
    'leading_jet_pt':    (';leading ak4 jet p_{T};events / 20 GeV',        50, 0., 1000  ),
    'subleading_jet_pt': (';sub-leading ak4 jet p_{T};events / 20 GeV',    50, 0., 1000  ),
    'largest_jet_eta':   ('most forward ak4 jet #eta',                     50, -5., 5.   ),
    'primary_lepton_pt': (';primary lepton p_{T};events / 20 GeV',         50, 0., 1000  ),
    'primary_lepton_eta':(';primary lepton #eta;events',                   25, -5., 5.   ),
    'primary_lepton_charge': (';primary lepton charge;events',             3, -1.5, 1.5  ),
    'h_tau21':           ('Higgs candidate #tau_{2}/#tau_{1}',             50, 0, 1      ),
    'h_tau32':           ('Higgs candidate #tau_{3}/#tau_{2}',             50, 0, 1      ),
    'n_jets':            ('N_{ak4 jet}',                                   21, -.5, 20.5 ),
    'n_leptons':         ('N_{lepton}',                                    11, -.5, 10.5 ),
    'n_fwd_jets':        ('N_{ak4 fwd jet}',                               5, -.5, 4.5   ),
    'n_htags':           ('N_{H jet}',                                     5, -.5, 4.5   ),
    'ST':                (';ST;events / 100 GeV',                          25, 0, 2500   ),
    'tlep_eta':          ('lept. top #eta',                                50, -5., 5.   ),
    'tlep_mass':         (';lept. top mass;events / 10 GeV',               25, 100, 350  ),
    'h_eta':             ('Higgs candidate #eta',                          50, -5., 5.   ),
    'vlq_pt':            (';T p_{T};events / 20 GeV',                      50, 0, 1000   ),
    'vlq_eta':           ('T #eta',                                        50, -5., 5.   ),
    'vlq_mass':          (';T mass;events / 80 GeV',                       25, 0, 2000   ),
#    'trigger_accept':    ('trigger accept',                                2, -.5, 1.5   ),
}
params = {
    'histos': histo_names_args,
    'treename': 'AnalysisTree',
}

samples = [
    'TTbar',
    'SingleT',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015D',
    'TpB_TH_700',
    'TpB_TH_1700',
] + varial.settings.my_lh_signals  + varial.settings.my_rh_signals

baseline_selection = [
#    'ST                     > 400',
#    'leading_jet_pt         > 100',
#    'h_pt                   > 100',
#    'tlep_pt                > 100',
#    'h_mass                 > 90',
#    'h_mass                 < 160',
#    'dr_higg_top            > 2.',
#    '(TwoDCut_ptrel > 40. || TwoDCut_dr > 0.4)',
]

sr_selection = baseline_selection + [
    'h_n_subjet_btags       == 2',
    'abs_largest_jet_eta    > 2.4',
]

sb_selection = baseline_selection + [
    'h_n_subjet_btags       == 1',
    'abs_largest_jet_eta    < 2.4',
    'tlep_mass              > 150',
    #'tlep_mass              < 350',
]
# TODO no_top_mass_cut_sb for comparison

sb_lepchargeplus_selection = baseline_selection + [
    'primary_lepton_charge  > 0.1',
]

sb_lepchargeminus_selection = baseline_selection + [
    'primary_lepton_charge  < 0.1',
]


sec_sel_weight = [
    ('BaseLineSelection', baseline_selection, 'weight'),
    ('SignalRegion', sr_selection, 'weight'),
    ('SidebandRegion', sb_selection, 'weight'),
    # ('PS_lep_plus',  sb_lepchargeplus_selection, 'weight'),
    # ('PS_lep_minus', sb_lepchargeminus_selection, 'weight'),
]

def mk_tp(input_pat):
    all_files = glob.glob(input_pat)
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    return TreeProjector(
        samples, filenames, params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name='TreeProjector'
    )

if __name__ == '__main__':
    input_pat = './*.root'
    varial.tools.Runner(mk_tp(input_pat))
