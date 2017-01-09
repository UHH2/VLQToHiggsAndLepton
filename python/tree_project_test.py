#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector
import varial.tools
import glob
import sys
import os


tree_aliases = {
    'rng': 'sin(2*pi*rndm)*sqrt(-2*log(rndm))*(abs(weight-1.0)>1e-10)',  # random gaus for MC
    'ht_weight': '(HT>600 && abs(weight-1.0)>1e-10 ? 1.194407 - HT*0.000408987 : 1.)',
}


core_histos = {
    'vlq_mass':          (';T quark mass / GeV;events / 80 GeV',           25, 0, 2000   ),
    'h_n_subjet_btags':  ('N_{H-jet subjet b-tags}',                       5, -.5, 4.5   ),
    'n_fwd_jets':        ('N_{ak4 fwd jet}',                               5, -.5, 4.5   ),
    'abs_largest_jet_eta': ('most forward jet #eta',                       50, 0., 5.    ),
    'h_mass':            ('h_mass_10', ';H candidate mass / GeV;events / 10 GeV',  20, 50, 250   ),
    'ST':                (';S_{T} / GeV;events / 100 GeV',                          25, 0, 2500   ),
    'tlep_mass':         (';lept. top mass / GeV;events / 10 GeV',               25, 100, 350  ),
    'tlep_pt':           (';lept. top p_{T} / GeV;events / 40 GeV',              25, 0, 1000   ),
    'primary_lepton_pt': (';lepton p_{T} / GeV;events / 40 GeV',                 25, 0., 1000  ),
    'leading_jet_pt':    (';leading ak4 jet p_{T} / GeV;events / 40 GeV',        25, 0., 1000  ),
    'subleading_jet_pt': (';sub-leading ak4 jet p_{T} / GeV;events / 40 GeV',    25, 0., 1000  ),
    'fwd_jets.m_eta':    (';fwd jet #eta;events',                          40, -5., 5.   ),
    'fwd_jets.m_pt':     (';fwd jet p_{T};events / 20 GeV',                25, 0., 500   ),
}

more_histos = {
    'event_chi2':        ('event chi2',                                    100, 0, 200   ),
    'dr_higg_top':       ('#DeltaR(H, t)',                                 50, 0, 5      ),
    'h_pt':              (';Higgs candidate p_{T} / GeV;events / 40 GeV',  25, 0, 1000   ),
    'n_leading_btags':   ('N_{b-tag leading}',                             11, -.5, 10.5 ),
    'n_btags':           ('N_{b-tag}',                                     11, -.5, 10.5 ),
    'n_btags_tight':     ('N_{b-tag tight}',                               11, -.5, 10.5 ),
    'largest_jet_eta':   ('most forward ak4 jet #eta',                     50, -5., 5.   ),
    'primary_lepton_eta':(';lepton #eta;events',                           25, -5., 5.   ),
    'primary_lepton_charge': (';lepton charge;events',                     3, -1.5, 1.5  ),
    'h_tau21':           ('Higgs candidate #tau_{2}/#tau_{1}',             50, 0, 1      ),
    'h_tau32':           ('Higgs candidate #tau_{3}/#tau_{2}',             50, 0, 1      ),
    'n_jets':            ('N_{ak4 jet}',                                   21, -.5, 20.5 ),
    'n_leptons':         ('N_{lepton}',                                    11, -.5, 10.5 ),
    'n_htags':           ('N_{H jet}',                                     5, -.5, 4.5   ),
    'tlep_eta':          ('lept. top #eta',                                50, -5., 5.   ),
    'h_eta':             ('Higgs candidate #eta',                          50, -5., 5.   ),
    'vlq_pt':            (';T p_{T} / GeV;events / 40 GeV',                25, 0, 1000   ),
    'vlq_eta':           ('T #eta',                                        50, -5., 5.   ),
    'h_mass-.00001':     (';H candidate soft drop mass / GeV;events / 10 GeV', 40, 50, 250   ),
    'h_jet.m_prunedmass': (';H candidate pruned mass / GeV;events / 10 GeV',   40, 50, 250   ),
    'HT':                (';H_{T} / GeV;events / 100 GeV',                     30, 0, 3000   ),
}
more_histos.update(core_histos)

samples = [
    'TTbar',
    'SingleT',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015D',
    'TpB_TH_0700',
    'TpB_TH_1200',
    'TpB_TH_1700',
] #  + varial.settings.all_signals

bl_selection = [
#    'ST                     > 400',
#    'leading_jet_pt         > 100',
#    'h_pt                   > 100',
#    'tlep_pt                > 100',
    'h_mass_10 > 90',
    'h_mass_10 < 160',
#    'dr_higg_top            > 2.',
#    '(TwoDCut_ptrel > 40. || TwoDCut_dr > 0.4)',
]

sr_selection = [
    # 'primary_lepton_charge  > 0',
    'h_n_subjet_btags       == 2',
    'n_fwd_jets             >= 1',
]

sb_selection = [
    'h_n_subjet_btags       == 1',
    'n_fwd_jets             == 0',
]

b0_selection = [
    'h_n_subjet_btags       == 0',
]

fw1_b0_selection = b0_selection + [
    'n_fwd_jets             >= 1',
]

fw0_b0_selection = b0_selection + [
    'n_fwd_jets             == 0',
]

jet_selection = [
    'leading_jet_pt         > 250',
    'subleading_jet_pt      > 70',
]

ttbar_selection = [
    'n_btags_tight          >= 2',
]

tau21_selection = [
    'h_tau21                < .4',
]

base_weight = 'weight'
ht_weight = 'ht_weight*' + base_weight

def get_sec_sel_weight(additional_sel=None):
    bl_sel = bl_selection + (additional_sel or [])
    sr_sel = bl_sel + sr_selection
    sb_sel = bl_sel + sb_selection
    fw1_b0_sel = bl_sel + fw1_b0_selection
    fw0_b0_sel = bl_sel + fw0_b0_selection
    sb_jet_sel = bl_sel + sb_selection + jet_selection
    ttbar_sel = ttbar_selection + (additional_sel or [])
    ttbar2_sel = ttbar_selection + tau21_selection + (additional_sel or [])
    b0_sel = b0_selection + (additional_sel or [])

    lepchargeplus_selection = [
        'primary_lepton_charge  > 0.1',
    ]

    lepchargeminus_selection = [
        'primary_lepton_charge  < 0.1',
    ]

    sec_sel_weight = [
        ('BaseLineSelection', bl_sel, base_weight),
        ('BaseLineSelectionHTWeight', bl_sel, ht_weight),
        ('BaseLineSelectionJetPT', sb_jet_sel, base_weight),
        ('TTbarSelection', ttbar_sel, base_weight),
        ('TTbar2Selection', ttbar2_sel, base_weight),
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('Fw1B0Selection', fw1_b0_sel, base_weight),
        ('Fw0B0Selection', fw0_b0_sel, base_weight),
        ('B0Selection', b0_sel, base_weight),
        ('B0SelectionHTWeight', b0_sel, ht_weight),
        # ('BaselineLepPlus', bl_sel + lepchargeplus_selection, base_weight),
        # ('BaselineLepMnus', bl_sel + lepchargeminus_selection, base_weight),
        # ('SRLepPlus', sr_selection + lepchargeplus_selection, base_weight),
        # ('SRLepMnus', sr_selection + lepchargeminus_selection, base_weight),
    ]

    return sec_sel_weight


def mk_tp(input_pat, add_sel=None):
    all_files = glob.glob(input_pat)
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    params = {
        'histos': more_histos,
        'treename': 'AnalysisTree',
        'aliases': tree_aliases,
    }

    tp = TreeProjector(
        filenames, params, get_sec_sel_weight(add_sel),
        name='TreeProjector',
    )

    return tp


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Please give me a pattern.'
        exit(-1)
    inp_pat = sys.argv[1]
    sel = ['trigger_accept_el > 0.5']
    varial.tools.Runner(
        mk_tp(inp_pat, sel)
    )
