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
    explicit NBTags(Context &ctx,
                    int nmin_,
                    int nmax_ = -1):
        hndl(ctx.get_handle<int>("n_btags")), nmin(nmin_), nmax(nmax_) {}

    virtual bool passes(const Event & event) override {
        int nbtag = event.get(hndl);
        return nbtag >= nmin && (nmax < 0 || nbtag <= nmax);
    }

private:
    Event::Handle<int> hndl;
    int nmin, nmax;
};

class OneFwdJet: public Selection {
public:
    explicit OneFwdJet(Context & ctx):
        hndl(ctx.get_handle<std::vector<Jet> >("fwd_jets")) {}

    bool passes(const Event & e) override {
        return e.get(hndl).size() > 0;
    }

private:
    Event::Handle<std::vector<Jet> > hndl;
};

}