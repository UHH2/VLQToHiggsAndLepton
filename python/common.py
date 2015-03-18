import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')


import varial


def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def add_wrp_info(wrps):
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path.split('/')[0],
        legend=lambda w: ('100* ' if 'TpJ_TH_M' in w.sample else '') + w.sample,
        is_signal=lambda w: 'TpJ_TH_M' in w.sample,
        lumi=lambda w: 0.01 if 'TpJ_TH_M' in w.sample else 1.
    )


def merge_decay_channels(wrps, postfixes=('_Tlep', '_NonTlep')):
    """histos must be sorted!!"""
    buffer = []
    for w in wrps:
        if any(w.sample.endswith(p) for p in postfixes):
            buffer.append(w)
            if len(buffer) == len(postfixes):
                res = varial.operations.sum(buffer)
                res.sample = ''.join(res.sample[:-len(p)] 
                                     for p in postfixes 
                                     if res.sample.endswith(p))
                res.legend = ''.join(res.legend[:-len(p)] 
                                     for p in postfixes 
                                     if res.legend.endswith(p))
                buffer = []
                yield res
        else:
            yield w


