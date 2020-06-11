#===============================================================================
#                               Export Functions
#===============================================================================
import csv
import json

from . import Global

class NameFile():
    """
    Functions for naming the exported files.
    """

    ### Initialize objects that will be used in class methods.
    def __init__(self):
        self._illegal_chars = Global.illegal_chars

    ### Fix f_name if illegal filename characters are present.
    def _fix(self, name):
        fixed = ["_" if char in self._illegal_chars else char for char in name]
        return "".join(fixed)

    ### Category name switch.
    def _r_category(self, cat_i, category_n):
        switch = {
            0: Global.categories[5],
            1: Global.categories[Global.short_cat.index(cat_i)] \
                if cat_i != Global.short_cat[5] and isinstance(cat_i, str) \
                    else None,
            2: Global.categories[cat_i] \
                if isinstance(cat_i, int) \
                    else None
        }

        return switch.get(category_n)

    ### Choose category name.
    def _r_get_category(self, args, cat_i):
        if args.subreddit:
            category_n = 0 if cat_i == Global.short_cat[5] else 1
        elif args.basic:
            category_n = 2

        return category_n

    ### Determine file name format for CLI scraper.
    def _get_raw_n(self, args, cat_i, end, search_for, sub):
        category_n = self._r_get_category(args, cat_i)
        category = self._r_category(cat_i, category_n)

        return str(("r-%s-%s-'%s'") % (sub, category, search_for)) \
            if cat_i == Global.short_cat[5] \
                else str(("r-%s-%s-%s-%s") % 
                    (sub, category, search_for, end))

    ### Determine file name format for Subreddit scraping.
    def r_fname(self, args, cat_i, search_for, sub):
        raw_n = ""
        end = "result" if isinstance(search_for, int) and int(search_for) < 2 \
            else "results"

        raw_n = self._get_raw_n(args, cat_i, end, search_for, sub)
        f_name = self._fix(raw_n)

        return f_name

    ### Determine file name format for Redditor scraping.
    def u_fname(self, limit, string):
        end = "result" if int(limit) < 2 else "results"
        raw_n = str(("u-%s-%s-%s") % (string, limit, end))
        return self._fix(raw_n)

    ### Determine file name format for comments scraping.
    def c_fname(self, limit, string):
        if int(limit) != 0:
            end = "result" if int(limit) < 2 else "results"
            raw_n = str(("c-%s-%s-%s") % (string, limit, end))
        else:
            raw_n = str(("c-%s-%s") % (string, "RAW"))
        
        return self._fix(raw_n)

class Export():
    """
    Functions for creating directories and export the file.
    """

    ### Export to CSV.
    @staticmethod
    def _write_csv(filename, overview):
        with open(filename, "w", encoding = "utf-8") as results:
            writer = csv.writer(results, delimiter = ",")
            writer.writerow(overview.keys())
            writer.writerows(zip(*overview.values()))

    ### Export to JSON.
    @staticmethod
    def _write_json(filename, overview):
        with open(filename, "w", encoding = "utf-8") as results:
            json.dump(overview, results, indent = 4)
        
    ### Write overview dictionary to CSV or JSON.
    @staticmethod
    def export(f_name, f_type, overview):
        dir_path = "../scrapes/%s" % Global.date

        filename = dir_path + "/%s.json" % f_name if f_type == Global.eo[1] else \
            dir_path + "/%s.csv" % f_name

        Export._write_json(filename, overview) if f_type == Global.eo[1] else \
            Export._write_csv(filename, overview)
