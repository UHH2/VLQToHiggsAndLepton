######################################################
# check THIS out: https://ghm.web.cern.ch/ghm/plots/ #
######################################################

import ctypes
import ROOT
import os

ROOT.gStyle.SetEndErrorSize(0)
p_base = 'VLQ2HT/Outputs/'
ext = '.pdf'

def get_p_lim(sig):
    return p_base + 'Limits' + sig + '/DataBackground/'


pas_single = {
    'selblock_primary_el_pt_lin.pdf': p_base + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/primary_lepton_pt_lin.pdf',
    'selblock_primary_mu_pt_lin.pdf': p_base + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/primary_lepton_pt_lin.pdf',
    'selblock_ST_lin.pdf':            p_base + 'SelectionsElNoFwdSys/Stacks/BaseLineSelection/ST_lin.pdf',
    'selblock_h_mass_lin.pdf':        p_base + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/h_mass_lin.pdf',
    'tlep_mass_lin.pdf': p_base + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/tlep_mass_lin.pdf',
    'tlep_pt_lin.pdf': p_base + 'SelectionsMuNoFwdSys/Stacks/BaseLineSelection/tlep_pt_lin.pdf',
    'SignalRegion_data__el_lin.pdf': p_base + 'SelectionsEl/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion_data__mu_lin.pdf': p_base + 'SelectionsMu/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion__el_lin.pdf': p_base + 'SelectionsElNoData/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion__mu_lin.pdf': p_base + 'SelectionsMuNoData/Stacks/SignalRegion/vlq_mass_lin.pdf',
    'SignalRegion_bkg__el_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__el_lin.pdf',
    'SignalRegion_bkg__mu_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__mu_lin.pdf',
    'SignalRegion_bkg__comb_lin.pdf': p_base + 'LimitsTpBLH/DataBackground/PostFit/SignalRegion__comb_lin.pdf',
    'Sideband__el_lin.pdf': p_base + 'SelectionsElNoFwdSys/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband__mu_lin.pdf': p_base + 'SelectionsMuNoFwdSys/Stacks/SidebandRegion/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__el.pdf': p_base+'SidebandsEl/Nominal/Plotter/vlq_mass_lin.pdf',
    'Sideband_vs_SignalRegion__mu.pdf': p_base+'SidebandsMu/Nominal/Plotter/vlq_mass_lin.pdf',
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
    'El_ct_MultiRegion.pdf': p_base+'SidebandsEl/MultiRegion/Plotter/vlq_mass_lin.pdf',
    'Mu_ct_MultiRegion.pdf': p_base+'SidebandsMu/MultiRegion/Plotter/vlq_mass_lin.pdf',
    'El_ct_DataB0vsSB.pdf':  p_base+'SidebandsEl/DataB0vsSB/Plotter/vlq_mass_lin.pdf',
    'Mu_ct_DataB0vsSB.pdf':  p_base+'SidebandsMu/DataB0vsSB/Plotter/vlq_mass_lin.pdf',
}


plot_config = {  #                   lumi legend x1 x2 y1 y2    CMS pos   chan pos    y_max
# 'sel_eff_el.pdf':                   (0,   (.70, .90, .65, .85), (.2, .8), (.2, .6, 1),   1.9),
# 'sel_eff_mu.pdf':                   (0,   (.70, .90, .20, .40), (.2, .8), (.65,.255,2),  1.9),
# 'sel_eff_new.pdf':                  (0,   (.50, .70, .65, .85), (.2, .8), (.2, .6, 0),   2.8),

'selblock_h_mass_lin.pdf':          (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  5500),
'selblock_primary_el_pt_lin.pdf':   (2.2, (.62, .82, .24, .73), (.9, .8), (.61,.8, 1),  1100),
'selblock_primary_mu_pt_lin.pdf':   (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  6000),
'selblock_ST_lin.pdf':              (2.2, (.62, .82, .36, .85), (.2, .8), (.2, .7, 1),  1050),

'Sideband__el_lin.pdf':             (2.2, (.18, .37, .36, .85), (.9, .8), (.9, .7, 1),   150),
'Sideband__mu_lin.pdf':             (2.3, (.62, .82, .36, .85), (.2, .8), (.2, .7, 2),   800),

'Sideband_vs_SignalRegion__el.pdf': (0,   (.62, .82, .67, .85), (.2, .8), (.2,.62, 1),  0.19),
'Sideband_vs_SignalRegion__mu.pdf': (0,   (.62, .82, .67, .85), (.2, .8), (.2,.62, 2),   0.0),

'El_ct_MultiRegion.pdf':            (0,   (.62, .82, .55, .85), (.2, .8), (.2,.62, 1),  0.19),
'Mu_ct_MultiRegion.pdf':            (0,   (.62, .82, .55, .85), (.2, .8), (.2,.62, 2),   0.0),
'El_ct_DataB0vsSB.pdf':             (2.2, (.62, .82, .61, .85), (.2, .8), (.2,.62, 1),  0.19),
'Mu_ct_DataB0vsSB.pdf':             (2.3, (.62, .82, .61, .85), (.2, .8), (.2,.62, 2),   0.0),

'SignalRegion_data__el_lin.pdf':    (2.2, (.20, .40, .36, .85), (.9, .8), (.9, .7, 1),  13.5),
'SignalRegion_data__mu_lin.pdf':    (2.3, (.60, .80, .36, .85), (.2, .8), (.2, .7, 2),  50.0),

# 'SignalRegion__el_lin.pdf':         (2.2, (.20, .40, .46, .85), (.9, .8), (.2,.38, 1),  13.5),
# 'SignalRegion__mu_lin.pdf':         (2.3, (.60, .80, .46, .85), (.2, .8), (.2,.62, 2),  50.0),

'SignalRegion_bkg__el_lin.pdf':     (2.2, (.65, .85, .55, .85), (.2, .8), (.2, .7, 1),  11.0),
'SignalRegion_bkg__mu_lin.pdf':     (2.3, (.65, .85, .55, .85), (.2, .8), (.2, .7, 2),  35.0),
'SignalRegion_bkg__comb_lin.pdf':   (2.3, (.65, .85, .55, .85), (.2, .8), (.2, .7, 3),  45.0),

'tlep_mass_lin.pdf':                (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  2000),
'tlep_pt_lin.pdf':                  (2.3, (.62, .82, .24, .73), (.9, .8), (.61,.8, 2),  2700),

'TpBLH_limits.pdf':                 (2.3, (.35, .55, .58, .85), (.2, .8), (.9, .6, 0),   99.),
# 'TpBRH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),
# 'TpTLH_limits.pdf':                 (2.3, (.38, .58, .58, .85), (.2, .8), (.9, .6, 0),   99.),
'TpTRH_limits.pdf':                 (2.3, (.35, .55, .58, .85), (.2, .8), (.9, .6, 0),   99.),

# 'TpBLH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   0.0),
# 'TpBRH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   0.0),
# 'TpTLH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   9.9),
# 'TpTRH_coupling_limits.pdf':        (2.3, (.38, .58, .63, .85), (.2, .8), (.2, .6, 0),   9.9),
}


def build_sel_eff_canvas():
    c_mu = get_canvas('sel_eff_mu.pdf')
    c_el = get_canvas('sel_eff_el.pdf')

    # start with legends (they contain the labels)
    el_leg = list(c_el.GetListOfPrimitives())[-1]
    mu_leg = list(c_mu.GetListOfPrimitives())[-1]

    # get the graphs
    el_objs = dict(
        (e.GetLabel(), e)
        for e in el_leg.GetListOfPrimitives()
    )
    mu_objs = dict(
        (e.GetLabel(), e)
        for e in mu_leg.GetListOfPrimitives()
    )

    def migrate_points(from_g, to_g):
        x, y = ctypes.c_double(), ctypes.c_double()
        for i in xrange(to_g.GetN()):
            to_g.RemovePoint(0)
        for i in xrange(from_g.GetN()):
            from_g.GetPoint(i, x, y)
            to_g.SetPoint(i, x.value, y.value)

    # set points in electron graphs to the ones from the mu graphs
    # T_{lh} b in ele chan can stay
    migrate_points(el_objs['T_{rh} t'].GetObject(), el_objs['T_{rh} b'].GetObject())
    migrate_points(mu_objs['T_{lh} b'].GetObject(), el_objs['T_{lh} t'].GetObject())
    migrate_points(mu_objs['T_{rh} t'].GetObject(), el_objs['T_{rh} t'].GetObject())

    # update the legend
    el_objs['T_{lh} b'].SetLabel('pp#rightarrowT_{lh}b+X (ele. ch.)')
    el_objs['T_{rh} b'].SetLabel('pp#rightarrowT_{rh}t+X (ele. ch.)')
    el_objs['T_{lh} t'].SetLabel('pp#rightarrowT_{lh}b+X (mu. ch.)')
    el_objs['T_{rh} t'].SetLabel('pp#rightarrowT_{rh}t+X (mu. ch.)')

    return c_el


def get_canvas(name):
    if name == 'sel_eff_new.pdf':
        return build_sel_eff_canvas()

    path = pas_single[name]
    path, basename = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    canvname = basename.replace('_log', '').replace('_lin', '')
    f = ROOT.TFile(path + '/_varial_rootobjects.root.rt')
    c = f.Get('{n}/{n}'.format(n=canvname))
    f.Close()
    return c


def handle_plot(name):
    # get parameters
    lumi, (x1, x2, y1, y2), (cms_x, cms_y), (chan_x, chan_y, chan), y_scale_max = plot_config[name]
    save_name = name.replace('.pdf', '')

    # get some info and fetch canvas
    c = get_canvas(name)

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
    if (any(isinstance(h, ROOT.THStack) for h in main_hists) and
        4 < len(main_hists) and
        '_ct_' not in save_name
    ):
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

    if '_ct_' in save_name:
        entries_tlist = legend.GetListOfPrimitives()
        entries = list(entries_tlist)
        y_axis_2nd.SetRangeUser(-0.9, 0.9)

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
            entries[0].SetLabel('Region A (data)')
            entries[1].SetLabel('Region B (data)')
            entries[3].SetLabel('Control region (data)')
            entries[2].SetLabel('Stat. uncert. CR')
            y_axis.SetTitle('Arbitrary units')
            # latex.DrawLatex(0.2, 0.75, '(Data)')
        else:
            main_hists[3].SetLineStyle(2)
            main_hists[2].SetLineStyle(2)
            second_pad.GetListOfPrimitives()[3].SetLineStyle(2)
            second_pad.GetListOfPrimitives()[2].SetLineStyle(2)
            entries_tlist.Clear()
            for i in (0,2,1,3,4):  # swap A and B
                entries_tlist.AddLast(entries[i])

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

    if name.startswith('SignalRegion_bkg__'):
        hdat = ROOT.TH1F('foo', 'foo', 25, 0., 2000.)
        for i in xrange(20):
            x, y = ctypes.c_double(), ctypes.c_double()
            main_hists[-1].GetPoint(i, x, y)
            # print i, x.value, y.value
            hdat.SetBinContent(i+6, y.value)
        hdat.SetBinErrorOption(ROOT.TH1.kPoisson)
        print hdat.KolmogorovTest(main_hists[1])
        print hdat.Chi2Test(main_hists[1], 'UW')


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
        # print p
        handle_plot(p)
