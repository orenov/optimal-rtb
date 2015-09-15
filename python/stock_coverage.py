import bz2
import sys

if __name__ == '__main__':
    bids_files1   = ["bid.20130311.txt.bz2", "bid.20130312.txt.bz2", "bid.20130313.txt.bz2", "bid.20130314.txt.bz2",
                     "bid.20130315.txt.bz2", "bid.20130316.txt.bz2", "bid.20130317.txt.bz2"]
    imp_files1    = ["imp.20130311.txt.bz2", "imp.20130312.txt.bz2", "imp.20130313.txt.bz2", "imp.20130314.txt.bz2",
                     "imp.20130315.txt.bz2", "imp.20130316.txt.bz2", "imp.20130317.txt.bz2"]
    folder_files1 = "training1st"

    counter_bids = {}

    with open("../../make-ipinyou-data/1458/train.log.txt", 'r') as f:   
        for line in f: 
            print line
            print len(line.strip().split("\t"))
            sys.exit(1)
        print "Exiting" 
        print "I used file: " + osm_file 
