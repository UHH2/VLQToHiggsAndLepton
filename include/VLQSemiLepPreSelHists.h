#pragma once

#include "UHH2/core/include/Hists.h"
#include "TH1F.h"

class VLQSemiLepPreSelHists: public uhh2::Hists {
public:
    VLQSemiLepPreSelHists(uhh2::Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        lepPt(book<TH1F>(
            "PrimaryLeptonPt",
            ";primary lepton p_{T};events",
            1000, 0, 1000
        )),
        muoPt(book<TH1F>(
            "PrimaryMuonPt",
            ";primary muon p_{T};events",
            1000, 0, 1000
        )),
        elePt(book<TH1F>(
            "PrimaryElePt",
            ";primary electron p_{T};events",
            1000, 0, 1000
        )),
        leadingJetPt(book<TH1F>(
            "LeadingJetPt",
            ";leading jet p_{T};events",
            1000, 0, 2000
        )),
        st(book<TH1F>(
            "ST",
            ";ST;events",
            1000, 0, 4000
        )) {}
    virtual void fill(const uhh2::Event &) override {}
    virtual ~VLQSemiLepPreSelHists() {}

    TH1F * lepPt;
    TH1F * muoPt;
    TH1F * elePt;
    TH1F * leadingJetPt;
    TH1F * st;
};
