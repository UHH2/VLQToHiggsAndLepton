#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector
#from varial_ext.treeprojector import TreeProjector
import multiprocessing as mp
from os.path import join
import varial.tools
import plot
import glob
import ast
import os


if False:
    TreeProjector = BatchTreeProjector
    from varial_ext.sgeworker import SGESubmitter
    import varial_ext.treeprojector as tp
    SGESubmitter(500, tp.jug_work_dir_pat, tp.jug_file_search_pat).submit()


iteration = [1]  # non-local variable
tree_aliases = {
    'rng': 'sin(2*pi*rndm)*sqrt(-2*log(rndm))*(abs(weight-1.0)>1e-10)',  # random gaus for MC
    'ht_weight': '(HT>600 && abs(weight-1.0)>1e-10 ? 1.194407 - HT*0.000408987 : 1.)',
    # 'h_mass_10': 'h_mass + 0.10*h_mass*rng',
    # 'h_mass_20': 'h_mass + 0.20*h_mass*rng',
}



varial.settings.all_signals = [
     'Signal_700',
     'Signal_800',
     'Signal_900',
     'Signal_1000',
     'Signal_1100',
     'Signal_1200',
     'Signal_1400',
     'Signal_1500',
     'Signal_1700',
     'Signal_1800',
     'Signal_M1000_Width-30p',
     'Signal_M1000_Width-10p',
     'Signal_M1000_Width-20p',
     'Signal_M1100_Width-10p',
     'Signal_M1200_Width-10p',
     'Signal_M1200_Width-20p',
     'Signal_M1200_Width-30p',
     'Signal_M1300_Width-10p',
     'Signal_M1400_Width-10p',
     'Signal_M1400_Width-20p',
     'Signal_M1400_Width-30p',
     'Signal_M1500_Width-10p',
     'Signal_M1600_Width-10p',
     'Signal_M1600_Width-20p',
     'Signal_M1600_Width-30p',
     'Signal_M1700_Width-10p',
     'Signal_M1800_Width-10p',
     'Signal_M1800_Width-20p',
     'Signal_M1800_Width-30p',
     'Signal_M1900_Width-10p',
     'Signal_M2000_Width-10p',
     'Signal_M2000_Width-20p',
     'Signal_M2000_Width-30p',
     'Signal_M2200_Width-10p',
     'Signal_M2200_Width-20p',
     'Signal_M2200_Width-30p',
     'Signal_M2400_Width-10p',
     'Signal_M2400_Width-20p',
     'Signal_M2400_Width-30p',
     'Signal_M2600_Width-10p',
     'Signal_M2600_Width-20p',
     'Signal_M2600_Width-30p',
     'Signal_M700_Width-10p',
     'Signal_M800_Width-10p',
     'Signal_M800_Width-20p',
     'Signal_M800_Width-30p',
     'Signal_M900_Width-10p',
]

core_histos = {
    'vlq_mass':          (';T quark mass / GeV;events / 80 GeV',           35, 0, 2800   ),
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
    'DY',
    'WJets',
    'Data',
    'Signal_700',
    'Signal_800',
    'Signal_900',
    'Signal_1000',
    'Signal_1100',
    'Signal_1200',
    'Signal_1400',
    'Signal_1500',
    'Signal_1700',
    'Signal_1800',


] #+ varial.settings.all_signals

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

sr_selection_addB0 = [
    'n_add_btags_incl_top  == 0',
]

sr_selection_addB1 = [
    'n_add_btags_incl_top  == 1',
]

sr_selection_addB2 = [
    'n_add_btags_incl_top  > 1',   
]

sr_selection_addB12 = [
    'n_add_btags_incl_top  > 0',   
]

el_selection = [
    'trigger_accept_el > 0.5',
]
mu_selection = [
    'trigger_accept_mu > 0.5',
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
    sr_sel_ab0 = sr_sel + sr_selection_addB0
    sr_sel_ab1 = sr_sel + sr_selection_addB1
    sr_sel_ab2 = sr_sel + sr_selection_addB2
    sr_sel_ab12 = sr_sel + sr_selection_addB12
    sb_sel_ab0 = sb_sel + sr_selection_addB0
    sb_sel_ab1 = sb_sel + sr_selection_addB1
    sb_sel_ab2 = sb_sel + sr_selection_addB2
    sb_sel_ab12 = sb_sel + sr_selection_addB12
    fw1_b0_sel_ab0 = fw1_b0_sel + sr_selection_addB0
    fw1_b0_sel_ab1 = fw1_b0_sel + sr_selection_addB1
    fw1_b0_sel_ab2 = fw1_b0_sel + sr_selection_addB2
    fw1_b0_sel_ab12 = fw1_b0_sel + sr_selection_addB12
    fw0_b0_sel_ab0 = fw0_b0_sel + sr_selection_addB0
    fw0_b0_sel_ab1 = fw0_b0_sel + sr_selection_addB1
    fw0_b0_sel_ab2 = fw0_b0_sel + sr_selection_addB2
    fw0_b0_sel_ab12 = fw0_b0_sel + sr_selection_addB12


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
        ('SignalRegionAddB0', sr_sel_ab0, base_weight),
        ('SignalRegionAddB1', sr_sel_ab1, base_weight),
        ('SignalRegionAddB2', sr_sel_ab2, base_weight),
        ('SignalRegionAddB12', sr_sel_ab12, base_weight),
        ('SidebandRegionAddB0', sb_sel_ab0, base_weight),
        ('SidebandRegionAddB1', sb_sel_ab1, base_weight),
        ('SidebandRegionAddB2', sb_sel_ab2, base_weight),
        ('SidebandRegionAddB12', sb_sel_ab12, base_weight),
        ('Fw1B0SelectionAddB0', fw1_b0_sel_ab0, base_weight),
        ('Fw1B0SelectionAddB1', fw1_b0_sel_ab1, base_weight),
        ('Fw1B0SelectionAddB2', fw1_b0_sel_ab2, base_weight),
        ('Fw1B0SelectionAddB12', fw1_b0_sel_ab12, base_weight),
        ('Fw0B0SelectionAddB0', fw0_b0_sel_ab0, base_weight),
        ('Fw0B0SelectionAddB1', fw0_b0_sel_ab1, base_weight),
        ('Fw0B0SelectionAddB2', fw0_b0_sel_ab2, base_weight),
        ('Fw0B0SelectionAddB12', fw0_b0_sel_ab12, base_weight),

        # ('BaselineLepPlus', bl_sel + lepchargeplus_selection, base_weight),
        # ('BaselineLepMnus', bl_sel + lepchargeminus_selection, base_weight),
        # ('SRLepPlus', sr_selection + lepchargeplus_selection, base_weight),
        # ('SRLepMnus', sr_selection + lepchargeminus_selection, base_weight),
    ]

    return sec_sel_weight


def mk_tp(input_pat, add_sel=None, channel = 'Default'):
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
        name='TreeProjector' + channel,
    )

    iteration[0] += 1
    tp.iteration = 10 * iteration[0]  # batch tp's should not interfere
    return tp

def mk_sys_tps(add_sel=None, channel='Default'):
    # some defs
    base_path = '/nfs/dust/cms/user/schumas/ANALYSIS/80X_v4/CMSSW_8_0_24_patch1/src/UHH2/FILES/BASELINE/MERGED/'
    sys_params = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
        'aliases': tree_aliases,
    }
    bl_sel = bl_selection + (add_sel or [])
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    sr_sel_ab0 = sr_sel + sr_selection_addB0
    sr_sel_ab1 = sr_sel + sr_selection_addB1
    sr_sel_ab2 = sr_sel + sr_selection_addB2
    sr_sel_ab12 = sr_sel + sr_selection_addB12
    sb_sel_ab0 = sb_sel + sr_selection_addB0
    sb_sel_ab1 = sb_sel + sr_selection_addB1
    sb_sel_ab2 = sb_sel + sr_selection_addB2
    sb_sel_ab12 = sb_sel + sr_selection_addB12
    b0_sel = b0_selection + bl_sel
    fw1_b0_sel = bl_sel + fw1_b0_selection
    fw0_b0_sel = fw0_b0_selection + bl_sel
    fw1_b0_sel_ab0 = fw1_b0_sel + sr_selection_addB0
    fw1_b0_sel_ab1 = fw1_b0_sel + sr_selection_addB1
    fw1_b0_sel_ab2 = fw1_b0_sel + sr_selection_addB2
    fw1_b0_sel_ab12 = fw1_b0_sel + sr_selection_addB12
    fw0_b0_sel_ab0 = fw0_b0_sel + sr_selection_addB0
    fw0_b0_sel_ab1 = fw0_b0_sel + sr_selection_addB1
    fw0_b0_sel_ab2 = fw0_b0_sel + sr_selection_addB2
    fw0_b0_sel_ab12 = fw0_b0_sel + sr_selection_addB12


     ################### first put together jerc uncert with nominal weights ###
    jercs = list(
        (name, base_path + uncrt_pth + '/*.root')
        for name, uncrt_pth in (
            ('JES__minus', 'jec_down'),
            ('JES__plus', 'jec_up'),
            ('JER__minus', 'jer_down'),
            ('JER__plus', 'jer_up'),
            )
        )
    nominal_sec_sel_weight = [
        ('SignalRegion',              sr_sel,          base_weight),
        ('SignalRegionAddB0',         sr_sel_ab0,      base_weight),
        ('SignalRegionAddB1',         sr_sel_ab1,      base_weight),
        ('SignalRegionAddB2',         sr_sel_ab2,      base_weight),
        ('SignalRegionAddB12',        sr_sel_ab12,     base_weight),
        ('SidebandRegion',            sb_sel,          base_weight),
        ('SidebandRegionAddB0',       sb_sel_ab0,      base_weight),
        ('SidebandRegionAddB1',       sb_sel_ab1,      base_weight),
        ('SidebandRegionAddB2',       sb_sel_ab2,      base_weight),
        ('SidebandRegionAddB12',      sb_sel_ab12,     base_weight),
        ('BaseLineSelection',         bl_sel,          base_weight),
        ('Fw0B0Selection',            fw0_b0_sel,      base_weight),
        ('Fw1B0Selection',            fw1_b0_sel,      base_weight),
        ('B0Selection',               b0_sel,          base_weight),
        ('Fw0B0SelectionAddB0',       fw0_b0_sel_ab0,  base_weight),
        ('Fw0B0SelectionAddB1',       fw0_b0_sel_ab1,  base_weight),
        ('Fw0B0SelectionAddB2',       fw0_b0_sel_ab2,  base_weight),
        ('Fw0B0SelectionAddB12',      fw0_b0_sel_ab12, base_weight),
        ('Fw1B0SelectionAddB0',       fw1_b0_sel_ab0,  base_weight),
        ('Fw1B0SelectionAddB1',       fw1_b0_sel_ab1,  base_weight),
        ('Fw1B0SelectionAddB2',       fw1_b0_sel_ab2,  base_weight),
        ('Fw1B0SelectionAddB12',      fw1_b0_sel_ab12, base_weight),
        ]
    sys_tps = list(
        TreeProjector(
            dict(
                (sample, list(f for f in glob.glob(pat) if sample in f))
                for sample in samples
                if 'Data' not in sample
                ),
            sys_params,
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name=name,
            )
        for name, pat in jercs
        )


    ############ next put together nominal samples with with weight uncerts ###
    nominal_files = base_path + '*.root'
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
        if 'Data' not in sample
    )
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
    percent_errs = {
        'TTbar':        0.08,    # 0.15,  # 0.05650
        'SingleT':      0.2,     # 0.15,  # 0.04166
        'QCD':          0.3,
        'DYJets':       0.2,     # 0.15,  # 0.01728
        'WJets':        0.06,    # 0.15,  # 0.03759
    }
    filenames_bkg = dict(
        (s, fs)
        for s, fs in filenames.iteritems()
        if s in percent_errs
    )

    rate_xsec_minus_dict = dict(
        (s, base_weight + ('*(1-%g)'% sw))
        for s, sw in percent_errs.iteritems()
    )
    rate_xsec_plus_dict = dict(
        (s, base_weight + ('*(1+%g)'% sw))
        for s, sw in percent_errs.iteritems()
    )
    sys_sec_sel_weight = list(
        (name, [
            ('SignalRegion',              sr_sel,          w if isinstance(w, dict) else base_weight+'*'+w),
            ('SignalRegionAddB0',         sr_sel_ab0,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SignalRegionAddB1',         sr_sel_ab1,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SignalRegionAddB2',         sr_sel_ab2,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SignalRegionAddB12',        sr_sel_ab12,     w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegion',            sb_sel,          w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegionAddB0',       sb_sel_ab0,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegionAddB1',       sb_sel_ab1,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegionAddB2',       sb_sel_ab2,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegionAddB12',      sb_sel_ab12,     w if isinstance(w, dict) else base_weight+'*'+w),
            ('BaseLineSelection',         bl_sel,          w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0Selection',            fw0_b0_sel,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw1B0Selection',            fw1_b0_sel,      w if isinstance(w, dict) else base_weight+'*'+w),
            ('B0Selection',               b0_sel,          w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0SelectionAddB0',       fw0_b0_sel_ab0,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0SelectionAddB1',       fw0_b0_sel_ab1,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0SelectionAddB2',       fw0_b0_sel_ab2,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0SelectionAddB12',      fw0_b0_sel_ab12, w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw1B0SelectionAddB0',       fw1_b0_sel_ab0,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw1B0SelectionAddB1',       fw1_b0_sel_ab1,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw1B0SelectionAddB2',       fw1_b0_sel_ab2,  w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw1B0SelectionAddB12',      fw1_b0_sel_ab12, w if isinstance(w, dict) else base_weight+'*'+w),
        ])

        for name, w in (
            ('b_tag_bc_AK4__minus',     'weight_btag_bc_down_AK4/weight_btag_AK4'),
            ('b_tag_bc_AK4__plus',      'weight_btag_bc_up_AK4/weight_btag_AK4'),
            ('b_tag_udsg_AK4__minus',   'weight_btag_udsg_down_AK4/weight_btag_AK4'),
            ('b_tag_udsg_AK4__plus',    'weight_btag_udsg_up_AK4/weight_btag_AK4'),
            ('b_tag_bc_subjet__minus',     'weight_btag_bc_down_HJet/weight_btag_HJet'),
            ('b_tag_bc_subjet__plus',      'weight_btag_bc_up_HJet/weight_btag_HJet'),
            ('b_tag_udsg_subjet__minus',   'weight_btag_udsg_down_HJet/weight_btag_HJet'),
            ('b_tag_udsg_subjet__plus',    'weight_btag_udsg_up_HJet/weight_btag_HJet'),
            ('muon_ID__minus',      'weight_sfmu_id_down/weight_sfmu_id'),
            ('muon_ID__plus',       'weight_sfmu_id_up/weight_sfmu_id'),
            ('muon_trigger__minus', 'weight_sfmu_trg_down/weight_sfmu_trg'),
            ('muon_trigger__plus',  'weight_sfmu_trg_up/weight_sfmu_trg'),
            ('elec_ID__minus',      'weight_sfelec_eleid_down/weight_sfelec_eleid'),
            ('elec_ID__plus',       'weight_sfelec_eleid_up/weight_sfelec_eleid'),
            ('pileup__minus',       'weight_pu_down/weight_pu'),
            ('pileup__plus',        'weight_pu_up/weight_pu'),
            
            #('jet_pt__minus',       '1'),
            #('jet_pt__plus',        'weight_ak4jet'),
            #('HT__minus',           '1'),
            #('HT__plus',            'ht_weight'),
            #('rate_xsec__minus',    rate_xsec_minus_dict),
            #('rate_xsec__plus',     rate_xsec_plus_dict),
            #('rate_fwdjet__minus',  '0.85'),
            #('rate_fwdjet__plus',   '1.15'),
            #('rate_lepiso__minus',  '0.95'),
            #('rate_lepiso__plus',   '1.05'),
        )
    )

    sys_tps += list(
        TreeProjector(
            filenames_bkg if name.startswith('rate_') else filenames,
            sys_params,
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight
    )

  ####################################################### PDF uncertainty ###
    with open('weight_dict_TpB') as f:
        weight_dict = ast.literal_eval(f.read())
    #with open('weight_dict_TpT') as f:
        #weight_dict.update(ast.literal_eval(f.read()))
    sys_params_pdf = {
        'histos': {'vlq_mass': core_histos['vlq_mass']},
        'treename': 'AnalysisTree',
        'aliases': tree_aliases,
        }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, [
                ('SignalRegionAddB0',         sr_sel_ab0,      dict((smpl, base_weight+'*weight_pdf_%i/%s'%(i, weight_list[i]))for smpl, weight_list in weight_dict.iteritems())),
                #('SignalRegionAddB1',         sr_sel_ab1,      dict((smpl, base_weight+'*weight_pdf_%i/%s'%(i, weight_list[i]))for smpl, weight_list in weight_dict.iteritems())),
                #('SignalRegionAddB2',         sr_sel_ab2,      dict((smpl, base_weight+'*weight_pdf_%i/%s'%(i, weight_list[i]))for smpl, weight_list in weight_dict.iteritems())),
                #('SignalRegionAddB12',        sr_sel_ab12,     dict((smpl, base_weight+'*weight_pdf_%i/%s'%(i, weight_list[i]))for smpl, weight_list in weight_dict.iteritems())),
         ])
        for i in xrange(100)
        )
    filenames_pdf = dict(
        (s, fs)
        for s, fs in filenames.iteritems()
        if s in varial.settings.all_signals
        )
    print filenames_pdf
    sys_tps_pdf = list(
        TreeProjector(
            filenames_pdf,
            sys_params_pdf,
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            )
        for name, ssw in sys_sec_sel_weight_pdf
        )
    sys_tps_pdf.append(PDFHistoSquash())
    sys_tps += [
        varial.tools.ToolChain('SysTreeProjectorsPDF', sys_tps_pdf),
        PDFUpDown(name='PDF__plus'),
        PDFUpDown(name='PDF__minus'),
        ]


  ####################################################### h_mass smearing ###
    # ttbar2_sel = ttbar_selection + tau21_selection + (add_sel or [])
    bl_skimmed = bl_selection[:]
    bl_skimmed.remove('h_mass_10 > 90')
    bl_skimmed.remove('h_mass_10 < 160')

    # h_mass minus
    bl_sel = bl_skimmed + (add_sel or []) + [
        'h_mass_20 > 90',
        'h_mass_20 < 160'
    ]
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    sr_sel_ab0 = sr_sel + sr_selection_addB0
    sr_sel_ab1 = sr_sel + sr_selection_addB1
    sr_sel_ab2 = sr_sel + sr_selection_addB2
    sr_sel_ab12 = sr_sel + sr_selection_addB12
    sb_sel_ab0 = sb_sel + sr_selection_addB0
    sb_sel_ab1 = sb_sel + sr_selection_addB1
    sb_sel_ab2 = sb_sel + sr_selection_addB2
    sb_sel_ab12 = sb_sel + sr_selection_addB12
    fw1_b0_sel = bl_sel + fw1_b0_selection
    fw0_b0_sel = fw0_b0_selection + bl_sel
    fw1_b0_sel_ab0 = fw1_b0_sel + sr_selection_addB0
    fw1_b0_sel_ab1 = fw1_b0_sel + sr_selection_addB1
    fw1_b0_sel_ab2 = fw1_b0_sel + sr_selection_addB2
    fw1_b0_sel_ab12 = fw1_b0_sel + sr_selection_addB12
    fw0_b0_sel_ab0 = fw0_b0_sel + sr_selection_addB0
    fw0_b0_sel_ab1 = fw0_b0_sel + sr_selection_addB1
    fw0_b0_sel_ab2 = fw0_b0_sel + sr_selection_addB2
    fw0_b0_sel_ab12 = fw0_b0_sel + sr_selection_addB12

    nominal_sec_sel_weight = [
        ('BaseLineSelection', bl_sel, base_weight),
        ('SignalRegion',              sr_sel,          base_weight),
        ('SignalRegionAddB0',         sr_sel_ab0,      base_weight),
        ('SignalRegionAddB1',         sr_sel_ab1,      base_weight),
        ('SignalRegionAddB2',         sr_sel_ab2,      base_weight),
        ('SignalRegionAddB12',        sr_sel_ab12,     base_weight),
        ('SidebandRegion',            sb_sel,          base_weight),
        ('SidebandRegionAddB0',       sb_sel_ab0,      base_weight),
        ('SidebandRegionAddB1',       sb_sel_ab1,      base_weight),
        ('SidebandRegionAddB2',       sb_sel_ab2,      base_weight),
        ('SidebandRegionAddB12',      sb_sel_ab12,     base_weight),
        ('Fw0B0Selection',            fw0_b0_sel,      base_weight),
        ('Fw1B0Selection',            fw1_b0_sel,      base_weight),
        ('Fw0B0SelectionAddB0',       fw0_b0_sel_ab0,  base_weight),
        ('Fw0B0SelectionAddB1',       fw0_b0_sel_ab1,  base_weight),
        ('Fw0B0SelectionAddB2',       fw0_b0_sel_ab2,  base_weight),
        ('Fw0B0SelectionAddB12',      fw0_b0_sel_ab12, base_weight),
        ('Fw1B0SelectionAddB0',       fw1_b0_sel_ab0,  base_weight),
        ('Fw1B0SelectionAddB1',       fw1_b0_sel_ab1,  base_weight),
        ('Fw1B0SelectionAddB2',       fw1_b0_sel_ab2,  base_weight),
        ('Fw1B0SelectionAddB12',      fw1_b0_sel_ab12, base_weight),
    ]
    sys_params_smear_down = sys_params.copy()
    sys_params_smear_down['histos'] = sys_params_smear_down['histos'].copy()
    sys_params_smear_down['histos']['h_mass'] = ('h_mass_20',
        ) + sys_params_smear_down['histos']['h_mass'][1:]
    sys_tps += [
        TreeProjector(
            filenames,
            sys_params_smear_down,
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name='MH_smear__minus',
        )
    ]

    # h_mass plus
    bl_sel = bl_skimmed + (add_sel or []) + [
        'h_mass > 90',
        'h_mass < 160'
    ]
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    sr_sel_ab0 = sr_sel + sr_selection_addB0
    sr_sel_ab1 = sr_sel + sr_selection_addB1
    sr_sel_ab2 = sr_sel + sr_selection_addB2
    sr_sel_ab12 = sr_sel + sr_selection_addB12
    sb_sel_ab0 = sb_sel + sr_selection_addB0
    sb_sel_ab1 = sb_sel + sr_selection_addB1
    sb_sel_ab2 = sb_sel + sr_selection_addB2
    sb_sel_ab12 = sb_sel + sr_selection_addB12
    fw1_b0_sel = bl_sel + fw1_b0_selection
    fw0_b0_sel = fw0_b0_selection + bl_sel
    fw1_b0_sel_ab0 = fw1_b0_sel + sr_selection_addB0
    fw1_b0_sel_ab1 = fw1_b0_sel + sr_selection_addB1
    fw1_b0_sel_ab2 = fw1_b0_sel + sr_selection_addB2
    fw1_b0_sel_ab12 = fw1_b0_sel + sr_selection_addB12
    fw0_b0_sel_ab0 = fw0_b0_sel + sr_selection_addB0
    fw0_b0_sel_ab1 = fw0_b0_sel + sr_selection_addB1
    fw0_b0_sel_ab2 = fw0_b0_sel + sr_selection_addB2
    fw0_b0_sel_ab12 = fw0_b0_sel + sr_selection_addB12

    nominal_sec_sel_weight = [
        ('BaseLineSelection', bl_sel, base_weight),
        ('SignalRegion',              sr_sel,          base_weight),
        ('SignalRegionAddB0',         sr_sel_ab0,      base_weight),
        ('SignalRegionAddB1',         sr_sel_ab1,      base_weight),
        ('SignalRegionAddB2',         sr_sel_ab2,      base_weight),
        ('SignalRegionAddB12',        sr_sel_ab12,     base_weight),
        ('SidebandRegion',            sb_sel,          base_weight),
        ('SidebandRegionAddB0',       sb_sel_ab0,      base_weight),
        ('SidebandRegionAddB1',       sb_sel_ab1,      base_weight),
        ('SidebandRegionAddB2',       sb_sel_ab2,      base_weight),
        ('SidebandRegionAddB12',      sb_sel_ab12,     base_weight),
        ('Fw0B0Selection',            fw0_b0_sel,      base_weight),
        ('Fw1B0Selection',            fw1_b0_sel,      base_weight),
        ('Fw0B0SelectionAddB0',       fw0_b0_sel_ab0,  base_weight),
        ('Fw0B0SelectionAddB1',       fw0_b0_sel_ab1,  base_weight),
        ('Fw0B0SelectionAddB2',       fw0_b0_sel_ab2,  base_weight),
        ('Fw0B0SelectionAddB12',      fw0_b0_sel_ab12, base_weight),
        ('Fw1B0SelectionAddB0',       fw1_b0_sel_ab0,  base_weight),
        ('Fw1B0SelectionAddB1',       fw1_b0_sel_ab1,  base_weight),
        ('Fw1B0SelectionAddB2',       fw1_b0_sel_ab2,  base_weight),
        ('Fw1B0SelectionAddB12',      fw1_b0_sel_ab12, base_weight),
    ]
    sys_params_smear_up = sys_params.copy()
    sys_params_smear_up['histos'] = sys_params_smear_up['histos'].copy()
    sys_params_smear_up['histos']['h_mass'] = ('h_mass',
        ) + sys_params_smear_down['histos']['h_mass'][1:]
    sys_tps += [
        TreeProjector(
            filenames,
            sys_params_smear_up,
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name='MH_smear__plus',
        )
        ]






   ##### NO OTHER SYS AFTER THIS POINT (SEL LISTS ARE CHANGED)

    for tp in sys_tps:
        iteration[0] += 1
        tp.iteration = 10 * iteration[0]  # batch tp's should not interfere

    # make it complete with a tooloolchain!
    return varial.tools.ToolChainParallel(
        'SysTreeProjectors' + channel , sys_tps, n_workers=1
        )

class PDFHistoSquash(varial.tools.Tool):
    io = varial.pklio

    def run(self):
        pdf_paths = glob.glob(self.cwd + '../*')
        pdf_paths.remove(self.cwd + '../PDFHistoSquash')
        pdf_histos = (
            w
            for p in pdf_paths
            for w in varial.diskio.bulk_load_histograms(
                        varial.gen.dir_content(p+'/*.root'))
        )
        pdf_histos = sorted(pdf_histos, key=lambda w: w.sample)
        pdf_histos = varial.gen.group(pdf_histos, lambda w: w.sample)
        pdf_histos = (varial.op.squash_sys_stddev(h) for h in pdf_histos)
        self.result = list(pdf_histos)
        
        print pdf_histos
        os.system('touch %s/webcreate_denial' % self.cwd)
 

class PDFUpDown(varial.tools.Tool):
    io = varial.pklio

    def run(self):
        assert '__plus' in self.name or '__minus' in self.name
        factor = 1. if '__plus' in self.name else -1.
        self.message('INFO adding error with factor: %i' % factor)

        def set_values(w):
            h = w.histo
            h_sys = w.histo_sys_err
            for i in xrange(h_sys.GetNbinsX()+2):
                h.SetBinContent(i, h_sys.GetBinContent(i)
                                   + factor*h_sys.GetBinError(i))
            w.histo_sys_err = None
            return w

        def norm_thing(wrps):
            sigs = varial.gen.dir_content('../../TreeProjector/*.root')
            sigs = (s for s in sigs if '/Signal_' in s.file_path)
            sigs = (s for s in sigs if s.name == 'vlq_mass')
            sigs = (s for s in sigs if 'SignalRegion' in s.in_file_path)
            sigs = varial.gen.load(sigs)
            sigs = dict((s.sample, s.histo) for s in sigs)
            for w in wrps:
                w.histo.Scale(sigs[w.sample].Integral() / w.histo.Integral())
                yield w

        def store(w):
            fsw = varial.wrp.FileServiceWrapper(name=w.in_file_path)
            fsw.vlq_mass = w.histo
            varial.diskio.write(fsw, w.sample)
            return w
        

        histos = self.lookup_result('../SysTreeProjectorsPDF/PDFHistoSquash')
        assert histos
        histos = (varial.op.copy(w) for w in histos)
        histos = (set_values(w) for w in histos)
        # histos = norm_thing(histos)
        histos = (store(w) for w in histos)
        histos = list(histos)

 

        alia = varial.diskio.generate_aliases(self.cwd + '*.root')
        alia = varial.gen.gen_add_wrp_info(alia,
            sample=lambda a: os.path.basename(os.path.splitext(a.file_path)[0]))
        self.result = list(alia)
        os.system('touch %s/aliases.in.result' % self.cwd)
        os.system('touch %s/webcreate_denial' % self.cwd)





if __name__ == '__main__':
    inp_pat = './*.root'
    #varial.tools.Runner(mk_tp(inp_pat, el_selection, 'Electron'))
    #varial.tools.Runner(mk_tp(inp_pat, mu_selection, 'Muon'))
    varial.tools.Runner(mk_sys_tps(mu_selection, 'Muon'))
    varial.tools.Runner(mk_sys_tps(el_selection, 'Electron'))
