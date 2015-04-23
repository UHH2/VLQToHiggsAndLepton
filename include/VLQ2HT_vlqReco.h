#pragma once

#include <vector>
#include <string>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Particle.h"


using namespace uhh2;
using namespace std;


class VlqReco: public AnalysisModule {
public:
    VlqReco(Context & ctx):
        h_h_jets(ctx.get_handle<vector<TopJet>>("h_jets")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),
        h_vlq_mass(ctx.get_handle<float>("vlq_mass")),
        h_vlq_pt(ctx.get_handle<float>("vlq_pt")),
        h_vlq_eta(ctx.get_handle<float>("vlq_eta")) {}

    virtual bool process(Event & event) override {
        const auto & h_jets = event.get(h_h_jets);
        if (!(event.is_valid(h_top_lep) && h_jets.size())) {
            return false;
        }

        LorentzVector vlq_v4 = event.get(h_top_lep) + h_jets[0].v4();
        event.set(h_vlq_mass, inv_mass(vlq_v4));
        event.set(h_vlq_pt, vlq_v4.pt());
        event.set(h_vlq_eta, vlq_v4.eta());
        return true;
    }

private:
    Event::Handle<vector<TopJet>> h_h_jets;
    Event::Handle<LorentzVector> h_top_lep;
    Event::Handle<float> h_vlq_mass;
    Event::Handle<float> h_vlq_pt;
    Event::Handle<float> h_vlq_eta;
};
