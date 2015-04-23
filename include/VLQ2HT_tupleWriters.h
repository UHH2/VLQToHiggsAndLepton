#pragma once

#include <ofstream>

#include "UHH2/core/include/fwd.h"
#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"


template<typename HANDLETYPE>
class HandleTxtWriter: public uhh2::AnalysisModule {
public:
    explicit HandleTxtWriter(uhh2::Context & ctx,
                             const std::string & handlename,
                             std::ofstream &filestream):
        name_(handlename),
        ofs_(filestream),
        hndl(ctx.get_handle<HANDLETYPE>(handlename)) {}

    virtual bool process(const uhh2::Event & e) override {
        ofs_ << e.get(hndl) << "\t";
    }

    const std::string &name() const {return name_;}

private:
    std::string name_;
    std::ofstream &ofs_;
    uhh2::Event::Handle<HANDLETYPE> hndl;
};
