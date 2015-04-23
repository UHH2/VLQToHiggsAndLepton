#pragma once

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

using namespace uhh2;


class TriggerAcceptProcuder : public AnalysisModule {
public:
    explicit TriggerAcceptProcuder(Context & ctx):
        h(ctx.get_handle<int>("trigger_accept")) {}

    virtual bool process(Event & e) override {
        auto ele_trig = e.get_trigger_index("HLT_Ele95_CaloIdVT_GsfTrkIdT_v*");
        auto mu_trig = e.get_trigger_index("HLT_Mu40_v*");
        if (e.passes_trigger(ele_trig) || e.passes_trigger(mu_trig)) {
            e.set(h, 1);
        } else {
            e.set(h, 0);
        };
        return true;
    }

private:
    Event::Handle<int> h;
};


class NJetsProducer: public AnalysisModule {
public:
    explicit NJetsProducer(Context & ctx):
        h(ctx.get_handle<int>("n_jets")) {}

    virtual bool process(Event & e) override {
        e.set(h, e.jets->size());
        return true;
    }

private:
    Event::Handle<int> h;
};


class NLeptonsProducer: public AnalysisModule {
public:
    explicit NLeptonsProducer(Context & ctx):
        h(ctx.get_handle<int>("n_leptons")) {}

    virtual bool process(Event & e) override {
        e.set(h, e.electrons->size() + e.muons->size());
        return true;
    }

private:
    Event::Handle<int> h;
};


class NFwdJetsProducer: public AnalysisModule {
public:
    explicit NFwdJetsProducer(Context & ctx):
        h(ctx.get_handle<int>("n_fwd_jets")),
        h_fw_js(ctx.get_handle<std::vector<Jet>>("fwd_jets")) {}

    virtual bool process(Event & e) override {
        e.set(h, e.get(h_fw_js).size());
        return true;
    }

private:
    Event::Handle<int> h;
    Event::Handle<std::vector<Jet>> h_fw_js;
};


class LeadingJetPtProducer: public AnalysisModule {
public:
    explicit LeadingJetPtProducer(Context & ctx):
        h(ctx.get_handle<float>("leading_jet_pt")) {}

    virtual bool process(Event & e) override {
        if (e.jets->size() > 0) {
            e.set(h, e.jets->at(0).pt());
            return true;
        } else {
            e.set(h, 0.);
            return false;
        }
    }

private:
    Event::Handle<float> h;
};


class SubleadingJetPtProducer: public AnalysisModule {
public:
    explicit SubleadingJetPtProducer(Context & ctx):
        h(ctx.get_handle<float>("subleading_jet_pt")) {}

    virtual bool process(Event & e) override {
        if (e.jets->size() > 1) {
            e.set(h, e.jets->at(1).pt());
            return true;
        } else {
            e.set(h, 0.);
            return false;
        }
    }

private:
    Event::Handle<float> h;
};


class LeptonPtProducer: public AnalysisModule {
public:
    explicit LeptonPtProducer(Context & ctx):
        h(ctx.get_handle<float>("primary_lepton_pt")),
        h_prim_lep(ctx.get_handle<FlavorParticle>("PrimaryLepton")) {}

    virtual bool process(Event & e) override {
        if (e.is_valid(h_prim_lep)) {
            e.set(h, e.get(h_prim_lep).pt());
        } else {
            e.set(h, 0.);
        }
        return true;
    }

private:
    Event::Handle<float> h;
    Event::Handle<FlavorParticle> h_prim_lep;
};