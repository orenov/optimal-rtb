import bz2
import sys
from csv import DictReader

if __name__ == '__main__':
    folders = ["1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476"]
    path    = "../../make-ipinyou-data/"

    with open('bid_price_click_train.csv', 'w') as output:
        output.write('IsClick,BidPrice,PayingPrice,Campaign\n')
        for folder in folders:
            source = path + folder + "/train.log.txt"
	    print("Source file: {0}".format(source))
            for t, line in enumerate(DictReader(open(source), delimiter='\t')):
                output.write('%s,%s,%s,%s\n' % (str(line['click']), str(line['bidprice']), str(line['payprice']), folder))

    with open('bid_price_click_test.csv', 'w') as output:
	output.write('IsClick,BidPrice,PayingPrice,Campaign\n')
	for folder in folders:
	    source = path + folder + "/test.log.txt"
	    print("Source file: {0}".format(source))
	    for t, line in enumerate(DictReader(open(source), delimiter = '\t')):
		output.write('%s,%s,%s,%s\n' % (str(line['click']), str(line['bidprice']), str(line['payprice']), folder))







