import bz2
import sys

if __name__ == '__main__':
    folders = ["1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476"]
    path    = "../../make-ipinyou-data/"

    with open('bid_price_click.csv', 'w') as output:
        output.write('IsClick, BidPrice, PayingPrice, Campaign\n')
        for folder in folders:
            source = path + folder + "/train.log.txt"
            for t, line in enumerate(DictReader(open(source), delimiter=',')):
                output.write('%s,%s,%s,%s\n' % (str(line['click']), str(line['bidprice'], str(line['payprice'])), folder))








