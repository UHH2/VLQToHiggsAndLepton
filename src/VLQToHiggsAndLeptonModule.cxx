#include <algorithm>
#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/ElectronHists.h"
// #include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQToHiggsAndLeptonSelections.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQToHiggsAndLeptonHists.h"

using namespace std;
using namespace uhh2;

typedef std::vector<std::unique_ptr<Selection> >    SelVector;
typedef std::vector<std::unique_ptr<Hists> >        HistVector;


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
                           btagging::csv_wp wp = btagging::csv_wp::medium):
        hndl(ctx.get_handle<int>("n_btags")),
        min_csv(btagging::csv_threshold(wp)) {}

    bool process(Event & event){
        int nbtag = 0;
        for(const Jet & j : *event.jets){
            if(j.btag_combinedSecondaryVertex() >= min_csv) ++nbtag;
        }
        event.set(hndl, nbtag);
        return true;
    }

private:
    Event::Handle<int> hndl;
    float min_csv;
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
    std::unique_ptr<ElectronCleaner> elecleaner;
    std::unique_ptr<MuonCleaner> mucleaner;
    std::unique_ptr<JetCleaner> jetcleaner;
    std::unique_ptr<FwdJetSwitch> fwdjetswitch;
    std::unique_ptr<NBTagProducer> nbtagprod;
    std::unique_ptr<HTCalculator> htcalc;

    // declare the Selections to use.
    std::vector<std::unique_ptr<Selection> > v_sel;
    
    // store the Hists collection as member variables.
    std::unique_ptr<Hists>  h_SC_EtaPtN,
                            h_SC_Ele,
                            h_SC_Evt,
                            h_SC_Jet,
                            h_SC_FwdJet,
                            h_allcuts;
                            // h_mu;
    std::vector<std::unique_ptr<Hists> > vh_nocuts,
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
    nbtagprod.reset(new NBTagProducer(ctx));
    fwdjetswitch.reset(new FwdJetSwitch(ctx));
    jetcleaner.reset(new JetCleaner(30.0, 7.0));
    elecleaner.reset(new ElectronCleaner(
        AndId<Electron>(
            ElectronID_CSA14_50ns_medium,
            PtEtaCut(20.0, 2.4)
        )
    ));
    mucleaner.reset(new MuonCleaner(
        AndId<Muon>(
            MuonIDTight(),
            PtEtaCut(20.0, 2.1)
        )
    ));
    htcalc.reset(new HTCalculator(ctx));

    // 2. set up selections:
    int n_cuts = 4;
    v_sel.resize(n_cuts);
    v_sel[0].reset(new NJetSelection(2));
    v_sel[1].reset(new vlq2hl_sel::NBTags(ctx, 2));
    v_sel[2].reset(new vlq2hl_sel::NFwdJets(ctx, 1));
    v_sel[3].reset(new vlq2hl_sel::NLeptons(1, 1));

    // 3. Set up Hists classes:
    vh_nocuts.resize(n_cuts);
    vh_nocuts[0].reset(new vlq2hl_hist::NJets(ctx, "SelNone"));
    vh_nocuts[1].reset(new vlq2hl_hist::NBTags(ctx, "SelNone"));
    vh_nocuts[2].reset(new vlq2hl_hist::NFwdJets(ctx, "SelNone"));
    vh_nocuts[3].reset(new vlq2hl_hist::NLeptons(ctx, "SelNone"));

    vh_nm1.resize(n_cuts);
    vh_nm1[0].reset(new vlq2hl_hist::NJets(ctx, "SelNm1"));
    vh_nm1[1].reset(new vlq2hl_hist::NBTags(ctx, "SelNm1"));
    vh_nm1[2].reset(new vlq2hl_hist::NFwdJets(ctx, "SelNm1"));
    vh_nm1[3].reset(new vlq2hl_hist::NLeptons(ctx, "SelNm1"));

    h_SC_EtaPtN.reset(new VLQToHiggsAndLeptonHists(ctx, "SanityCheckEtaPtN"));
    h_SC_Ele.reset(new ElectronHists(ctx, "SanityCheckEle", true));
    h_SC_Evt.reset(new EventHists(ctx, "SanityCheckEvent"));
    h_SC_Jet.reset(new JetHists(ctx, "SanityCheckJets"));
    h_SC_FwdJet.reset(new JetHists(ctx, "SanityCheckFwdJets", "fwd_jets"));
    h_allcuts.reset(new VLQToHiggsAndLeptonHists(ctx, "AllSel"));
    // h_mu.reset(new MuonHists(ctx, "mu_nocuts"));
}


bool VLQToHiggsAndLeptonModule::process(Event & event) {

    cout << "VLQToHiggsAndLeptonModule: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << "); weight = " << event.weight << endl;
    
    // 1. run all modules
    jetcleaner->process(event);
    fwdjetswitch->process(event);
    nbtagprod->process(event);
    elecleaner->process(event);
    mucleaner->process(event);
    htcalc->process(event);

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
    h_SC_EtaPtN->fill(event);
    h_SC_Ele->fill(event);
    h_SC_Evt->fill(event);
    h_SC_Jet->fill(event);
    h_SC_FwdJet->fill(event);
    // h_mu->fill(event);

    if (all_accepted) {
        h_allcuts->fill(event);
    }

    for (unsigned i=0; i<vh_nocuts.size(); ++i) {
        vh_nocuts[i]->fill(event);
    }

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
