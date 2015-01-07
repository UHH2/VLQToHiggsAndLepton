#include "UHH2/VLQToHiggsAndLepton/include/VLQToHiggsAndLeptonHists.h"
#include "UHH2/core/include/Event.h"

#include <iostream>

using namespace std;
using namespace uhh2;

VLQToHiggsAndLeptonHists::VLQToHiggsAndLeptonHists(Context & ctx, const string & dirname): Hists(ctx, dirname){
  // book all histograms here
  // jets
  book<TH1F>("N_fwd_jets", "N_{fwd jets}", 20, 0, 20);
  book<TH1F>("fwd_jet_eta", "#eta^{fwd jets}", 40, -5, 5);
  book<TH1F>("fwd_jet_pt", "p_{T}^{fwd jets} [GeV/c]", 40, 0, 200);
  book<TH1F>("fwd_jet_energy", "E^{fwd jets} [GeV/c]", 80, 0, 400);

  // book<TH1F>("N_jets", "N_{jets}", 20, 0, 20);
  book<TH1F>("eta_jet1", "#eta^{jet 1}", 40, -5, 5);
  book<TH1F>("eta_jet2", "#eta^{jet 2}", 40, -5, 5);
  book<TH1F>("eta_jet3", "#eta^{jet 3}", 40, -5, 5);
  book<TH1F>("eta_jet4", "#eta^{jet 4}", 40, -5, 5);

  // leptons
  book<TH1F>("N_mu", "N^{#mu}", 10, 0, 10);
  book<TH1F>("pt_mu", "p_{T}^{#mu} [GeV/c]", 40, 0, 200);
  book<TH1F>("eta_mu", "#eta^{#mu}", 40, -2.1, 2.1);
  book<TH1F>("reliso_mu", "#mu rel. Iso", 40, 0, 0.5);

  // primary vertices
  book<TH1F>("N_pv", "N^{PV}", 50, 0, 50);

  fwd_jets_h = ctx.get_handle<std::vector<Jet> >("fwd_jets");
}


void VLQToHiggsAndLeptonHists::fill(const Event & event){
  // fill the histograms. Please note the comments in the header file:
  // 'hist' is used here a lot for simplicity, but it will be rather
  // slow when you have many histograms; therefore, better
  // use histogram pointers as members as in 'UHH2/common/include/ElectronHists.h'
  
  // Don't forget to always use the weight when filling.
  double weight = event.weight;

  const std::vector<Jet> & fwd_jets = event.get(fwd_jets_h);
  hist("N_fwd_jets")->Fill(fwd_jets.size(), weight);
  for (auto jet: fwd_jets) {
    hist("fwd_jet_eta")->Fill(jet.eta(), weight);
    hist("fwd_jet_pt")->Fill(jet.pt(), weight);
    hist("fwd_jet_energy")->Fill(jet.energy(), weight);
  }

  std::vector<Jet>* jets = event.jets;
  int Njets = jets->size();
  // hist("N_jets")->Fill(Njets, weight);
  
  if(Njets>=1){
    hist("eta_jet1")->Fill(jets->at(0).eta(), weight);
  }
  if(Njets>=2){
    hist("eta_jet2")->Fill(jets->at(1).eta(), weight);
  }
  if(Njets>=3){
    hist("eta_jet3")->Fill(jets->at(2).eta(), weight);
  }
  if(Njets>=4){
    hist("eta_jet4")->Fill(jets->at(3).eta(), weight);
  }

  int Nmuons = event.muons->size();
  hist("N_mu")->Fill(Nmuons, weight);
  for (const Muon & thismu : *event.muons){
      hist("pt_mu")->Fill(thismu.pt(), weight);
      hist("eta_mu")->Fill(thismu.eta(), weight);
      hist("reliso_mu")->Fill(thismu.relIso(), weight);
  }
  
  int Npvs = event.pvs->size();
  hist("N_pv")->Fill(Npvs, weight);
}

VLQToHiggsAndLeptonHists::~VLQToHiggsAndLeptonHists(){}
