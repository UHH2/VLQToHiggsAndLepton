#pragma once

#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQ2HT {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "ele+Jets OR mu+Jets",      2, -.5, 1.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",               11, -.5, 10.5       ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    "leading jet p_{T}",        50, 100, 1500               )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T}",    50, 100, 1500               )),
    shared_ptr<SelectionItem>(new SelDatF("largest_jet_eta",   "most forward jet #eta",    50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("event_chi2",        "event chi2",               50, 0, 100                  )),

    shared_ptr<SelectionItem>(new SelDatF("es_isotropy",          "isotropy",                 60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_circularity",       "circularity",              60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_sphericity",        "sphericity",               60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_aplanarity",        "aplanarity",               60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_C",                 "C",                        60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_D",                 "D",                        60, -0.1, 1.1               )),

    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_isotropy",    "plus_lep_isotropy",     60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_circularity", "plus_lep_circularity",  60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_sphericity",  "plus_lep_sphericity",   60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_aplanarity",  "plus_lep_aplanarity",   60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_C",           "plus_lep_C",            60, -0.1, 1.1               )),
    shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_D",           "plus_lep_D",            60, -0.1, 1.1               )),

    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{jet}",                  21, -.5, 20.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{fwd jet}",              11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",        11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags",      "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",     50, 100, 1500               )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                "ST",                       100, 0, 5000                )),
    shared_ptr<SelectionItem>(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",            50, 0, 5                    )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_pt",           "lept. top p_{T}",          50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_eta",          "lept. top #eta",           50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_mass",         "lept. top mass",           50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_pt",              "Higgs p_{T}",              50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs #eta",               50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass",            "Higgs mass",               50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_pt",            "T p_{T}",                  50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_eta",           "T #eta",                   50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_mass",          "T mass",                   50, 0, 2000                 )),
};