import bz2
import sys

def compute_coverage(folder, bids_files, imp_files):
    counter_bids = 0
    counter_imps = 0
    for bid_file in bids_files:    
        source_file = bz2.BZ2File("../../make-ipinyou-data/original-data/ipinyou.contest.dataset/" + folder + "/" + bid_file , "r") 
        for line in source_file: 
            counter_bids += 1
        print("File {0} counting finished".format(bid_file))
    
    print("Bids counter = {0}".format(counter_bids))

    for imp_file in imp_files:    
        source_file = bz2.BZ2File("../../make-ipinyou-data/original-data/ipinyou.contest.dataset/" + folder + "/" + imp_file , "r") 
        for line in source_file: 
            counter_imps += 1
        print("File {0} counting finished".format(imp_file))

    print("Imps counter = {0}".format(counter_imps))
    cover = float(counter_imps)/counter_bids
    print("Stock Coverage = {0}".format(cover))
    string = "Bids count = {0}, Imps count = {1}, Stock coverage = {2}".format(counter_bids, counter_imps, cover)

    return(string)

if __name__ == '__main__':
    # Season 1 data
    bids_files1   = ["bid.20130311.txt.bz2", "bid.20130312.txt.bz2", "bid.20130313.txt.bz2", "bid.20130314.txt.bz2",
                     "bid.20130315.txt.bz2", "bid.20130316.txt.bz2", "bid.20130317.txt.bz2"]
    imp_files1    = ["imp.20130311.txt.bz2", "imp.20130312.txt.bz2", "imp.20130313.txt.bz2", "imp.20130314.txt.bz2",
                     "imp.20130315.txt.bz2", "imp.20130316.txt.bz2", "imp.20130317.txt.bz2"]
    folder_files1 = "training1st"
    # Season 2 data
    bids_files2   = ["bid.20130606.txt.bz2", "bid.20130607.txt.bz2", "bid.20130608.txt.bz2", "bid.20130609.txt.bz2",
                     "bid.20130610.txt.bz2", "bid.20130611.txt.bz2", "bid.20130612.txt.bz2"]
    imp_files2    = ["imp.20130606.txt.bz2", "imp.20130607.txt.bz2", "imp.20130608.txt.bz2", "imp.20130609.txt.bz2",
                     "imp.20130610.txt.bz2", "imp.20130611.txt.bz2", "imp.20130612.txt.bz2"]
    folder_files2 = "training2nd"
    # Season 3 data
    bids_files3   = ["bid.20131019.txt.bz2", "bid.20131020.txt.bz2", "bid.20131021.txt.bz2", "bid.20131022.txt.bz2",
                     "bid.20131023.txt.bz2", "bid.20131024.txt.bz2", "bid.20131025.txt.bz2",
                     "bid.20131026.txt.bz2", "bid.20131027.txt.bz2", "bid.20131028.txt.bz2"]
    imp_files3    = ["imp.20131019.txt.bz2", "imp.20131020.txt.bz2", "imp.20131021.txt.bz2", "imp.20131022.txt.bz2",
                     "imp.20131023.txt.bz2", "imp.20131024.txt.bz2", "imp.20131025.txt.bz2",
                     "imp.20131026.txt.bz2", "imp.20131027.txt.bz2"]
    folder_files3 = "training3rd"
    #Dict for saving presentages
    res = {}

    res["Season1"] = compute_coverage(folder_files1, bids_files1, imp_files1)
    res["Season2"] = compute_coverage(folder_files2, bids_files2, imp_files2)
    res["Season3"] = compute_coverage(folder_files3, bids_files3, imp_files3)

    print(res)






