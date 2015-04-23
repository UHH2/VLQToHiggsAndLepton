#pragma once

#include <vector>
#include <string>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Particle.h"
#include "UHH2/core/include/Utils.h"


using namespace uhh2;
using namespace std;


class VlqReco: public AnalysisModule {
public:
    VlqReco(Context & ctx):
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),
        h_vlq(ctx.get_handle<LorentzVector>("vlq")),
        h_dr_higg_top(ctx.get_handle<float>("dr_higg_top"))
    {}

    virtual bool process(Event & event) override {
        if (!(event.is_valid(h_top_lep) && event.is_valid(h_higgs))) {
            return false;
        }
        const auto & higgs = event.get(h_higgs);
        const auto & top_lep = event.get(h_top_lep);

        LorentzVector vlq_v4 = top_lep + higgs;
        event.set(h_vlq, vlq_v4);
        event.set(h_dr_higg_top, deltaR(top_lep, higgs));

        return true;
    }

private:
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;
    Event::Handle<LorentzVector> h_vlq;
    Event::Handle<float> h_dr_higg_top;
};
