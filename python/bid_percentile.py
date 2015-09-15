import bz2
import sys
import numpy as np
from csv import DictReader

if __name__ == '__main__':
    file_all_name = "../../make-ipinyou-data/all/train.log.txt"
    arr = []
    with open(file_all_name, 'r') as f:
        next(f)
        for t, line in enumerate(DictReader(open(test), delimiter=',')):
            arr.append(line['payprice'])

    per = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
    qua = np.percentile(arr, per)

    print("--- Percentiles ---- ")
    print(per)
    print("--- Values ----")
    print(qua)


