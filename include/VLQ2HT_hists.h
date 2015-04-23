#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Utils.h"
#include "TH1F.h"
#include "TH2F.h"


using namespace uhh2;


template<class HANDLETYPE>
class HandleHist: public uhh2::Hists {
public:
    template<class... TARGS>
    explicit HandleHist(uhh2::Context & ctx,
                        const std::string & dirname,
                        const std::string & handlename,
                        TARGS... args):
        uhh2::Hists(ctx, dirname),
        hndl(ctx.get_handle<HANDLETYPE>(handlename)) {
            hist=book<TH1F>(handlename.c_str(), args...);
        }

    virtual void fill(const uhh2::Event & e) override {
        if (e.is_valid(hndl)) {
            hist->Fill(e.get(hndl), e.weight);
        }
    }

private:
    uhh2::Event::Handle<HANDLETYPE> hndl;
    TH1F * hist;
};


class SingleLepTrigHists: public Hists {
public:
    SingleLepTrigHists(Context & ctx,
                  const std::string & dir,
                  const std::string & trig_path,
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
    const std::string trig_path_;
    bool is_ele_;
    TH1F * eff_sub_;
    TH1F * eff_tot_;
};  // class SingleLepTrigHists


namespace vlq2hl_hist {
using namespace uhh2;

class Trigger: public HandleHist<int> {
public:
    Trigger(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "trigger_accept", ";ele+Jets OR mu+Jets;events", 2, -.5, 1.5) {}
};

class NJets: public HandleHist<int> {
public:
    NJets(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_jets", ";N_{jet};events", 21, -.5, 20.5) {}
};

class NLeptons: public HandleHist<int> {
public:
    NLeptons(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_leptons", ";N_{lepton};events", 11, -.5, 10.5) {}
};

class NFwdJets: public HandleHist<int> {
public:
    NFwdJets(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_fwd_jets", ";N_{fwd jet};events", 11, -.5, 10.5) {}
};

class NBTags: public HandleHist<int> {
public:
    NBTags(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_btags", ";N_{b-tag};events", 11, -.5, 10.5) {}
};

class NLeadingBTags: public HandleHist<int> {
public:
    NLeadingBTags(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_leading_btags", ";N_{b-tag leading};events", 11, -.5, 10.5) {}
};

class NHTags: public HandleHist<int> {
public:
    NHTags(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "n_higgs_tags", ";N_{H jet};events", 11, -.5, 10.5) {}
};

class LeadingJetPt: public HandleHist<float> {
public:
    LeadingJetPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "leading_jet_pt","leading jet p_{T}",50,100,1500) {}
};

class SubLeadingJetPt: public HandleHist<float> {
public:
    SubLeadingJetPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "subleading_jet_pt","sub-leading jet p_{T}",50,100,1500) {}
};

class PrimaryLeptonPt: public HandleHist<float> {
public:
    PrimaryLeptonPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "primary_lepton_pt","primary lepton p_{T}",50,100,1500) {}
};

class ST: public HandleHist<double> {
public:
    ST(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "ST", ";ST;events", 100, 0, 5000) {}
};


class EventChi2: public HandleHist<float> {
public:
    EventChi2(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "event_chi2","event chi2",50,0,100) {}
};

class DrHiggTop: public HandleHist<float> {
public:
    DrHiggTop(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "dr_higg_top","#DeltaR(H, t)",50,0,5) {}
};

class TopLepPt: public HandleHist<float> {
public:
    TopLepPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "tlep_pt","lept. top p_{T}",50,0,1000) {}
};

class TopLepEta: public HandleHist<float> {
public:
    TopLepEta(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "tlep_eta","lept. top #eta",50,-5.,5.) {}
};

class TopLepMass: public HandleHist<float> {
public:
    TopLepMass(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "tlep_mass","lept. top mass",50,0,1000) {}
};

class VlqPt: public HandleHist<float> {
public:
    VlqPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "vlq_pt","VLQ p_{T}",50,0,1000) {}
};

class VlqEta: public HandleHist<float> {
public:
    VlqEta(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "vlq_eta","VLQ #eta",50,-5.,5.) {}
};

class VlqMass: public HandleHist<float> {
public:
    VlqMass(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "vlq_mass","VLQ mass",50,0,2000) {}
};

class HiggsPt: public HandleHist<float> {
public:
    HiggsPt(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "h_pt","Higgs p_{T}",50,0,1000) {}
};

class HiggsEta: public HandleHist<float> {
public:
    HiggsEta(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "h_eta","Higgs #eta",50,-5.,5.) {}
};

class HiggsMass: public HandleHist<float> {
public:
    HiggsMass(Context & ctx, const std::string & dir):
        HandleHist(ctx, dir, "h_mass","Higgs mass",50,0,1000) {}
};


}


class VLQ2HTRecoGenComparison: public Hists {
public:
    VLQ2HTRecoGenComparison(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),

        tophigggenDR(book<TH1F>(
            "tophigggenDR",
            ";#DeltaR(t_{gen}, H_{gen}); events",
            100, 0, 5.
        )),
        topDRDPt(book<TH2F>(
            "topDRDPt",
            ";#DeltaR(t_{reco}, t_{gen});#DeltaP_{T, rel}(t_{reco}, t_{gen})",
            100, 0, 5.,
            100, 0., 2.
        )),
        higDRDPt(book<TH2F>(
            "higgDRDPt",
            ";#DeltaR(H_{reco}, H_{gen});#DeltaP_{T, rel}(H_{reco}, H_{gen})",
            100, 0., 5.,
            100, 0., 2.
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
    VLQ2HTGenHists(Context & ctx, const std::string & dir):
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
            higgProdPdgId->Fill(std::to_string(abs(higg.daughter(gps, 1)->pdgId())).c_str(), w);
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
