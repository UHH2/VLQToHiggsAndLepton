#pragma once

#include <map>
#include <string>
#include <vector>
#include "UHH2/VLQToHiggsAndLepton/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


const vector<unique_ptr<SelectionItem>> & sel_items_vec() {
    static vector<unique_ptr<SelectionItem>> v;
    if (!v.size()) {
        v.emplace_back(new SelDatI("trigger_accept",    "ele+Jets OR mu+Jets",      2, -.5, 1.5         ,1      ));
        v.emplace_back(new SelDatI("n_jets",            "N_{jet}",                  21, -.5, 20.5               ));
        v.emplace_back(new SelDatI("n_leptons",         "N_{lepton}",               11, -.5, 10.5       ,1      ));
        v.emplace_back(new SelDatI("n_fwd_jets",        "N_{fwd jet}",              11, -.5, 10.5               ));
        v.emplace_back(new SelDatI("n_btags",           "N_{b-tag}",                11, -.5, 10.5       ,2      ));
        v.emplace_back(new SelDatI("n_leading_btags",   "N_{b-tag leading}",        11, -.5, 10.5               ));
        v.emplace_back(new SelDatI("n_higgs_tags",      "N_{H jet}",                11, -.5, 10.5               ));
        v.emplace_back(new SelDatF("leading_jet_pt",    "leading jet p_{T}",        50, 100, 1500       ,250    ));
        v.emplace_back(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T}",    50, 100, 1500       ,65     ));
        v.emplace_back(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",     50, 100, 1500               ));
        v.emplace_back(new SelDatD("ST",                "ST",                       100, 0, 5000                ));
        v.emplace_back(new SelDatF("event_chi2",        "event chi2",               50, 0, 100                  ));
        v.emplace_back(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",            50, 0, 5                    ));
        v.emplace_back(new SelDatF("tlep_pt",           "lept. top p_{T}",          50, 0, 1000                 ));
        v.emplace_back(new SelDatF("tlep_eta",          "lept. top #eta",           50, -5., 5.                 ));
        v.emplace_back(new SelDatF("tlep_mass",         "lept. top mass",           50, 0, 1000                 ));
        v.emplace_back(new SelDatF("h_pt",              "Higgs p_{T}",              50, 0, 1000                 ));
        v.emplace_back(new SelDatF("h_eta",             "Higgs #eta",               50, -5., 5.                 ));
        v.emplace_back(new SelDatF("h_mass",            "Higgs mass",               50, 0, 1000                 ));
        v.emplace_back(new SelDatF("vlq_pt",            "T' p_{T}",                 50, 0, 1000                 ));
        v.emplace_back(new SelDatF("vlq_eta",           "T' #eta",                  50, -5., 5.                 ));
        v.emplace_back(new SelDatF("vlq_mass",          "T' mass",                  50, 0, 2000                 ));
    }
    return v;
}

