#!/usr/bin/env python

# from varial_ext.treeprojector import BatchTreeProjector as TreeProjector
from varial_ext.treeprojector import TreeProjector
import multiprocessing as mp
from os.path import join
import varial.tools
import plot
import glob
import os


# from varial_ext.sgeworker import SGESubmitter
# import varial_ext.treeprojector as tp
# SGESubmitter(500, tp.jug_work_dir_pat, tp.jug_file_search_pat).submit()


iteration = [1]  # non-local variable


core_histos = {
    'vlq_mass':          (';T mass;events / 80 GeV',                       25, 0, 2000   ),
    'h_n_subjet_btags':  ('N_{H-jet subjet b-tags}',                       5, -.5, 4.5   ),
    'n_fwd_jets':        ('N_{ak4 fwd jet}',                               5, -.5, 4.5   ),
    'abs_largest_jet_eta': ('most forward jet #eta',                       50, 0., 5.    ),
    'h_mass':            (';Higgs candidate mass;events / 10 GeV',         25, 50, 300   ),
    'ST':                (';ST;events / 100 GeV',                          25, 0, 2500   ),
    'tlep_mass':         (';lept. top mass;events / 10 GeV',               25, 100, 350  ),
    'tlep_pt':           (';lept. top p_{T};events / 40 GeV',              25, 0, 1000   ),
    'primary_lepton_pt': (';lepton p_{T};events / 40 GeV',                 25, 0., 1000  ),
    'leading_jet_pt':    (';leading ak4 jet p_{T};events / 40 GeV',        25, 0., 1000  ),
    'subleading_jet_pt': (';sub-leading ak4 jet p_{T};events / 40 GeV',    25, 0., 1000  ),
    'fwd_jets.m_eta':    (';fwd jet #eta;events',                          40, -5., 5.   ),
    'fwd_jets.m_pt':     (';fwd jet p_{T};events / 20 GeV',                25, 0., 500   ),
}

more_histos = {
    'event_chi2':        ('event chi2',                                    100, 0, 200   ),
    'dr_higg_top':       ('#DeltaR(H, t)',                                 50, 0, 5      ),
    'h_pt':              (';Higgs candidate p_{T};events / 40 GeV',        25, 0, 1000   ),
    'n_leading_btags':   ('N_{b-tag leading}',                             11, -.5, 10.5 ),
    'n_btags':           ('N_{b-tag}',                                     11, -.5, 10.5 ),
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
    'vlq_pt':            (';T p_{T};events / 40 GeV',                      25, 0, 1000   ),
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

bl_selection = [
    #    'ST                     > 400',
    #    'leading_jet_pt         > 100',
    #    'h_pt                   > 100',
    #    'tlep_pt                > 100',
        'h_mass                 > 90',
        'h_mass                 < 160',
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

fw_selection = [
    'h_n_subjet_btags       == 0',
    'n_fwd_jets             >= 1',
]

base_weight = 'weight/weight_ak4jet'


def get_sec_sel_weight(additional_sel=None):
    bl_sel = bl_selection + (additional_sel or [])
    sr_sel = bl_sel + sr_selection
    sb_sel = bl_sel + sb_selection
    fw_sel = bl_sel + fw_selection

    lepchargeplus_selection = [
        'primary_lepton_charge  > 0.1',
    ]

    lepchargeminus_selection = [
        'primary_lepton_charge  < 0.1',
    ]

    sec_sel_weight = [
        ('BaseLineSelection', bl_sel, base_weight),
        ('FwdSelection', fw_sel, base_weight),
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('BaselineLepPlus', bl_sel + lepchargeplus_selection, base_weight),
        ('BaselineLepMnus', bl_sel + lepchargeminus_selection, base_weight),
        ('SRLepPlus', sr_selection + lepchargeplus_selection, base_weight),
        ('SRLepMnus', sr_selection + lepchargeminus_selection, base_weight),
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
    }
    bl_sel = bl_selection + (add_sel or [])
    sr_sel = sr_selection + bl_sel
    sb_sel = sb_selection + bl_sel
    fw_sel = fw_selection + bl_sel


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
        ('SignalRegion', sr_sel, base_weight),
        ('SidebandRegion', sb_sel, base_weight),
        ('BaseLineSelection', bl_sel, base_weight),
        ('FwdSelection', fw_sel, base_weight),
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
            ('SignalRegion',        sr_sel, base_weight + '*' + w),
            ('SidebandRegion',      sb_sel, base_weight + '*' + w),
            ('BaseLineSelection',   bl_sel, base_weight + '*' + w),
            ('FwdSelection',        fw_sel, base_weight + '*' + w),
        ])
        for name, w in (
            ('b_tag_bc__minus',     'weight_btag_bc_down/weight_btag'),
            ('b_tag_bc__plus',      'weight_btag_bc_up/weight_btag'),
            ('b_tag_udsg__minus',   'weight_btag_udsg_down/weight_btag'),
            ('b_tag_udsg__plus',    'weight_btag_udsg_up/weight_btag'),
            ('muon_ID__minus',      'weight_sfmu_id_down/weight_sfmu_id'),
            ('muon_ID__plus',       'weight_sfmu_id_up/weight_sfmu_id'),
            ('muon_trigger__minus', 'weight_sfmu_trg_down/weight_sfmu_trg'),
            ('muon_trigger__plus',  'weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pileup__minus',       'weight_pu_down/weight_pu'),
            ('pileup__plus',        'weight_pu_up/weight_pu'),
            ('jet_pt__minus',       '1'),
            ('jet_pt__plus',        'weight_ak4jet'),
            ('rate__minus',         '0.841886'),  # 1 - (0.05**2 + 0.15**2)**.5
            ('rate__plus',          '1.158114'),  # 1 + (0.05**2 + 0.15**2)**.5
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

    # PDF uncertainty
    sys_params_pdf = {
        'histos': {'vlq_mass': core_histos['vlq_mass']},
        'treename': 'AnalysisTree',
    }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, [
            ('SignalRegion', sr_sel, base_weight+'*weight_pdf_%i/%f'%(i, combo_weights[i])),
        ])
        for i in xrange(100)
    )
    filenames_pdf = dict(
        (s, fs)
        for s, fs in filenames.iteritems()
        if s in varial.settings.my_lh_signals or s in varial.settings.my_rh_signals
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

    for tp in sys_tps:
        iteration[0] += 1
        tp.iteration = 10 * iteration[0]  # batch tp's should not interfere

    # make it complete with a tooloolchain!
    return varial.tools.ToolChain(
        'SysTreeProjectors', sys_tps
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


combo_weights = [
    0.89517049779189073,
    1.01429053659902,
    1.0222920941697375,
    0.96226922692382444,
    0.94149487213971694,
    1.0819818187038894,
    0.93260735523125138,
    1.0079334040255432,
    0.86298621419224386,
    0.94330586948820161,
    0.92129004903942091,
    0.9741587546874263,
    1.1603499813399889,
    0.98671659265544343,
    0.9252785765765712,
    1.0345548238060811,
    1.162448966493733,
    1.0134905770204279,
    0.97866146726220682,
    1.0263896297728308,
    0.93708154947355116,
    0.94522951456200965,
    0.92500212504175761,
    1.1782493288156288,
    1.0626042060054772,
    1.0345267406162011,
    1.0472846641593168,
    0.96288213122246835,
    0.98766053098312134,
    0.97684012093239037,
    1.0615330892824064,
    1.0033917440649909,
    0.95086989865263116,
    0.93308726683001264,
    0.91409398851428225,
    0.93021616715498001,
    0.93814099589410671,
    0.99866972400912879,
    1.0108074779220158,
    0.94574617170905573,
    0.97648750561342446,
    1.0100184515318396,
    0.9627738417115913,
    1.0141041246502458,
    1.1234021963156129,
    0.94033725994048378,
    1.0040322426700354,
    0.90792987590814367,
    1.1642097627916428,
    0.98444955231310372,
    0.93045359059703603,
    0.99511602180027248,
    1.2919222223277018,
    0.97065499201742689,
    1.2677046594025092,
    0.92779917198351858,
    1.0292627856157264,
    0.99270798307364982,
    0.96758092729442857,
    0.99689785837851619,
    0.98430825018208135,
    1.0276935726295764,
    0.97882911614971213,
    0.97791466592375609,
    0.98645291744851005,
    1.2025828756336656,
    1.0217214821327369,
    0.9823407719118723,
    0.96120234945104877,
    0.98233334036843012,
    1.0631576747390923,
    1.0150597167587494,
    0.98120405835577174,
    0.99637763860328687,
    1.021727396828755,
    1.0128653944435222,
    0.91460991548372628,
    0.99457980225682141,
    0.97136936047214406,
    0.97449845655941192,
    1.0200904493899199,
    0.9673112980459142,
    0.98593292670694888,
    1.0048513838334407,
    0.99169879053484766,
    1.0924421422423107,
    1.1736455842101834,
    0.96954308962699232,
    1.0054257360314494,
    0.92885856373108977,
    0.94076808459861494,
    0.91753189130862012,
    1.0411542093957973,
    0.94494274779871257,
    0.99330133789777819,
    0.94709759492001777,
    1.054192859880297,
    1.0086163841231859,
    0.95475748683029238,
    0.96872370971635102,
]


if __name__ == '__main__':
    inp_pat = './*.root'
    varial.tools.Runner(mk_tp(inp_pat))
