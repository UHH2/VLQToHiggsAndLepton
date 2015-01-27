#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "TH1F.h"
#include "TH2F.h"

/**  \brief Example class for booking and filling histograms
 * 
 * NOTE: This class uses the 'hist' method to retrieve histograms.
 * This requires a string lookup and is therefore slow if you have
 * many histograms. Therefore, it is recommended to use histogram
 * pointers as member data instead, like in 'common/include/ElectronHists.h'.
 */
class VLQToHiggsAndLeptonHists: public uhh2::Hists {
public:
    // use the same constructor arguments as Hists for forwarding:
    VLQToHiggsAndLeptonHists(uhh2::Context & ctx, const std::string & dirname);

    virtual void fill(const uhh2::Event & ev) override;
    virtual ~VLQToHiggsAndLeptonHists();

private:
    uhh2::Event::Handle<std::vector<Jet> > fwd_jets_h;
};

using namespace uhh2;

class GenHists: public Hists {
public:
    GenHists(Context & ctx, const std::string & dir):
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
            auto d1 = gp.daughter(gps,1);
            auto d2 = gp.daughter(gps,2);
            if (d1 && abs(d1->pdgId()) < 6000009 && abs(d1->pdgId()) > 6000003) {
                tprime = *d1;
                fwd_parton = *d2;
                break;
            }
            else if (d2 && abs(d2->pdgId()) < 6000009 && abs(d2->pdgId()) > 6000003) {
                tprime = *d2;
                fwd_parton = *d1;
                break;
            }
        }
        if (!tprime.pdgId()) {
            std::cout << "Missing T' particle. Skipping Event." << std::endl;
            return;
        }
        auto d1 = tprime.daughter(gps,1);
        auto d2 = tprime.daughter(gps,2);
        if (d1 && abs(d1->pdgId()) == 6) {
            top = *d1;
            higg = *d2;
        } else {
            top = *d2;
            higg = *d1;
        }
        auto d3 = top.daughter(gps,1);
        auto d4 = top.daughter(gps,2);
        if (d3 && d4) {
            if (abs(d3->pdgId()) == 5) {
                top_b = *d3;
                top_w = *d4;
            } else {
                top_b = *d4;
                top_w = *d3;
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
    }

private:
    TH2F * tPrimeKinematic;
    TH2F * fwJetKinematic;
    TH2F * higgKinematic;
    TH2F * higgProdKinematic;
    TH1F * higgProdPdgId;
    TH2F * topKinematic;
    TH2F * topWKinematic;
    TH2F * topBKinematic;
    TH2F * topWProdKinematic;
};  // class GenHists


namespace vlq2hl_hist {
using namespace uhh2;

class Trigger: public Hists {
public:
    Trigger(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("Trigger", ";ele+Jets OR mu+Jets;events", 2, -.5, 1.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        auto ele_trig = e.get_trigger_index("HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*");
        auto mu_trig = e.get_trigger_index("HLT_Mu40_eta2p1_PFJet200_PFJet50_v*");
        h->Fill(e.passes_trigger(ele_trig) || e.passes_trigger(mu_trig), e.weight);
    }

private:
    TH1F * h;
};  // class Trigger

class NJets: public Hists {
public:
    NJets(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("NJets", ";N_{jet};events", 21, -.5, 20.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.jets->size(), e.weight);
    }

private:
    TH1F * h;
};  // class NJets

class LeadingJetPt: public Hists {
public:
    LeadingJetPt(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("LeadingJetPt","leading jet p_{T}",50,100,1500)) {}

    virtual void fill(const uhh2::Event & e) override {
        if (e.jets->size() > 0) {
            h->Fill(e.jets->at(0).pt(), e.weight);
        }
    }

private:
    TH1F * h;
};  // class LeadingJetPt

class SubLeadingJetPt: public Hists {
public:
    SubLeadingJetPt(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("SubLeadingJetPt","sub-leading jet p_{T}",50,100,1500)) {}

    virtual void fill(const uhh2::Event & e) override {
        if (e.jets->size() > 1) {
            h->Fill(e.jets->at(1).pt(), e.weight);
        }
    }

private:
    TH1F * h;
};  // class SubLeadingJetPt

class NBTags: public Hists {
public:
    NBTags(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        hndl(ctx.get_handle<int>("n_btags")),
        h(book<TH1F>("NBTags", ";N_{b-tag};events", 11, -.5, 10.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.get(hndl), e.weight);
    }

private:
    Event::Handle<int> hndl;
    TH1F * h;
};  // class NBTags

class NFwdJets: public Hists {
public:
    NFwdJets(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        hndl(ctx.get_handle<std::vector<Jet> >("fwd_jets")),
        h(book<TH1F>("NFwdJets", ";N_{fwd jet};events", 11, -.5, 10.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.get(hndl).size(), e.weight);
    }

private:
    Event::Handle<std::vector<Jet> > hndl;
    TH1F * h;
};  // class NFwdJets

class NLeptons: public Hists {
public:
    NLeptons(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("NLeptons", ";N_{lepton};events", 11, -.5, 10.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.electrons->size() + e.muons->size(), e.weight);
    }

private:
    TH1F * h;
};  // class NLeptons

class LeptonPt: public Hists {
public:
    LeptonPt(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h_ele(book<TH1F>("LeptonPtELE","lepton p_{T} (electron)",50,0,500)),
        h_mu(book<TH1F>("LeptonPtMUO","lepton p_{T} (muon)",50,0,500)) {}

    virtual void fill(const uhh2::Event & e) override {
        if (e.electrons->size()) {
            h_ele->Fill(e.electrons->at(0).pt(), e.weight);
        }
        if (e.muons->size()) {
            h_mu->Fill(e.muons->at(0).pt(), e.weight);
        }
    }

private:
    TH1F * h_ele;
    TH1F * h_mu;
};  // class LeptonPt

}
