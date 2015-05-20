#pragma once

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/Utils.h"

using namespace uhh2;


// DEPRECATED: replaced by CollectionSizeProducer class; needs to be tested still!
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


// DEPRECATED: replaced by CollectionSizeProducer class; needs to be tested still!
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


class LorentzVectorInfoProducer: public AnalysisModule {
public:
    explicit LorentzVectorInfoProducer(Context & ctx, const string & name):
        h_input(ctx.get_handle<LorentzVector>(name)),
        h_mass(ctx.get_handle<float>(name + "_mass")),
        h_eta(ctx.get_handle<float>(name + "_eta")),
        h_pt(ctx.get_handle<float>(name + "_pt")) {}

    virtual bool process(Event & e) override {
        if (e.is_valid(h_input)) {
            const auto & vec = e.get(h_input);
            e.set(h_mass, inv_mass_safe(vec));
            e.set(h_pt, vec.pt());
            e.set(h_eta, vec.eta());
            return true;
        }
        return false;
    }

private:
    Event::Handle<LorentzVector> h_input;
    Event::Handle<float> h_mass;
    Event::Handle<float> h_eta;
    Event::Handle<float> h_pt;
};
