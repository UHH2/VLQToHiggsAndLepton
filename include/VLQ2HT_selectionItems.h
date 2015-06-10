#pragma once

#include <string>
#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


// --------------------------------------------------------
// Cut values for requested signal efficiency: 0.5
// Corresponding background efficiency       : 0.096195
// Transformation applied to input variables : None
// --------------------------------------------------------
// Cut[ 0]:    2.25731 <          dr_higg_top <=    7.34709   only lower
// Cut[ 1]:    57.4837 <               h_mass <=    157.531   both!
// Cut[ 2]:    160.538 <                 h_pt <=    909.998   only lower
// Cut[ 3]:   0.957339 < abs(largest_jet_eta) <=    5.71082   only lower
// Cut[ 5]:       0.98 <      n_leading_btags <=       4.04   only lower
// --------------------------------------------------------

// ------------------------------------------------------------
// Cut values for requested signal efficiency: 0.4
// Corresponding background efficiency       : 0.0774732
// Transformation applied to input variables : None
// ------------------------------------------------------------
// Cut[ 0]:    1.44821 <              dr_higg_top <=      1e+30
// Cut[ 1]:    61.1548 <                   h_mass <=    174.707
// Cut[ 2]:    225.171 <                     h_pt <=      1e+30
// Cut[ 3]:     2.4325 < abs(abs_largest_jet_eta) <=      1e+30
// ------------------------------------------------------------


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQ2HT {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "ele+Jets OR mu+Jets",      2, -.5, 1.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",               11, -.5, 10.5       ,1      )),
    shared_ptr<SelectionItem>(new SelDatF("event_chi2",        "event chi2",               100, 0, 200         ,150    )),
    shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",        11, -.5, 10.5       ,1      )),
    shared_ptr<SelectionItem>(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",            50, 0, 5            ,2      )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass",            "Higgs mass",               50, 0, 1000         ,60 ,160)),

    shared_ptr<SelectionItem>(new SelDatF("h_pt",              "Higgs p_{T}",              50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("abs_largest_jet_eta", "most forward jet #eta",  50, 0., 5.                  )),

    // shared_ptr<SelectionItem>(new SelDatF("abs_vlq_eta",       "T #eta",                   50, 0., 5.                  )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    "leading jet p_{T}",        75, 0., 1500                )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T}",    75, 0., 1500                )),
    shared_ptr<SelectionItem>(new SelDatF("largest_jet_eta",   "most forward jet #eta",    50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",     75, 0., 1500                )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{jet}",                  21, -.5, 20.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{fwd jet}",              11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_htags",           "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                "ST",                       100, 0, 5000                )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_pt",           "lept. top p_{T}",          50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_eta",          "lept. top #eta",           50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_mass",         "lept. top mass",           50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs #eta",               50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_pt",            "T p_{T}",                  50, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_eta",           "T #eta",                   50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_mass",          "T mass",                   50, 0, 2000                 )),

    // shared_ptr<SelectionItem>(new SelDatF("es_isotropy",          "isotropy",              60, -0.1, 1.1               )),
    // shared_ptr<SelectionItem>(new SelDatF("es_circularity",       "circularity",           60, -0.1, 1.1               )),
    // shared_ptr<SelectionItem>(new SelDatF("es_sphericity",        "sphericity",            60, -0.1, 1.1               )),
    // shared_ptr<SelectionItem>(new SelDatF("es_aplanarity",        "aplanarity",            60, -0.1, 1.1               )),
    // shared_ptr<SelectionItem>(new SelDatF("es_C",                 "C",                     60, -0.1, 1.1               )),
    // shared_ptr<SelectionItem>(new SelDatF("es_D",                 "D",                     60, -0.1, 1.1               )),

    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_isotropy",    "plus_lep_isotropy",     60, -0.1, 1.1            )),
    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_circularity", "plus_lep_circularity",  60, -0.1, 1.1            )),
    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_sphericity",  "plus_lep_sphericity",   60, -0.1, 1.1            )),
    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_aplanarity",  "plus_lep_aplanarity",   60, -0.1, 1.1            )),
    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_C",           "plus_lep_C",            60, -0.1, 1.1            )),
    // shared_ptr<SelectionItem>(new SelDatF("es_plus_lep_D",           "plus_lep_D",            60, -0.1, 1.1            )),
};


static const vector<std::string> TRIGGER_PATHS {
    "HLT_Ele95_CaloIdVT_GsfTrkIdT_v*",
    "HLT_Mu40_v*",
};


