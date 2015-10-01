#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <memory>

#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_hists.h"

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
#include "UHH2/common/include/CollectionProducer.h"
#include "UHH2/common/include/MCWeight.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"

#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_cutProducers.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_hists.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_selectionItems.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_topReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_higgsReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_vlqReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_eventHypDiscr.h"
#include "UHH2/VLQToHiggsAndLepton/include/OneBTagHiggsTag.h"


using namespace std;
using namespace uhh2;


template <typename TYPE>
static bool is_true(const TYPE &, const Event &) {
    return true;
}


/** \brief Basic analysis example of an AnalysisModule in UHH2
 */
class VLQToHiggsAndLeptonModule: public AnalysisModule {
public:
    
    explicit VLQToHiggsAndLeptonModule(Context & ctx);
    virtual bool process(Event & event) override;

private:
    string version;
    string type;

    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    vector<unique_ptr<AnalysisModule>> v_cat_modules;

    unique_ptr<Selection> cat_check_module;
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
    type = ctx.get("dataset_type", "");

    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    auto n_htags = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        HiggsTag(100., 160., CSVBTag(CSVBTag::WP_LOOSE))
    ));
    auto n_htags_masssb = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OrId<TopJet>(
            HiggsTag(60., 100., CSVBTag(CSVBTag::WP_LOOSE)),
            HiggsTag(160., 99999., CSVBTag(CSVBTag::WP_LOOSE))
        )
    ));
    auto n_htags_onebtag = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OneBTagHiggsTag(100., 160., CSVBTag(CSVBTag::WP_LOOSE))
    ));
    auto n_htags_onebtag_masssb = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OrId<TopJet>(
            OneBTagHiggsTag(60., 100., CSVBTag(CSVBTag::WP_LOOSE)),
            OneBTagHiggsTag(160., 99999., CSVBTag(CSVBTag::WP_LOOSE))
        )
    ));
    auto n_htags_onebtag_massplus = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OneBTagHiggsTag(100., 175., CSVBTag(CSVBTag::WP_LOOSE))
    ));
    auto n_htags_zerobtag = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OneBTagHiggsTag(100., 160., is_true<Jet>)
    ));
    auto n_htags_zerobtag_masssb = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OrId<TopJet>(
            OneBTagHiggsTag(60., 100., is_true<Jet>),
            OneBTagHiggsTag(160., 99999., is_true<Jet>)
        )
    ));
    auto n_htags_zerobtag_massplus = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        OneBTagHiggsTag(105., 195., is_true<Jet>)
    ));

    // setup modules to check if this event belongs into this category
    v_pre_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags", n_htags));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_masssb", n_htags_masssb));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_onebtag", n_htags_onebtag));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_onebtag_masssb", n_htags_onebtag_masssb));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_onebtag_massplus", n_htags_onebtag_massplus));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_zerobtag", n_htags_zerobtag));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_zerobtag_masssb", n_htags_zerobtag_masssb));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "n_htags_zerobtag_massplus", n_htags_zerobtag_massplus));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "jets", "n_btags", JetId(AndId<Jet>(PtEtaCut(30., 2.4), 
        CSVBTag(CSVBTag::WP_LOOSE)))));

    const string & category = ctx.get("category", "");

    // higgs tag with softdrop jets
    if (category == "AK8SoftDropCat1htag") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags));
        if (version.substr(version.size() - 5, 100) == "_Tlep") {
            gen_hists.reset(new VLQ2HTGenHists(ctx, "GenHists"));
        }

    } else if (category == "AK8SoftDropCat0h3btag") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            // new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            // new HandleSelection<int>(ctx, "n_htags_onebtag_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 3)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags));

    } else if (category == "AK8SoftDropCat0h2btag") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            // new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            // new HandleSelection<int>(ctx, "n_htags_onebtag_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 0, 2)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags));

    // other categories
    } else if (category == "AK8SoftDropCat1htagWith1b") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_onebtag));

    } else if (category == "AK8SoftDropCat1htagMassSB") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_masssb", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_masssb));

    } else if (category == "AK8SoftDropCat1htagWith1bMassSB") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag_masssb", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_onebtag_masssb));

    } else if (category == "AK8SoftDropCat1htagWith1bMassPlus") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag_massplus", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_onebtag_massplus));

    } else if (category == "AK8SoftDropCat1htagWith0b") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_zerobtag", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_zerobtag));

    } else if (category == "AK8SoftDropCat1htagWith0bMassSB") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_zerobtag_masssb", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_zerobtag));

    } else if (category == "AK8SoftDropCat1htagWith0bMassPlus") {
        cat_check_module.reset(new VectorAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_onebtag_masssb", 0, 0),
            new HandleSelection<int>(ctx, "n_htags_zerobtag_massplus", 1)
        }));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_zerobtag_massplus));

    // a category must be given
    } else {
        assert(false);  
    }

    // setup modules to prepare the event.
    // weights
    v_cat_modules.emplace_back(new MCLumiWeight(ctx));
    v_cat_modules.emplace_back(new MCPileupReweight(ctx));

    // leptons
    v_cat_modules.emplace_back(new ElectronCleaner(PtEtaCut(105.0, 2.4)));
    v_cat_modules.emplace_back(new MuonCleaner(PtEtaCut(50.0, 2.4)));
    v_cat_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_cat_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));

    // jets
    v_cat_modules.emplace_back(new LargestJetEtaProducer(
        ctx, "largest_jet_eta", "jets"));
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "b_jets", JetId(AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)))));
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "fwd_jets", JetId(VetoId<Jet>(PtEtaCut(0.0, 2.4)))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "fwd_jets", "n_fwd_jets", JetId(is_true<Jet>)));
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "jets", JetId(PtEtaCut(0.0, 2.4))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "jets", "n_jets", JetId(is_true<Jet>)));
    v_cat_modules.emplace_back(new NLeadingBTagProducer(
        ctx, CSVBTag::WP_LOOSE, "n_leading_btags"));
    v_cat_modules.emplace_back(new LeadingJetPtProducer(
        ctx, "leading_jet_pt"));
    v_cat_modules.emplace_back(new SubleadingJetPtProducer(
        ctx, "subleading_jet_pt"));
    v_cat_modules.emplace_back(new LeadingTopjetMassProducer(
        ctx, "h_jets", "h_topjet_mass"));

    // event variables
    v_cat_modules.emplace_back(new LepPtPlusMETProducer(ctx, "PrimaryLepton", "lep_plus_met", "lep_plus_met_vec_sum"));
    v_cat_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_cat_modules.emplace_back(new STCalculator(ctx, "ST", JetId(PtEtaCut(0., 2.4))));
    v_cat_modules.emplace_back(new STCalculator(ctx, "STgt70", JetId(PtEtaCut(70., 2.4))));
    // v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "", "", "es_", 2., 100));
    // v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "electrons", "muons", "es_plus_lep_", 2., 100));

    // event reconstruction
    v_cat_modules.emplace_back(new TopLepHypProducer(ctx, NeutrinoReconstruction));
    v_cat_modules.emplace_back(new HiggsHypProducer(ctx));
    v_cat_modules.emplace_back(new EventHypDiscr(ctx, "LeptTopHyps", "HiggsHyps"));
    v_cat_modules.emplace_back(new VlqReco(ctx));
    v_cat_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "tlep"));
    v_cat_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "h"));
    v_cat_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "vlq"));

    // Other CutProducers
    v_cat_modules.emplace_back(new EventWeightOutputHandle(ctx, "weight"));
    // v_cat_modules.emplace_back(new TriggerAcceptProducer(ctx, TRIGGER_PATHS, "trigger_accept"));
    v_cat_modules.emplace_back(new AbsValueProducer<float>(ctx, "largest_jet_eta"));
    v_cat_modules.emplace_back(new TwoDCutProducer(ctx));
    // v_pre_modules.emplace_back(new AbsValueProducer<float>(ctx, "vlq_eta"));

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQ2HT, ctx);
    // sel_helper.write_cuts_to_texfile();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));
    // sel_helper.declare_items_for_output();

    // 3. Set up Hists classes:
    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);

    // insert 2D cut
    // unsigned pos_2d_cut = 9;
    // sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT, DPT_2D_CUT));
    // nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
    // cf_hists->insert_step(pos_2d_cut, "2D cut");
    // v_hists.insert(v_hists.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));

    // fat jet hists
    v_hists.emplace_back(new TopJetHists(ctx, "HiggsJetsNoSel", 2, "h_jets"));
    v_hists_after_sel.emplace_back(new TopJetHists(ctx, "HiggsJetsAfterSel", 2, "h_jets"));

    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true));
    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false));

    v_hists.emplace_back(new ElectronHists(ctx, "SanityCheckEle", true));
    v_hists.emplace_back(new MuonHists(ctx, "SanityCheckMu"));
    v_hists.emplace_back(new EventHists(ctx, "SanityCheckEvent"));
    v_hists.emplace_back(new JetHists(ctx, "SanityCheckJets"));
    v_hists.emplace_back(new JetHists(ctx, "SanityCheckFwdJets", 4, "fwd_jets"));

    // event reconstruction
    v_hists.emplace_back(new VLQ2HTEventReco(ctx, "EventRecoBeforeSel"));
    v_hists_after_sel.emplace_back(new VLQ2HTEventReco(ctx, "EventRecoAfterSel"));

    // signal sample gen hists
    if (version.substr(version.size() - 4, 100) == "Tlep") {
        v_hists.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHists"));
        v_hists.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatch"));
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHistsAfterSel"));
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatchAfterSel"));
    }

    // if (type == "MC") {
    if (false) {
        ctx.undeclare_event_output("GenParticles");
        ctx.undeclare_event_output("beamspot_x0");
        ctx.undeclare_event_output("beamspot_y0");
        ctx.undeclare_event_output("beamspot_z0");
        ctx.undeclare_event_output("event");
        ctx.undeclare_event_output("genInfo");
        ctx.undeclare_event_output("isRealData");
        ctx.undeclare_event_output("luminosityBlock");
        ctx.undeclare_event_output("offlineSlimmedPrimaryVertices");
        ctx.undeclare_event_output("patJetsCa15CHSJetsFilteredPacked_daughters");
        ctx.undeclare_event_output("patJetsAk8CHSJetsSoftDropPacked_daughters");
        ctx.undeclare_event_output("rho");
        ctx.undeclare_event_output("run");
        ctx.undeclare_event_output("slimmedElectronsUSER");
        ctx.undeclare_event_output("slimmedMETs");
        ctx.undeclare_event_output("slimmedMuonsUSER");
        ctx.undeclare_event_output("slimmedTaus");
        ctx.undeclare_event_output("triggerNames");
        ctx.undeclare_event_output("triggerResults");
        // ctx.undeclare_event_output("trigger_accept");
    }

    // TODO - adjust lepton pt cut to lowest trigger (should go into every trigger leg and test??)
}


bool VLQToHiggsAndLeptonModule::process(Event & event) {

    if (gen_hists) {
        gen_hists->fill(event);
    }
 
    // bool tlepEvt = isTlepEvent(event.genparticles);
    // if (version.substr(version.size() - 5, 100) == "_Tlep" && !tlepEvt) {
    //     return false;
    // }
    // if (version.substr(version.size() - 8, 100) == "_NonTlep" && tlepEvt) {
    //     return false;
    // }

    // run category decision
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }
    if (!cat_check_module->passes(event)) {
        return false;
    }

    // run all modules
    for (auto & mod : v_cat_modules) {
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
