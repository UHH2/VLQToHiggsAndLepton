import UHH2.VLQSemiLepPreSel.common as common
import varial.plotter
import varial.tools
import itertools
import cPickle
import array
import ROOT


class EffNumTable(varial.tools.Tool):
    def run(self):
        def get_line_info(info):
            return sorted(
                (k.replace('(700', '(0700'), v)
                for k, v in info.iteritems()
                if k.startswith('Integral___T_')
            )

        def get_fmt(line_tuple, f):
            f /= 100.
            name, nums = line_tuple
            if len(nums) == 4:
                i, st, _, sy = nums
                st, sy = max(st, 0.01), max(sy, 0.01)
                sy = (sy**2 + (i*0.15)**2)**.5
            else:
                (i, st), sy = nums, 0.
            num = r'& $%5.1f \pm %4.1f \pm %4.1f$ ' % (i, st, sy)
            eff = r'& $%2.2f \pm %2.2f \pm %2.2f$ ' % (i/f, st/f, sy/f)
            return ('%50s'%name) + num + eff

        res = ['TpBLH', 'TpBRH', 'TpTLH', 'TpTRH']
        res = (
            './VLQ2HT/Outputs/Limits%s/DataBackground/PostFit/_varial_infodata.pkl' % tok
            for tok in res
        )
        res = (cPickle.load(open(fname)) for fname in res)
        res = (
            sorted(
                (name, info)
                for name, info in pkldata.iteritems()
                if name.endswith('el') or name.endswith('mu')
            )
            for pkldata in res
        )
        res = ((item[0][1], item[1][1]) for item in res)  # drop name
        res = (                                    # pull integrals out of wrps
            line_tuple
            for w_el, w_mu in res
            for line_tuple in zip(get_line_info(w_el), get_line_info(w_mu))
        )
        res = (
            get_fmt(line_el, 2318.-93.) + get_fmt(line_mu, 2318.)
            for line_el, line_mu in res
        )
        res = '\n'.join(res)
        with open(self.cwd+'table_content.tex', 'w') as f:
            f.write('WARNING!!! Manually adding 15\\% fwd jet uncert!!\n')
            f.write('WARNING!!! Manually adding 15\\% fwd jet uncert!!\n')
            f.write('WARNING!!! Manually adding 15\\% fwd jet uncert!!\n')
            f.write(res)


class SigEffGraph(varial.tools.Tool):
    graph_attrs = {
        'TpBLH': 'T_{lh} b',
        'TpBRH': 'T_{rh} b',
        'TpTLH': 'T_{lh} t',
        'TpTRH': 'T_{rh} t',
    }

    def get_signal_wrps(self, token):
        inp_path = 'VLQ2HT/Outputs/Limits%s/DataBackground/HistoLoader' % token
        inp_path_sys = inp_path + 'Sys'
        group_key = lambda w: w.category+'__'+w.sample

        wrps = (w
                for p in (inp_path, inp_path_sys)
                for w in self.lookup_result(p))
        wrps = (w
                for w in wrps
                if w.is_signal)
        wrps = sorted(wrps, key=group_key)
        wrps = varial.gen.group(wrps, group_key)
        wrps = (varial.gen.gen_squash_sys(grp)
                for grp in wrps)
        return wrps

    def make_single_graph(self, wrps, token):
        def ntgrl_err(w):
            i, stat = varial.util.integral_and_error(w.histo)
            i, sys = varial.util.integral_and_error(w.histo_sys_err)
            return i, (stat**2 + sys**2)**.5
        mass = lambda w: float(w.sample[-4:])
        norm = {'el': 22.25, 'mu': 23.18}

        vals = ((mass(w),) + ntgrl_err(w) + (w,)  # tuple of (m, eff, eff_err, wrp)
                for w in wrps)
        vals = list(vals)
        cat = vals[0][-1].category
        vals = list((x, y/norm[cat], ye/norm[cat], w)
                    for x, y, ye, w in vals)
        x = array.array('f', (v[0] for v in vals))
        y = array.array('f', (v[1] for v in vals))
        xe = array.array('f', (0. for v in vals))
        ye = array.array('f', (v[2] for v in vals))

        graph = ROOT.TGraph(len(x), x, y)  # , xe, ye)
        graph.SetLineWidth(2)
        graph.GetXaxis().SetTitle('T quark mass (GeV)')
        graph.GetYaxis().SetTitle('#epsilon_{sel.} (%)')
        graph.SetMarkerStyle(20)

        return varial.wrp.GraphWrapper(
            graph,
            legend=self.graph_attrs[token],
            category=cat,
            draw_option='L',
        )

    def make_graphs(self, token):
        wrps = self.get_signal_wrps(token)
        wrps = varial.gen.group(wrps, lambda w: w.category)
        wrps = (self.make_single_graph(grp, token)
                for grp in wrps)
        return wrps

    def run(self):
        tokens = ['TpBLH', 'TpBRH', 'TpTLH', 'TpTRH']
        wrps = (w
                for t in tokens
                for w in self.make_graphs(t))
        wrps = sorted(wrps, key=lambda w: w.category)
        self.result = wrps


def plot_setup(grps):
    def set_line_style(wrps):
        line_styles = [1, 2, 3, 4]
        for wrp, style in itertools.izip(wrps,line_styles):
            wrp.obj.SetLineStyle(style)
            wrp.obj.SetLineWidth(2)
            yield wrp
    return (set_line_style(grp) for grp in grps)


sig_eff_grph_pltr = varial.tools.Plotter(
    input_result_path='../SigEffGraph',
    plot_grouper=lambda ws: varial.gen.group(ws, lambda w: w.category),
    plot_setup=plot_setup,
    save_name_func=lambda c: c._renderers[0].category,
    name='SigEffGraphPlot',
)
