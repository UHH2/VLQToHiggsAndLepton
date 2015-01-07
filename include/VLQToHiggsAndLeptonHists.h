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
        h(book<TH1F>("N_jets", "N_{jet}", 21, -.5, 20.5)) {}

    virtual void fill(const uhh2::Event & event) override {
        h->Fill(event.jets->size(), event.weight);
    }

private:
    TH1F * h;
};

class NBTags: public Hists {
public:
    NBTags(Context & ctx, const std::string & dir):
        Hists(ctx, dir),
        hndl(ctx.get_handle<int>("n_btags")),
        h(book<TH1F>("N_btags", "N_{b-tag}", 11, -.5, 10.5)) {}

    virtual void fill(const uhh2::Event & event) override {
        h->Fill(event.get(hndl), event.weight);
    }

private:
    Event::Handle<int> hndl;
    TH1F * h;
};

}