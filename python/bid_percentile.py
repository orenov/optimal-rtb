import bz2
import sys
import numpy as np
from csv import DictReader

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: train.yzx.txt'
        exit(-1)

    file_all_name = "../../make-ipinyou-data/" + str(sys.argv[1]) + "/train.log.txt"
    arr = []
        
    for t, line in enumerate(DictReader(open(file_all_name), delimiter='\t')):
        arr.append(line['payprice'])
    arr = np.array(arr, np.float)
    per = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
    qua = np.percentile(arr, per)

    print("--- Percentiles For Campaign {0}---- ".format(sys.argv[1]))
    print(per)
    print("--- Values For Campaign {0} ----".format(sys.argv[1]))
    print(qua)


