#!/usr/bin/python
import sys
import random
import math
import os
import yaml
import itertools
import datadrivenbidder

random.seed(10)

def bidding_const(bid):
    return bid

def bidding_rand(upper):
    return int(random.random() * upper)

def bidding_mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def bidding_lin(pctr, base_ctr, base_bid):
    return int(pctr * base_bid / base_ctr)

def win_auction(case, bid):
    return bid > case[1]  # bid > winning price

def bidding_ortb1(pctr, para):
    c, multiplier = para
    sq = math.sqrt(c * pctr/float(multiplier) + c**2) - c
    return int(sq)

def bidding_ortb2(pctr, para):
    c, multiplier = para
    c = float(c)
    multiplier  = float(multiplier)
    s1 = (pctr + math.sqrt((c*multiplier)**2 + pctr**2)) / (c * multiplier)
    s2 = (c * multiplier) / (pctr + math.sqrt((c*multiplier)**2 + pctr**2))
    sq = c * (s1**(1./3) - s2**(1./3))
    return int(sq)

# budgetProportion clk cnv bid imp budget spend para
def simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion, algo, para):
    budget = int(tcost / proportion) # intialise the budget
    cost = 0
    clks = 0
    bids = 0
    imps = 0
    
    for idx in range(0, len(cases)):
        bid = 0
        pctr = ctrs[idx]
        if algo == "const":
            bid = bidding_const(para)
        elif algo == "rand":
            bid = bidding_rand(para)
        elif algo == "mcpc":
            bid = bidding_mcpc(original_ecpc, pctr)
        elif algo == "lin":
            bid = bidding_lin(pctr, original_ctr, para)
        elif algo == "ortb1":
            c, lamb = para
            bidder  = datadrivenbidder.DD_ORTB1(c, lamb)
            bid     = bidder.bidding(pctr) 
        elif algo == "ortb2":
            c, lamb = para
            bidder  = datadrivenbidder.DD_ORTB2(c, lamb)
            bid     = bidder.bidding(pctr)
        else:
            print 'wrong bidding strategy name'
            sys.exit(-1)
        bids += 1
        case = cases[idx]
        if win_auction(case, bid):
            imps += 1
            clks += case[0]
            cost += case[1]
        if cost > budget:
            break
    return str(proportion) + '\t' + str(clks) + '\t' + str(bids) + '\t' + \
        str(imps) + '\t' + str(budget) + '\t' + str(cost) + '\t' + algo + '\t' + str(para)

def simulate_one_bidding_strategy(cases, ctrs, tcost, proportion, algo, writer):
    paras = algo_paras[algo]
    for para in paras:
        res = simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion, algo, para)
        print res
        writer.write(res + '\n')


if len(sys.argv) < 5:
    print 'Usage: python rtb-test.py train.yzx.txt test.yzx.txt test.yzx.txt.lr.pred rtb.result.txt'
    exit(-1)


with open('../config.yaml', 'r') as f:
    config = yaml.load(f)

max_bid        = config["bidprice"]["maximumbid"]
clicks_prices  = []  # clk and price
pctrs          = []  # pCTR from logistic regression prediciton
total_cost     = 0   # total original cost during the test data
original_ecpc  = 0.  # original eCPC from train data
original_ctr   = 0.  # original ctr from train data
data_for_ddrtb = []
# read in train data for original_ecpc and original_ctr
fi      = open(sys.argv[1], 'r') # train.yzx.txt
first   = True
imp_num = 0

data_tr = []

for line in fi:
    s = line.split(' ')
    if first:
        first = False
        continue
    click = int(s[0])  # y
    cost  = int(s[1])  # z
    if cost > max_bid:
        continue
    data_for_ddrtb.append((None, float(cost)))
    imp_num       += 1
    original_ctr  += click
    original_ecpc += cost
    data_tr.append((click, cost))
fi.close()
original_ecpc /= original_ctr
original_ctr  /= imp_num

# Fitting init
class_ortb1 = datadrivenbidder.DD_ORTB1()
class_ortb2 = datadrivenbidder.DD_ORTB2()
class_ortb1.batch_fit(data_for_ddrtb)
class_ortb2.batch_fit(data_for_ddrtb)

constant = datadrivenbidder.const_bidder()
constant.fit(data_tr)
print("Best param = {0}, Best score = {1}".foramt(constant.constbid, constant.best_score))


# read in test data
fi = open(sys.argv[2], 'r') # test.yzx.txt
for line in fi:
    s = line.split(' ')
    click = int(s[0])
    winning_price = int(s[1])
    clicks_prices.append((click, winning_price))
    total_cost += winning_price
fi.close()

# read in pctr from logistic regression
fi = open(sys.argv[3], 'r')  # test.yzx.txt.lr.pred
for line in fi:
    pctrs.append(float(line.strip()))
fi.close()

# parameters setting for each bidding strategy
budget_proportions = [64, 32]  # , 32, 8]
const_paras     = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)
rand_paras      = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)
mcpc_paras      = [1]
lin_paras       = range(2, 20, 2) + range(20, 100, 5) + range(100, 400, 10) + range(400, 800, 50)

best_c          = class_ortb1.getC()
list_lambd      = [x * 1E-07 for x in range(1, 100)]
ortb1_paras     = [(best_c, x) for x in list_lambd]
ortb2_paras     = [(best_c, x) for x in list_lambd]

algo_paras = {"const" : const_paras, "rand"  : rand_paras,
              "mcpc"  : mcpc_paras,  "lin"   : lin_paras,
              "ortb1" : ortb1_paras, "ortb2" : ortb2_paras}

# initalisation finished
# rock!

fo = open(sys.argv[4], 'w')  # rtb.results.txt
#header = "proportion\tclicks\tbids\timpressions\tbudget\tspend\tstrategy\tparameter"
header = "prop\tclks\tbids\timps\tbudget\tspend\talgo\tpara"
fo.write(header + "\n")
print header
for proportion in budget_proportions:
    for algo in algo_paras:
        simulate_one_bidding_strategy(clicks_prices, pctrs, total_cost, proportion, algo, fo)
fo.close()
