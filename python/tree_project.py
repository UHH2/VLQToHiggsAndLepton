#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector
from os.path import join
import varial.tools
import plot
import glob


core_histos = {
    'vlq_mass':          (';T mass;events / 80 GeV',                       25, 0, 2000   ),
    'h_n_subjet_btags':  ('N_{H-jet subjet b-tags}',                       5, -.5, 4.5   ),
    'n_fwd_jets':        ('N_{ak4 fwd jet}',                               5, -.5, 4.5   ),
    'abs_largest_jet_eta': ('most forward jet #eta',                       50, 0., 5.    ),
}

more_histos = {
    'event_chi2':        ('event chi2',                                    100, 0, 200   ),
    'dr_higg_top':       ('#DeltaR(H, t)',                                 50, 0, 5      ),
    'h_pt':              (';Higgs candidate p_{T};events / 40 GeV',        25, 0, 1000   ),
    'tlep_pt':           (';lept. top p_{T};events / 20 GeV',              50, 0, 1000   ),
    'h_mass':            (';Higgs candidate mass;events / 10 GeV',         25, 50, 300   ),
    'n_leading_btags':   ('N_{b-tag leading}',                             11, -.5, 10.5 ),
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
    'n_htags':           ('N_{H jet}',                                     5, -.5, 4.5   ),
    'ST':                (';ST;events / 100 GeV',                          25, 0, 2500   ),
    'tlep_eta':          ('lept. top #eta',                                50, -5., 5.   ),
    'tlep_mass':         (';lept. top mass;events / 10 GeV',               25, 100, 350  ),
    'h_eta':             ('Higgs candidate #eta',                          50, -5., 5.   ),
    'vlq_pt':            (';T p_{T};events / 20 GeV',                      50, 0, 1000   ),
    'vlq_eta':           ('T #eta',                                        50, -5., 5.   ),
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
] + varial.settings.my_lh_signals  + varial.settings.my_rh_signals

sr_selection = [
    # 'primary_lepton_charge  > 0',
    'h_n_subjet_btags       == 2',
    'n_fwd_jets             >= 1',
]

sb_selection = [
    'h_n_subjet_btags       == 1',
    'n_fwd_jets             == 0',
]

fw_selection = [
    'h_n_subjet_btags       <= 1',
    'n_fwd_jets             >= 1',
]


def get_sec_sel_weight(additional_sel=None):
    baseline_selection = [
    #    'ST                     > 400',
    #    'leading_jet_pt         > 100',
    #    'h_pt                   > 100',
    #    'tlep_pt                > 100',
    #    'h_mass                 > 90',
    #    'h_mass                 < 160',
    #    'dr_higg_top            > 2.',
    #    '(TwoDCut_ptrel > 40. || TwoDCut_dr > 0.4)',
    ] + (additional_sel or [])

    sr_sel = baseline_selection + sr_selection
    sb_sel = baseline_selection + sb_selection
    fw_sel = baseline_selection + fw_selection

    lepchargeplus_selection = [
        'primary_lepton_charge  > 0.1',
    ]

    lepchargeminus_selection = [
        'primary_lepton_charge  < 0.1',
    ]

    sec_sel_weight = [
        ('BaseLineSelection', baseline_selection, 'weight'),
        ('FwdSelection', fw_sel, 'weight'),
        ('SignalRegion', sr_sel, 'weight'),
        ('SidebandRegion', sb_sel, 'weight'),
        ('BaselineLepPlus', baseline_selection + lepchargeplus_selection, 'weight'),
        ('BaselineLepMnus', baseline_selection + lepchargeminus_selection, 'weight'),
        ('SRLepPlus', sr_selection + lepchargeplus_selection, 'weight'),
        ('SRLepMnus', sr_selection + lepchargeminus_selection, 'weight'),
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
    }

    return TreeProjector(
        filenames, params, get_sec_sel_weight(add_sel),
        name='TreeProjector',
    )


def mk_sys_tps(add_sel=None):
    # some defs
    base_path = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/'
    sys_params = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
    }
    base_sel = (add_sel or [])
    sr_sel = sr_selection + base_sel
    sb_sel = sb_selection + base_sel
    fw_sel = fw_selection + base_sel


    # first put together jerc uncert with nominal weights
    jercs = list(
        (name, base_path + uncrt_pth + '/workdir/uhh2.AnalysisModuleRunner.MC.*.root') 
        for name, uncrt_pth in (
            ('JES__minus', 'jec_down'),
            ('JES__plus', 'jec_up'),
            ('JER__minus', 'jer_down'),
            ('JER__plus', 'jer_up'),
        )
    )
    nominal_sec_sel_weight = [
        ('SignalRegion', sr_sel, 'weight'),
        ('SidebandRegion', sb_sel, 'weight'),
        ('BaseLineSelection', base_sel, 'weight'),
        ('FwdSelection', fw_sel, 'weight'),
    ]
    sys_tps = list(
        TreeProjector(
            dict(
                (sample, list(f for f in glob.glob(pat) if sample in f))
                for sample in samples
                if 'Run20' not in sample
            ), 
            sys_params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, pat in jercs
    )

    # next put together nominal samples with with weight uncerts.
    nominal_files = base_path + 'samples/uhh2.AnalysisModuleRunner.MC.*.root'
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
        if 'Run20' not in sample
    )
    sys_sec_sel_weight = list(
        (name, [
            ('SignalRegion', sr_sel, 'weight*' + w),
            ('SidebandRegion', sb_sel, 'weight*' + w),
            ('BaseLineSelection', base_sel, 'weight*' + w),
            ('FwdSelection', fw_sel, 'weight*' + w),
        ])
        for name, w in (
            ('b_tag_bc__minus', 'weight_btag_bc_down/weight_btag'),
            ('b_tag_bc__plus', 'weight_btag_bc_up/weight_btag'),
            ('b_tag_udsg__minus', 'weight_btag_udsg_down/weight_btag'),
            ('b_tag_udsg__plus', 'weight_btag_udsg_up/weight_btag'),
            ('muon_ID__minus', 'weight_sfmu_id_down/weight_sfmu_id'),
            ('muon_ID__plus', 'weight_sfmu_id_up/weight_sfmu_id'),
            ('muon_trigger__minus', 'weight_sfmu_trg_down/weight_sfmu_trg'),
            ('muon_trigger__plus', 'weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pileup__minus', 'weight_pu_down/weight_pu'),
            ('pileup__plus', 'weight_pu_up/weight_pu'),
            ('jet_pt__minus', 'weight_ak4jet_up/weight_ak4jet'),
            ('jet_pt__plus', 'weight_ak4jet_down/weight_ak4jet'),
        )
    )
    sys_tps += list(
        TreeProjector(
            filenames, 
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight
    )

    # make it complete with a tooloolchain!
    return varial.tools.ToolChain(
        'SysTreeProjectors', sys_tps
    )


if __name__ == '__main__':
    inp_pat = './*.root'
    varial.tools.Runner(mk_tp(inp_pat))
