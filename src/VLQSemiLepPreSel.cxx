#include <algorithm>
#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/JetCorrections.h"
#include "UHH2/common/include/TTbarReconstruction.h"

#include "UHH2/VLQToHiggsAndLepton/include/VLQCommonModules.h"
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
    Event::Handle<double> h_st;

    std::unique_ptr<VLQSemiLepPreSelHists> hists;
};


VLQSemiLepPreSel::VLQSemiLepPreSel(Context & ctx):
    h_primlep(ctx.get_handle<FlavorParticle>("PrimaryLepton")),
    h_st(ctx.get_handle<double>("ST"))
{

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
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new PrimaryLepton(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new STCalculator(ctx)));

    hists.reset(new VLQSemiLepPreSelHists(ctx, "PreSelCtrl"));
}


bool VLQSemiLepPreSel::process(Event & event) {

    // reject event if no jets or lepton
    if (!event.jets->size()) {
        return false;
    }
    if (!(event.muons->size() || event.electrons->size())) {
        return false;
    }

    // run all event modules
    for (auto & mod : v_pre_modules) {
         mod->process(event);
    }

    // test again + good lepton
    if (!event.jets->size()) {
        return false;
    }
    if (!(event.muons->size() || event.electrons->size())) {
        return false;
    }
    if (!event.is_valid(h_primlep)) {
        return false;
    }

    // fill ctrl hists
    hists->fill(event);

    // decide
    return event.get(h_primlep).pt() >= 50.
           && event.jets->at(0).pt() >= 200.
           && event.get(h_st) >= 500.;
}

UHH2_REGISTER_ANALYSIS_MODULE(VLQSemiLepPreSel)
