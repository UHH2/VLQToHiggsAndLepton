#pragma once

#include <string>
#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const float DR_2D_CUT = 0.4;
static const float DPT_2D_CUT = 40.0;


static vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQ2HT {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "trigger accept",                                2, -.5, 1.5       ,1        )),    
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    ";leading ak4 jet p_{T};events / 20 GeV",        50, 0., 1000                )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", ";sub-leading ak4 jet p_{T};events / 20 GeV",    50, 0., 1000                )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                ";ST;events / 100 GeV",                          25, 0, 2500       ,400      )),
    shared_ptr<SelectionItem>(new SelDatF("event_chi2",        "event chi2",                                    50, 0, 200       ,-0.1,5000)),
    shared_ptr<SelectionItem>(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",                                 25, 0, 5          ,2.       )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_pt",           ";lept. top p_{T};events / 20 GeV",              25, 0, 1000       ,100      )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass",            ";Higgs candidate mass;events / 10 GeV",         25, 50, 300                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass_subjet",     ";Higgs candidate mass (from subjets);events / 10 GeV", 25, 50, 300                 )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", ";primary lepton p_{T};events / 20 GeV",         50, 0., 1000                )),
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el", "electron trigger accept (mu veto)",             2, -.5, 1.5                 )),
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu", "muon trigger accept",                           2, -.5, 1.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("h_pt",              ";Higgs candidate p_{T};events / 40 GeV",        25, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",                             11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("abs_largest_jet_eta", "most forward jet #eta",                       50, 0., 5.                  )),
    shared_ptr<SelectionItem>(new SelDatD("HT",                ";HT;events / 100 GeV",                          30, 0, 3000                 )),

    // shared_ptr<SelectionItem>(new SelDatF("abs_vlq_eta",       "T #eta",                            50, 0., 5.                  )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                                     11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags_tight",           "N_{b-tag}",                               11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_add_btags",  "N_{b-tag} without Higgs and Top",                    11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_add_btags_incl_top",  "N_{b-tag} without Higgs",                   11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_top_btags",  "N_{b-tag} (top)",                                    11, -.5, 10.5               )),


    shared_ptr<SelectionItem>(new SelDatF("largest_jet_eta",   "most forward ak4 jet #eta",                     50, -5., 5.                 )),
    
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_eta", ";primary lepton #eta;events",                  25, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatI("primary_lepton_charge", ";primary lepton charge;events",             3, -1.5, 1.5                )),

    shared_ptr<SelectionItem>(new SelDatI("h_n_subjet_btags",  "N_{H jet subjet b-tags}",                       5, -.5, 4.5               )),
    shared_ptr<SelectionItem>(new SelDatF("h_tau21",           "Higgs candidate #tau_{2}/#tau_{1}",             50, 0, 1                    )),
    shared_ptr<SelectionItem>(new SelDatF("h_tau32",           "Higgs candidate #tau_{3}/#tau_{2}",             50, 0, 1                    )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{ak4 jet}",                                   21, -.5, 20.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",                                    11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{ak4 fwd jet}",                               11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_htags",           "N_{H jet}",                                     5, -.5, 4.5               )),
    
    // shared_ptr<SelectionItem>(new SelDatD("STgt70",            ";STgt70;events / 50 GeV",                       50, 0, 2500                 )),
    // shared_ptr<SelectionItem>(new SelDatF("lep_plus_met_vec_sum", ";p_{T} of prim. lep + MET;events / 20 GeV",  75, 0, 1500              )),
    // shared_ptr<SelectionItem>(new SelDatF("lep_plus_met",      ";sum of p_{T} of prim. lep and MET;events / 20 GeV", 75, 0, 1500        )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_eta",          "lept. top #eta",                                25, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("tlep_mass",         ";lept. top mass;events / 10 GeV",               25, 100, 350                )),
    shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs candidate #eta",                          25, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_pt",            ";T p_{T};events / 20 GeV",                      25, 0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_eta",           "T #eta",                                        25, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("vlq_mass",          ";T mass;events / 80 GeV",                       35, 0, 2800                 )),

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


static const vector<std::string> TRIGGER_PATHS_MU {
    "HLT_Mu50_v*",
    "HLT_TkMu50_v*",
};


static const vector<std::string> TRIGGER_PATHS_MU_B {
  "HLT_Mu50_v*",
};
 

static const vector<std::string> TRIGGER_PATHS_ELE {
  //"HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*",
  //"HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"
  "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
  "HLT_Photon175_v*"

};
