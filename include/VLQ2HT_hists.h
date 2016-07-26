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


class VLQ2HTGenHists: public Hists {
public:
    VLQ2HTGenHists(Context & ctx, const string & dir):
        Hists(ctx, dir),

        higgTopDr(book<TH1F>(
            "higgTopDr",
            ";#DeltaR(H, top);events",
            50, 0., 5.
        )),
        higgTopDPhi(book<TH1F>(
            "higgTopDPhi",
            ";#Delta#Phi(H, top);events",
            50, 0., 5.
        )),
        tPrimeKinematic(book<TH2F>(
            "tPrimeKinematic",
            ";T' p_{T};T' #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        fwJetKinematic(book<TH2F>(
            "fwJetKinematic",
            ";ass. parton p_{T};ass. parton #eta",
            100, 0, 1000,
            100, -6., 6.
        )),
        fwPartonPdgId(book<TH1F>(
            "fwPartonPdgId",
            ";ass. parton pdgId;events",
            1, 0, -1
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
        higgProdDPhi(book<TH1F>(
            "higgProdDPhi",
            ";#Delta#Phi(H decay prods);events",
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
        topWProdCharge(book<TH1F>(
            "topWProdCharge",
            ";charge of W decay prods.;events",
            31, -1.55, 1.55
        )),
        topWProdKinematic(book<TH2F>(
            "topWProdKinematic",
            ";p_{T} of W decay prods.;#eta of W decay prods.",
            100, 0, 1000,
            100, -6., 6.
        )),
        topProdMaxDr(book<TH1F>(
            "topProdMaxDr",
            ";max #DeltaR(top decay prods);events",
            50, 0., 5.
        )),
        topProdMaxDPhi(book<TH1F>(
            "topProdMaxDPhi",
            ";max #Delta#Phi(top decay prods);events",
            50, 0., 5.
        )),
        topProdDrBToLepton(book<TH1F>(
            "topProdDrBToLepton",
            ";top products: #DeltaR(b to l);events",
            50, 0., 5.
        )),
        topProdDrBToNeutrino(book<TH1F>(
            "topProdDrBToNeutrino",
            ";top products: #DeltaR(b to #nu);events",
            50, 0., 5.
        )),
        topProdDrLeptonToNeutrino(book<TH1F>(
            "topProdDrLeptonToNeutrino",
            ";top products: #DeltaR(l to #nu);events",
            50, 0., 5.
        )),
        topProdDPhiBToLepton(book<TH1F>(
            "topProdDPhiBToLepton",
            ";top products: #Delta#Phi(b to l);events",
            50, 0., 5.
        )),
        topProdDPhiBToNeutrino(book<TH1F>(
            "topProdDPhiBToNeutrino",
            ";top products: #Delta#Phi(b to #nu);events",
            50, 0., 5.
        )),
        topProdDPhiLeptonToNeutrino(book<TH1F>(
            "topProdDPhiLeptonToNeutrino",
            ";top products: #Delta#Phi(l to #nu);events",
            50, 0., 5.
        )) // ,
        // topDrToLepton(book<TH1F>(
        //     "topProdDrBToLepton",
        //     ";top products: #DeltaR(b to l);events",
        //     50, 0., 5.
        // )),
        // topDrToNeutrino(book<TH1F>(
        //     "topProdDrBToNeutrino",
        //     ";top products: #DeltaR(b to #nu);events",
        //     50, 0., 5.
        // )),
        // topDrToB(book<TH1F>(
        //     "topProdDrLeptonToNeutrino",
        //     ";top products: #DeltaR(l to #nu);events",
        //     50, 0., 5.
        // )),
        // topDPhiToLepton(book<TH1F>(
        //     "topProdDPhiBToLepton",
        //     ";top products: #Delta#Phi(b to l);events",
        //     50, 0., 5.
        // )),
        // topDPhiToNeutrino(book<TH1F>(
        //     "topProdDPhiBToNeutrino",
        //     ";top products: #Delta#Phi(b to #nu);events",
        //     50, 0., 5.
        // )),
        // topDPhiToB(book<TH1F>(
        //     "topProdDPhiLeptonToNeutrino",
        //     ";top products: #Delta#Phi(l to #nu);events",
        //     50, 0., 5.
        // ))
    {
        higgProdPdgId->SetCanExtend(TH1::kXaxis);
        fwPartonPdgId->SetCanExtend(TH1::kXaxis);
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
            if (abs(gp.pdgId()) > 6000000) {
                tprime = gp;
                break;
            }
        }
        if (tprime.mother(gps, 1)) {
            auto mom = tprime.mother(gps, 1);
            auto d1 = mom->daughter(gps,1);
            auto d2 = mom->daughter(gps,2);
            if (abs(d1->pdgId()) > 6000000) {
                fwd_parton = *d2;
            } else {
                fwd_parton = *d1;
            }
        } else {
            for (const auto &gp : *gps) {
                if (!gp.mother(gps, 1) && abs(gp.pdgId()) < 6000000) {
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
        higgTopDr->Fill(deltaR(top.v4(), higg.v4()), w);
        higgTopDPhi->Fill(deltaPhi(top.v4(), higg.v4()), w);
        tPrimeKinematic->Fill(tprime.pt(), tprime.eta(), w);
        fwJetKinematic->Fill(fwd_parton.pt(), fwd_parton.eta(), w);
        fwPartonPdgId->Fill(to_string(abs(fwd_parton.pdgId())).c_str(), w);
        topKinematic->Fill(top.pt(), top.eta(), w);
        if (top_w.pdgId()) {
            topWKinematic->Fill(top_w.pt(), top_w.eta(), w);
            topBKinematic->Fill(top_b.pt(), top_b.eta(), w);
            if (top_w.daughter(gps, 1) && top_w.daughter(gps, 2)) {
                auto tw_d1 = top_w.daughter(gps, 1);
                auto tw_d2 = top_w.daughter(gps, 2);

                topWProdKinematic->Fill(tw_d1->pt(), tw_d1->eta(), w);
                topWProdKinematic->Fill(tw_d2->pt(), tw_d2->eta(), w);

                topWProdCharge->Fill(tw_d1->charge(), w);
                topWProdCharge->Fill(tw_d2->charge(), w);

                auto tw_nu = (tw_d1->pdgId() % 2 == 0) ? tw_d1 : tw_d2;
                auto tw_le = (tw_d1->pdgId() % 2 == 0) ? tw_d2 : tw_d1;

                auto tw_nu_v4 = tw_nu->v4();
                auto tw_le_v4 = tw_le->v4();

                float dr1 = deltaR(top_b.v4(), tw_nu_v4);
                float dr2 = deltaR(top_b.v4(), tw_le_v4);
                float dr3 = deltaR(tw_le_v4, tw_nu_v4);
                if (dr1 > dr2 && dr1 > dr3) {
                    topProdMaxDr->Fill(dr1, w);
                } else if (dr2 > dr3) {
                    topProdMaxDr->Fill(dr2, w);
                } else {
                    topProdMaxDr->Fill(dr3, w);
                }
                topProdDrBToNeutrino->Fill(dr1, w);
                topProdDrBToLepton->Fill(dr2, w);
                topProdDrLeptonToNeutrino->Fill(dr3, w);

                float dphi1 = deltaPhi(top_b.v4(), tw_nu_v4);
                float dphi2 = deltaPhi(top_b.v4(), tw_le_v4);
                float dphi3 = deltaPhi(tw_le_v4, tw_nu_v4);
                if (dphi1 > dphi2 && dphi1 > dphi3) {
                    topProdMaxDPhi->Fill(dphi1, w);
                } else if (dphi2 > dphi3) {
                    topProdMaxDPhi->Fill(dphi2, w);
                } else {
                    topProdMaxDPhi->Fill(dphi3, w);
                }
                topProdDPhiBToNeutrino->Fill(dphi1, w);
                topProdDPhiBToLepton->Fill(dphi2, w);
                topProdDPhiLeptonToNeutrino->Fill(dphi3, w);
            }
        }
        higgKinematic->Fill(higg.pt(), higg.eta(), w);
        if (higg.daughter(gps, 1)) {
            higgProdKinematic->Fill(higg.daughter(gps, 1)->pt(), higg.daughter(gps, 1)->eta(), w);
            higgProdPdgId->Fill(to_string(abs(higg.daughter(gps, 1)->pdgId())).c_str(), w);
        }
        if (higg.daughter(gps, 1) && higg.daughter(gps, 2)) {
            higgProdKinematic->Fill(higg.daughter(gps, 2)->pt(), higg.daughter(gps, 2)->eta(), w);
            higgProdDr->Fill(deltaR(higg.daughter(gps, 1)->v4(),
                                    higg.daughter(gps, 2)->v4()), w);
            higgProdDPhi->Fill(deltaPhi(higg.daughter(gps, 1)->v4(),
                                        higg.daughter(gps, 2)->v4()), w);
        }
    }

private:
    TH1F * higgTopDr;
    TH1F * higgTopDPhi;
    TH2F * tPrimeKinematic;
    TH2F * fwJetKinematic;
    TH1F * fwPartonPdgId;
    TH2F * higgKinematic;
    TH2F * higgProdKinematic;
    TH1F * higgProdPdgId;
    TH1F * higgProdDr;
    TH1F * higgProdDPhi;
    TH2F * topKinematic;
    TH2F * topWKinematic;
    TH2F * topBKinematic;
    TH1F * topWProdCharge;
    TH2F * topWProdKinematic;
    TH1F * topProdMaxDr;
    TH1F * topProdMaxDPhi;
    TH1F * topProdDrBToLepton;
    TH1F * topProdDrBToNeutrino;
    TH1F * topProdDrLeptonToNeutrino;
    TH1F * topProdDPhiBToLepton;
    TH1F * topProdDPhiBToNeutrino;
    TH1F * topProdDPhiLeptonToNeutrino;
};  // class VLQ2HTGenHists
