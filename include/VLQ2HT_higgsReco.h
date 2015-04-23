#pragma once

#include <map>
#include <vector>
#include <string>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Utils.h"
#include "UHH2/core/include/Particle.h"
#include "UHH2/common/include/TTbarReconstruction.h"


using namespace uhh2;
using namespace std;


class HiggsRecoHyp {
public:
    HiggsRecoHyp(const LorentzVector & h_v4,
                 const vector<TopJet> & hjs = vector<TopJet>(),
                 const vector<Jet> & js = vector<Jet>()):
         higgs_v4(h_v4),
         higgs_jets(hjs),
         jets(js) {}
    LorentzVector       higgs_v4;
    vector<TopJet>      higgs_jets;
    vector<Jet>         jets;
    map<string, float>  discriminators;
};


class HiggsHypProducer: public AnalysisModule {
public:
    explicit HiggsHypProducer(Context & ctx, const string & label="HiggsHyps"):
       h_recohyps(ctx.get_handle<vector<HiggsRecoHyp>>(label)),
       h_h_jets(ctx.get_handle<vector<TopJet>>("h_jets")),
       h_b_jets(ctx.get_handle<vector<Jet>>("b_jets")) {}

    virtual bool process(Event & event) override {
        // boilerplate (checks and objects)
        assert(event.jets);
        const auto & b_jets = event.get(h_b_jets);
        const auto & h_jets = event.get(h_h_jets);
        if (b_jets.size() < 3 || !h_jets.size()) {
            return false;
        }
        vector<HiggsRecoHyp> reco_hyps;

        if (h_jets.size()) {
            // first option: from higgs-tagged jets
            for (const auto & hj : h_jets) {
                reco_hyps.emplace_back(
                    hj.v4(),
                    vector<TopJet>({hj})
                );
            }
        } else {
            // else try combos from b-jets
            for (const auto & bj1 : b_jets) {
                for (const auto & bj2 : b_jets) {
                    if (deltaR(bj1, bj2) < 0.1) {
                        continue;
                    }
                    LorentzVector higgs_v4 = bj1.v4() + bj2.v4();
                    reco_hyps.emplace_back(
                        higgs_v4,
                        vector<TopJet>(),
                        vector<Jet>({bj1, bj2})
                    );
                    for (const auto & j : *event.jets) {
                        if (deltaR(j, bj1) < 0.1 || deltaR(j, bj2) < 0.1 ) {
                            continue;
                        }
                        LorentzVector higgs_j_v4 = higgs_v4 + j.v4();
                        reco_hyps.emplace_back(
                            higgs_j_v4,
                            vector<TopJet>(),
                            vector<Jet>({bj1, bj2, j})
                        );
                    }
                }
            }
        }

        event.set(h_recohyps, reco_hyps);
        return true;
    }

private:
    Event::Handle<vector<HiggsRecoHyp>> h_recohyps;
    Event::Handle<vector<TopJet>> h_h_jets;
    Event::Handle<vector<Jet>> h_b_jets;
};  // HiggsHypProducer

