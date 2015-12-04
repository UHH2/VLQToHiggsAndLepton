#pragma once

#include "UHH2/common/include/Utils.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_topReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_higgsReco.h"


class EventHypDiscr: public AnalysisModule {
private:
    // input
    Event::Handle<vector<TopLeptRecoHyp>> h_t_hyps;
    Event::Handle<vector<HiggsRecoHyp>> h_h_hyps;

    // output
    Event::Handle<LorentzVector> h_higgs;
    Event::Handle<LorentzVector> h_top_lep;
    Event::Handle<float> h_event_chi2;
    Event::Handle<vector<Jet>> h_subjets;
    Event::Handle<float> h_higgs_tau21;
    Event::Handle<float> h_higgs_tau32;

public:
    EventHypDiscr(Context & ctx,
                    const string & tophyps_name,
                    const string & higgshyps_name):
        h_t_hyps(ctx.get_handle<vector<TopLeptRecoHyp>>(tophyps_name)),
        h_h_hyps(ctx.get_handle<vector<HiggsRecoHyp>>(higgshyps_name)),
        h_higgs(ctx.get_handle<LorentzVector>("h")),
        h_top_lep(ctx.get_handle<LorentzVector>("tlep")),
        h_event_chi2(ctx.get_handle<float>("event_chi2")),
        h_subjets(ctx.get_handle<vector<Jet>>("h_subjets")),
        h_higgs_tau21(ctx.get_handle<float>("h_tau21")),
        h_higgs_tau32(ctx.get_handle<float>("h_tau32")) {}

    virtual bool process(Event & event) override {
        event.set(h_subjets, vector<Jet>());

        if (!event.is_valid(h_h_hyps)) {
            return false;
        }
        auto & h_hyps = event.get(h_h_hyps);
        if (!h_hyps.size()) {
            return false;
        }
        if (!event.is_valid(h_t_hyps)) {
            return false;
        }
        auto & t_hyps = event.get(h_t_hyps);
        if (!t_hyps.size()) {
            return false;
        }
        const float mass_tlep = 174;
        const float mass_tlep_sigma = 14.5 ;
        const float mass_higgs = 125;
        const float mass_higgs_sigma = 14.5;  // copied from tlep
        const float dr_higg_top = 3.15;
        const float dr_higg_top_sigma = 0.098 * 2; // factor of 2 less importance

        // generate mass chi2: top
        for(auto & hyp: t_hyps) {
            float mass_rec = inv_mass_safe(hyp.toplep_v4);
            float chi2_tlep = pow((mass_rec - mass_tlep) / mass_tlep_sigma, 2);
            hyp.discriminators["Chi2_tlep"] = chi2_tlep;
        }

        // generate mass chi2: higgs
        for(auto & hyp: h_hyps) {
            float mass_rec = inv_mass_safe(hyp.higgs_v4);
            float chi2_higgs = pow((mass_rec - mass_higgs) / mass_higgs_sigma, 2);
            hyp.discriminators["Chi2_higgs"] = chi2_higgs;
        }

        // make combined chi2
        for(auto & h_hyp: h_hyps) {
            for(auto & t_hyp: t_hyps) {
                float dr_rec = deltaR(h_hyp.higgs_v4, t_hyp.toplep_v4);
                float chi2_dr = pow((dr_rec - dr_higg_top) / dr_higg_top_sigma, 2);
                float chi2 = chi2_dr
                           + t_hyp.discriminators["Chi2_tlep"]
                           + h_hyp.discriminators["Chi2_higgs"];
                t_hyp.discriminators["Chi2_event"] = chi2;
                h_hyp.discriminators["Chi2_event"] = chi2;
            }
        }

        // find best hyps and store
        float chi2 = 999999.;
        auto best_h_hyp = get_best_hypothesis(h_hyps, "Chi2_event", chi2);
        auto best_t_hyp = get_best_hypothesis(t_hyps, "Chi2_event", chi2);
        if (best_h_hyp) {
            event.set(h_higgs, best_h_hyp->higgs_v4);
            if (best_h_hyp->higgs_jets.size()) {
                auto j = best_h_hyp->higgs_jets[0];
                event.set(h_subjets, j.subjets());
                event.set(h_higgs_tau21, j.tau2() / j.tau1());
                event.set(h_higgs_tau32, j.tau3() / j.tau2());
            }
        }
        if (best_t_hyp) {
            event.set(h_top_lep, best_t_hyp->toplep_v4);
        }
        event.set(h_event_chi2, chi2);
        return true;
    }
};