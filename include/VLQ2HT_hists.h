#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/Utils.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"

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


static int find_top_and_higgs(const vector<GenParticle> & genparticles,
                              LorentzVector & t_gen,
                              LorentzVector & h_gen) {
    int found_n = 0;
    for (const auto &gp : genparticles) {
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
    return found_n;
}  // function find_top_and_higgs


class VLQ2HTRecoGenMatchHists: public Hists {
public:
    VLQ2HTRecoGenMatchHists(Context & ctx, const string & dir):
        Hists(ctx, dir),
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),

        top_hig_dr(book<TH1F>(
            "matching_top_hig_dr",
            ";#DeltaR(t_{reco}, H_{reco});events",
            100, 0, 5.
        )),
        top_mass_(book<TH1F>(
            "matching_top_mass",
            "M_{top cand., reco} / GeV; events",
            100, 0, 500.
        )),
        hig_mass_(book<TH1F>(
            "matching_hig_mass",
            "M_{higgs cand., reco} / GeV; events",
            100, 0, 500.
        ))
    {}

    virtual void fill(const uhh2::Event & e) override {
        float w = e.weight;

        // grab particles
        LorentzVector t_gen, h_gen;
        if (find_top_and_higgs(*e.genparticles, t_gen, h_gen) != 2) {
            return;
        }
        if (!(e.is_valid(h_top_lep) && e.is_valid(h_higgs))) {
            return;
        }

        const LorentzVector & t_reco = e.get(h_top_lep);
        const LorentzVector & h_reco = e.get(h_higgs);

        // matching condition
        if (deltaR(t_gen, t_reco) > 0.2 || deltaR(h_gen, h_reco) > 0.2) {
            return;
        }

        top_hig_dr->Fill(deltaR(h_reco, t_reco), w);
        top_mass_->Fill(inv_mass_safe(t_reco), w);
        hig_mass_->Fill(inv_mass_safe(h_reco), w);
    }

private:
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;

    TH1F * top_hig_dr;
    TH1F * top_mass_;
    TH1F * hig_mass_;
};  // class VLQ2HTRecoGenMatchHists


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
        foundGenParticles(book<TH1F>(
            "foundGenParticles",
            ";top and higgs generator particles found;events",
            2, -.5, 1.5
        )),
        foundRecoTopAndHiggs(book<TH2F>(
            "foundRecoTopAndHiggs",
            ";top reconstruction successful;Higgs reconstruction successful",
            2, -.5, 1.5,
            2, -.5, 1.5
        )),
        topDRDPt(book<TH2F>(
            "topDRDPt",
            ";#DeltaR(t_{reco}, t_{gen});top: (P_{T, gen} - P_{T, reco}) / P_{T, gen}",
            100, 0, 5.,
            60, -1.5, 1.5
        )),
        higDRDPt(book<TH2F>(
            "higgDRDPt",
            ";#DeltaR(H_{reco}, H_{gen});Higgs: (P_{T, gen} - P_{T, reco}) / P_{T, gen}",
            100, 0., 5.,
            60, -1.5, 1.5
        )),
        topPtResponse(book<TProfile>(
            "topPtResponse",
            ";top quark P_{T, gen} / GeV;top quark (P_{T, gen} - P_{T, reco}) / P_{T, gen}",
            70, 0., 700,
            -1., 1.
        )),
        higPtResponse(book<TProfile>(
            "higPtResponse",
            ";Higgs cand. P_{T, gen} / GeV;Higgs cand. (P_{T, gen} - P_{T, reco}) / P_{T, gen}",
            70, 0., 700,
            -1., 1.
        ))
    {}

    virtual void fill(const uhh2::Event & e) override {
        float w = e.weight;

        LorentzVector t_gen, h_gen;
        bool gen_available = (find_top_and_higgs(*e.genparticles, t_gen, h_gen) == 2);
        bool top_available = e.is_valid(h_top_lep);
        bool higgs_available = e.is_valid(h_higgs);

        // availability
        foundGenParticles->Fill((int) gen_available, w);
        foundRecoTopAndHiggs->Fill((int) top_available, (int) higgs_available, w);

        // gen
        if (gen_available) {
            tophigggenDR->Fill(deltaR(t_gen, h_gen), w);
        }

        // top
        if (gen_available && top_available) {
            const auto & t_reco = e.get(h_top_lep);
            float top_rel_pt = (t_gen.pt() - t_reco.pt())/t_gen.pt();
            topDRDPt->Fill(deltaR(t_gen, t_reco), top_rel_pt, w);
            topPtResponse->Fill(t_gen.pt(), top_rel_pt, w);
        }

        // higgs
        if (gen_available && higgs_available) {
            const auto & h_reco = e.get(h_higgs);
            float hig_rel_pt = (h_gen.pt() - h_reco.pt())/h_gen.pt();
            higDRDPt->Fill(deltaR(h_gen, h_reco), hig_rel_pt, w);
            higPtResponse->Fill(h_gen.pt(), hig_rel_pt, w);
        }
    }

private:
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;

    TH1F * tophigggenDR;
    TH1F * foundGenParticles;
    TH2F * foundRecoTopAndHiggs;
    TH2F * topDRDPt;
    TH2F * higDRDPt;
    TProfile * topPtResponse;
    TProfile * higPtResponse;
};  // class VLQ2HTRecoGenComparison


class VLQ2HTEventReco: public Hists {
public:
    VLQ2HTEventReco(Context & ctx, const string & dir):
        Hists(ctx, dir),
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),

        higgPtVsTopPt(book<TH2F>(
            "higgPtVsTopPt",
            ";H^{rec} p_{T};top^{rec} p_{T}",
            70, 0, 700,
            70, 0, 700
        ))
    {}

    virtual void fill(const uhh2::Event & e) override {
        float w = e.weight;

        bool top_available = e.is_valid(h_top_lep);
        bool higgs_available = e.is_valid(h_higgs);

        if (top_available && higgs_available) {
            const auto & t_reco = e.get(h_top_lep);
            const auto & h_reco = e.get(h_higgs);
            higgPtVsTopPt->Fill(h_reco.pt(), t_reco.pt(), w);
        }
    }

private:
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;

    TH2F * higgPtVsTopPt;
};  // class VLQ2HTEventReco

