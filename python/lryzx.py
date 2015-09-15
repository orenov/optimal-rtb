#!/usr/bin/python
import sys
import random
import math
import operator
import yaml
import os
from utils_metrics import *


def convert_to_ints(s):
    res = [int(ss) for ss in s]
    return res

class OnlineLogisticRegression:
    def __init__(self, eta, lamb, initWeight):
        self.eta        = eta
        self.lamb       = lamb
        self.initWeight = initWeight
        self.featWeight = {}

    def __sigmoid(self, p):
        return 1.0 / (1.0 + math.exp(-p))

    def __nextInitWeight(self):
        return (random.random() - 0.5) * self.initWeight

    def update(self, data, pred, actual):
        for i in range(0, len(data)):
            feat = data[i]
            self.featWeight[feat] = self.featWeight * (1 - self.lamb) + self.eta * (actual - pred)

        return(0)

    def predict(self, data):
        pred = 0.0
        for i in range(0, len(data)):
            feat = data[i]
            if feat not in self.featWeight:
                self.featWeight[feat] = self.nextInitWeight()
            pred += self.featWeight[feat]
        pred = sigmoid(pred)

        return(pred)

    def getWeights(self):
        return(self.featWeight)

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
    trainRounds   = config["logit"]["trainRounds"]
    initWeight    = config["logit"]["initWeight"]
    random.seed(config["logit"]["randomSeed"])

    olr = OnlineLogisticRegression(eta, lamb, initWeight)

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
                    clk  = train_obs[0]
                    mp   = train_obs[1]
                    pred = olr.predict(train_obs[2:])
                    olr.update(train_obs[2:], pred, clk)
                trainData = []

        if len(trainData) > 0:
            for train_obs in trainData:
                clk  = train_obs[0]
                mp   = train_obs[1]
                pred = olr.predict(train_obs[2:])
                olr.update(train_obs[2:], pred, clk)
        fi.close()

        # test for this round
        y  = []
        yp = []
        fi = open(sys.argv[2], 'r')
        for line in fi:
            data_obs  = convert_to_ints(line.replace(":1", "").split())
            pred = olr.predict(data_obs[2:])
            clk  = data_obs[0] 
            y.append(clk)
            yp.append(pred)
        fi.close()
        auc  = auc_roc_score(y, yp)
        rmse = math.sqrt(mse(y, yp))
        print str(round) + '\t' + str(auc) + '\t' + str(rmse)

    # output the weights
    fo = open(sys.argv[1] + '.lr.weight', 'w')
    featvalue = sorted(olr.getWeights().iteritems(), key = operator.itemgetter(0))
    for fv in featvalue:
        fo.write(str(fv[0]) + '\t' + str(fv[1]) + '\n')
    fo.close()


    # output the prediction
    fi = open(sys.argv[2], 'r')
    fo = open(sys.argv[2] + '.lr.pred', 'w')

    for line in fi:
        data = convert_to_ints(line.replace(":1", "").split())
        pred = olr.predict(data[1:])
        fo.write(str(pred) + '\n')    
    fo.close()
    fi.close()



