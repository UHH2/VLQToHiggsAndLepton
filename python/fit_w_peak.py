import UHH2.VLQSemiLepPreSel.common as common
import varial.plotter
import varial.tools
import ROOT

def histowrapperize(wrps):
    for w in wrps:
        if isinstance(w, varial.wrp.StackWrapper):
            w = varial.wrp.HistoWrapper(w.histo, **w.all_info())
        yield w


def w_peak_histo_squash(wrps):
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    wrps = varial.gen.group(wrps, lambda w: w.in_file_path)
    wrps = varial.gen.mc_stack_n_data_sum(wrps)
    wrps = (w for grp in wrps for w in grp)
    wrps = histowrapperize(wrps)
    return wrps


################################################# histos for w peak fitting ###
class WPeakFitter(varial.tools.Tool):
    def run(self):
        wrps = varial.gen.dir_content('../../Inputs/Mu/TreeProjector/*.root')
        wrps = (w for w in wrps if 'TTbar2Selection' in w.in_file_path)
        wrps = (w for w in wrps if w.name in ('h_mass-.00001', 'h_jet.m_prunedmass'))
        wrps = (w for w in wrps if '_TH_' not in w.file_path)
        # wrps = (w for w in wrps if w.sample in ('Run2015D', 'TTbar'))
        wrps = varial.gen.load(wrps)
        wrps = common.add_wrp_info(wrps)
        wrps = w_peak_histo_squash(wrps)
        # assert len(wrps) == 1
        # wrps = wrps[0]
        # print wrps
        # assert len(wrps) == 2, str(wrps)
        wrps = varial.gen.gen_norm_to_integral(wrps)
        self.result = list(wrps)


####################################### comparison of smeared distributions ###
def hook_sys_comp(wrps):
    def put_info(w):
        w.sys_info = ''
        w.obj.SetYTitle('a.u.')
        if '__plus' in w.file_path:
            w.name += '_up'
            w.in_file_path += '_up'
            w.legend = 'no smearing'
        elif '__minus' in w.file_path:
            w.name += '_down'
            w.in_file_path += '_down'
            w.legend = '20% smearing'
        elif w.is_data:
            w.obj.SetLineColor(ROOT.kBlack)
        else:
            w.legend = '10% smearing'
        return w

    wrps = common.add_wrp_info(wrps)
    wrps = (put_info(w) for w in wrps)
    wrps = w_peak_histo_squash(wrps)
    wrps = varial.gen.gen_norm_to_max_val(wrps)
    return wrps


def plot_setup(ws):
    ws = varial.gen.apply_linecolor(ws)
    for w in ws:
        if not w.is_data:
            w.draw_option = 'histE0'
            w.obj.SetMarkerSize(0)
            w.obj.SetFillStyle(0)
            w.obj.SetLineWidth(2)
        yield w


tc_sys_comp = varial.tools.ToolChain(
    'SysWPeakCompare',
    [
        varial.tools.HistoLoader(
            pattern=[
                'VLQ2HT/Inputs/Mu/TreeProjector/*.root',
                'VLQ2HT/Inputs/Mu/SysTreeProjectors/MH_smear__*/*.root',
            ],
            filter_keyfunc=lambda w: (
                w.in_file_path == 'TTbar2Selection/h_mass' and
                '_TH_' not in w.sample
            ),
            hook_loaded_histos=hook_sys_comp,
        ),
        varial.plotter.Plotter(
            plot_grouper=lambda ws: [ws],
            plot_setup=lambda grps: (plot_setup(ws) for ws in grps)
        ),
    ]
)
