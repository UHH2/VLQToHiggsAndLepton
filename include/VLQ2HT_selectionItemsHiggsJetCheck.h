#pragma once

#include <string>
#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const float DR_2D_CUT = 0.25;
static const float DPT_2D_CUT = 40.0;


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQ2HT {
    // shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "trigger accept",                    2, -.5, 1.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{jet}",                           21, -.5, 20.5             )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",                        11, -.5, 10.5             )),
    shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",                 11, -.5, 10.5             )),
    shared_ptr<SelectionItem>(new SelDatF("abs_largest_jet_eta", "most forward jet #eta",           50, 0., 5.                )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass",            "jet mass / 5 GeV",                  50, 50, 300               )),
    shared_ptr<SelectionItem>(new SelDatF("h_pt",              "jet p_{T} / 20 GeV",                50, 0, 1000      , 400        )),
    shared_ptr<SelectionItem>(new SelDatF("h_mass_topjet",     "jet mass from subjets / 5 GeV",     50, 50, 300                 )),

    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                         11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    "leading jet p_{T} / 20 GeV",        75, 0., 1500                )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T} / 20 GeV",    75, 0., 1500                )),
    shared_ptr<SelectionItem>(new SelDatF("largest_jet_eta",   "most forward jet #eta",             50, -5., 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T} / 10 GeV",     50, 0., 500                )),

    shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{fwd jet}",                       11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_htags",           "N_{H jet}",                         11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                "ST / 50 GeV",                       100, 0, 5000                )),
    shared_ptr<SelectionItem>(new SelDatD("STgt40",            "STgt40 / 50 GeV",                   100, 0, 5000                )),
    shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs #eta",                        50, -5., 5.                 )),
};


// static const vector<std::string> TRIGGER_PATHS {
//     "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*",
//     "HLT_Mu40_v*",
//     "HLT_PFHT900_v*",
// };


