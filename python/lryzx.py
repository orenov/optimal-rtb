#!/usr/bin/python
import sys
import random
import math
import operator
import yaml
import os
from utils_metrics import *


def nextInitWeight():
    return (random.random() - 0.5) * initWeight

def convert_to_ints(s):
    res = [int(ss) for ss in s]
    return res

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))

def train_update_lr(data):
    clk  = data[0]
    mp   = data[1]
    fsid = 2 # feature start id # predict part
    pred = 0.0
    for i in range(fsid, len(data)):
        feat = data[i]
        if feat not in featWeight:
            featWeight[feat] = nextInitWeight()
        pred += featWeight[feat]
    pred = sigmoid(pred)
    # start to update weight
    # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ] 
    for i in range(fsid, len(data)):
        feat = data[i]
        featWeight[feat] = featWeight[feat] * (1 - lamb) + eta * (clk - pred) 
    return(0)

def predict(data):
    mp   = data[1]
    fsid = 2 # feature start id
    pred = 0.0
    for i in range(fsid, len(data)):
        feat = data[i]
        if feat in featWeight:
            pred += featWeight[feat]
    pred = sigmoid(pred)
    return pred


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: train.yzx.txt test.yzx.txt'
        exit(-1)

    with open('../config.yaml', 'r') as f:
        config = yaml.load(f)

    bufferCaseNum = config["logit"]["buffercase"]
    eta           = config["logit"]["learning_rate"]
    lamb          = config["logit"]["lambda"]
    featWeight    = {}
    trainRounds   = config["logit"]["trainRounds"]
    initWeight    = config["logit"]["initWeight"]
    random.seed(config["logit"]["randomSeed"])

    for round in range(0, trainRounds):
        # train for this round
        fi = open(sys.argv[1], 'r')
        lineNum   = 0
        trainData = []
        for line in fi:
            lineNum = (lineNum + 1) % bufferCaseNum
            trainData.append(convert_to_ints(line.replace(":1", "").split())) # orenov: why replace?
            if lineNum == 0:
                for train_obs in trainData:
                    train_update_lr(train_obs)
                trainData = []

        if len(trainData) > 0:
            for train_obs in trainData:
                train_update_lr(train_obs)
        fi.close()

        # test for this round
        y  = []
        yp = []
        fi = open(sys.argv[2], 'r')
        for line in fi:
            data_obs  = convert_to_ints(line.replace(":1", "").split())
            pred = predict(data_obs)
            clk  = data_obs[0] 
            y.append(clk)
            yp.append(pred)
        fi.close()
        auc  = auc_roc_score(y, yp)
        rmse = math.sqrt(mse(y, yp))
        print str(round) + '\t' + str(auc) + '\t' + str(rmse)

    # output the weights
    fo = open(sys.argv[1] + '.lr.weight', 'w')
    featvalue = sorted(featWeight.iteritems(), key = operator.itemgetter(0))
    for fv in featvalue:
        fo.write(str(fv[0]) + '\t' + str(fv[1]) + '\n')
    fo.close()


    # output the prediction
    fi = open(sys.argv[2], 'r')
    fo = open(sys.argv[2] + '.lr.pred', 'w')

    for line in fi:
        data = convert_to_ints(line.replace(":1", "").split())
        pred = 0.0
        for i in range(1, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        fo.write(str(pred) + '\n')    
    fo.close()
    fi.close()



