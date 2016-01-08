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
#include "UHH2/common/include/LuminosityHists.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/common/include/TTbarReconstruction.h"
#include "UHH2/common/include/CollectionProducer.h"
#include "UHH2/common/include/MCWeight.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"
#include "UHH2/VLQSemiLepPreSel/include/EventHists.h"

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

    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    auto data_dir_path = ctx.get("data_dir_path");

    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    // remove everything from the output branch
    // ctx.undeclare_all_event_output();

    // jet correction (if nominal, the corrections were already applied in the preselection)
    if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
        auto ak8_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK8PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK8PFchs_DATA;
        auto ak4_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK8PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK8PFchs_DATA;
        v_pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
            ak8_corr, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        v_pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
            ak4_corr, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        v_pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    }
    // v_pre_modules.emplace_back(new GenericTopJetCleaner(ctx,
    //     PtEtaCut(150., 2.4), "patJetsAk8CHSJetsSoftDropPacked_daughters"));
    if (type == "MC") {
        v_pre_modules.emplace_back(new JetResolutionSmearer(ctx));    
    }

    // first event content modules
    auto n_htags_all = TopJetId(AndId<TopJet>(
        PrimaryLeptonDeltaPhiId(ctx, 1.0),
        HiggsTag(60., 99999., is_true<Jet>)
    ));
    v_pre_modules.emplace_back(new TriggerAcceptProducer(
        ctx, TRIGGER_PATHS_ELE, TRIGGER_PATHS_MU, "trigger_accept_el"));  // Vetoing mu trigger!
    v_pre_modules.emplace_back(new TriggerAcceptProducer(
        ctx, TRIGGER_PATHS_MU, "trigger_accept_mu"));
    v_pre_modules.emplace_back(new TriggerAwarePrimaryLepton(
        ctx, "PrimaryLepton", "trigger_accept_el", "trigger_accept_mu", 50., 47.));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(
        ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "h_jets", n_htags_all));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "h_jets", "n_htags"));
    
    // cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags", 1.)); want to have the full thing over presel in the cutflow.

    // setup modules to prepare the event.
    // weights
    v_cat_modules.emplace_back(new MCLumiWeight(ctx));
    v_cat_modules.emplace_back(new MCPileupReweight(ctx));
    v_cat_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_LOOSE, "h_jets"));
    v_cat_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "MuonID_Z_RunD_Reco74X_Nov20.root", 
        "NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id"));
    v_cat_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "SingleMuonTrigger_Z_RunD_Reco74X_Nov20.root", 
        "Mu45_eta2p1_PtEtaBins", 1., "trg"));

    // leptons
    v_cat_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_cat_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, 
        "PrimaryLepton", "primary_lepton_pt", "primary_lepton_eta", "primary_lepton_charge"));

    // jets: forward
    v_cat_modules.emplace_back(new LargestJetEtaProducer(
        ctx, "largest_jet_eta", "jets"));
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "fwd_jets", JetId(VetoId<Jet>(PtEtaCut(0.0, 2.4)))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "fwd_jets", "n_fwd_jets", JetId(is_true<Jet>)));

    // jets: central
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "jets", JetId(PtEtaCut(0.0, 2.4))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "jets", "n_jets", JetId(is_true<Jet>)));

    // jets: b-tags
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "b_jets", JetId(AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "b_jets", "n_btags", JetId(is_true<Jet>)));
    v_cat_modules.emplace_back(new NLeadingBTagProducer(
        ctx, CSVBTag::WP_LOOSE, "n_leading_btags"));

    // jets: other producers
    v_cat_modules.emplace_back(new LeadingJetPtProducer(
        ctx, "leading_jet_pt"));
    v_cat_modules.emplace_back(new SubleadingJetPtProducer(
        ctx, "subleading_jet_pt"));
    v_cat_modules.emplace_back(new LeadingTopjetMassProducer(
        ctx, "h_jets", "h_topjet_mass"));

    // event variables
    v_cat_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_cat_modules.emplace_back(new STCalculator(ctx, "ST", JetId(PtEtaCut(0., 2.4))));
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
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "h_subjets", "h_n_subjet_btags", JetId(CSVBTag(CSVBTag::WP_LOOSE))));

    // Other CutProducers
    v_cat_modules.emplace_back(new EventWeightOutputHandle(ctx, "weight"));
    v_cat_modules.emplace_back(new AbsValueProducer<float>(ctx, "largest_jet_eta"));
    v_cat_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLepton", "TwoDCut_dr", "TwoDCut_ptrel", true));
    v_cat_modules.emplace_back(new TriggerXOR(ctx, "trigger_accept_el", "trigger_accept_mu", "trigger_accept"));
    v_cat_modules.emplace_back(new EleChJetCuts(ctx, "jets", "trigger_accept_el", "ele_ch_jet_cuts"));

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQ2HT, ctx);
    // sel_helper.write_cuts_to_texfile();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));
    sel_helper.declare_items_for_output();

    // 3. Set up Hists classes:
    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);

    // insert 2D cut
    unsigned pos_2d_cut = 1;
    sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT, DPT_2D_CUT));
    nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
    cf_hists->insert_step(pos_2d_cut, "2D cut");
    v_hists.insert(v_hists.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));

    // fat jet hists
    v_hists_after_sel.emplace_back(new TopJetHists(ctx, "HiggsJetsAfterSel", 2, "h_jets"));
    v_hists_after_sel.emplace_back(new BTagMCEfficiencyHists(ctx, "BTagMCEfficiencyHists", CSVBTag::WP_LOOSE, "h_jets"));

    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true));
    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false));

    v_hists_after_sel.emplace_back(new ElectronHists(ctx, "SanityCheckEle", true));
    v_hists_after_sel.emplace_back(new MuonHists(ctx, "SanityCheckMu"));
    v_hists_after_sel.emplace_back(new EventHists(ctx, "SanityCheckEvent"));
    v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckJets"));
    v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckFwdJets", 4, "fwd_jets"));
    v_hists_after_sel.emplace_back(new TopJetHists(ctx, "SanityCheckAK8Jets", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));

    // event reconstruction
    v_hists_after_sel.emplace_back(new VLQ2HTEventReco(ctx, "EventRecoAfterSel"));
    v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost", type == "MC"));

    // lumi hists
    if (type == "DATA") {
        v_hists          .emplace_back(new LuminosityHists(ctx, "LumiHistPre"));
        v_hists_after_sel.emplace_back(new LuminosityHists(ctx, "LumiHistPost"));
    }

    // signal sample gen hists
    if (version.substr(version.size() - 4, 100) == "Tlep") {
        v_hists.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHists"));
        v_hists.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatch"));
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHistsAfterSel"));
        v_hists_after_sel.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatchAfterSel"));
    }

    if (version.size() > 7 && version.substr(0, 7) == "TpB_TH_") {
        gen_hists.reset(new VLQ2HTGenHists(ctx, "VLQ2HTGenHists"));
    }
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

    // pre-selection
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }
    if (cat_check_module && !cat_check_module->passes(event)) {
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

UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsAndLeptonModule)
