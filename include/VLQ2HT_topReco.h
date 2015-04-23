#pragma once

#include <map>
#include <vector>
#include <string>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Utils.h"
#include "UHH2/core/include/Particle.h"
#include "UHH2/common/include/TTbarReconstruction.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"

using namespace uhh2;
using namespace std;


class TopLeptRecoHyp {
public:
    LorentzVector       blep_v4;
    LorentzVector       neutrino_v4;
    LorentzVector       toplep_v4;
    Particle            lepton;
    vector<Particle>    toplep_jets;
    map<string, float>  discriminators;
};


class TopLepHypProducer: public AnalysisModule {
public:
    explicit TopLepHypProducer(Context & ctx,
                       const NeutrinoReconstructionMethod & neutrinofunc,
                       const string & label="LeptTopHyps"):
       neutrinofunc_(neutrinofunc),
       h_recohyps(ctx.get_handle<vector<TopLeptRecoHyp>>(label)),
       h_b_jets(ctx.get_handle<vector<Jet>>("b_jets")),
       h_primlep(ctx.get_handle<FlavorParticle>("PrimaryLepton")) {}

    virtual bool process(Event & event) override {

        // boilerplate (checks and objects)
        assert(event.jets);
        assert(event.met);
        const auto & b_jets = event.get(h_b_jets);
        if (!b_jets.size()) {
            return false;
        }
        if (!event.is_valid(h_primlep)) {
            return false;
        }
        const Particle & lepton = event.get(h_primlep);
        vector<LorentzVector> neutrino_hyps = neutrinofunc_(lepton.v4(), event.met->v4());

        // make all combinations
        vector<TopLeptRecoHyp> reco_hyps;
        for(const auto & neutrino_p4 : neutrino_hyps) {
            const LorentzVector wlep_v4 = lepton.v4() + neutrino_p4;
            for (const auto & b_jet : b_jets) {
                LorentzVector toplep_v4 = wlep_v4 + b_jet.v4();

                // push new hyp
                reco_hyps.emplace_back();
                auto & hyp = reco_hyps.back();
                hyp.toplep_v4 = toplep_v4;
                hyp.blep_v4 = b_jet.v4();
                hyp.lepton = lepton;
                hyp.neutrino_v4 = neutrino_p4;

                // up to one radiated jet
                for (const auto & jet : *event.jets) {
                    if (deltaR(jet, b_jet) < 0.1) {
                        continue;
                    }
                    LorentzVector toplep_j_v4 = toplep_v4 + jet.v4();

                    // push new hyp
                    TopLeptRecoHyp hyp;
                    hyp.toplep_v4 = toplep_j_v4;
                    hyp.blep_v4 = b_jet.v4();
                    hyp.lepton = lepton;
                    hyp.neutrino_v4 = neutrino_p4;
                    hyp.toplep_jets.push_back(jet);
                    reco_hyps.push_back(hyp);

                    for (const auto & jet2 : *event.jets) {
                        if (deltaR(jet2, b_jet) < 0.1 || deltaR(jet2, jet) < 0.1 ) {
                            continue;
                        }
                        LorentzVector toplep_j_j_v4 = toplep_j_v4 + jet2.v4();

                        // push new hyp
                        TopLeptRecoHyp hyp;
                        hyp.toplep_v4 = toplep_j_j_v4;
                        hyp.blep_v4 = b_jet.v4();
                        hyp.lepton = lepton;
                        hyp.neutrino_v4 = neutrino_p4;
                        hyp.toplep_jets.push_back(jet);
                        hyp.toplep_jets.push_back(jet2);
                        reco_hyps.push_back(hyp);
                    }
                }
            }
        }
        event.set(h_recohyps, reco_hyps);
        return true;
    }

private:
    NeutrinoReconstructionMethod neutrinofunc_;
    Event::Handle<vector<TopLeptRecoHyp>> h_recohyps;
    Event::Handle<vector<Jet>> h_b_jets;
    Event::Handle<FlavorParticle> h_primlep;
};  // TopLepHypProducer


class TopLepChi2Discr: public AnalysisModule {
public:
    TopLepChi2Discr(Context & ctx,
                    const string & rechyps_name):
        h_hyps(ctx.get_handle<vector<TopLeptRecoHyp>>(rechyps_name)),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),
        h_top_lep_chi2(ctx.get_handle<float>("tlep_chi2")) {}

    virtual bool process(Event & event) override {
        if (!event.is_valid(h_hyps)) {
            return false;
        }

        auto & hyps = event.get(h_hyps);
        const float mass_tlep = 174;
        const float mass_tlep_sigma = 18;
        for(auto & hyp: hyps){
            float mass_tlep_rec = inv_mass_save(hyp.toplep_v4);
            float chi2_tlep = pow((mass_tlep_rec - mass_tlep) / mass_tlep_sigma, 2);
            hyp.discriminators["Chi2_tlep"] = chi2_tlep;
        }

        float chi2;
        auto best_hyp = get_best_hypothesis(hyps, "Chi2_tlep", chi2);
        if (best_hyp) {
            event.set(h_top_lep, best_hyp->toplep_v4);
            event.set(h_top_lep_chi2, chi2);
            return true;
        }
        return false;
    }

private:
    Event::Handle<vector<TopLeptRecoHyp>> h_hyps;
    Event::Handle<LorentzVector> h_top_lep;
    Event::Handle<float> h_top_lep_chi2;
};