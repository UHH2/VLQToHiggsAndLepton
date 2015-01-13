#pragma once

#include "UHH2/core/include/fwd.h"
#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Selection.h"

#include <stdexcept>

namespace uhh2 {

/** \brief Various definitions of b-tagging, in particular working points
 *
 * This is useful for various selection modules, and thus defined outside of a particular Selection class.
 */
namespace btagging {
using namespace std;

enum class csv_wp {
    loose, medium, tight
};

/// convert a CSV working point to a numerical threshold of the discriminator.
float csv_threshold(const csv_wp & wp){
    using namespace btagging;
    switch(wp){
        case csv_wp::loose: return 0.244f;
        case csv_wp::medium: return 0.679f;
        case csv_wp::tight: return 0.898f;
    }
    // This should never happen; even if, the coompiler should warn in the switch.
    // But to avoid a compiler warning that no value is returned, include this line:
    throw invalid_argument("unknown working point given to btagging::csv_threshold");
}

}

}

namespace vlq2hl_sel {
using namespace uhh2;

class NBTags: public Selection {
public:
    /// In case nmax=-1, no cut on the maximum is applied.
    explicit NBTags(Context &ctx, int nmin_, int nmax_ = -1):
        hndl(ctx.get_handle<int>("n_btags")), nmin(nmin_), nmax(nmax_) {}

    virtual bool passes(const Event & event) override {
        int n = event.get(hndl);
        return n >= nmin && (nmax < 0 || n <= nmax);
    }

private:
    Event::Handle<int> hndl;
    int nmin, nmax;
};  // class NJets

class NFwdJets: public Selection {
public:
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

}