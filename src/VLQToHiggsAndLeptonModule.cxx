#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
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
#include "UHH2/common/include/NSelections.h"
#include "UHH2/common/include/TTbarReconstruction.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_cutProducers.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_hists.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_selection.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_topReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_vlqReco.h"

using namespace std;


static bool isTlepEvent(const std::vector<GenParticle> * gps) {
    for (const auto & gp : *gps) {
        if (abs(gp.pdgId()) == 6) {
            auto d1 = gp.daughter(gps, 1);
            auto d2 = gp.daughter(gps, 2);
            if (!(d1 && d2)) {
                return false;
            }
            if (abs(d1->pdgId()) == 24 || abs(d2->pdgId()) == 24) {
                auto w = (abs(d1->pdgId() == 24)) ? d1 : d2;
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
    //virtual ~VLQToHiggsAndLeptonModule();

private:
    std::string version;
    // modules for setting up collections and cleaning
    std::vector<std::unique_ptr<AnalysisModule>> v_pre_modules;

    // declare the Selections to use
    std::vector<std::unique_ptr<Selection>> v_sel;
    
    // store the Hists collection
    std::unique_ptr<Hists> gen_hists;
    std::vector<std::unique_ptr<Hists>> v_trig_hists,
                                        v_sanity_hists,
                                        vh_nocuts,
                                        vh_nm1;
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
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new ElectronCleaner(PtEtaCut(105.0, 2.4))));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new MuonCleaner(PtEtaCut(50.0, 2.4))));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new FwdJetSwitch(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new BJetsProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new PrimaryLepton(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new HTCalculator(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new STCalculator(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NBTagProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NHTagProducer(ctx, "patJetsCa15CHSJetsFilteredPacked")));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new TopTagCalculator(ctx.get_handle<int>("n_toptags"))));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NLeadingBTagProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new HJetsProducer(ctx, "patJetsCa15CHSJetsFilteredPacked")));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new TopLepHypProducer(ctx, NeutrinoReconstruction)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new TopLepChi2Discr(ctx, "LeptTopHyps")));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new VlqReco(ctx)));
    // TODO : 2d-cut

    // CutProducers
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new TriggerAcceptProcuder(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NJetsProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NLeptonsProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new NFwdJetsProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new LeadingJetPtProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new SubleadingJetPtProducer(ctx)));
    v_pre_modules.push_back(std::unique_ptr<AnalysisModule>(new LeptonPtProducer(ctx)));

    // 2. set up selections:
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "trigger_accept",     1)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_jets",             2)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_leptons",          1, 1)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_fwd_jets",         1)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_btags",            2)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_leading_btags",    0)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<int>     (ctx, "n_higgs_tags",       1)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "leading_jet_pt",     250)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "subleading_jet_pt",  65)));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "primary_lepton_pt"   )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<double>  (ctx, "ST"                  )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "tlep_chi2"           )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "tlep_mass"           )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "tlep_pt"             )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "tlep_eta"            )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "vlq_mass"           )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "vlq_pt"             )));
    v_sel.push_back(std::unique_ptr<Selection>(new HandleSelection<float>   (ctx, "vlq_eta"            )));

    // 3. Set up Hists classes:
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger         (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets           (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons        (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets        (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags          (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeadingBTags   (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NHTags          (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::LeadingJetPt    (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::SubLeadingJetPt (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::PrimaryLeptonPt (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::ST              (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepChi2      (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepMass      (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepPt        (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepEta       (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqMass         (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqPt           (ctx, "SelNone")));
    vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqEta          (ctx, "SelNone")));

    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger         (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets           (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons        (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets        (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags          (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeadingBTags   (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NHTags          (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::LeadingJetPt    (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::SubLeadingJetPt (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::PrimaryLeptonPt (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::ST              (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepChi2      (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepMass      (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepPt        (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::TopLepEta       (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqMass         (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqPt           (ctx, "SelNm1")));
    vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::VlqEta          (ctx, "SelNm1")));

    v_trig_hists.push_back(std::unique_ptr<Hists>(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true)));
    v_trig_hists.push_back(std::unique_ptr<Hists>(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false)));

    v_sanity_hists.push_back(std::unique_ptr<Hists>(new ElectronHists(ctx, "SanityCheckEle", true)));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new MuonHists(ctx, "SanityCheckMu")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new EventHists(ctx, "SanityCheckEvent")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new JetHists(ctx, "SanityCheckJets")));
    v_sanity_hists.push_back(std::unique_ptr<Hists>(new JetHists(ctx, "SanityCheckFwdJets", 4, "fwd_jets")));

    if (version.substr(version.size() - 5, 100) == "_Tlep") {
        gen_hists.reset(new GenHists(ctx, "GenHists"));
    }

    //cut_ofstream = ofstream(version + "_cuts.txt", ofstream::out);
    //for (auto & sel : v_sel) {
    //    const auto & name = ((HandleSelection<int>*)sel.get())->name();
    //    v_cut_names.push_back(name);
    //    if cuts_ofstream.is_open() {
    //        cuts_ofstream << name << "\t";
    //    }
    //}
    //if cuts_ofstream.is_open() {
    //    cuts_ofstream << endl;
    //}
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
    for (auto & hist : vh_nocuts) {
        hist->fill(event);
    }

    // trigger
    for (auto & hist : v_trig_hists) {
         hist->fill(event);
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
