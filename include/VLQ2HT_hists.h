#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Utils.h"
#include "TH1F.h"
#include "TH2F.h"

#include "UHH2/VLQToHiggsAndLepton/include/HandleHist.h"
#include "UHH2/VLQToHiggsAndLepton/include/SelectionItem.h"

using namespace std;
using namespace uhh2;


class SingleLepTrigHists: public Hists {
public:
    SingleLepTrigHists(Context & ctx,
                  const string & dir,
                  const string & trig_path,
                  bool is_ele):
        Hists(ctx, dir),
        trig_path_(trig_path + '*'),
        is_ele_(is_ele),
        eff_sub_(book<TH1F>((trig_path+"_eff_sub").c_str(), "p_{T}", 100, 0, 1000)),
        eff_tot_(book<TH1F>((trig_path+"_eff_tot").c_str(), "p_{T}", 100, 0, 1000)) {}

    virtual void fill(const uhh2::Event & e) override {
        float pt;
        if (is_ele_) {
            pt = e.electrons->size() ? e.electrons->at(0).pt() : -1.;
        } else {
            pt = e.muons->size() ? e.muons->at(0).pt() : -1.;
        }
        if (pt > 0.) {
            eff_tot_->Fill(pt, e.weight);
            auto trg_idx = e.get_trigger_index(trig_path_);
            if (e.passes_trigger(trg_idx)) {
                eff_sub_->Fill(pt, e.weight);
            }
        }
    }

private:
    const string trig_path_;
    bool is_ele_;
    TH1F * eff_sub_;
    TH1F * eff_tot_;
};  // class SingleLepTrigHists


class Nm1SelHists: public Hists {
public:
    explicit Nm1SelHists(Context & ctx,
                         const string & dir,
                         const SelItemsHelper & sel_helper):
        Hists(ctx, dir),
        h_sel_res(ctx.get_handle<vector<bool>>("sel_accept"))
    {
        sel_helper.fill_hists_vector(v_hists, dir);
    }

    virtual void fill(const Event & event) override {
        const auto & v_accept = event.get(h_sel_res);
        for (unsigned i=0; i<v_hists.size(); ++i) {
            bool accept_nm1 = true;
            for (unsigned j=0; j<v_accept.size(); ++j) {
                if (i==j) {
                    continue;
                }
                if (!v_accept[j]) {
                    accept_nm1 = false;
                    break;
                }
            }
            if (accept_nm1) {
                v_hists[i]->fill(event);
            }
        }
    }

private:
    Event::Handle<vector<bool>> h_sel_res;
    vector<unique_ptr<Hists>> v_hists;
};


class VLQ2HTCutflow: public Hists {
public:
    VLQ2HTCutflow(Context & ctx,
                  const string & dir,
                  const SelItemsHelper & sel_helper):
        Hists(ctx, dir),
        h(book<TH1F>("cutflow", ";;events", 1, 0, -1)),
        names(sel_helper.get_item_names()),
        h_sel(ctx.get_handle<vector<bool>>("sel_accept"))
    {
        h->SetBit(TH1::kCanRebin);
        h->Fill("pre-sel.", 1e-7);
        for (const string & name : names) {
            h->Fill(name.c_str(), 1e-7);
        }
    }

    virtual void fill(const uhh2::Event & e) override {
        float w = e.weight;
        const auto & sel = e.get(h_sel);
        h->Fill("pre-sel.", w);
        for (unsigned i = 0; i < names.size(); ++i) {
            if (sel[i]) {
                h->Fill(names[i].c_str(), w);
            } else {
                break;
            }
        }
    }

private:
    TH1F * h;
    const vector<string> & names;
    Event::Handle<vector<bool>> h_sel;
};


class VLQ2HTRecoGenComparison: public Hists {
public:
    VLQ2HTRecoGenComparison(Context & ctx, const string & dir):
        Hists(ctx, dir),
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),

        tophigggenDR(book<TH1F>(
            "tophigggenDR",
            ";#DeltaR(t_{gen}, H_{gen});events",
            100, 0, 5.
        )),
        topDRDPt(book<TH2F>(
            "topDRDPt",
            ";#DeltaR(t_{reco}, t_{gen});#DeltaP_{T, rel}(t_{reco}, t_{gen})",
            100, 0, 5.,
            60, -1.5, 1.5
        )),
        higDRDPt(book<TH2F>(
            "higgDRDPt",
            ";#DeltaR(H_{reco}, H_{gen});#DeltaP_{T, rel}(H_{reco}, H_{gen})",
            100, 0., 5.,
            60, -1.5, 1.5
        ))
    {}

    virtual void fill(const uhh2::Event & e) override {
        const auto & gps = e.genparticles;
        float w = e.weight;

        // grab gen particles
        LorentzVector t_gen, h_gen;
        int found_n = 0;
        for (const auto &gp : *gps) {
            if (abs(gp.pdgId()) == 6) {
                t_gen = gp.v4();
                found_n++;
            }
            if (abs(gp.pdgId()) == 25) {
                h_gen = gp.v4();
                found_n++;
            }
            if (found_n == 2) {
                break;
            }
        }
        if (found_n != 2) {
            return;
        }

        // gen
        tophigggenDR->Fill(deltaR(t_gen, h_gen), w);

        // top
        if (e.is_valid(h_top_lep)) {
            const auto & t_reco = e.get(h_top_lep);
            topDRDPt->Fill(deltaR(t_gen, t_reco), (t_reco.pt() - t_gen.pt())/t_gen.pt(), w);
        }

        // higgs
        if (e.is_valid(h_higgs)) {
            const auto & h_reco = e.get(h_higgs);
            higDRDPt->Fill(deltaR(h_gen, h_reco), (h_reco.pt() - h_gen.pt())/h_gen.pt(), w);
        }
    }

private:
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;

    TH1F * tophigggenDR;
    TH2F * topDRDPt;
    TH2F * higDRDPt;
};


class VLQ2HTGenHists: public Hists {
public:
    VLQ2HTGenHists(Context & ctx, const string & dir):
        Hists(ctx, dir),
        tPrimeKinematic(book<TH2F>(
            "tPrimeKinematic",
            ";T' p_{T};T' #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        fwJetKinematic(book<TH2F>(
            "assJetKinematic",
            ";ass. parton p_{T};ass. parton #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        higgKinematic(book<TH2F>(
            "higgKinematic",
            ";H p_{T};H #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        higgProdKinematic(book<TH2F>(
            "higgProdKinematic",
            ";H decay prods. p_{T};H decay prods. #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        higgProdPdgId(book<TH1F>(
            "higgProdPdgId",
            ";H decay prod pdgid;events",
            1, 0, -1
        )),
        higgProdDr(book<TH1F>(
            "higgProdDr",
            ";#DeltaR(H decay prods);events",
            50, 0., 5.
        )),
        topKinematic(book<TH2F>(
            "topKinematic",
            ";top quark p_{T};top quark #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        topWKinematic(book<TH2F>(
            "topWKinematic",
            ";W p_{T};W #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        topBKinematic(book<TH2F>(
            "topBKinematic",
            ";b quark (from top) p_{T};b quark (from top) #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        topWProdKinematic(book<TH2F>(
            "topWProdKinematic",
            ";W decay prods. p_{T};W decay prods. #eta",
            100, 0, 1000,
            100, -6., 6.
        ))
    {
        higgProdPdgId->SetBit(TH1::kCanRebin);
    }

    virtual void fill(const uhh2::Event & e) override {
        const auto & gps = e.genparticles;
        float w = e.weight;

        // find particles
        GenParticle tprime,
                    fwd_parton,
                    higg,
                    top,
                    top_w,
                    top_b;
        for (const auto &gp : *gps) {
            if (abs(gp.pdgId()) == 6000006) {
                tprime = gp;
                break;
            }
        }
        if (tprime.mother(gps, 1)) {
            auto mom = tprime.mother(gps, 1);
            auto d1 = mom->daughter(gps,1);
            auto d2 = mom->daughter(gps,2);
            if (abs(d1->pdgId()) == 6000006) {
                fwd_parton = *d2;
            } else {
                fwd_parton = *d1;
            }
        } else {
            for (const auto &gp : *gps) {
                if (!gp.mother(gps, 1) && abs(gp.pdgId()) != 6000006) {
                    fwd_parton = gp;
                    break;
                }
            }
        }
        auto d1 = tprime.daughter(gps,1);
        auto d2 = tprime.daughter(gps,2);
        if (abs(d1->pdgId()) == 6) {
            top = *d1;
            higg = *d2;
        } else {
            top = *d2;
            higg = *d1;
        }
        auto d3 = top.daughter(gps,1);
        auto d4 = top.daughter(gps,2);
        if (d3 && d4) {
            if (abs(d3->pdgId()) == 24) {
                top_b = *d4;
                top_w = *d3;
            } else {
                top_b = *d3;
                top_w = *d4;
            }
        }
        // fill hists
        tPrimeKinematic->Fill(tprime.pt(), tprime.eta(), w);
        fwJetKinematic->Fill(fwd_parton.pt(), fwd_parton.eta(), w);
        topKinematic->Fill(top.pt(), top.eta(), w);
        if (top_w.pdgId()) {
            topWKinematic->Fill(top_w.pt(), top_w.eta(), w);
            topBKinematic->Fill(top_b.pt(), top_b.eta(), w);
            if (top_w.daughter(gps, 1)) {
                topWProdKinematic->Fill(top_w.daughter(gps, 1)->pt(), top_w.daughter(gps, 1)->eta(), w);
                topWProdKinematic->Fill(top_w.daughter(gps, 2)->pt(), top_w.daughter(gps, 2)->eta(), w);
            }
        }
        higgKinematic->Fill(higg.pt(), higg.eta(), w);
        if (higg.daughter(gps, 1)) {
            higgProdKinematic->Fill(higg.daughter(gps, 1)->pt(), higg.daughter(gps, 1)->eta(), w);
            higgProdKinematic->Fill(higg.daughter(gps, 2)->pt(), higg.daughter(gps, 2)->eta(), w);
            higgProdPdgId->Fill(to_string(abs(higg.daughter(gps, 1)->pdgId())).c_str(), w);
        }
        if (higg.daughter(gps, 1) && higg.daughter(gps, 2)) {
            higgProdDr->Fill(deltaR(higg.daughter(gps, 1)->v4(),
                                    higg.daughter(gps, 2)->v4()), w);
        }
    }

private:
    TH2F * tPrimeKinematic;
    TH2F * fwJetKinematic;
    TH2F * higgKinematic;
    TH2F * higgProdKinematic;
    TH1F * higgProdPdgId;
    TH1F * higgProdDr;
    TH2F * topKinematic;
    TH2F * topWKinematic;
    TH2F * topBKinematic;
    TH2F * topWProdKinematic;
};  // class VLQ2HTGenHists
