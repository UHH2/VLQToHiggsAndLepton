######################################################
# check THIS out: https://ghm.web.cern.ch/ghm/plots/ #
######################################################

import ROOT
import os

ROOT.gStyle.SetEndErrorSize(0)
p_base = 'VLQ2HT/Outputs/'
ext = '.pdf'

def get_p_lim(sig):
    return p_base + 'Limits' + sig + '/DataBackground/'


pas_single = {
    'selblock_primary_el_pt_lin.pdf': p_base + 'SelectionsEl/Stacks/BaseLineSelection/primary_lepton_pt_lin.pdf',
    'selblock_primary_mu_pt_lin.pdf': p_base + 'SelectionsMu/Stacks/BaseLineSelection/primary_lepton_pt_lin.pdf',
    'selblock_ST_lin.pdf':                p_base + 'SelectionsEl/Stacks/BaseLineSelection/ST_lin.pdf',
    'selblock_h_mass_lin.pdf':            p_base + 'SelectionsMu/Stacks/BaseLineSelection/h_mass_lin.pdf',
    'tlep_mass_lin.pdf': p_base + 'SelectionsMu/Stacks/BaseLineSelection/tlep_mass_lin.pdf',
    'tlep_pt_lin.pdf': p_base + 'SelectionsMu/Stacks/BaseLineSelection/tlep_pt_lin.pdf',
    'SignalRegion__el_lin.pdf': p_base + 'SelectionsElNoData/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion__mu_lin.pdf': p_base + 'SelectionsMuNoData/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion_bkg__el_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__el_lin.pdf',
    'SignalRegion_bkg__mu_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__mu_lin.pdf',
    'SignalRegion_bkg__comb_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__comb_lin.pdf',
    'Sideband__el_lin.pdf': p_base + 'SelectionsEl/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband__mu_lin.pdf': p_base + 'SelectionsMu/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__el.pdf': p_base+'SidebandsEl/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__mu.pdf': p_base+'SidebandsMu/Plots/AllSamples/SideBandRegion/Plotter/vlq_mass_lin.pdf',
    'TpBLH_limits.pdf': get_p_lim('TpBLH')+'/LimitGraphsPlot/Graph_log'+ext,
    'TpBRH_limits.pdf': get_p_lim('TpBRH')+'/LimitGraphsPlot/Graph_log'+ext,
    'TpTLH_limits.pdf': get_p_lim('TpTLH')+'/LimitGraphsPlot/Graph_log'+ext,
    'TpTRH_limits.pdf': get_p_lim('TpTRH')+'/LimitGraphsPlot/Graph_log'+ext,
    'TpBLH_coupling_limits.pdf': get_p_lim('TpBLH')+'/CouplingLimitPlot/Graph_lin'+ext,
    'TpBRH_coupling_limits.pdf': get_p_lim('TpBRH')+'/CouplingLimitPlot/Graph_lin'+ext,
    'TpTLH_coupling_limits.pdf': get_p_lim('TpTLH')+'/CouplingLimitPlot/Graph_lin'+ext,
    'TpTRH_coupling_limits.pdf': get_p_lim('TpTRH')+'/CouplingLimitPlot/Graph_lin'+ext,
    'sel_eff_el.pdf': 'VLQ2HT/SigEffGraphPlot/el_lin'+ext,
    'sel_eff_mu.pdf': 'VLQ2HT/SigEffGraphPlot/mu_lin'+ext,
}


plot_config = {  #                   lumi legend x1 x2 y1 y2    CMS pos   chan pos    y_max
'sel_eff_el.pdf':                   (0,   (.70, .90, .65, .85), (.2, .8), (.2, .6, 1),   1.9),
'sel_eff_mu.pdf':                   (0,   (.70, .90, .20, .40), (.2, .8), (.65,.255,2),  1.9),

'selblock_h_mass_lin.pdf':          (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  5500),
'selblock_primary_el_pt_lin.pdf':   (2.2, (.62, .82, .24, .73), (.9, .8), (.61,.8, 1),  1100),
'selblock_primary_mu_pt_lin.pdf':   (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  6000),
'selblock_ST_lin.pdf':              (2.2, (.62, .82, .36, .85), (.2, .8), (.2, .7, 1),  1050),

'Sideband__el_lin.pdf':             (2.2, (.18, .37, .36, .85), (.9, .8), (.9, .7, 1),   150),
'Sideband__mu_lin.pdf':             (2.3, (.62, .82, .36, .85), (.2, .8), (.2, .7, 2),   800),

'Sideband_vs_SignalRegion__el.pdf': (0,   (.62, .82, .67, .85), (.2, .8), (.2,.62, 1),  0.19),
'Sideband_vs_SignalRegion__mu.pdf': (0,   (.62, .82, .67, .85), (.2, .8), (.2,.62, 2),   0.0),

'SignalRegion__el_lin.pdf':         (0,   (.20, .40, .46, .85), (.9, .8), (.2,.38, 1),  13.5),
'SignalRegion__mu_lin.pdf':         (0,   (.60, .80, .46, .85), (.2, .8), (.2,.62, 2),  50.0),

'SignalRegion_bkg__el_lin.pdf':     (2.2, (.65, .85, .55, .85), (.2, .8), (.2, .7, 1),  11.0),
'SignalRegion_bkg__mu_lin.pdf':     (2.3, (.65, .85, .55, .85), (.2, .8), (.2, .7, 2),  35.0),
'SignalRegion_bkg__comb_lin.pdf':   (2.3, (.65, .85, .55, .85), (.2, .8), (.2, .7, 3),  45.0),

'tlep_mass_lin.pdf':                (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  2000),
'tlep_pt_lin.pdf':                  (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  2700),

'TpBLH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),
'TpBRH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),
'TpTLH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),
'TpTRH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),

'TpBLH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   0.0),
'TpBRH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   0.0),
'TpTLH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   9.9),
'TpTRH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   9.9),
}


def handle_plot(name):
    # get parameters
    lumi, (x1, x2, y1, y2), (cms_x, cms_y), (chan_x, chan_y, chan), y_scale_max = plot_config[name]
    save_name = name.replace('.pdf', '')

    # get some info and fetch canvas
    path = pas_single[name]
    path, basename = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    canvname = basename.replace('_log', '').replace('_lin', '')
    f = ROOT.TFile(path + '/_varial_rootobjects.root.rt')
    c = f.Get('{n}/{n}'.format(n=canvname))
    f.Close()

    # pull items out of canvas
    canv_prims = list(c.GetListOfPrimitives())
    legend = next(p for p in canv_prims if isinstance(p, ROOT.TLegend))
    if isinstance(canv_prims[0], ROOT.TPad) and isinstance(canv_prims[1], ROOT.TPad):
        main_pad, second_pad, size_factor = canv_prims[0], canv_prims[1], 0.8
    else:
        main_pad, second_pad, size_factor = c, c, 1

    def get_pos(old_pos):
        return old_pos*size_factor + (1 - size_factor)

    main_hists = list(
        p
        for p in main_pad.GetListOfPrimitives()
        if any(isinstance(p, cl) for cl in (ROOT.THStack, ROOT.TH1, ROOT.TGraph))
    )

    # set margins
    main_pad.SetTopMargin(0.087)
    main_pad.SetRightMargin(0.05)
    second_pad.SetRightMargin(0.05)

#    # area in coupling plots
#    if '_coupling_' in save_name:
#        obs_lim = main_hists[-1]
#        n = obs_lim.GetN()
#        obs_lim.SetPoint(n, 1800, 40)
#        obs_lim.SetPoint(n+1, 700, 40)
#        obs_lim.SetFillStyle(3344)
#        obs_lim.SetFillColor(ROOT.kGray + 1)
#        obs_lim.SetLineColor(ROOT.kGray + 1)
#        obs_lim.SetLineWidth(2)
#        obs_lim.Draw('F')
#        legend_entry = legend.GetListOfPrimitives()[0]
#        legend_entry.SetObject(obs_lim)
#        legend_entry.SetOption('F')
#        # legend_entry.SetFillColor(ROOT.kGray + 1)
#        # legend_entry.SetFillStyle(3244)

    # move legend
    # legend.SetTextSize(1.1 * legend.GetTextSize())
    legend.SetX1NDC(x1)
    legend.SetX2NDC(x2)
    legend.SetY1NDC(get_pos(y1))
    legend.SetY2NDC(get_pos(y2))

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
    if not lumi:
        latex.DrawLatex(cms_x, get_pos(cms_y - 1.0*cmsTextSize), 'Simulation')

    # electron / muon channel
    if chan:
        chan_txts = {1: 'electron', 2: 'muon', 3: 'electron+muon'}
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
    x_axis = second_pad.GetListOfPrimitives()[1].GetXaxis()
    y_axis = first_obj.GetYaxis()
    y_axis.SetTitleOffset(1.4)
    y_axis.CenterTitle(0)
    y_axis.SetNoExponent()
    x_axis.SetTitle(x_axis.GetTitle().replace('/ GeV', '(GeV)'))

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
        if main_pad != second_pad:
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
        x_axis.SetRangeUser(700, 1700)

    if name.startswith('sel_eff_'):
        legend.SetTextSize(1.3 * legend.GetTextSize())
        y_axis.SetTitleSize(1.2 * y_axis.GetTitleSize())

    # more detail fixings...
    if save_name.endswith('H_limits'):
        main_pad.SetLogy()
        first_obj.SetMinimum(0.05)
        y_axis.SetTitle(y_axis.GetTitle().replace('->', '#rightarrow').replace('/ pb', '(pb)'))

    if name.startswith('SignalRegion_bkg__'):
        second_pad.GetListOfPrimitives()[1].GetYaxis().SetRangeUser(-0.9, 1.7)
        # legend.SetTextSize(1.3 * legend.GetTextSize())
        entries = list(legend.GetListOfPrimitives())
        entries[-1].GetObject().SetLineWidth(2)
        entries[-1].GetObject().SetLineColor(1)

    if name.startswith('Sideband_vs_SignalRegion__'):
        # legend.SetTextSize(1.3 * legend.GetTextSize())
        entries_tlist = legend.GetListOfPrimitives()
        entries = list(entries_tlist)
        entries[0].SetLabel('signal region')
        entries[1].SetLabel('stat. uncert. bkg.')
        entries[2].SetLabel('control region')
        entries[2].GetObject().SetLineWidth(2)
        entries[2].GetObject().SetLineColor(1)
        entries_tlist.Clear()
        entries_tlist.Add(entries[0])
        entries_tlist.Add(entries[2])
        entries_tlist.Add(entries[1])

    c.Modified()
    c.Update()
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
