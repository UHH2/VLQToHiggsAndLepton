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

#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/ElectronHists.h"
#include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQToHiggsAndLeptonHists.h"

#include "UHH2/common/include/NSelections.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQToHiggsAndLeptonSelections.h"


using namespace std;
using namespace uhh2;


class FwdJetSwitch: public AnalysisModule {
public:
    explicit FwdJetSwitch(Context & ctx):
        hndl(ctx.get_handle<std::vector<Jet> >("fwd_jets")) {}

    bool process(Event & event){
        std::vector<Jet> fwd;
        std::vector<Jet> cnt;
        for(const auto & jet: *event.jets) {
            if (fabs(jet.eta()) > 2.4) {
                fwd.push_back(jet);
            } else {
                cnt.push_back(jet);
            }
        }
        event.set(hndl, fwd);
        swap(*event.jets, cnt);
        return true;
    }

private:
    Event::Handle<std::vector<Jet> > hndl;
};

class NBTagProducer: public AnalysisModule {
public:
    explicit NBTagProducer(Context & ctx,
                           CSVBTag::wp wp = CSVBTag::WP_MEDIUM):
        hndl(ctx.get_handle<int>("n_btags")),
        tagger(CSVBTag(wp)) {}

    bool process(Event & event){
        int nbtag = 0;
        for(const Jet & j : *event.jets){
            if (tagger(j, event)) {
                ++nbtag;
            }
        }
        event.set(hndl, nbtag);
        return true;
    }

private:
    Event::Handle<int> hndl;
    CSVBTag tagger;
};


/** \brief Basic analysis example of an AnalysisModule (formerly 'cycle') in UHH2
 * 
 * This is the central class which calls other AnalysisModules, Hists or Selection classes.
 * This AnalysisModule, in turn, is called (via AnalysisModuleRunner) by SFrame.
 */

class VLQToHiggsAndLeptonModule: public AnalysisModule {
public:
    
    explicit VLQToHiggsAndLeptonModule(Context & ctx);
    virtual bool process(Event & event) override;

private:
    // modules for setting up collections and cleaning
    std::vector<std::unique_ptr<AnalysisModule>> v_pre_modules;

    // declare the Selections to use
    std::vector<std::unique_ptr<Selection>> v_sel;
    
    // store the Hists collection
    std::vector<std::unique_ptr<Hists>> v_sanity_hists,
                                        vh_nocuts,
                                        vh_nm1;
};


VLQToHiggsAndLeptonModule::VLQToHiggsAndLeptonModule(Context & ctx){

    // If needed, access the configuration of the module here, e.g.:
    string testvalue = ctx.get("TestKey", "<not set>");
    cout << "TestKey in the configuration was: " << testvalue << endl;
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup other modules. Here, only the jet cleaner
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new JetCorrector(JERFiles::PHYS14_L123_MC)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new JetCleaner(30.0, 7.0)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new FwdJetSwitch(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NBTagProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new ElectronCleaner(
        AndId<Electron>(
            ElectronID_CSA14_50ns_medium,
            PtEtaCut(20.0, 2.4)
        )
    )));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new MuonCleaner(
        AndId<Muon>(
            MuonIDTight(),
            PtEtaCut(20.0, 2.1)
        )
    )));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new HTCalculator(ctx)));

    // 2. set up selections:
    // v_sel.push_back(std::unique_ptr<Selection>(new vlq2hl_sel::Trigger()));
    v_sel.push_back(std::unique_ptr<Selection>(new NJetSelection(2)));
    v_sel.push_back(std::unique_ptr<Selection>(new vlq2hl_sel::NBTags(ctx, 2)));
    v_sel.push_back(std::unique_ptr<Selection>(new vlq2hl_sel::NFwdJets(ctx, 1)));
    v_sel.push_back(std::unique_ptr<Selection>(new vlq2hl_sel::NLeptons(1, 1)));

    // 3. Set up Hists classes:
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets   (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags  (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets(ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons(ctx, "SelNone")));

    // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets   (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags  (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets(ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons(ctx, "SelNm1")));

    v_sanity_hists.push_back(std::unique_ptr<Hists>(new ElectronHists(ctx, "SanityCheckEle", true)));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new MuonHists(ctx, "SanityCheckMu")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new EventHists(ctx, "SanityCheckEvent")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new JetHists(ctx, "SanityCheckJets")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new JetHists(ctx, "SanityCheckFwdJets", "fwd_jets")));

}


bool VLQToHiggsAndLeptonModule::process(Event & event) {

    // 1. run all modules
    for (auto & mod : v_pre_modules) {
         mod->process(event);
    }

    // 2.a test selections
    bool all_accepted = true;
    std::vector<bool> v_accept(v_sel.size());
    for (unsigned i=0; i<v_sel.size(); ++i) {
        bool accept = v_sel[i]->passes(event);
        v_accept[i] = accept;
        if (!accept) {
            all_accepted = false;
        }
    }

    // 2.b fill histograms
    // sanity
    if (all_accepted) {
        for (auto & hist : v_sanity_hists) {
            hist->fill(event);
        }
    }

    // selection: no cuts
    for (unsigned i=0; i<vh_nocuts.size(); ++i) {
        vh_nocuts[i]->fill(event);
    }

    // selection: n-1
    for (unsigned i=0; i<vh_nm1.size(); ++i) {
        bool accept_nm1 = true;
        for (unsigned j=0; j<v_accept.size(); ++j) {
            if (i==j) {
                continue;
            }
            if (!v_accept[j]) {
                accept_nm1 = false;
                break;
            }
        }
        if (accept_nm1) {
            vh_nm1[i]->fill(event);
        }
    }

    // 3. decide whether or not to keep the current event in the output:
    return all_accepted;
}

// as we want to run the ExampleCycleNew directly with AnalysisModuleRunner,
// make sure the VLQToHiggsAndLeptonModule is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsAndLeptonModule)
