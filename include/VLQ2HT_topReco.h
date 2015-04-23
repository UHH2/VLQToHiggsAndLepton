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


namespace {

// invariant mass of a lorentzVector, but save for timelike / spacelike vectors
float inv_mass(const LorentzVector & p4){
    if(p4.isTimelike()){
            return p4.mass();
    }
    else{
        return -sqrt(-p4.mass2());
    }
}

}

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
                LorentzVector toplep_v4 = wlep_v4;
                toplep_v4 += b_jet.v4();

                // push new hyp
                reco_hyps.emplace_back();
                auto & hyp = reco_hyps.back();
                hyp.toplep_v4 = toplep_v4;
                hyp.blep_v4 = b_jet.v4();
                hyp.lepton = lepton;
                hyp.neutrino_v4 = neutrino_p4;

                // up to one radiated jet
                for (const auto & jet : *event.jets) {
                    if (deltaR(jet, b_jet) < 1e-3) {
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


const TopLeptRecoHyp * get_best_hypothesis(
    const vector<TopLeptRecoHyp> & hyps,
    const string & label,
    float & chi2)
{
    const TopLeptRecoHyp * best = nullptr;
    float current_best_disc = numeric_limits<float>::infinity();
    for(const auto & hyp : hyps){
        if(!hyp.discriminators.count(label)) continue;
        float disc = hyp.discriminators.find(label)->second;
        if(disc < current_best_disc){
            best = &hyp;
            current_best_disc = disc;
        }
    }
    chi2 = current_best_disc;
    return best;  // note: might be nullptr
}


class TopLepChi2Discr: public uhh2::AnalysisModule {
public:
    TopLepChi2Discr(uhh2::Context & ctx,
                      const std::string & rechyps_name):
        h_hyps(ctx.get_handle<vector<TopLeptRecoHyp>>(rechyps_name)),
        h_top_lep_chi2(ctx.get_handle<float>("tlep_chi2")),
        h_top_lep_mass(ctx.get_handle<float>("tlep_mass")),
        h_top_lep_pt(ctx.get_handle<float>("tlep_pt")),
        h_top_lep_eta(ctx.get_handle<float>("tlep_eta")) {}

    virtual bool process(uhh2::Event & event) override {
        if (event.is_valid(h_hyps)) {
            auto & hyps = event.get(h_hyps);
            const double mass_tlep = 174;
            const double mass_tlep_sigma = 18;
            for(auto & hyp: hyps){
                double mass_tlep_rec = inv_mass(hyp.toplep_v4);
                double chi2_tlep = pow((mass_tlep_rec - mass_tlep) / mass_tlep_sigma, 2);
                hyp.discriminators["Chi2_tlep"] = chi2_tlep;
            }

            float chi2;
            auto best_hyp = get_best_hypothesis(hyps, "Chi2_tlep", chi2);
            if (best_hyp) {
                event.set(h_top_lep_chi2, chi2);
                event.set(h_top_lep_mass, inv_mass(best_hyp->toplep_v4));
                event.set(h_top_lep_pt, best_hyp->toplep_v4.pt());
                event.set(h_top_lep_eta, best_hyp->toplep_v4.eta());
                return true;
            }
        }
        return false;
    }

private:
    uhh2::Event::Handle<std::vector<TopLeptRecoHyp>> h_hyps;
    uhh2::Event::Handle<float> h_top_lep_chi2;
    uhh2::Event::Handle<float> h_top_lep_mass;
    uhh2::Event::Handle<float> h_top_lep_pt;
    uhh2::Event::Handle<float> h_top_lep_eta;
};