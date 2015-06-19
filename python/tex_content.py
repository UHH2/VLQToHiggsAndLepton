import varial.tools

# categories
p_filt1h = 'VLQ2HT/EventLoopAndPlots/FilteredCat1htag/'

# subfolders
p_nm1sel = 'Plots/VLQ2HT_stack/Nm1Selection/'
p_cutflow = 'Plots/CutflowTools/'

ext = '.png'
target_ext = '.png'

images = {
    'filt1h_Nm1Sel_tlep.tex': (
        p_filt1h + p_nm1sel + 'tlep_eta_lin' + ext,
        p_filt1h + p_nm1sel + 'tlep_pt_lin' + ext,
        p_filt1h + p_nm1sel + 'tlep_mass_lin' + ext,
    ),
    'filt1h_Nm1Sel_higg.tex': (
        p_filt1h + p_nm1sel + 'h_eta_lin' + ext,
        p_filt1h + p_nm1sel + 'h_pt_lin' + ext,
        p_filt1h + p_nm1sel + 'h_mass_lin' + ext,
    ),
    'filt1h_Nm1Sel_vlq.tex': (
        p_filt1h + p_nm1sel + 'vlq_eta_lin' + ext,
        p_filt1h + p_nm1sel + 'vlq_pt_lin' + ext,
        p_filt1h + p_nm1sel + 'vlq_mass_lin' + ext,
    ),
}

plain_files = {
    'filt1h_cutflow_tabular.tex':
        p_filt1h + p_cutflow + 'CutflowTableTex/cutflow_tabular.tex',
    'filt1h_cutflow_stack'+target_ext:
        p_filt1h + p_cutflow + 'CutflowStack/Cutflow_cutflow'+ext
}


dirname = 'AutoContentVLQ2HT'
tex_content = varial.tools.TexContent(
    images,
    plain_files,
    r"\includegraphics[width=0.49\textwidth]{" + dirname + "/%s}",
    dest_dir=None,
    name=dirname,
)