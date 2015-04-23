#pragma once

#include "UHH2/core/include/fwd.h"
#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Selection.h"
#include <string>
#include <stdexcept>


template<typename HANDLETYPE>
class HandleSelection: public uhh2::Selection {
public:
    explicit HandleSelection(uhh2::Context & ctx,
                             const std::string & handlename,
                             HANDLETYPE min_val=-99999.0,
                             HANDLETYPE max_val=99999.0):
        name_(handlename),
        hndl(ctx.get_handle<HANDLETYPE>(handlename)),
        min_(min_val),
        max_(max_val) {}

    virtual bool passes(const uhh2::Event & e) override {
        if (!e.is_valid(hndl)) {
            return false;
        }
        HANDLETYPE value = e.get(hndl);
        return min_ <= value && value <= max_;
    }

    const std::string &name() const {return name_;}

private:
    std::string name_;
    uhh2::Event::Handle<HANDLETYPE> hndl;
    HANDLETYPE min_;
    HANDLETYPE max_;
};
