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
    vector<unique_ptr<Hists>> v_hists_el;
    vector<unique_ptr<Hists>> v_hists_mu;
    vector<unique_ptr<Hists>> v_hists_after_sel_el;
    vector<unique_ptr<Hists>> v_hists_after_sel_mu;

    Event::Handle<int> h_ele_trg;
};


VLQToHiggsAndLeptonModule::VLQToHiggsAndLeptonModule(Context & ctx){

    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    auto data_dir_path = ctx.get("data_dir_path");
    double target_lumi = string2double(ctx.get("target_lumi"));
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    if (version == "Run2015D_Ele") {
        ctx.set("lumi_file", "/afs/desy.de/user/t/tholenhe/xxl-af-cms/CMSSW_7_4_15_patch1/src/UHH2/common/data/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_NoBadBSRuns.root");
    } else if (version == "Run2015D_Mu") {
        ctx.set("lumi_file", "/afs/desy.de/user/t/tholenhe/xxl-af-cms/CMSSW_7_4_15_patch1/src/UHH2/common/data/Latest_2015_Golden_JSON.root");
    }

    // remove everything from the output branch
    // ctx.undeclare_all_event_output();

    // jet correction (if nominal, the corrections were already applied in the preselection)
    if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
        auto ak8_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK8PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK8PFchs_DATA;
        auto ak4_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK4PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK4PFchs_DATA;
        v_pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
            ak8_corr, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        v_pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
            ak4_corr, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        v_pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    }
    v_pre_modules.emplace_back(new TopJetCleaner(ctx,
        PtEtaCut(200., 2.4),
            "patJetsAk8CHSJetsSoftDropPacked_daughters"));
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
    if (type == "MC") {
        v_cat_modules.emplace_back(new TriggerAwareEventWeight(ctx, "trigger_accept_el", (target_lumi - 90.)/target_lumi));
    }
    v_cat_modules.emplace_back(new MCLumiWeight(ctx));
    v_cat_modules.emplace_back(new MCPileupReweight(ctx));
    v_cat_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_LOOSE, "h_jets"));
    v_cat_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "MuonID_Z_RunD_Reco74X_Nov20.root", 
        "NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id", "nominal", "prim_mu_coll"));
    v_cat_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "SingleMuonTrigger_Z_RunD_Reco74X_Nov20.root", 
        "Mu45_eta2p1_PtEtaBins", 1., "trg", "nominal", "prim_mu_coll"));
    if (version.size() > 7 && version.substr(0, 7) == "Signal_") {
        v_cat_modules.emplace_back(new PDFWeightBranchCreator(ctx, 112));
    }

    // leptons
    v_cat_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_cat_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, 
        "PrimaryLepton", "primary_lepton_pt", "primary_lepton_eta", "primary_lepton_charge"));

    // jets: final pt threshold after JES/JER
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "jets", JetId(PtEtaCut(30.0, 7.0))));

    // jets: forward
    v_cat_modules.emplace_back(new LargestJetEtaProducer(
        ctx, "largest_jet_eta", "jets"));
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "fwd_jets", JetId(VetoId<Jet>(PtEtaCut(0.0, 2.4)))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "fwd_jets", "n_fwd_jets", JetId(is_true<Jet>)));
    ctx.declare_event_output<vector<Jet>>("fwd_jets");

    // jets: central
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "jets", JetId(PtEtaCut(0.0, 2.4))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "jets", "n_jets", JetId(is_true<Jet>)));

    // jets: b-tags
    v_cat_modules.emplace_back(new CollectionProducer<Jet>(
        ctx, "jets", "b_jets", JetId(AndId<Jet>(PtEtaCut(0., 2.4), CSVBTag(CSVBTag::WP_LOOSE)))));
    v_cat_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "b_jets", "n_btags", JetId(is_true<Jet>)));
    v_cat_modules.emplace_back(new NLeadingBTagProducer(
        ctx, CSVBTag::WP_LOOSE, "n_leading_btags"));

    // ak4 jet weight
    float jetsf_p0 = 1.09771;
    float jetsf_p1 = -0.000517529;
    float cov_p0_p0 = 0.0014795109823;
    float cov_p0_p1 = -3.6104869696e-06;
    float cov_p1_p1 = 9.89815635815e-09;
    v_cat_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx,
        "jets", jetsf_p0, jetsf_p1, cov_p0_p0, cov_p0_p1, cov_p1_p1,
        "weight_ak4jet", false));

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

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQ2HT, ctx);
    // sel_helper.write_cuts_to_texfile();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));
    sel_helper.declare_items_for_output();

    // 3. Set up Hists classes:
    sel_helper.fill_hists_vector(v_hists_el, "ElChan/NoSelection");
    auto nm1_hists_el = new Nm1SelHists(ctx, "ElChan/Nm1Selection", sel_helper);
    auto cf_hists_el = new VLQ2HTCutflow(ctx, "ElChan/Cutflow", sel_helper);
    v_hists_el.emplace_back(nm1_hists_el);
    v_hists_el.emplace_back(cf_hists_el);

    sel_helper.fill_hists_vector(v_hists_mu, "MuChan/NoSelection");
    auto nm1_hists_mu = new Nm1SelHists(ctx, "MuChan/Nm1Selection", sel_helper);
    auto cf_hists_mu = new VLQ2HTCutflow(ctx, "MuChan/Cutflow", sel_helper);
    v_hists_mu.emplace_back(nm1_hists_mu);
    v_hists_mu.emplace_back(cf_hists_mu);

    // insert trigger dependent jet cuts
    sel_module->replace_selection(1, new TriggerAwareHandleSelection<float>(
        ctx, "leading_jet_pt", "trigger_accept_el", 250., 100.));
    sel_module->replace_selection(2, new TriggerAwareHandleSelection<float>(
        ctx, "subleading_jet_pt", "trigger_accept_el", 70., 50.));

    // insert 2D cut
    unsigned pos_2d_cut = 3;
    sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT, DPT_2D_CUT));

    nm1_hists_el->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "ElChan/Nm1Selection"));
    cf_hists_el->insert_step(pos_2d_cut, "2D cut");
    v_hists_el.insert(v_hists_el.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "ElChan/NoSelection"))));
    
    nm1_hists_mu->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "MuChan/Nm1Selection"));
    cf_hists_mu->insert_step(pos_2d_cut, "2D cut");
    v_hists_mu.insert(v_hists_mu.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "MuChan/NoSelection"))));

    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true));
    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false));

    // SanityChecks and other histograms after selection
    // separately for ele and mu channel
    h_ele_trg = ctx.get_handle<int>("trigger_accept_el");
    v_hists_after_sel_el.emplace_back(new ElectronHists(ctx, "ElChan/SanityCheckEle", true));
    v_hists_after_sel_el.emplace_back(new MuonHists(ctx, "ElChan/SanityCheckMu"));
    v_hists_after_sel_el.emplace_back(new EventHists(ctx, "ElChan/SanityCheckEvent"));
    v_hists_after_sel_el.emplace_back(new JetHists(ctx, "ElChan/SanityCheckJets"));
    v_hists_after_sel_el.emplace_back(new JetHists(ctx, "ElChan/SanityCheckFwdJets", 4, "fwd_jets"));
    v_hists_after_sel_el.emplace_back(new TopJetHists(ctx, "ElChan/SanityCheckAK8Jets", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
    v_hists_after_sel_el.emplace_back(new TopJetHists(ctx, "ElChan/HiggsJetsAfterSel", 2, "h_jets"));
    v_hists_after_sel_el.emplace_back(new BTagMCEfficiencyHists(ctx, "ElChan/BTagMCEfficiencyHists", CSVBTag::WP_LOOSE, "h_jets"));
    v_hists_after_sel_el.emplace_back(new VLQ2HTEventReco(ctx, "ElChan/EventRecoAfterSel"));
    v_hists_after_sel_el.emplace_back(new HistCollector(ctx, "ElChan/EventHistsPost", type == "MC"));
    v_hists_after_sel_mu.emplace_back(new ElectronHists(ctx, "MuChan/SanityCheckEle", true));
    v_hists_after_sel_mu.emplace_back(new MuonHists(ctx, "MuChan/SanityCheckMu"));
    v_hists_after_sel_mu.emplace_back(new EventHists(ctx, "MuChan/SanityCheckEvent"));
    v_hists_after_sel_mu.emplace_back(new JetHists(ctx, "MuChan/SanityCheckJets"));
    v_hists_after_sel_mu.emplace_back(new JetHists(ctx, "MuChan/SanityCheckFwdJets", 4, "fwd_jets"));
    v_hists_after_sel_mu.emplace_back(new TopJetHists(ctx, "MuChan/SanityCheckAK8Jets", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
    v_hists_after_sel_mu.emplace_back(new TopJetHists(ctx, "MuChan/HiggsJetsAfterSel", 2, "h_jets"));
    v_hists_after_sel_mu.emplace_back(new BTagMCEfficiencyHists(ctx, "MuChan/BTagMCEfficiencyHists", CSVBTag::WP_LOOSE, "h_jets"));
    v_hists_after_sel_mu.emplace_back(new VLQ2HTEventReco(ctx, "MuChan/EventRecoAfterSel"));
    v_hists_after_sel_mu.emplace_back(new HistCollector(ctx, "MuChan/EventHistsPost", type == "MC"));

    // lumi hists
    if (type == "DATA") {
        v_hists_el          .emplace_back(new LuminosityHists(ctx, "ElChan/LumiHistPre"));
        v_hists_after_sel_el.emplace_back(new LuminosityHists(ctx, "ElChan/LumiHistPost"));
        v_hists_mu          .emplace_back(new LuminosityHists(ctx, "MuChan/LumiHistPre"));
        v_hists_after_sel_mu.emplace_back(new LuminosityHists(ctx, "MuChan/LumiHistPost"));
    }

    // signal sample gen hists
    if (version.size() > 5 && version.substr(version.size() - 5, 100) == "_Tlep") {
        v_hists_el.emplace_back(new VLQ2HTRecoGenComparison(ctx, "ElChan/GenRecoHists"));
        v_hists_el.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "ElChan/Chi2SignalMatch"));
        v_hists_after_sel_el.emplace_back(new VLQ2HTRecoGenComparison(ctx, "ElChan/GenRecoHistsAfterSel"));
        v_hists_after_sel_el.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "ElChan/Chi2SignalMatchAfterSel"));
        v_hists_mu.emplace_back(new VLQ2HTRecoGenComparison(ctx, "MuChan/GenRecoHists"));
        v_hists_mu.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "MuChan/Chi2SignalMatch"));
        v_hists_after_sel_mu.emplace_back(new VLQ2HTRecoGenComparison(ctx, "MuChan/GenRecoHistsAfterSel"));
        v_hists_after_sel_mu.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "MuChan/Chi2SignalMatchAfterSel"));
    }

    if (version.size() > 7 && version.substr(0, 7) == "TpB_TH_") {
        gen_hists.reset(new VLQ2HTGenHists(ctx, "VLQ2HTGenHists"));
    }
}


bool VLQToHiggsAndLeptonModule::process(Event & event) {

    if (gen_hists) {
        gen_hists->fill(event);
    }
 
    if (type == "MC") {
        bool tlepEvt = isTlepEvent(event.genparticles);
        if (version.size() > 5 && version.substr(version.size() - 5, 100) == "_Tlep" && !tlepEvt) {
            return false;
        }
        if (version.size() > 8 && version.substr(version.size() - 8, 100) == "_NonTlep" && tlepEvt) {
            return false;
        }
    }

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

    // pick histograms for channel
    bool ele_acc = event.get(h_ele_trg);
    const auto & v_hists = (ele_acc) ? v_hists_el : v_hists_mu;
    const auto & v_hists_after_sel = (ele_acc) ? v_hists_after_sel_el : v_hists_after_sel_mu;

    // fill histograms
    if (all_accepted) {
        for (auto & hist : v_hists_after_sel) {
            hist->fill(event);
        }
    }
    for (auto & hist : v_hists) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return all_accepted;
}

UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsAndLeptonModule)
