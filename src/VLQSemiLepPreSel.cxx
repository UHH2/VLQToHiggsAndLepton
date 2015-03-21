#include <algorithm>
#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/JetCorrections.h"
#include "UHH2/common/include/TTbarReconstruction.h"

#include "UHH2/VLQToHiggsAndLepton/include/VLQSemiLepPreSelHists.h"


using namespace std;
using namespace uhh2;


class VLQSemiLepPreSel: public AnalysisModule {
public:
    explicit VLQSemiLepPreSel(Context & ctx);
    virtual bool process(Event & event) override;

private:
    std::string version;
    // modules for setting up collections and cleaning
    std::vector<std::unique_ptr<AnalysisModule>> v_pre_modules;
    Event::Handle<FlavorParticle> h_primlep;
    std::unique_ptr<VLQSemiLepPreSelHists> hists;
};


VLQSemiLepPreSel::VLQSemiLepPreSel(Context & ctx){

    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version", "");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup modules to prepare the event.
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new JetCorrector(JERFiles::PHYS14_L123_MC)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new JetCleaner(30.0, 7.0)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new PrimaryLepton(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new ElectronCleaner(
        AndId<Electron>(
            ElectronID_PHYS14_25ns_medium,
            PtEtaCut(20.0, 2.4)
        )
    )));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new MuonCleaner(
        AndId<Muon>(
            MuonIDTight(),
            PtEtaCut(20.0, 2.4)
        )
    )));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new HTCalculator(ctx)));

    h_primlep = ctx.get_handle<FlavorParticle>("PrimaryLepton");
    hists.reset(new VLQSemiLepPreSelHists(ctx, "PreSelCtrl"));
}


bool VLQSemiLepPreSel::process(Event & event) {

    // run all event modules
    for (auto & mod : v_pre_modules) {
         mod->process(event);
    }

    // reject event if no good lepton or jets
    if (!event.is_valid(h_primlep)) {
        return false;
    }
    if (!event.jets || !event.jets->size()) {
        return false;
    }

    // mk data
    float lep_pt = event.get(h_primlep).pt();
    float lj_pt = event.jets->at(0).pt();
    float st = lep_pt;
    st += event.met->pt();
    for (const auto & j : *event.jets) {
        float pt = j.pt();
        float abseta = fabs(j.eta());
        if (pt > 30. && abseta < 2.4) {
            st += pt;
        }
    }

    // fill ctrl hists
    hists->lepPt->Fill(lep_pt);
    hists->leadingJetPt->Fill(lj_pt);
    hists->st->Fill(st);
    if (event.electrons && event.electrons->size()) {
        hists->elePt->Fill(event.electrons->at(0).pt());
    }
    if (event.muons && event.muons->size()) {
        hists->muoPt->Fill(event.muons->at(0).pt());
    }

    // decide
    return lep_pt >= 50. && lj_pt >= 200. && st >= 500.;
}

UHH2_REGISTER_ANALYSIS_MODULE(VLQSemiLepPreSel)
