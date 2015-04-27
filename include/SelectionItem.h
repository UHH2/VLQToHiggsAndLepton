#pragma once

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Hists.h"
#include "UHH2/VLQToHiggsAndLepton/include/HandleSelection.h"
#include "UHH2/VLQToHiggsAndLepton/include/HandleHist.h"


using namespace std;
using namespace uhh2;


class SelectionItem {
public:
    virtual Selection * make_selection(Context & ctx) const = 0;
    virtual Hists * make_hists(Context & ctx, const string & dir) const = 0;
    const string & name() const {return name_;}

protected:
    string name_;
};


template<typename DATATYPE>
class SelectionItemData : public SelectionItem {
public:
    SelectionItemData(string name, string title, int n_bins, float x_min, float x_max,
                      DATATYPE min_val=-99999.0, DATATYPE max_val=99999.0):
        title_(title), n_bins_(n_bins), x_min_(x_min), x_max_(x_max),
        min_val_(min_val), max_val_(max_val) {name_ = name;}

    virtual Selection * make_selection(Context & ctx) const override {
        return new HandleSelection<DATATYPE>(ctx, name_, min_val_, max_val_);
    }

    virtual Hists * make_hists(Context & ctx, const string & dir) const override {
        // TODO pass title with _%g(min)_to_%g(max)
        return new HandleHist<DATATYPE>(ctx, dir, name_, title_.c_str(), n_bins_, x_min_, x_max_);
    }

private:
    string title_;
    int n_bins_;
    float x_min_;
    float x_max_;
    DATATYPE min_val_;
    DATATYPE max_val_;
};

class SelItemsHelper {
public:
    SelItemsHelper(const vector<unique_ptr<SelectionItem>> & sel_items,
                   Context & context,
                   const vector<string> & names = vector<string>()):
        items(sel_items),
        ctx(context),
        item_names(names.size() ? names : all_item_names())
    {}

    const vector<string> & get_item_names() const {
        return item_names;
    }

    const vector<string> & all_item_names() const {
        static vector<string> v;
        if (!v.size()) {
            for (const auto & it: items) {
                v.push_back(it->name());
            }
        }
        return v;
    }

    const SelectionItem * get_sel_item(const string & name) const {
        static map<string, SelectionItem*> m;
        if (!m.size()) {
            for (const auto & it: items) {
                m[it->name()] = it.get();
            }
        }
        if (m.count(name)) {
            return m[name];
        } else {
            return NULL;
        }
    }

    void fill_hists_vector(vector<unique_ptr<Hists>> & target,
                          const string & dir) const {
        for (const auto & name: item_names) {
            target.emplace_back(get_sel_item(name)->make_hists(ctx, dir));
        }
    }

    void fill_sel_vector(vector<unique_ptr<Selection>> & target) const {
        for (const auto & name: item_names) {
            target.emplace_back(get_sel_item(name)->make_selection(ctx));
        }
    }

private:
    const vector<unique_ptr<SelectionItem>> & items;
    Context & ctx;
    const vector<string> & item_names;
};


class SelectionProducer: public AnalysisModule {
public:
    explicit SelectionProducer(Context & ctx,
                             const SelItemsHelper & sel_helper):
        h_sel_res(ctx.get_handle<vector<bool>>("sel_accept"))
    {
        sel_helper.fill_sel_vector(v_sel);
    }

    virtual bool process(Event & event) override {
        bool all_accepted = true;
        vector<bool> v_accept(v_sel.size());
        for (unsigned i=0; i<v_sel.size(); ++i) {
            bool accept = v_sel[i]->passes(event);
            v_accept[i] = accept;
            if (!accept) {
                all_accepted = false;
            }
        }
        event.set(h_sel_res, v_accept);
        return all_accepted;
    }

private:
    vector<unique_ptr<Selection>> v_sel;
    Event::Handle<vector<bool>> h_sel_res;
};