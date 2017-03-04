#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector
import multiprocessing as mp
from os.path import join
import varial.tools
import plot
import glob
import ast
import os


iteration = [1]  # non-local variable
tree_aliases = {
    'rng': 'sin(2*pi*rndm)*sqrt(-2*log(rndm))*(abs(weight-1.0)>1e-10)',  # random gaus for MC
    'ht_weight': '(HT>600 && abs(weight-1.0)>1e-10 ? 1.194407 - HT*0.000408987 : 1.)',
    # 'h_mass_10': 'h_mass + 0.10*h_mass*rng',
    # 'h_mass_20': 'h_mass + 0.20*h_mass*rng',
}


core_histos = {
    'h_n_vtx':           ('Number of primary vertices',                                     40, .5, 40.5  ),
    'h_n_true_vtx':      ('Number of true interactions',                                    40, .5, 40.5  ),

    'primary_lepton_pt': (';Lepton p_{T} / GeV;Events / 40 GeV',                            25,  0, 1000  ),
    'primary_lepton_eta':('Lepton #eta',                                                    16, -4, 4     ),

    'leading_jet_pt':    (';Leading AK4 jet p_{T} (GeV);Events / 50 GeV',                   40, 0., 2000),
    'subleading_jet_pt': (';Sub-leading AK4 jet p_{T} (GeV);Events / 50 GeV',               40, 0., 2000),
    'ak4_jet_eta':       ('slimmedJets.m_eta', 'AK4 jet #eta',                              20, -5., 5.   ),
    'n_jets':            ('Number of AK4 jets',                                             15, .5, 15.5  ),

    'fwd_jet_pt':        ('fwd_jets.m_pt',';Forward jet p_{T} (GeV);Events / 20 GeV',       25, 0., 500   ),
    'fwd_jet_eta':       ('fwd_jets.m_eta', 'Forward jet #eta',                             20, -5., 5.   ),
    'n_fwd_jets':        ('Number of forward jets',                                         9, -.5, 8.5   ),

    'ST':                (';S_{T} (GeV);Events / 100 GeV',                                  21, 400, 2500 ),
    'MET':               ('slimmedMETs.m_pt', ';Missing E_{T} (GeV);Events / 25 GeV',       32, 0, 800    ),

    'ak8_jet_pt':        ('slimmedJetsAK8_SoftDrop.m_pt',';AK8 jet p_{T} (GeV);Events / 20 GeV', 40, 0., 2000  ),
    'ak8_jet_eta':       ('slimmedJetsAK8_SoftDrop.m_eta', 'AK8 jet #eta',                       20, -5., 5.   ),
    'n_ak8_jets':        ('@slimmedJetsAK8_SoftDrop.size()', 'Number of AK8 jets',               8, .5, 8.5    ),

    'h_pt':              (';H candidate p_{T} (GeV);Events / 25 GeV',                       32, 200, 1000 ),
    'h_eta':             ('H candidate #eta',                                               20, -5., 5.   ),
    'h_mass':            ('h_mass_10', ';H candidate mass (GeV);Events / 10 GeV',           20, 50, 250   ),

    'h_mass_pruned':     ('h_jet.m_prunedmass', ';pruned jet mass (GeV);Events / 10 GeV',   20, 50, 250   ),
    'h_mass_softdrop':   ('h_mass', ';soft-drop jet mass (GeV);Events / 10 GeV',            20, 50, 250   ),

    'tlep_pt':           (';t quark candidate p_{T} (GeV);Events / 40 GeV',                 25, 0, 1000   ),
    'tlep_eta':          ('t quark candidate #eta',                                         20, -5., 5.   ),
    'tlep_mass':         (';t quark candidate mass (GeV);Events / 10 GeV',                  25, 100, 350  ),

    'vlq_pt':            (';T quark candidate p_{T} (GeV);Events / 40 GeV',                 25, 0, 1000   ),
    'vlq_eta':           ('T quark candidate #eta',                                         20, -5., 5.   ),
    'vlq_mass':          (';T quark candidate mass (GeV);Events / 80 GeV',                  25, 0, 2000   ),

    'h_n_subjet_btags':  ('Number of subjet b tags',                                        5, -.5, 4.5   ),
    'event_chi2':        ('#chi^2',                                                         20, 0, 200    ),
}

more_histos = {
    'abs_largest_jet_eta': ('most forward jet #eta',                       50, 0., 5.    ),
    'dr_higg_top':       ('#DeltaR(H, t)',                                 50, 0, 5      ),
    'n_leading_btags':   ('N_{b-tag leading}',                             11, -.5, 10.5 ),
    'n_btags':           ('N_{b-tag}',                                     11, -.5, 10.5 ),
    'n_btags_tight':     ('N_{b-tag tight}',                               11, -.5, 10.5 ),
    'largest_jet_eta':   ('most forward ak4 jet #eta',                     50, -5., 5.   ),
    'h_tau21':           ('Higgs candidate #tau_{2}/#tau_{1}',             50, 0, 1      ),
    'h_tau32':           ('Higgs candidate #tau_{3}/#tau_{2}',             50, 0, 1      ),
    'n_leptons':         ('N_{lepton}',                                    11, -.5, 10.5 ),
    'n_htags':           ('N_{H jet}',                                     5, -.5, 4.5   ),
    'HT':                (';H_{T} (GeV);Events / 100 GeV',                 30, 0, 3000   ),
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
] + varial.settings.all_signals


bl_selection_no_h_mass_cut = [
    '(TwoDCut_ptrel > 40. || TwoDCut_dr > 0.4)',
    '((trigger_accept_mu > 0.5 && leading_jet_pt > 100) || leading_jet_pt > 250)',
    '((trigger_accept_mu > 0.5 && subleading_jet_pt > 50) || subleading_jet_pt > 70)',
    'ST > 400',
    'dr_higg_top > 2.',
    'tlep_pt > 100',
    ]

bl_selection = bl_selection_no_h_mass_cut + [
    'h_mass_10 > 90',
    'h_mass_10 < 160',
]

sr_selection = [
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

# jet_selection = [
#     'leading_jet_pt         > 250',
#     'subleading_jet_pt      > 70',
# ]

ttbar_selection = bl_selection_no_h_mass_cut + [
    'n_btags_tight >= 2',
]

tau21_selection = [
    'h_tau21 < .4',
]

base_weight = 'weight'
ht_weight = 'ht_weight*' + base_weight

def get_sec_sel_weight(additional_sel=None):
    bl_sel = bl_selection + (additional_sel or [])
    sr_sel = bl_sel + sr_selection
    sb_sel = bl_sel + sb_selection
    b0_sel = bl_sel + b0_selection
    fw0_b0_sel = bl_sel + fw0_b0_selection
    fw1_b0_sel = bl_sel + fw1_b0_selection
    # sb_jet_sel = bl_sel + sb_selection + jet_selection
    # ttbar_sel = ttbar_selection + (additional_sel or [])
    ttbar2_sel = ttbar_selection + tau21_selection + (additional_sel or [])


    # lepchargeplus_selection = [
    #     'primary_lepton_charge  > 0.1',
    # ]

    # lepchargeminus_selection = [
    #     'primary_lepton_charge  < 0.1',
    # ]

    sec_sel_weight = [
        ('BaseLineSelection', bl_sel, base_weight),
        # ('BaseLineSelectionHTWeight', bl_sel, ht_weight),
        # ('BaseLineSelectionJetPT', sb_jet_sel, base_weight),
        # ('TTbarSelection', ttbar_sel, base_weight),
        ('TTbar2Selection', ttbar2_sel, base_weight),
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('Fw1B0Selection', fw1_b0_sel, base_weight),
        ('Fw0B0Selection', fw0_b0_sel, base_weight),
        ('B0Selection', b0_sel, base_weight),
        # ('B0SelectionHTWeight', b0_sel, ht_weight),
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

    iteration[0] += 1
    tp.iteration = 10 * iteration[0]  # batch tp's should not interfere
    return tp


def mk_sys_tps(add_sel=None):
    # some defs
    base_path = '/nfs/dust/cms/user/tholenhe/VLQToHiggsAndLepton/'
    sys_params = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
        'aliases': tree_aliases,
    }
    bl_sel = bl_selection + (add_sel or [])
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    b0_sel = b0_selection + bl_sel
    fw0_b0_sel = fw0_b0_selection + bl_sel

    ################### first put together jerc uncert with nominal weights ###
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
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('BaseLineSelection', bl_sel, base_weight),
        ('B0Selection', b0_sel, base_weight),
        ('Fw0B0Selection', fw0_b0_sel, base_weight),
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

    ############ next put together nominal samples with with weight uncerts ###
    nominal_files = base_path + 'samples/uhh2.AnalysisModuleRunner.MC.*.root'
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
        if 'Run20' not in sample
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
            ('SignalRegion',        sr_sel, w if isinstance(w, dict) else base_weight+'*'+w),
            ('SidebandRegion',      sb_sel, w if isinstance(w, dict) else base_weight+'*'+w),
            ('BaseLineSelection',   bl_sel, w if isinstance(w, dict) else base_weight+'*'+w),
            ('Fw0B0Selection',  fw0_b0_sel, w if isinstance(w, dict) else base_weight+'*'+w),
            # ('B0Selection',         b0_sel, w if isinstance(w, dict) else base_weight+'*'+w),
        ])
        for name, w in (
            ('b_tag_bc__minus',     'weight_btag_bc_down/weight_btag'),
            ('b_tag_bc__plus',      'weight_btag_bc_up/weight_btag'),
            ('b_tag_udsg__minus',   'weight_btag_udsg_down/weight_btag'),
            ('b_tag_udsg__plus',    'weight_btag_udsg_up/weight_btag'),
            # ('muon_ID__minus',      'weight_sfmu_id_down/weight_sfmu_id'),
            # ('muon_ID__plus',       'weight_sfmu_id_up/weight_sfmu_id'),
            # ('muon_trigger__minus', 'weight_sfmu_trg_down/weight_sfmu_trg'),
            # ('muon_trigger__plus',  'weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pileup__minus',       'weight_pu_down/weight_pu'),
            ('pileup__plus',        'weight_pu_up/weight_pu'),
            # ('jet_pt__minus',       '1'),
            # ('jet_pt__plus',        'weight_ak4jet'),
            # ('HT__minus',           '1'),
            # ('HT__plus',            'ht_weight'),
            ('rate_xsec__minus',    rate_xsec_minus_dict),
            ('rate_xsec__plus',     rate_xsec_plus_dict),
            ('rate_fwdjet__minus',  '0.85'),
            ('rate_fwdjet__plus',   '1.15'),
            ('rate_lepiso__minus',  '0.95'),
            ('rate_lepiso__plus',   '1.05'),
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
    with open('weight_dict_TpT') as f:
        weight_dict.update(ast.literal_eval(f.read()))
    sys_params_pdf = {
        'histos': {'vlq_mass': core_histos['vlq_mass']},
        'treename': 'AnalysisTree',
        'aliases': tree_aliases,
    }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, [
            (
                'SignalRegion',
                sr_sel,
                dict(
                    (smpl, base_weight+'*weight_pdf_%i/%s'%(i, weight_list[i]))
                    for smpl, weight_list in weight_dict.iteritems()
                )
            ),
        ])
        for i in xrange(100)
    )
    filenames_pdf = dict(
        (s, fs)
        for s, fs in filenames.iteritems()
        if s in varial.settings.all_signals
    )
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
    # b0_sel = b0_selection + bl_sel
    nominal_sec_sel_weight = [
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('BaseLineSelection', bl_sel, base_weight),
        # ('B0Selection', b0_sel, base_weight),
        # ('TTbar2Selection', ttbar2_sel, base_weight),
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
    # b0_sel = b0_selection + bl_sel
    nominal_sec_sel_weight = [
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('BaseLineSelection', bl_sel, base_weight),
        # ('B0Selection', b0_sel, base_weight),
        # ('TTbar2Selection', ttbar2_sel, base_weight),
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
        'SysTreeProjectors', sys_tps, n_workers=1
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
            fsw = varial.wrp.FileServiceWrapper(name='SignalRegion')
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
    varial.tools.Runner(mk_tp(inp_pat))
