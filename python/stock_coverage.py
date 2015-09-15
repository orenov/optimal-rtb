import bz2
import sys

if __name__ == '__main__':
    bids_files1   = ["bid.20130311.txt.bz2", "bid.20130312.txt.bz2", "bid.20130313.txt.bz2", "bid.20130314.txt.bz2",
                     "bid.20130315.txt.bz2", "bid.20130316.txt.bz2", "bid.20130317.txt.bz2"]
    imp_files1    = ["imp.20130311.txt.bz2", "imp.20130312.txt.bz2", "imp.20130313.txt.bz2", "imp.20130314.txt.bz2",
                     "imp.20130315.txt.bz2", "imp.20130316.txt.bz2", "imp.20130317.txt.bz2"]
    folder_files1 = "training1st"

    counter_bids = 0
    counter_imps = 0

    for bid_file in bids_files1:    
        source_file = bz2.BZ2File("../../make-ipinyou-data/original-data/ipinyou.contest.dataset/training1st/" + bid_file , "r") 
        for line in source_file: 
            counter_bids += 1
        print("File {0} counting finished".format(bid_file))
    
    print("Bids counter = {0}".format(counter_bids))

    for imp_file in imp_files1:    
        source_file = bz2.BZ2File("../../make-ipinyou-data/original-data/ipinyou.contest.dataset/training1st/" + imp_file , "r") 
        for line in source_file: 
            counter_imps += 1
        print("File {0} counting finished".format(imp_file))

    print("Imps counter = {0}".format(counter_imps))
    print("Stock Coverage = {0}".format(float(counter_imps)/counter_bids))
