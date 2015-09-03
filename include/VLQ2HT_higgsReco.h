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
        const auto & h_jets = event.is_valid(h_h_jets) ? event.get(h_h_jets) : vector<TopJet>();
        if (b_jets.size() < 2 && !h_jets.size()) {
            return false;
        }
        vector<HiggsRecoHyp> reco_hyps;

        if (h_jets.size()) {
            // first option: from higgs-tagged jets
            
            for (const auto & hj : h_jets) {
                LorentzVector hj_v4;
                for (const auto & sub_j : hj.subjets()) {
                    hj_v4 += sub_j.v4();
                }
                reco_hyps.emplace_back(
                    hj_v4,
                    vector<TopJet>({hj}),
                    hj.subjets()
                );
            }
        } else {
            // else try combos from b-jets

            for (unsigned i1 = 0; i1 < b_jets.size() - 1; i1++) {
                const auto &bj1 = b_jets[i1];

                for (unsigned i2 = i1 + 1; i2 < b_jets.size(); i2++) {
                    const auto &bj2 = b_jets[i2];

                    LorentzVector higgs_v4 = bj1.v4() + bj2.v4();
                    reco_hyps.emplace_back(
                        higgs_v4,
                        vector<TopJet>(),
                        vector<Jet>({bj1, bj2})
                    );
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

