#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "TH1F.h"

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

namespace vlq2hl_hist {
using namespace uhh2;

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