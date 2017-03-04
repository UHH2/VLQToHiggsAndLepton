######################################################
# check THIS out: https://ghm.web.cern.ch/ghm/plots/ #
######################################################

import ctypes
import ROOT
import os

ROOT.gStyle.SetEndErrorSize(0)
pb = 'VLQ2HT/Outputs/'
ext = '.pdf'

def get_p_lim(sig):
    return pb + 'Limits' + sig + '/DataBackground/'


path_single = {
'El_h_n_vtx_lin.pdf':               pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_n_vtx_lin.pdf',
'Mu_h_n_vtx_lin.pdf':               pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_n_vtx_lin.pdf',

'El_primary_lepton_eta_lin.pdf':    pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/primary_lepton_eta_lin.pdf',
'Mu_primary_lepton_eta_lin.pdf':    pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/primary_lepton_eta_lin.pdf',

'El_TwoDCut_QCD_lin.pdf':           pb + 'SFramePlots/Stacks/ElChan/Nm1Selection/TwoDCut_QCD_lin.pdf',
'El_TwoDCut_TpB_TH_1200_lin.pdf':   pb + 'SFramePlots/Stacks/ElChan/Nm1Selection/TwoDCut_TpB_TH_1200_lin.pdf',

'El_leading_jet_pt_log.pdf':        pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/leading_jet_pt_log.pdf',
'Mu_leading_jet_pt_log.pdf':        pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/leading_jet_pt_log.pdf',
'El_subleading_jet_pt_log.pdf':     pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/subleading_jet_pt_log.pdf',
'Mu_subleading_jet_pt_log.pdf':     pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/subleading_jet_pt_log.pdf',
'El_ak4_jet_eta_lin.pdf':           pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ak4_jet_eta_lin.pdf',
'Mu_ak4_jet_eta_lin.pdf':           pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ak4_jet_eta_lin.pdf',
'El_n_jets_log.pdf':                pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_jets_log.pdf',
'Mu_n_jets_log.pdf':                pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_jets_log.pdf',

'El_fwd_jet_pt_log.pdf':            pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/fwd_jet_pt_log.pdf',
'Mu_fwd_jet_pt_log.pdf':            pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/fwd_jet_pt_log.pdf',
'El_fwd_jet_eta_lin.pdf':           pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/fwd_jet_eta_lin.pdf',
'Mu_fwd_jet_eta_lin.pdf':           pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/fwd_jet_eta_lin.pdf',
'El_n_fwd_jets_log.pdf':            pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_log.pdf',
'Mu_n_fwd_jets_log.pdf':            pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_fwd_jets_log.pdf',

'Mu_ST_lin.pdf':                    pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ST_lin.pdf',
'El_MET_lin.pdf':                   pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/MET_lin.pdf',
'Mu_MET_lin.pdf':                   pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/MET_lin.pdf',

'El_ak8_jet_pt_log.pdf':            pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ak8_jet_pt_log.pdf',
'Mu_ak8_jet_pt_log.pdf':            pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ak8_jet_pt_log.pdf',
'El_ak8_jet_eta_lin.pdf':           pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ak8_jet_eta_lin.pdf',
'Mu_ak8_jet_eta_lin.pdf':           pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/ak8_jet_eta_lin.pdf',
'El_n_ak8_jets_log.pdf':            pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/n_ak8_jets_log.pdf',
'Mu_n_ak8_jets_log.pdf':            pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/n_ak8_jets_log.pdf',

'El_h_pt_lin.pdf':                  pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_pt_lin.pdf',
'Mu_h_pt_lin.pdf':                  pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_pt_lin.pdf',
'El_h_mass_lin.pdf':                pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_mass_lin.pdf',

'Mu_h_mass_pruned_lin.pdf':         pb + 'SelectionsMuJERC/Stacks/TTbar2Selection/h_mass_pruned_lin.pdf',
'Mu_h_mass_softdrop_lin.pdf':       pb + 'SelectionsMuJERC/Stacks/TTbar2Selection/h_mass_softdrop_lin.pdf',

'El_tlep_pt_lin.pdf':               pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_pt_lin.pdf',
'El_tlep_eta_lin.pdf':              pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_eta_lin.pdf',
'Mu_tlep_eta_lin.pdf':              pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/tlep_eta_lin.pdf',
'El_tlep_mass_lin.pdf':             pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/tlep_mass_lin.pdf',

'Mu_matching_hig_mass_lin.pdf':     pb + 'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_hig_mass_lin.pdf',
'Mu_matching_top_mass_lin.pdf':     pb + 'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_top_mass_lin.pdf',
'Mu_matching_top_hig_dr_lin.pdf':   pb + 'SFramePlotsNoRebin/Stacks/MuChan/Chi2SignalMatch/matching_top_hig_dr_lin.pdf',

'El_vlq_pt_lin.pdf':                pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_pt_lin.pdf',
'Mu_vlq_pt_lin.pdf':                pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_pt_lin.pdf',
'El_vlq_eta_lin.pdf':               pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_eta_lin.pdf',
'Mu_vlq_eta_lin.pdf':               pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_eta_lin.pdf',
'El_bl_vlq_mass_lin.pdf':           pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/vlq_mass_lin.pdf',
'Mu_bl_vlq_mass_lin.pdf':           pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/vlq_mass_lin.pdf',

'El_h_n_subjet_btags_lin.pdf':      pb + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/h_n_subjet_btags_lin.pdf',
'Mu_h_n_subjet_btags_lin.pdf':      pb + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_n_subjet_btags_lin.pdf',

'El_Fw0B0_vlq_mass_lin.pdf':        pb + 'SelectionsElNoFwdSys/Stacks/Fw0B0Selection/vlq_mass_lin.pdf',
'Mu_Fw0B0_vlq_mass_lin.pdf':        pb + 'SelectionsMuNoFwdSys/Stacks/Fw0B0Selection/vlq_mass_lin.pdf',

'El_n_fwd_jets_log.pdf':            pb + 'SelectionsElNoFwdSys/Stacks/B0Selection/n_fwd_jets_log.pdf',
'Mu_n_fwd_jets_log.pdf':            pb + 'SelectionsMuNoFwdSys/Stacks/B0Selection/n_fwd_jets_log.pdf',
'El_fwd_jet_eta_lin.pdf':           pb + 'SelectionsElNoFwdSys/Stacks/B0Selection/fwd_jet_eta_lin.pdf',
'Mu_fwd_jet_eta_lin.pdf':           pb + 'SelectionsMuNoFwdSys/Stacks/B0Selection/fwd_jet_eta_lin.pdf',

'SigInj_0700_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0700/LimitGraphsPlot/Graph_log.pdf',
'SigInj_0800_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0800/LimitGraphsPlot/Graph_log.pdf',
'SigInj_0900_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M0900/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1000_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1000/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1100_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1100/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1200_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1200/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1500_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1500/LimitGraphsPlot/Graph_log.pdf',
'SigInj_1800_log.pdf':              pb + 'LimitsTpBLH/DataBackgroundSigInjSignal_TpB_TH_LH_M1800/LimitGraphsPlot/Graph_log.pdf',
}


def_leg_pos = (.62, .82, .36, .85)
def_chan_pos = (.2, .8)

plot_config = {  #                    y_min_max,   legend x1 x2 y1 y2    chan pos
'selblock_h_mass_lin.pdf':          ((None, 5500), (.62, .82, .24, .73), (.61,.8)),
'selblock_primary_el_pt_lin.pdf':   ((None, 1100), (.62, .82, .24, .73), (.61,.8)),
'selblock_primary_mu_pt_lin.pdf':   ((None, 6000), (.62, .82, .24, .73), (.61,.8)),
'selblock_ST_lin.pdf':              ((None, 1050), (.62, .82, .36, .85), (.2, .7)),

'Sideband__el_lin.pdf':             ((None,  150), (.18, .37, .36, .85), (.9, .7)),
'Sideband__mu_lin.pdf':             ((None,  800), (.62, .82, .36, .85), (.2, .7)),

'Sideband_vs_SignalRegion__el.pdf': ((None, 0.19), (.62, .82, .67, .85), (.2,.62)),
'Sideband_vs_SignalRegion__mu.pdf': ((None,  0.0), (.62, .82, .67, .85), (.2,.62)),

'SignalRegion_data__el_lin.pdf':    ((None, 13.5), (.20, .40, .36, .85), (.9, .7)),
'SignalRegion_data__mu_lin.pdf':    ((None, 50.0), (.60, .80, .36, .85), (.2, .7)),

'SignalRegion__el_lin.pdf':         ((None, 13.5), (.20, .40, .46, .85), (.2,.38)),
'SignalRegion__mu_lin.pdf':         ((None, 50.0), (.60, .80, .46, .85), (.2,.62)),

'SignalRegion_bkg__el_lin.pdf':     ((None, 11.0), (.65, .85, .55, .85), (.2, .7)),
'SignalRegion_bkg__mu_lin.pdf':     ((None, 35.0), (.65, .85, .55, .85), (.2, .7)),

'tlep_mass_lin.pdf':                ((None, 2000), (.62, .82, .24, .73), (.61,.8)),
'tlep_pt_lin.pdf':                  ((None, 2700), (.62, .82, .24, .73), (.61,.8)),

'TpBLH_limits.pdf':                 ((None,  99.), (.35, .55, .58, .85), (.9, .6)),
'TpTRH_limits.pdf':                 ((None,  99.), (.35, .55, .58, .85), (.9, .6)),
}


def get_canvas(name):
    path = path_single[name]
    path, basename = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    is_log_plot = basename.endswith('_log')
    if is_log_plot or basename.endswith('_lin'):
        basename = basename[:-4]
    f = ROOT.TFile(path + '/_varial_rootobjects.root.rt')
    c = f.Get('{n}/{n}'.format(n=basename))
    f.Close()
    return c, is_log_plot


def handle_plot(name):
    # get parameters
    lumi, (x1, x2, y1, y2), (chan_x, chan_y), y_scale_max = plot_config[name]
    save_name = name.replace('.pdf', '')

    # get some info and fetch canvas
    c, is_log_plot = get_canvas(name)

    # pull items out of canvas
    canv_prims = list(c.GetListOfPrimitives())
    legend = next(p for p in canv_prims if isinstance(p, ROOT.TLegend))
    if isinstance(canv_prims[0], ROOT.TPad) and isinstance(canv_prims[1], ROOT.TPad):
        main_pad, second_pad, size_factor = canv_prims[0], canv_prims[1], 0.8
    else:
        main_pad, second_pad, size_factor = c, None, 1

    def get_pos(old_pos):
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
    legend.SetY1NDC(get_pos(y1))
    legend.SetY2NDC(get_pos(y2))
    first_legend_entry = legend.GetListOfPrimitives()[0]
    if first_legend_entry.GetLabel() == 'Data':
        first_legend_entry.SetOption('pe')
        main_hists[-1].SetMarkerSize(1)

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

    # CMS preliminary text
    cmsTextSize = 0.075 * size_factor
    latex = ROOT.TLatex()
    latex.SetNDC()

    latex.SetTextFont(61)
    latex.SetTextSize(cmsTextSize)
    latex.SetTextAlign(31 if cms_x > 0.5 else 11)
    latex.DrawLatex(cms_x, get_pos(cms_y), 'CMS')

    latex.SetTextFont(52)
    latex.SetTextAlign(31 if cms_x > 0.5 else 11)
    latex.SetTextSize(0.76 * cmsTextSize)
    if (not lumi) or name.startswith('SignalRegion__'):
        latex.DrawLatex(cms_x, get_pos(cms_y - 1.0*cmsTextSize), 'Simulation')

    # electron / muon channel
    if chan:
        chan_txts = {1: 'Electron', 2: 'Muon', 3: 'Electron+muon'}
        chan_txt2 = 'channel'
        latex.SetTextFont(42)
        latex.SetTextAlign(31 if chan_x > 0.5 else 11)
        latex.SetTextSize(0.65 * cmsTextSize)
        latex.DrawLatex(chan_x, get_pos(chan_y), chan_txts[chan])
        latex.DrawLatex(chan_x, get_pos(chan_y - 0.7*cmsTextSize), chan_txt2)

    # darker shade on uncertainties
    for obj in main_hists:
        if 'uncert.' in obj.GetTitle():
            obj.SetFillColor(ROOT.kBlack)

    # x and y axes
    first_obj = main_hists[0]
    x_axis = (second_pad or main_pad).GetListOfPrimitives()[1].GetXaxis()
    x_axis.SetTitle(x_axis.GetTitle().replace('/ GeV', '(GeV)'))

    y_axis = first_obj.GetYaxis()
    y_axis.CenterTitle(0)
    y_axis.SetNoExponent()
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


    # if y_axis_2nd:
    #     y_axis.SetTitleSize(0.8 * y_axis.GetTitleSize())  # y-titles were to large
    #     y_axis.SetTitleOffset(1.6)
    #     y_axis.SetLabelSize(0.8 * y_axis.GetLabelSize())

    # fix signal lines
    if any(isinstance(h, ROOT.THStack) for h in main_hists) and 4 < len(main_hists):
        offset = 1 if len(main_hists) == 5 else 2
        for i in xrange(3):
            main_hists[-offset-i].SetLineWidth(2)
            main_hists[-offset-i].SetLineColor(602)
            main_hists[-offset-i].SetLineStyle(i+1)

    # fix err fill style
    if isinstance(main_hists[0], ROOT.THStack):
        stl, clr = 3475, ROOT.kGray+3
        main_hists[1].SetFillStyle(stl)
        main_hists[1].SetFillColor(clr)
        if second_pad:
            err_hist = second_pad.GetListOfPrimitives()[1]
            err_hist.SetFillStyle(stl)
            err_hist.SetFillColor(clr)

    if y_scale_max:
        first_obj.SetMaximum(y_scale_max)

    if save_name.endswith('_log'):
        main_pad.SetLogy()

    if save_name.endswith('_limits'):
        legend.SetTextSize(1.2 * legend.GetTextSize())
        x_axis = first_obj.GetXaxis()
        x_axis.SetRangeUser(700, 1800)

    if name == 'tlep_pt_lin.pdf':
        x_axis.SetTitle('t quark candidate p_{T} (GeV)')

    if name == 'tlep_mass_lin.pdf':
        x_axis.SetTitle('t quark candidate mass (GeV)')

    if name == 'selblock_primary_el_pt_lin.pdf':
        x_axis.SetTitle('Electron p_{T} (GeV)')

    if name == 'selblock_primary_mu_pt_lin.pdf':
        x_axis.SetTitle('Muon p_{T} (GeV)')

    if name.startswith('sel_eff_'):
        legend.SetTextSize(1.3 * legend.GetTextSize())
        y_axis.SetTitleOffset(1.0)
        # y_axis.SetTitle('Arbitrary units')
    elif 'limit' not in name:
        x_axis.SetTitle(x_axis.GetTitle().replace('T quark mass', 'T quark candidate mass'))

    if name.startswith('Sideband_vs_SignalRegion__'):
        y_axis.SetTitle('Arbitrary units')

    # more detail fixings...
    if save_name.endswith('_limits'):
        y_axis.SetTitleOffset(1.0)

    if save_name.endswith('H_limits'):
        main_pad.SetLogy()
        first_obj.SetMinimum(0.02)
        y_axis.SetTitle(y_axis.GetTitle().replace(
            '->', '#rightarrow').replace(
            '/ pb', '(pb)').replace(
            'BR', '#bf{#it{#Beta}}'))
        entries = list(legend.GetListOfPrimitives())
        entries[0].SetLabel(entries[0].GetLabel().replace(
            'Tb, ', 'pp#rightarrowT_{lh}b+X, ').replace(
            'Tt, ', 'pp#rightarrowT_{rh}t+X, ').replace(
            'BR', '#it{B}').replace(
            '=1.0,', '=0.5,'))
        th = main_hists[-1]
        for i in xrange(th.GetN()):
            x, y = ctypes.c_double(), ctypes.c_double()
            th.GetPoint(i, x, y)
            th.SetPoint(i, x.value, y.value / 4.)
        # y_axis.SetRangeUser(0.01, 99.)
        th.Draw()

    if name.startswith('SignalRegion_bkg__'):
        y_axis_2nd.SetRangeUser(-0.9, 1.7)
        # legend.SetTextSize(1.3 * legend.GetTextSize())
        entries = list(legend.GetListOfPrimitives())
        entries[-1].GetObject().SetLineWidth(2)
        entries[-1].GetObject().SetLineColor(1)
        entries[-2].SetLabel('Stat. uncert. bkg.')
        for e in entries:
            e.SetLabel(e.GetLabel().replace('rightarrowtH', 'rightarrowtH (1pb)'))

    if name.startswith('Sideband_vs_SignalRegion__'):
        # legend.SetTextSize(1.3 * legend.GetTextSize())
        entries_tlist = legend.GetListOfPrimitives()
        entries = list(entries_tlist)
        entries[0].SetLabel('Signal region')
        entries[1].SetLabel('Stat. uncert. bkg.')
        entries[2].SetLabel('Control region')
        entries[2].GetObject().SetLineWidth(2)
        entries[2].GetObject().SetLineColor(1)
        entries_tlist.Clear()
        entries_tlist.Add(entries[0])
        entries_tlist.Add(entries[2])
        entries_tlist.Add(entries[1])

    if name == 'selblock_ST_lin.pdf':
        x_axis.SetRangeUser(400., 2500.)
        x_axis_1st.SetRangeUser(400., 2500.)


    c.Modified()
    c.Update()
    # c.SaveAs('PlotBeautifier/'+name.replace('.pdf', '.root'))
    c.SaveAs('PlotBeautifier/'+name)


    #return varial.wrp.CanvasWrapper(c, save_name=save_name)


# class PlotBeautifier(varial.tools.Tool):
#     def run(self):
#         canvs = (handle_plot(self, p) for p in plot_config)
#         for _ in canvs:
#             pass
#         #varial.sparseio.bulk_write(
#         #    canvs, lambda c: c.save_name, suffices=('.pdf',))


if __name__ == '__main__':
    # pb = PlotBeautifier()
    # varial.tools.Runner(pb)
    for p in plot_config:
        handle_plot(p)
