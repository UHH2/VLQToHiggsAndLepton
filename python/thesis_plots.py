######################################################
# check THIS out: https://ghm.web.cern.ch/ghm/plots/ #
######################################################

import ctypes
import ROOT
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetEndErrorSize(0)
pb = 'VLQ2HT/Outputs/'
p_presel = '../../VLQSemiLepPreSel/output/VLQ_presel/VLQ_presel_stack/VLQ2HTGenHists/'
ext = '.pdf'

def get_p_lim(sig):
    return pb + 'Limits' + sig + '/DataBackground/'

path_single = {
'gen_higgKinematic_px_lin.pdf':                 p_presel+'higgKinematic_px_lin.pdf',
'gen_higgKinematic_py_lin.pdf':                 p_presel+'higgKinematic_py_lin.pdf',
'gen_topKinematic_px_lin.pdf':                  p_presel+'topKinematic_px_lin.pdf',
'gen_higgTopDr_lin.pdf':                        p_presel+'higgTopDr_lin.pdf',

'gen_topLepKinematic_px_lin.pdf':               p_presel+'topLepKinematic_px_lin.pdf',
'gen_topLepKinematic_py_lin.pdf':               p_presel+'topLepKinematic_py_lin.pdf',
'gen_topProdDrBToLepton_lin.pdf':               p_presel+'topProdDrBToLepton_lin.pdf',
'gen_higgBbDr_lin.pdf':                         p_presel+'higgBbDr_lin.pdf',

'gen_fwJetKinematic_px_log.pdf':                p_presel+'fwJetKinematic_px_log.pdf',
'gen_fwJetKinematic_py_lin.pdf':                p_presel+'fwJetKinematic_py_lin.pdf',

'El_h_n_vtx_lin.pdf':                           pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_n_vtx_lin.pdf',
'Mu_h_n_vtx_lin.pdf':                           pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_n_vtx_lin.pdf',

'El_primary_lepton_eta_lin.pdf':                pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/primary_lepton_eta_lin.pdf',
'Mu_primary_lepton_eta_lin.pdf':                pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/primary_lepton_eta_lin.pdf',

'El_TwoDCut_QCD_lin.pdf':                       pb+'SFramePlots/Stacks/ElChan/Nm1Selection/TwoDCut_QCD_lin.pdf',
'El_TwoDCut_TpB_TH_1200_lin.pdf':               pb+'SFramePlots/Stacks/ElChan/Nm1Selection/TwoDCut_TpB_TH_1200_lin.pdf',

'El_full_jet_eta_lin.pdf':                      pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/full_jet_eta_lin.pdf',
'Mu_full_jet_eta_lin.pdf':                      pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/full_jet_eta_lin.pdf',

'El_leading_jet_pt_log.pdf':                    pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/leading_jet_pt_log.pdf',
'Mu_leading_jet_pt_log.pdf':                    pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/leading_jet_pt_log.pdf',
'El_subleading_jet_pt_log.pdf':                 pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/subleading_jet_pt_log.pdf',
'Mu_subleading_jet_pt_log.pdf':                 pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/subleading_jet_pt_log.pdf',
'El_n_jets_log.pdf':                            pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_jets_log.pdf',
'Mu_n_jets_log.pdf':                            pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_jets_log.pdf',

'El_fwd_jet_pt_log.pdf':                        pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/fwd_jet_pt_log.pdf',
'Mu_fwd_jet_pt_log.pdf':                        pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/fwd_jet_pt_log.pdf',
'El_n_fwd_jets_log.pdf':                        pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_log.pdf',
'Mu_n_fwd_jets_log.pdf':                        pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_log.pdf',

'Mu_ST_lin.pdf':                                pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ST_lin.pdf',
'El_MET_lin.pdf':                               pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/MET_lin.pdf',
'Mu_MET_lin.pdf':                               pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/MET_lin.pdf',

'El_ak8_jet_pt_log.pdf':                        pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ak8_jet_pt_log.pdf',
'Mu_ak8_jet_pt_log.pdf':                        pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ak8_jet_pt_log.pdf',
'El_ak8_jet_eta_lin.pdf':                       pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ak8_jet_eta_lin.pdf',
'Mu_ak8_jet_eta_lin.pdf':                       pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ak8_jet_eta_lin.pdf',
'El_n_ak8_jets_log.pdf':                        pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_ak8_jets_log.pdf',
'Mu_n_ak8_jets_log.pdf':                        pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_ak8_jets_log.pdf',

'El_h_pt_lin.pdf':                              pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_pt_lin.pdf',
'Mu_h_pt_lin.pdf':                              pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_pt_lin.pdf',
'El_h_mass_lin.pdf':                            pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_mass_lin.pdf',

'Mu_h_mass_pruned_lin.pdf':                     pb+'SelectionsMuJERC/Stacks/TTbar2Selection/h_mass_pruned_lin.pdf',
'Mu_h_mass_softdrop_lin.pdf':                   pb+'SelectionsMuJERC/Stacks/TTbar2Selection/h_mass_softdrop_lin.pdf',

'El_tlep_pt_lin.pdf':                           pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_pt_lin.pdf',
'El_tlep_eta_lin.pdf':                          pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_eta_lin.pdf',
'Mu_tlep_eta_lin.pdf':                          pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/tlep_eta_lin.pdf',
'El_tlep_mass_lin.pdf':                         pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_mass_lin.pdf',

'Mu_matching_hig_mass_lin.pdf':                 pb+'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_hig_mass_lin.pdf',
'Mu_matching_top_mass_lin.pdf':                 pb+'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_top_mass_lin.pdf',
'Mu_matching_top_hig_dr_lin.pdf':               pb+'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_top_hig_dr_lin.pdf',

'El_vlq_pt_lin.pdf':                            pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_pt_lin.pdf',
'Mu_vlq_pt_lin.pdf':                            pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_pt_lin.pdf',
'El_vlq_eta_lin.pdf':                           pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_eta_lin.pdf',
'Mu_vlq_eta_lin.pdf':                           pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_eta_lin.pdf',
'El_bl_vlq_mass_lin.pdf':                       pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_mass_lin.pdf',
'Mu_bl_vlq_mass_lin.pdf':                       pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_mass_lin.pdf',

'El_h_n_subjet_btags_lin.pdf':                  pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_n_subjet_btags_lin.pdf',
'Mu_h_n_subjet_btags_lin.pdf':                  pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_n_subjet_btags_lin.pdf',
'El_n_fwd_jets_lin.pdf':                        pb+'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_lin.pdf',
'Mu_n_fwd_jets_lin.pdf':                        pb+'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_lin.pdf',

'Mu_ct_Nominal_h_pt.pdf':                       pb+'SidebandsMu/Nominal/Plotter/h_pt_lin.pdf',
'Mu_ct_Nominal_tlep_pt.pdf':                    pb+'SidebandsMu/Nominal/Plotter/tlep_pt_lin.pdf',

'El_ct_JES__minus.pdf':                         pb+'SidebandsEl/JES__minus/Plotter/vlq_mass_lin.pdf',
'Mu_ct_JES__minus.pdf':                         pb+'SidebandsMu/JES__minus/Plotter/vlq_mass_lin.pdf',

'El_Fw0B0_vlq_mass_lin.pdf':                    pb+'SelectionsElNoFwdSys/Stacks/Fw0B0Selection/vlq_mass_lin.pdf',
'Mu_Fw0B0_vlq_mass_lin.pdf':                    pb+'SelectionsMuNoFwdSys/Stacks/Fw0B0Selection/vlq_mass_lin.pdf',

'El_ct_MultiRegion.pdf':                        pb+'SidebandsEl/MultiRegion/Plotter/vlq_mass_lin.pdf',
'Mu_ct_MultiRegion.pdf':                        pb+'SidebandsMu/MultiRegion/Plotter/vlq_mass_lin.pdf',

'El_ct_DataB0vsSB.pdf':                         pb+'SidebandsEl/DataB0vsSB/Plotter/vlq_mass_lin.pdf',
'Mu_ct_DataB0vsSB.pdf':                         pb+'SidebandsMu/DataB0vsSB/Plotter/vlq_mass_lin.pdf',

'El_B0_n_fwd_jets_lin.pdf':                     pb+'SelectionsElNoFwdSys/Stacks/B0Selection/n_fwd_jets_lin.pdf',
'Mu_B0_n_fwd_jets_lin.pdf':                     pb+'SelectionsMuNoFwdSys/Stacks/B0Selection/n_fwd_jets_lin.pdf',
'El_B0_fwd_jet_eta_lin.pdf':                    pb+'SelectionsElNoFwdSys/Stacks/B0Selection/fwd_jet_eta_lin.pdf',
'Mu_B0_fwd_jet_eta_lin.pdf':                    pb+'SelectionsMuNoFwdSys/Stacks/B0Selection/fwd_jet_eta_lin.pdf',

'El_money_bins_lin.pdf':                        pb+'LimitsTpBLH/DataBackground/PostFitBins/SignalRegion__el_lin.pdf',
'Mu_money_bins_lin.pdf':                        pb+'LimitsTpBLH/DataBackground/PostFitBins/SignalRegion__mu_lin.pdf',

'El_ct_JER__minus.pdf':                         pb+'SidebandsEl/JER__minus/Plotter/vlq_mass_lin.pdf',
'Mu_ct_JER__minus.pdf':                         pb+'SidebandsMu/JER__minus/Plotter/vlq_mass_lin.pdf',
'El_ct_TTbar__minus.pdf':                       pb+'SidebandsEl/TTbar__minus/Plotter/vlq_mass_lin.pdf',
'Mu_ct_JER__plus.pdf':                          pb+'SidebandsMu/JER__plus/Plotter/vlq_mass_lin.pdf',
'El_ct_WJets__plus.pdf':                        pb+'SidebandsEl/WJets__plus/Plotter/vlq_mass_lin.pdf',
'Mu_ct_QCD__minus.pdf':                         pb+'SidebandsMu/QCD__minus/Plotter/vlq_mass_lin.pdf',

'SigInj_0700_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0700/LimitGraphsPlot/Graph_log.pdf',
'SigInj_0800_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0800/LimitGraphsPlot/Graph_log.pdf',
'SigInj_0900_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0900/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1000_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1000/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1100_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1100/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1200_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1200/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1500_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1500/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1800_limits_log.pdf':                   pb+'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1800/LimitGraphsPlot/Graph_log.pdf',
}

def_legend_poosition = (.62, .82, .36, .85)
two_column_legeeeend = (.40, .93, .58, .85)
def_chan = (.2, .8)
def_params = def_legend_poosition, def_chan

token_configs = (  #             legend x1 x2 y1 y2    chan pos
# swap legend and chan
(('_eta_',
  'El_bl_vlq_mass_',
  'El_Fw0B0_vlq_mass_'),         ((.18, .38, .36, .85), (.9, .8))),

# legend into middle
(('_fwd_jet_eta_',),             ((.40, .66, .36, .85), def_chan)),
(('_limits',),                   ((.55, .75, .63, .85), def_chan)),
(('_matching_', 'gen_'),         ((.62, .82, .67, .85), def_chan)),

# small legend in money plots
(('_money_bins_',),              ((.65, .85, .55, .85), def_chan)),

(('_ct_',),                      ((.62, .82, .67, .85), def_chan)),
(('_ct_DataB0vsSB',),            ((.62, .82, .61, .85), def_chan)),
(('_ct_MultiRegion',),           ((.62, .82, .55, .85), def_chan)),

# two columns in top row
(('_fwd_jet_pt_log',
  '_vlq_eta_lin',
  '_n_jets_log',),               (two_column_legeeeend, def_chan)),
)


plot_config = {
'selblock_h_mass_lin':           (def_legend_poosition, def_chan),
'selblock_primary_el_pt_lin':    ((.40, .66, .36, .85), (.61,.8)),
}


ratio_y_range = {
'_B0_fwd_jet_eta_lin':          (-0.9, 0.49),
'_full_jet_eta_lin':            (-0.9, 0.49),
'_money_bins_lin':              (-0.9, 1.7),
}


y_max_values = {
'El_money_bins_lin':            11.,
'El_n_jets_log':                200000.,
'Mu_n_jets_log':                999999.,
'El_vlq_eta_lin':               420.,
'Mu_vlq_eta_lin':               1700.,
}


def get_canvas(name):
    path = path_single[name]
    path, basename = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    if basename.endswith('_log') or basename.endswith('_lin'):
        basename = basename[:-4]
    f = ROOT.TFile(path + '/_varial_rootobjects.root.rt')
    c = f.Get('{n}/{n}'.format(n=basename))
    f.Close()
    return c


def handle_plot(name):
    save_name = name.replace('.pdf', '')

    # get parameters
    def_par = def_params  # get local variable
    for toks, params in token_configs:
        assert isinstance(toks, tuple)
        for t in toks:
            if t in save_name:
                def_par = params
    (x1, x2, y1, y2), (chan_x, chan_y) = plot_config.get(save_name, def_par)


    is_el_chan = name.startswith('El_')
    is_mu_chan = name.startswith('Mu_')
    is_limit = '_limits' in name
    is_log = save_name.endswith('_log')
    lumi = 2.2 if is_el_chan else 2.3 if is_mu_chan or is_limit or name.startswith('gen_') else 0.
    chan_name = 'Electron' if is_el_chan else 'Muon' if is_mu_chan else ''
    is_sim = (not lumi) or name.split('_')[1] == 'sim'

    # get some info and fetch canvas
    c = get_canvas(name)

    # pull items out of canvas
    canv_prims = list(c.GetListOfPrimitives())
    legend = next(p for p in canv_prims if isinstance(p, ROOT.TLegend))
    entries_tlist = legend.GetListOfPrimitives()
    entries = list(entries_tlist)
    if isinstance(canv_prims[0], ROOT.TPad) and isinstance(canv_prims[1], ROOT.TPad):
        main_pad, second_pad, size_factor = canv_prims[0], canv_prims[1], 0.8
    else:
        main_pad, second_pad, size_factor = c, None, 1

    def fix_y_pos(old_pos):
        return old_pos*size_factor + (1 - size_factor)

    main_hists = list(
        p
        for p in main_pad.GetListOfPrimitives()
        if any(isinstance(p, cl) for cl in (ROOT.THStack, ROOT.TH1, ROOT.TGraph))
    )

    # set margins
    c.Modified()
    c.Update()
    main_pad.SetTopMargin(0.087)
    main_pad.SetRightMargin(0.05)
    if second_pad:
        second_pad.SetRightMargin(0.05)
        second_pad.SetTopMargin(0.05)

        # lift ylow very slightly
        pars = [ctypes.c_double(), ctypes.c_double(), ctypes.c_double(), ctypes.c_double()]
        main_pad.GetPadPar(*pars)
        pars = [d.value for d in pars]
        pars[1] += 0.002  # lift ylow very slightly
        main_pad.SetPad(*pars)

        # redraw to squelch strange box under frame
        second_pad.cd()
        second_pad.SetBottomMargin(0.1 + second_pad.GetBottomMargin())
        c.cd()
        second_pad.Draw()
        main_pad.cd()

    # legend
    # legend.SetTextSize(1.1 * legend.GetTextSize())
    legend.SetX1NDC(x1)
    legend.SetX2NDC(x2)
    legend.SetY1NDC(fix_y_pos(y1))
    legend.SetY2NDC(fix_y_pos(y2))
    first_legend_entry = entries[0]
    if first_legend_entry.GetLabel() == 'Data':
        first_legend_entry.SetOption('pe')
        main_hists[-1].SetMarkerSize(1)
    if def_par[0] == two_column_legeeeend:
        legend.SetNColumns(2)
        entries_tlist.Clear()
        for i in (5,0,6,1,7,2,8,3,9,4):  # mc bkg in first column
            entries_tlist.AddLast(entries[i])

    # labels
    bigTextSize = 0.075 * size_factor
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)

    # the canvas is cleared so it must be done early
    if 'TwoDCut_' in save_name:
        c.SetRightMargin(0.05)
        c.RecursiveRemove(legend)
        h = main_hists[-1]
        h.Scale(1./h.Integral())
        h.SetFillStyle(1001)
        h.SetLineWidth(2)
        h.SetLineColor(ROOT.kBlue+2)
        h.SetFillColor(ROOT.kBlue+1)  # 851)
        c.Clear()
        h.Draw('BOX')
        h.GetXaxis().SetTitle('#DeltaR(l, j)')
        h.GetYaxis().SetTitle('p_{T}^{rel}(l, j)')

        if 'QCD' in save_name:
            latex.DrawLatex(0.2, 0.65, 'Multijet background')
        else:
            latex.DrawLatex(0.2, 0.65, 'T_{lh}(1200) signal')

    # a white box is needed to hide ROOT-foo
    if name.startswith('gen_'):
        box = ROOT.TPave(0.155, 0.9145, 0.9, 1., 0, 'brNDC')
        box.SetFillColor(ROOT.kWhite)
        box.Draw()

    # lumi / sqrt s text
    lumi_line = ('%.1f fb^{-1} (13 TeV)' % lumi) if lumi else '(13 TeV)'
    lumi_txt = ROOT.TPaveText(0.5, 0.87, 0.975, 1.0, 'brNDC')
    lumi_txt.AddText(lumi_line)
    lumi_txt.SetTextColor(ROOT.kBlack)
    lumi_txt.SetTextFont(42)
    lumi_txt.SetTextAlign(31)
    lumi_txt.SetTextSize(0.06 * size_factor)
    lumi_txt.SetFillStyle(0)
    lumi_txt.SetBorderSize(0)
    lumi_txt.Draw('same')

    if is_sim:
        latex.SetTextFont(52)
        latex.SetTextAlign(31 if chan_x > 0.5 else 11)
        latex.SetTextSize(0.76 * bigTextSize)
        latex.DrawLatex(chan_x, fix_y_pos(chan_y), 'Simulation')

    # electron / muon channel
    if chan_name:
        chan_offset = 1.0*bigTextSize if is_sim else 0.
        chan_txt = 'channel'
        latex.SetTextFont(42)
        latex.SetTextAlign(31 if chan_x > 0.5 else 11)
        latex.SetTextSize(0.65 * bigTextSize)
        latex.DrawLatex(chan_x, fix_y_pos(chan_y - chan_offset), chan_name)
        latex.DrawLatex(chan_x, fix_y_pos(chan_y - chan_offset - 0.7*bigTextSize), chan_txt)

    # darker shade on uncertainties
    for obj in main_hists:
        if 'uncert.' in obj.GetTitle():
            obj.SetFillColor(ROOT.kBlack)

    # fix err fill style
    if isinstance(main_hists[0], ROOT.THStack):
        stl, clr = 3475, ROOT.kGray+3
        main_hists[1].SetFillStyle(stl)
        main_hists[1].SetFillColor(clr)
        if second_pad:
            err_hist = second_pad.GetListOfPrimitives()[1]
            err_hist.SetFillStyle(stl)
            err_hist.SetFillColor(clr)

    # x and y axes
    first_obj = main_hists[0]
    x_axis = (second_pad or main_pad).GetListOfPrimitives()[1].GetXaxis()
    x_axis.SetTitle(x_axis.GetTitle().replace('/ GeV', '(GeV)'))

    y_axis = first_obj.GetYaxis()
    y_axis.CenterTitle(0)
    y_axis.SetTitle(y_axis.GetTitle().replace('events / ', 'Events / '))

    x_axis_1st = main_pad.GetListOfPrimitives()[1].GetXaxis() if second_pad else None
    y_axis_2nd = second_pad.GetListOfPrimitives()[1].GetYaxis() if second_pad else None

    # main axes font sizes
    y_axis.SetTitleOffset(1.45)
    x_axis.SetTitleOffset(1.0)
    x_axis.SetTitleSize(1.3 * x_axis.GetTitleSize())
    if not y_axis_2nd:  # all plots without ratio plot
        y_axis.SetTitleSize(1.3 * y_axis.GetTitleSize())
        y_axis.SetTitleOffset(1.2)
        x_axis.SetTitleOffset(1.)

    # fix signal lines
    if (any(isinstance(h, ROOT.THStack) for h in main_hists) and
        len(main_hists) > 4 and
        '_ct_' not in save_name
    ) or (
        save_name.startswith('gen_') or
        save_name.startswith('Mu_matching_')
    ):
        offset = {5:1, 3:1}.get(len(main_hists), 2)
        for i in xrange(3):
            main_hists[-offset-i].SetLineWidth(2)
            main_hists[-offset-i].SetLineColor(602)
            main_hists[-offset-i].SetLineStyle(i+1)

    max_y_val = max(h.GetMaximum() for h in main_hists)
    if save_name in y_max_values:
        max_y_val = y_max_values[save_name]
        first_obj.SetMaximum(max_y_val)
    elif is_log:
        first_obj.SetMaximum(max_y_val*10)
    else:
        first_obj.SetMaximum(max_y_val*1.4)
    if not (is_log and max_y_val > 999):
        y_axis.SetNoExponent()

    for token, rt_mi_ma in ratio_y_range.items():
        if save_name.endswith(token):
            y_axis_2nd.SetRangeUser(*rt_mi_ma)

    # if y_min:
    #     first_obj.SetMinimum(y_min)  # nope.... doesn't exist

    if is_log:
        main_pad.SetLogy()

    if is_limit:
        legend.SetTextSize(1.2 * legend.GetTextSize())
        x_axis = first_obj.GetXaxis()
        x_axis.SetRangeUser(700, 1800)
        y_axis.SetTitleOffset(1.0)

        first_obj.SetMinimum(0.02)
        y_axis.SetTitle(y_axis.GetTitle().replace(
            '->', '#rightarrow').replace(
            '/ pb', '(pb)').replace(
            'BR', '#bf{#it{#Beta}}'))
        entries = list(legend.GetListOfPrimitives())
        legend.GetListOfPrimitives().RecursiveRemove(entries[0])
        c.GetListOfPrimitives().RecursiveRemove(main_hists[-1])
        latex.SetTextFont(42)
        mass = int(save_name.split('_')[1])
        strength = {700:4, 800:3, 900:2}.get(mass, 1)
        latex.DrawLatex(
            0.2, 0.2, 'Signal injection test: T_{lh}(%i), #beta_{s}=%i.0'%(mass, strength))

    if '_money_' in name:
        # legend.SetTextSize(1.3 * legend.GetTextSize())
        entries[-1].GetObject().SetLineWidth(2)
        entries[-1].GetObject().SetLineColor(1)
        entries[-2].SetLabel('Stat. uncert. bkg.')
        for e in entries:
            e.SetLabel(e.GetLabel().replace('rightarrowtH', 'rightarrowtH (1pb)'))

    if '_ct_' in save_name:
        for e in entries:
            if e.GetLabel() == 'Fw0B0Selection':
                e.SetLabel('Region A')
            if e.GetLabel() == 'Fw1B0Selection':
                e.SetLabel('Region B')
            if e.GetLabel() == 'SignalRegion':
                e.SetLabel('Signal region')
            if e.GetLabel() == 'SidebandRegion':
                e.SetLabel('Control region')
                h = e.GetObject()
                h.SetOption('hist')
                h.SetLineColor(1)
                h.SetLineWidth(2)
            if e.GetLabel() == 'Stat. uncert. MC':
                e.SetLabel('Stat. uncert. bkg.')
                entries_tlist.RecursiveRemove(e)
                entries_tlist.Add(e)

        if any(s in name for s in ('minus', 'plus')):
            text = '(%s)' % save_name.split('_ct_')[-1].replace('__', ' ')
            for a, b in [
                ('QCD', '#sigma_{Multijet}'),
                ('TTbar', '#sigma_{t#bar{t}}'),
                ('WJets', '#sigma_{W+jets}'),
            ]:
                text = text.replace(a, b)
            latex.DrawLatex(0.2, 0.75, text)

    if save_name.endswith('_ct_DataB0vsSB'):
        entries[0].SetOption('P')
        entries[1].SetOption('P')
        entries[2].SetLabel('Stat. uncert. CR')
        latex.DrawLatex(0.2, 0.75, '(Data)')


    if name == 'El_ak8_jet_pt_log.pdf':
        x_axis.SetRangeUser(200., 2000.)
        x_axis_1st.SetRangeUser(200., 2000.)

    if save_name == 'Mu_matching_hig_mass_lin':
        x_axis.SetTitle('Higgs boson candidate mass (GeV)')
        y_axis.SetTitle('Events / 5 GeV')

    if save_name == 'Mu_matching_top_mass_lin':
        x_axis.SetTitle('top quark candidate mass (GeV)')
        y_axis.SetTitle('Events / 5 GeV')

    if save_name == 'Mu_matching_top_hig_dr_lin':
        y_axis.SetTitle('Events')

    if name.startswith('gen_'):
        y_axis.SetTitle('Events')
        x_axis.SetTitle(x_axis.GetTitle().replace(
            'ass.', 'associated').replace(
            'top products', 't decay products').replace(
            'b to l', 'b, l').replace(
            '(H, top)', '(H, t)'
        ))

    if save_name == 'gen_higgBbDr_lin':
        x_axis.SetTitle('H decay products: #DeltaR(b, #bar{b})')

    if save_name == 'El_primary_lepton_eta_lin':
        x_axis.SetTitle('Electron #eta')

    if save_name == 'Mu_primary_lepton_eta_lin':
        x_axis.SetTitle('Muon #eta')

    c.Modified()
    c.Update()

    c.cd()
    main_pad.Draw()

    # c.SaveAs('Beautifier/'+name.replace('.pdf', '.root'))
    c.SaveAs('Beautifier/'+name)


if __name__ == '__main__':
    for p in sorted(path_single):
        handle_plot(p)
