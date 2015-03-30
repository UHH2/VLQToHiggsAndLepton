#pragma once

#include "UHH2/core/include/fwd.h"
#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Selection.h"

#include <stdexcept>

namespace vlq2hl_sel {
using namespace uhh2;

class Trigger: public Selection {
public:
    explicit Trigger() {}

    bool passes(const uhh2::Event & e) override {
        // auto ele_trig = e.get_trigger_index("HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*");
        // auto mu_trig = e.get_trigger_index("HLT_Mu40_eta2p1_PFJet200_PFJet50_v*");
        auto ele_trig = e.get_trigger_index("HLT_Ele95_CaloIdVT_GsfTrkIdT_v*");
        auto mu_trig = e.get_trigger_index("HLT_Mu40_v*");
        return e.passes_trigger(ele_trig) || e.passes_trigger(mu_trig);
    }
};  // class Trigger

class JetPt: public Selection {
public:
    explicit JetPt(unsigned jet_index_, float min_pt_):
        jet_index(jet_index_),
        min_pt(min_pt_) {}

    virtual bool passes(const Event & e) override {
        return (e.jets->size() > jet_index
                && e.jets->at(jet_index).pt() > min_pt);
    }

private:
    unsigned jet_index;
    float min_pt;
};  // class JetPt

class NBTags: public Selection {
public:
    /// In case nmax=-1, no cut on the maximum is applied.
    explicit NBTags(Context &ctx, int nmin_, int nmax_ = -1):
        hndl(ctx.get_handle<int>("n_btags")), nmin(nmin_), nmax(nmax_) {}

    virtual bool passes(const Event & e) override {
        int n = e.get(hndl);
        return n >= nmin && (nmax < 0 || n <= nmax);
    }

private:
    Event::Handle<int> hndl;
    int nmin, nmax;
};  // class NBTags

class NFwdJets: public Selection {
public:
    /// In case nmax=-1, no cut on the maximum is applied.
    explicit NFwdJets(Context & ctx, int nmin_, int nmax_ = -1):
        hndl(ctx.get_handle<std::vector<Jet> >("fwd_jets")),
        nmin(nmin_), nmax(nmax_) {}

    bool passes(const Event & e) override {
        int n = e.get(hndl).size();
        return n >= nmin && (nmax < 0 || n <= nmax);
    }

private:
    Event::Handle<std::vector<Jet> > hndl;
    int nmin, nmax;
};  // class NFwdJets

class NHTags: public Selection {
public:
    /// In case nmax=-1, no cut on the maximum is applied.
    explicit NHTags(Context & ctx, int nmin_, int nmax_ = -1):
        hndl(ctx.get_handle<int>("n_higgs_tags")),
        nmin(nmin_), nmax(nmax_) {}

    bool passes(const Event & e) override {
        int n = e.get(hndl);
        return n >= nmin && (nmax < 0 || n <= nmax);
    }

private:
    Event::Handle<int> hndl;
    int nmin, nmax;
};  // class NHTags

class NLeptons: public Selection {
public:
    explicit NLeptons(int nmin_, int nmax_ = -1):
        nmin(nmin_), nmax(nmax_) {}

    bool passes(const uhh2::Event & e) override {
        int n = e.electrons->size() + e.muons->size();
        return n >= nmin && (nmax < 0 || n <= nmax);
    }

private:
    int nmin, nmax;
};  // class NLeptons

class LeptonPt: public Selection {
public:
    explicit LeptonPt(float ele_cut_, float mu_cut_):
        ele_cut(ele_cut_), mu_cut(mu_cut_) {}

    bool passes(const uhh2::Event & e) override {
        return (e.electrons->size() && e.electrons->at(0).pt() > ele_cut)
               || (e.muons->size() && e.muons->at(0).pt() > mu_cut);
    }

private:
    float ele_cut, mu_cut;
};  // class LeptonPt

}