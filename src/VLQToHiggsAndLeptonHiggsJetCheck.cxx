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
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_topReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_higgsReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_vlqReco.h"
#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_eventHypDiscr.h"
#include "UHH2/VLQToHiggsAndLepton/include/OneBTagHiggsTag.h"

#include "UHH2/VLQToHiggsAndLepton/include/VLQ2HT_selectionItemsHiggsJetCheck.h"


using namespace std;
using namespace uhh2;


template <typename TYPE>
static bool is_true(const TYPE &, const Event &) {
    return true;
}


class MyAndSelection: public Selection {
public:
    explicit MyAndSelection(const vector<Selection*> &sel_vec) {
        for (const auto & sel : sel_vec) {
            sel_vec_.emplace_back(sel);
        }
    }

    bool passes(const Event & e) override {
        for (const auto & sel : sel_vec_) {
            if (!sel->passes(e)) {
                return false;
            }
        }
        return true;
    }

private:
    vector<unique_ptr<Selection>> sel_vec_;
};


class SpikeProtection: public AnalysisModule {
    virtual bool process(Event & event) override {
        if (event.weight > 30.) {
            cerr << "WARNING: SpikeProtection sets event.weight from " << event.weight << " to 30." << endl;
            event.weight = 30.;
        }
        return true;
    }
};


class NHEgt30 {
public:
    bool operator()(const Jet & jet, const uhh2::Event &) const {
        return jet.neutralHadronEnergyFraction() * jet.energy() > 30;
    }
};


class NHElt30 {
public:
    bool operator()(const Jet & jet, const uhh2::Event &) const {
        return jet.neutralHadronEnergyFraction() * jet.energy() < 30;
    }
};


/** \brief Basic analysis example of an AnalysisModule in UHH2
 */
class VLQToHiggsAndLeptonHiggsJetCheck: public AnalysisModule {
public:
    
    explicit VLQToHiggsAndLeptonHiggsJetCheck(Context & ctx);
    virtual bool process(Event & event) override;

private:
    string version;
    string type;

    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    vector<unique_ptr<AnalysisModule>> v_cat_modules;

    unique_ptr<Selection> cat_check_module;
    unique_ptr<Selection> prim_lep_check_module;
    unique_ptr<SelectionProducer> sel_module;

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;
};


VLQToHiggsAndLeptonHiggsJetCheck::VLQToHiggsAndLeptonHiggsJetCheck(Context & ctx){

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

    // setup modules to check if this event belongs into this category
    string ak8_topjets = "topjets";
    v_pre_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 50, 115));
    v_pre_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx));
    prim_lep_check_module.reset(new HandleSelection<float>(ctx, "primary_lepton_pt", 1.));

    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsHepTopTagCHSPacked_daughters", "n_htags_heptoptag", 
        TopJetId(HEPTopTag())));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, ak8_topjets, "n_htags_toptag", 
        TopJetId(CMSTopTag(CMSTopTag::MassType::groomed))));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, ak8_topjets, "n_htags_toptag_tau32", 
        TopJetId(AndId<TopJet>(CMSTopTag(CMSTopTag::MassType::groomed), Tau32()))));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, ak8_topjets, "n_htags_onebtag", 
        TopJetId(OneBTagHiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, "patJetsCa15CHSJetsFilteredPacked_daughters", "n_htags_filtered", 
        TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(
        ctx, ak8_topjets, "n_htags", 
        TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(
        ctx, "jets", "n_btags", 
        JetId(AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)))));

    const string & category = ctx.get("category", "");

    // higgs tag with filtered jets
    if (category.substr(0, 4) == "CA15") {
        v_cat_modules.emplace_back(new CollectionSizeProducer<TopJet>(
            ctx, "patJetsCa15CHSJetsFilteredPacked_daughters", "n_htags", 
            TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));
    }

    // higgs tag with filtered jets
    if (category == "CA15FilteredCat1htag") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_filtered", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsCa15CHSJetsFilteredPacked_daughters", "h_jets", 
            TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));

    } else if (category == "CA15FilteredCat0h3btag") {
        cat_check_module.reset(new MyAndSelection({
            new HandleSelection<int>(ctx, "n_htags_filtered", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 3)
        }));

    } else if (category == "CA15FilteredCat0h2btag") {
        cat_check_module.reset(new MyAndSelection({
            new HandleSelection<int>(ctx, "n_htags_filtered", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 0, 2)
        }));

    // higgs tag with softdrop jets
    } else if (category == "AK8Cat1htag") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, ak8_topjets, "h_jets", TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));
        if (version.substr(version.size() - 5, 100) == "_Tlep") {
            gen_hists.reset(new VLQ2HTGenHists(ctx, "GenHists"));
        }

    } else if (category == "AK8SoftDropCat0h3btag") {
        cat_check_module.reset(new MyAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 3)
        }));

    } else if (category == "AK8SoftDropCat0h2btag") {
        cat_check_module.reset(new MyAndSelection({
            new HandleSelection<int>(ctx, "n_htags", 0, 0),
            new HandleSelection<int>(ctx, "n_btags", 0, 2)
        }));

    // other categories
    } else if (category == "CA15CatHEPtoptag") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_heptoptag", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, "patJetsHepTopTagCHSPacked_daughters", "h_jets", TopJetId(HEPTopTag())));

    } else if (category == "AK8Cat1htagWith1b") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_onebtag", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, ak8_topjets, "h_jets", TopJetId(OneBTagHiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))));

    } else if (category == "AK8Cat1CMStoptag") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_toptag", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, ak8_topjets, "h_jets", TopJetId(CMSTopTag(CMSTopTag::MassType::groomed))));

    } else if (category == "AK8Cat1CMStoptagTau32") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_toptag_tau32", 1));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, ak8_topjets, "h_jets", TopJetId(AndId<TopJet>(CMSTopTag(CMSTopTag::MassType::groomed), Tau32()))));

    } else if (category == "NoCat") {
        cat_check_module.reset(new HandleSelection<int>(ctx, "n_htags_onebtag", 0));
        v_cat_modules.emplace_back(new CollectionProducer<TopJet>(
            ctx, ak8_topjets, "h_jets", TopJetId(is_true<TopJet>)));

    // a category must be givenf
    } else {
        assert(false);  
    }

    // setup modules to prepare the event.
    // weights
    v_cat_modules.emplace_back(new MCLumiWeight(ctx));
    v_cat_modules.emplace_back(new MCPileupReweight(ctx));
    v_cat_modules.emplace_back(new SpikeProtection());

    // leptons
    v_cat_modules.emplace_back(new ElectronCleaner(PtEtaCut(25.0, 2.4)));
    v_cat_modules.emplace_back(new MuonCleaner(PtEtaCut(25.0, 2.4)));
    v_cat_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));

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
        ctx, "h_jets", "h_mass_topjet"));

    // event variables
    v_cat_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_cat_modules.emplace_back(new STCalculator(ctx, "ST", JetId(PtEtaCut(0., 2.4))));
    v_cat_modules.emplace_back(new STCalculator(ctx, "STgt40", JetId(PtEtaCut(40., 2.4))));
    // v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "", "", "es_", 2., 100));
    // v_pre_modules.emplace_back(new EventShapeVariables(ctx, "jets", "electrons", "muons", "es_plus_lep_", 2., 100));

    // event reconstruction
    v_cat_modules.emplace_back(new LeadingTopjetLorentzVectorProducer(ctx, "h_jets", "h"));
    v_cat_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "h"));

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
    sel_helper.declare_items_for_output();

    // 3. Set up Hists classes:
    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);

    // insert 2D cut
    unsigned pos_2d_cut = 9;
    sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT, DPT_2D_CUT));
    nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
    cf_hists->insert_step(pos_2d_cut, "2D cut");
    // v_hists.insert(v_hists.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));

    // fat jet hists
    if (category == "NoCat") {
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSel", 2, "topjets"));
        v_hists.emplace_back(new TopJetHists(ctx, "Ak8SoftDropPreSel", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15FilteredPreSel", 2, "patJetsCa15CHSJetsFilteredPacked_daughters"));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15HEPTTPreSel", 2, "patJetsHepTopTagCHSPacked_daughters"));

        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelTau32", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "Ak8SoftDropPreSelTau32", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15FilteredPreSelTau32", 2, "patJetsCa15CHSJetsFilteredPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15HEPTTPreSelTau32", 2, "patJetsHepTopTagCHSPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(Tau32()));

        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(PtEtaCut(400., 2.4)));
        v_hists.emplace_back(new TopJetHists(ctx, "Ak8SoftDropPreSelPt400", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(PtEtaCut(400., 2.4)));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15FilteredPreSelPt400", 2, "patJetsCa15CHSJetsFilteredPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(PtEtaCut(400., 2.4)));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15HEPTTPreSelPt200", 2, "patJetsHepTopTagCHSPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(PtEtaCut(200., 2.4)));

        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400Tau32", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(AndId<TopJet>(Tau32(), PtEtaCut(400., 2.4))));
        v_hists.emplace_back(new TopJetHists(ctx, "Ak8SoftDropPreSelPt400Tau32", 2, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(AndId<TopJet>(Tau32(), PtEtaCut(400., 2.4))));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15FilteredPreSelPt400Tau32", 2, "patJetsCa15CHSJetsFilteredPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(AndId<TopJet>(Tau32(), PtEtaCut(400., 2.4))));
        v_hists.emplace_back(new TopJetHists(ctx, "Ca15HEPTTPreSelPt200Tau32", 2, "patJetsHepTopTagCHSPacked_daughters"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(AndId<TopJet>(Tau32(), PtEtaCut(200., 2.4))));

        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400NHEgt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), NHEgt30()));
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400NHElt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), NHElt30()));
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelTau32NHEgt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(NHEgt30(), Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelTau32NHElt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(NHElt30(), Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400Tau32NHEgt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), NHEgt30(), Tau32()));
        v_hists.emplace_back(new TopJetHists(ctx, "TopJetsPreSelPt400Tau32NHElt30", 2, "topjets"));
        ((TopJetHists*)v_hists.back().get())->set_TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), NHElt30(), Tau32()));
    }

    v_hists.emplace_back(new TopJetHists(ctx, "HiggsJetsPreSel", 2, "h_jets"));
    v_hists.emplace_back(new TopJetHists(ctx, "HiggsJetsPreSelPt400", 2, "h_jets"));
    ((TopJetHists*)v_hists.back().get())->set_TopJetId(TopJetId(PtEtaCut(400., 2.4)));

    // v_hists_after_sel.emplace_back(new ElectronHists(ctx, "SanityCheckEle", true));
    // v_hists_after_sel.emplace_back(new MuonHists(ctx, "SanityCheckMu"));
    v_hists_after_sel.emplace_back(new EventHists(ctx, "SanityCheckEvent"));
    // v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckJets"));
    // v_hists_after_sel.emplace_back(new JetHists(ctx, "SanityCheckFwdJets", 4, "fwd_jets"));

    // signal sample gen hists
    // if (version.substr(version.size() - 4, 100) == "Tlep") {
    //     v_hists.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHists"));
    //     v_hists.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatch"));
    //     v_hists_after_sel.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHistsAfterSel"));
    //     v_hists_after_sel.emplace_back(new VLQ2HTRecoGenMatchHists(ctx, "Chi2SignalMatchAfterSel"));
    // }


    // TODO - adjust lepton pt cut to lowest trigger (should go into every trigger leg and test??)
}


bool VLQToHiggsAndLeptonHiggsJetCheck::process(Event & event) {

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

    if (!prim_lep_check_module->passes(event)) {
        return false;
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
// make sure the VLQToHiggsAndLeptonHiggsJetCheck is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsAndLeptonHiggsJetCheck)
