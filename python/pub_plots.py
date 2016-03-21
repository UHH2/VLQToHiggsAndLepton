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
'sel_eff_el.pdf':                   (0,   (.70, .90, .20, .40), (.2, .8), (.2,.63, 1),  .014),
'sel_eff_mu.pdf':                   (0,   (.70, .90, .20, .40), (.2, .8), (.2,.63, 2),  .019),

'SignalRegion_bkg__el_lin.pdf':     (2.2, (.65, .85, .50, .85), (.2, .8), (.2, .6, 1),  11.0),
'SignalRegion_bkg__mu_lin.pdf':     (2.3, (.65, .85, .50, .85), (.2, .8), (.2, .6, 2),  35.0),
'SignalRegion_bkg__comb_lin.pdf':   (2.3, (.65, .85, .50, .85), (.2, .8), (.2, .6, 3),  39.0),

'SignalRegion__el_lin.pdf':         (0,   (.20, .40, .46, .85), (.9, .8), (.2,.38, 1),  13.5),
'SignalRegion__mu_lin.pdf':         (0,   (.60, .80, .46, .85), (.2, .8), (.2, .6, 2),  50.0),

'selblock_primary_el_pt_lin.pdf':   (2.2, (.65, .85, .16, .65), (.9, .8), (.65,.8, 1),  1100),
'selblock_primary_mu_pt_lin.pdf':   (2.3, (.65, .85, .16, .65), (.9, .8), (.65,.8, 2),  6000),
'selblock_ST_lin.pdf':              (2.2, (.65, .85, .36, .85), (.2, .8), (.2, .6, 1),  1050),
'selblock_h_mass_lin.pdf':          (2.3, (.65, .85, .16, .65), (.9, .8), (.65,.8, 2),  5500),

'tlep_mass_lin.pdf':                (2.3, (.65, .85, .16, .65), (.9, .8), (.65,.8, 2),  2000),
'tlep_pt_lin.pdf':                  (2.3, (.65, .85, .16, .65), (.9, .8), (.65,.8, 2),  2700),

'Sideband__el_lin.pdf':             (2.2, (.65, .85, .36, .85), (.2, .8), (.2, .6, 1),   150),
'Sideband__mu_lin.pdf':             (2.3, (.65, .85, .36, .85), (.2, .8), (.2, .6, 2),   800),

'Sideband_vs_SignalRegion__el.pdf': (0,   (.70, .90, .67, .85), (.2, .8), (.2, .6, 1),  0.19),
'Sideband_vs_SignalRegion__mu.pdf': (0,   (.70, .90, .67, .85), (.2, .8), (.2, .6, 2),   0.0),

'TpBLH_limits.pdf':                 (2.3, (.30, .50, .63, .85), (.9, .8), (.9, .6, 0),   99.),
'TpBRH_limits.pdf':                 (2.3, (.30, .50, .63, .85), (.9, .8), (.9, .6, 0),   99.),
'TpTLH_limits.pdf':                 (2.3, (.30, .50, .63, .85), (.9, .8), (.9, .6, 0),   99.),
'TpTRH_limits.pdf':                 (2.3, (.30, .50, .63, .85), (.9, .8), (.9, .6, 0),   99.),

'TpBLH_coupling_limits.pdf':        (2.3, (.50, .70, .68, .85), (.2, .8), (.2, .6, 0),   0.0),
'TpBRH_coupling_limits.pdf':        (2.3, (.50, .70, .68, .85), (.2, .8), (.2, .6, 0),   0.0),
'TpTLH_coupling_limits.pdf':        (2.3, (.50, .70, .68, .85), (.2, .8), (.2, .6, 0),   0.0),
'TpTRH_coupling_limits.pdf':        (2.3, (.50, .70, .68, .85), (.2, .8), (.2, .6, 0),   0.0),
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
        main_pad, second_pad = canv_prims[0], canv_prims[1]
    else:
        main_pad, second_pad = c, c

    main_hists = list(
        p
        for p in main_pad.GetListOfPrimitives()
        if any(isinstance(p, cl) for cl in (ROOT.THStack, ROOT.TH1, ROOT.TGraph))
    )

    # set margins
    main_pad.SetTopMargin(0.087)
    main_pad.SetRightMargin(0.05)
    second_pad.SetRightMargin(0.05)

    # move legend
    legend.SetX1NDC(x1)
    legend.SetX2NDC(x2)
    legend.SetY1NDC(y1)
    legend.SetY2NDC(y2)

    c.cd()

    # lumi / sqrt s text
    lumi_line = ('%.1f fb^{-1} (13 TeV)' % lumi) if lumi else '(simulation 13 TeV)'
    lumi_txt = ROOT.TPaveText(0.5, 0.87, 0.975, 1.0, 'brNDC')
    lumi_txt.AddText(lumi_line)
    lumi_txt.SetTextColor(ROOT.kBlack)
    lumi_txt.SetTextFont(42)
    lumi_txt.SetTextAlign(31)
    lumi_txt.SetTextSize(0.06)
    lumi_txt.SetFillStyle(0)
    lumi_txt.SetBorderSize(0)
    lumi_txt.Draw('same')

    # CMS preliminary text
    cmsTextSize = 0.075
    latex = ROOT.TLatex()
    latex.SetNDC()

    latex.SetTextFont(61)
    latex.SetTextSize(cmsTextSize)
    latex.SetTextAlign(31 if cms_x > 0.5 else 11)
    latex.DrawLatex(cms_x, cms_y, 'CMS')

    latex.SetTextFont(52)
    latex.SetTextAlign(31 if cms_x > 0.5 else 11)
    latex.SetTextSize(0.76 * cmsTextSize)
    latex.DrawLatex(cms_x, cms_y - 1.0*cmsTextSize, 'Preliminary')

    # electron / muon channel
    if chan:
        chan_txts = {1: 'electron', 2: 'muon', 3: 'electron+muon'}
        chan_txt2 = 'channel'
        latex.SetTextFont(42)
        latex.SetTextAlign(31 if chan_x > 0.5 else 11)
        latex.SetTextSize(0.65 * cmsTextSize)
        latex.DrawLatex(chan_x, chan_y, chan_txts[chan])
        latex.DrawLatex(chan_x, chan_y - 0.6*cmsTextSize, chan_txt2)

    # darker shade on uncertainties
    for obj in main_hists:
        if 'uncert.' in obj.GetTitle():
            obj.SetFillColor(ROOT.kBlack)

    if main_pad != second_pad:
        second_pad.GetListOfPrimitives()[-2].SetFillColor(ROOT.kBlack)

    # x and y axes
    first_obj = main_hists[0]
    x_axis = second_pad.GetListOfPrimitives()[1].GetXaxis()
    y_axis = first_obj.GetYaxis()
    y_axis.SetTitleOffset(1.25)
    y_axis.CenterTitle(0)
    y_axis.SetNoExponent()

    x_axis.SetTitle(x_axis.GetTitle().replace('/ GeV', '(GeV)'))

    if y_scale_max:
        first_obj.SetMaximum(y_scale_max)

    if save_name.endswith('_log'):
        main_pad.SetLogy()

    # more detail fixings...
    if save_name.endswith('H_limits'):
        main_pad.SetLogy()
        first_obj.SetMinimum(0.05)
        y_axis.SetTitle(y_axis.GetTitle().replace('->', '#rightarrow').replace('/ pb', '(pb)'))

    if name.startswith('SignalRegion_bkg__'):
        second_pad.GetListOfPrimitives()[1].GetYaxis().SetRangeUser(-0.9, 1.7)
        # legend.SetTextSize(0.55*cmsTextSize)


    c.Modified()
    c.Update()
    # c.SaveAs('PlotBeautifier/'+name+'.root')
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
