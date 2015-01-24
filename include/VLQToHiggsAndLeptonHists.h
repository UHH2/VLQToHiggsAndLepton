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
            100, 0., 10.
        )),
        fwJetKinematic(book<TH2F>(
            "fwJetKinematic",
            ";forward parton p_{T};forward parton #eta",
            100, 0, 1000,
            100, 0., 10.
        )),
        higgKinematic(book<TH2F>(
            "higgKinematic",
            ";H p_{T};H #eta",
            100, 0, 1000,
            100, 0., 10.
        )),
        // HProdDeltaR(book<TH1F>(
        //     "HProdDeltaR",
        //     ";#DeltaR(X,X) from H->XX;events",
        //     100, 0., 5.
        // ))
        topKinematic(book<TH2F>(
            "topKinematic",
            ";top quark p_{T};top quark #eta",
            100, 0, 1000,
            100, 0., 10.
        ))  // ,
        // leptonKinematic(book<TH2F>(
        //     "leptonKinematic",
        //     ";lepton p_{T};lepton #eta",
        //     100, 0, 1000,
        //     100, 0., 10.
        // )),
        {}

    virtual void fill(const uhh2::Event & e) override {
        const auto & gps = e.genparticles;
        float w = e.weight;

        // find tprime mom
        GenParticle tprime,
                    fwd_parton,
                    higg,
                    top;
                    // top_w,
                    // top_b,
                    // lepton;
        for (const auto &gp : *gps) {
            auto d1 = gp.daughter(gps,1);
            auto d2 = gp.daughter(gps,2);
            if (d1 && abs(d1->pdgId()) == 6000006) {
                tprime = *d1;
                fwd_parton = *d2;
                break;
            }
            else if (d2 && abs(d2->pdgId()) == 6000006) {
                tprime = *d2;
                fwd_parton = *d1;
                break;
            }
        }
        auto d1 = tprime.daughter(gps,1);
        auto d2 = tprime.daughter(gps,2);
        if (d1 && abs(d1->pdgId()) == 6) {
            top = *d1;
            higg = *d2;
        }
        else if (d2 && abs(d2->pdgId()) == 6) {
            top = *d2;
            higg = *d1;
        }
        if (tprime.pdgId())
            tPrimeKinematic->Fill(tprime.pt(), fabs(tprime.eta()), w);
        if (fwd_parton.pdgId())
            fwJetKinematic->Fill(fwd_parton.pt(), fabs(fwd_parton.eta()), w);
        if (top.pdgId())
            topKinematic->Fill(top.pt(), fabs(top.eta()), w);
        if (higg.pdgId())
            higgKinematic->Fill(higg.pt(), fabs(higg.eta()), w);

    }

private:
    TH2F * tPrimeKinematic;
    TH2F * fwJetKinematic;
    TH2F * higgKinematic;
    // TH1F * HProdDeltaR;
    TH2F * topKinematic;
    // TH2F * leptonKinematic;
};  // class GenHists


namespace vlq2hl_hist {
using namespace uhh2;

class Trigger: public Hists {
public:
    Trigger(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        h(book<TH1F>("trigger", ";ele+Jets OR mu+Jets;events", 2, -.5, 1.5)) {}

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
        h(book<TH1F>("N_jets", ";N_{jet};events", 21, -.5, 20.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.jets->size(), e.weight);
    }

private:
    TH1F * h;
};  // class NJets

class NBTags: public Hists {
public:
    NBTags(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        hndl(ctx.get_handle<int>("n_btags")),
        h(book<TH1F>("N_btags", ";N_{b-tag};events", 11, -.5, 10.5)) {}

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
        h(book<TH1F>("N_fwd_jets", ";N_{fwd jet};events", 11, -.5, 10.5)) {}

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
        h(book<TH1F>("N_leptons", ";N_{lepton};events", 11, -.5, 10.5)) {}

    virtual void fill(const uhh2::Event & e) override {
        h->Fill(e.electrons->size() + e.muons->size(), e.weight);
    }

private:
    TH1F * h;
};  // class NLeptons


}