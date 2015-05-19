#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/EventShapeVariables.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/JetCorrections.h"
#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/ElectronHists.h"
#include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/common/include/TTbarReconstruction.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQSLPS_selectionItems.h"

#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_cutProducers.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_hists.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_selectionItems.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_topReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_higgsReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_vlqReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_eventHypDiscr.h"


using namespace std;


static bool isTlepEvent(const vector<GenParticle> * gps) {
    for (const auto & gp : *gps) {
        if (abs(gp.pdgId()) == 6) {
            auto d1 = gp.daughter(gps, 1);
            auto d2 = gp.daughter(gps, 2);
            if (!(d1 && d2)) {
                return false;
            }
            if (abs(d1->pdgId()) == 24 || abs(d2->pdgId()) == 24) {
                auto w = (abs(d1->pdgId()) == 24) ? d1 : d2;
                auto w_dau = w->daughter(gps, 1);
                if (w_dau && abs(w_dau->pdgId()) < 17 && abs(w_dau->pdgId()) > 10) {
                    return true;
                } 
            } else {
                return (abs(d1->pdgId()) < 17 && abs(d1->pdgId()) > 10)
                    || (abs(d2->pdgId()) < 17 && abs(d2->pdgId()) > 10);
            }
        }
    }
    return false;
}


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
    string version;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    unique_ptr<SelectionProducer> sel_module;

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;
};


VLQToHiggsAndLeptonModule::VLQToHiggsAndLeptonModule(Context & ctx){

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
    v_pre_modules.emplace_back(new EventWeightOutputHandle(ctx));
    v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "", "", "es_", 2., 100));
    v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "electrons", "muons", "es_plus_lep_", 2., 100));
    v_pre_modules.emplace_back(new ElectronCleaner(PtEtaCut(105.0, 2.4)));
    v_pre_modules.emplace_back(new MuonCleaner(PtEtaCut(50.0, 2.4)));
    v_pre_modules.emplace_back(new FwdJetSwitch(ctx));
    v_pre_modules.emplace_back(new BJetsProducer(ctx));
    v_pre_modules.emplace_back(new PrimaryLepton(ctx));
    v_pre_modules.emplace_back(new HTCalculator(ctx));
    v_pre_modules.emplace_back(new STCalculator(ctx));
    v_pre_modules.emplace_back(new LargestJetEtaProducer(ctx, "jets", "fwd_jets"));
    v_pre_modules.emplace_back(new NBTagProducer(ctx));
    v_pre_modules.emplace_back(new NTaggedTopJetProducer(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                                                         "n_higgs_tags", "patJetsCa15CHSJetsFilteredPacked"));
    v_pre_modules.emplace_back(new NLeadingBTagProducer(ctx));
    v_pre_modules.emplace_back(new TaggedTopJetProducer(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                                                        "h_jets", "patJetsCa15CHSJetsFilteredPacked"));
    v_pre_modules.emplace_back(new TopLepHypProducer(ctx, NeutrinoReconstruction));
    v_pre_modules.emplace_back(new HiggsHypProducer(ctx));
    v_pre_modules.emplace_back(new EventHypDiscr(ctx, "LeptTopHyps", "HiggsHyps"));
    v_pre_modules.emplace_back(new VlqReco(ctx));

    // Other CutProducers
    v_pre_modules.emplace_back(new TriggerAcceptProcuder(ctx));
    v_pre_modules.emplace_back(new NJetsProducer(ctx));
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx));
    v_pre_modules.emplace_back(new NFwdJetsProducer(ctx));
    v_pre_modules.emplace_back(new LeadingJetPtProducer(ctx));
    v_pre_modules.emplace_back(new SubleadingJetPtProducer(ctx));
    v_pre_modules.emplace_back(new LeptonPtProducer(ctx));

    v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "tlep"));
    v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "h"));
    v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "vlq"));

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQ2HT, ctx);
    sel_module.reset(new SelectionProducer(ctx, sel_helper));
    sel_helper.declare_items_for_output();

    // 3. Set up Hists classes:
    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);

    // append 2D cut
    sel_module->add_selection(new TwoDCutSel(ctx, 0.3, 20.));
    nm1_hists->add_hists(new TwoDCutHist(ctx, "Nm1Selection"));
    cf_hists->add_step("2D cut");
    v_hists.emplace_back(new TwoDCutHist(ctx, "NoSelection"));

    //v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true));
    //v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false));

    // sanity histograms after selection
    v_hists_after_sel.emplace_back(new ElectronHists(ctx, "SanityCheckEle", true));
    v_hists_after_sel.emplace_back(new MuonHists(ctx, "SanityCheckMu"));
    v_hists_after_sel.emplace_back(new EventHists(ctx, "SanityCheckEvent"));
    v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckJets"));
    v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckFwdJets", 4, "fwd_jets"));

    // signal sample gen hists
    if (version.substr(version.size() - 5, 100) == "_Tlep") {
        gen_hists.reset(new VLQ2HTGenHists(ctx, "GenHists"));
    }
    if (version.substr(version.size() - 4, 100) == "Tlep") {
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHists"));
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatch"));
    }

    ctx.undeclare_event_output("GenParticles");
    ctx.undeclare_event_output("beamspot_x0");
    ctx.undeclare_event_output("beamspot_y0");
    ctx.undeclare_event_output("beamspot_z0");
    ctx.undeclare_event_output("event");
    ctx.undeclare_event_output("genInfo");
    ctx.undeclare_event_output("isRealData");
    ctx.undeclare_event_output("luminosityBlock");
    ctx.undeclare_event_output("offlineSlimmedPrimaryVertices");
    ctx.undeclare_event_output("patJetsAk4PFCHS");
    ctx.undeclare_event_output("patJetsCa15CHSJetsFilteredPacked");
    ctx.undeclare_event_output("rho");
    ctx.undeclare_event_output("run");
    ctx.undeclare_event_output("slimmedElectrons");
    ctx.undeclare_event_output("slimmedMETs");
    ctx.undeclare_event_output("slimmedMuons");
    ctx.undeclare_event_output("slimmedTaus");
    ctx.undeclare_event_output("triggerNames");
    ctx.undeclare_event_output("triggerResults");
    ctx.undeclare_event_output("trigger_accept");
}


bool VLQToHiggsAndLeptonModule::process(Event & event) {

    if (gen_hists) {
        gen_hists->fill(event);
    }
 
    bool tlepEvt = isTlepEvent(event.genparticles);
    if (version.substr(version.size() - 5, 100) == "_Tlep" && !tlepEvt) {
        return false;
    }
    if (version.substr(version.size() - 8, 100) == "_NonTlep" && tlepEvt) {
        return false;
    }

    // run all modules
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }

    // run selection
    bool all_accepted = sel_module->process(event);

    // fill histograms
    if (all_accepted) {
        for (auto & hist : v_hists_after_sel) {
            hist->fill(event);
        }
    }

    // all hists
    for (auto & hist : v_hists) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return all_accepted;
}

// as we want to run the ExampleCycleNew directly with AnalysisModuleRunner,
// make sure the VLQToHiggsAndLeptonModule is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsAndLeptonModule)
