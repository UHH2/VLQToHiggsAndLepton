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
}


plot_config = {  #                       lumi legend x1 x2 y1 y2        CMS pos       y_max
    'SignalRegion_bkg__el_lin.pdf':     (2.2, (0.70, 0.90, 0.55, 0.85), (0.2, 0.8),  11.0),
    'SignalRegion_bkg__mu_lin.pdf':     (2.3, (0.70, 0.90, 0.55, 0.85), (0.2, 0.8),  35.0),
    'SignalRegion_bkg__comb_lin.pdf':   (2.3, (0.70, 0.90, 0.55, 0.85), (0.2, 0.8),  39.0),

    'SignalRegion__el_lin.pdf':         (2.2, (0.20, 0.40, 0.46, 0.85), (0.9, 0.8),  13.5),
    'SignalRegion__mu_lin.pdf':         (2.3, (0.60, 0.80, 0.46, 0.85), (0.2, 0.8),  50.0),

    'selblock_primary_el_pt_lin.pdf':   (2.2, (0.65, 0.85, 0.16, 0.65), (0.9, 0.8),  1100),
    'selblock_primary_mu_pt_lin.pdf':   (2.3, (0.65, 0.85, 0.16, 0.65), (0.9, 0.8),  6000),
    'selblock_ST_lin.pdf':              (2.2, (0.65, 0.85, 0.36, 0.85), (0.2, 0.8),  1050),
    'selblock_h_mass_lin.pdf':          (2.3, (0.65, 0.85, 0.16, 0.65), (0.9, 0.8),  5500),

    'tlep_mass_lin.pdf':                (2.3, (0.65, 0.85, 0.16, 0.65), (0.9, 0.8),  2000),
    'tlep_pt_lin.pdf':                  (2.3, (0.65, 0.85, 0.16, 0.65), (0.9, 0.8),  2700),

    'Sideband__el_lin.pdf':             (2.2, (0.65, 0.85, 0.36, 0.85), (0.2, 0.8),   150),
    'Sideband__mu_lin.pdf':             (2.3, (0.65, 0.85, 0.36, 0.85), (0.2, 0.8),   800),

    'Sideband_vs_SignalRegion__el.pdf': (0,   (0.70, 0.90, 0.67, 0.85), (0.2, 0.8),  0.19),
    'Sideband_vs_SignalRegion__mu.pdf': (0,   (0.70, 0.90, 0.67, 0.85), (0.2, 0.8),   0.0),

    'TpBLH_limits.pdf':                 (2.3, (0.40, 0.60, 0.63, 0.85), (0.9, 0.8),   0.0),
    'TpBRH_limits.pdf':                 (2.3, (0.40, 0.60, 0.63, 0.85), (0.9, 0.8),   0.0),
    'TpTLH_limits.pdf':                 (2.3, (0.40, 0.60, 0.63, 0.85), (0.9, 0.8),   0.0),
    'TpTRH_limits.pdf':                 (2.3, (0.40, 0.60, 0.63, 0.85), (0.9, 0.8),   0.0),

    'TpBLH_coupling_limits.pdf':        (2.3, (0.50, 0.70, 0.68, 0.85), (0.2, 0.8),   0.0),
    'TpBRH_coupling_limits.pdf':        (2.3, (0.50, 0.70, 0.68, 0.85), (0.2, 0.8),   0.0),
    'TpTLH_coupling_limits.pdf':        (2.3, (0.50, 0.70, 0.68, 0.85), (0.2, 0.8),   0.0),
    'TpTRH_coupling_limits.pdf':        (2.3, (0.50, 0.70, 0.68, 0.85), (0.2, 0.8),   0.0),
}


def handle_plot(name):
    # get parameters
    lumi, (x1, x2, y1, y2), (pos_x, pos_y), y_scale_max = plot_config[name]
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
    lumi_line = ('%.1f fb^{-1} (13 TeV)' % lumi) if lumi else '(13 TeV)'
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
    latex.SetTextAlign(31 if pos_x > 0.5 else 11)
    latex.DrawLatex(pos_x, pos_y, 'CMS')

    latex.SetTextFont(52)
    latex.SetTextAlign(31 if pos_x > 0.5 else 11)
    latex.SetTextSize(0.76 * cmsTextSize)
    latex.DrawLatex(pos_x, pos_y - 1.0*cmsTextSize, 'Preliminary')

    # y axis
    first_obj = main_hists[0]
    y_axis = first_obj.GetYaxis()
    y_axis.SetTitleOffset(1.25)
    y_axis.CenterTitle(0)
    if y_scale_max:
        first_obj.SetMaximum(y_scale_max)
    if save_name.endswith('_log'):
        main_pad.SetLogy()

    if save_name.endswith('H_limits'):
        main_pad.SetLogy()
        first_obj.SetMinimum(0.075)

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
