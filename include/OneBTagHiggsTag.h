#pragma once

#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/JetIds.h"


namespace {

class OneBTagHiggsTag {
public:
    explicit OneBTagHiggsTag(float minmass = 60.f, 
    				  		 float maxmass = std::numeric_limits<float>::infinity(), 
    				  		 JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM)) :
        minmass_(minmass), maxmass_(maxmass), btagid_(id) {}

    bool operator()(TopJet const & topjet, uhh2::Event const & event) const;

private:
    float minmass_, maxmass_;
    JetId btagid_;

};  // OneBTagHiggsTag


bool OneBTagHiggsTag::operator()(TopJet const & topjet, uhh2::Event const & event) const {
    auto subjets = topjet.subjets();
    if(subjets.size() < 2) return false;
    sort_by_pt(subjets);
    if (!(btagid_(subjets[0], event) || btagid_(subjets[1], event))) return false;

    LorentzVector firsttwosubjets = subjets[0].v4() + subjets[1].v4();
    if(!firsttwosubjets.isTimelike()) {
        return false;
    }
    auto mjet = firsttwosubjets.M();
    if(mjet < minmass_) return false;
    if(mjet > maxmass_) return false;
    return true;
}

}
