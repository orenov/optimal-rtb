#------------------------------------------------------------------------------------------------------------------------------
#    simple metrics
#------------------------------------------------------------------------------------------------------------------------------
import math

def se(actual, predicted):
    # Elementwise squared error
    if len(actual) != len(predicted):
        print("Lengths of predictions/actuals are different")
    temp = [0] * len(actual)
    for i in range(0, len(actual)):
        temp[i] = (actual[i] - predicted[i])^2

    return(temp)

def mse(actual, predicted):
    # Mean Squared Error
    temp = se(actual, predicted)

    return(sum(temp) / float(len(actual)))

def rmse(actual, predicted):
    # Root Mean Squared Error
    return(math.sqrt(mse(actual, predicted)))

def ae(actual, predicted):
    # Elementwise absolute error
    if len(actual) != len(predicted):
        print("Lengths of predictions/actuals are different")
    temp = [0] * len(actual)
    for i in range(0, len(actual)):
        temp[i] = abs(actual[i] - predicted[i])

    return(temp)

def mae(actual, predicted):
    # Mean Aboslute Error
    temp = ae(actual, predicted)
    return(sum(temp) / float(len(actual)))

def sle(actual, predicted):
    # Elementwise squared log error
    # sle   = function (actual, predicted) (log(1+actual)-log(1+predicted))^2
    if len(actual) != len(predicted):
        print("Lengths of predictions/actuals are different")
    temp = [0] * len(actual)
    for i in range(0, len(actual)):
        temp[i] = (math.log(1 + actual[i]) - math.log(1 + predicted[i]))^2

    return(temp)


def msle(actual, predicted):
    # Mean Squarel Log Error
    # msle  = function (actual, predicted) mean(sle(actual, predicted))
    temp = sle(actual, predicted)
    return(sum(temp) / float(len(actual)))

def rmsle(actual, predicted):
    # Root Mean Squared Log Error
    # rmsle = function (actual, predicted) sqrt(msle(actual, predicted))
    temp = msle(actual, predicted)
    return(math.sqrt(temp))

def ce(actual, predicted):
    # Classification error
    if len(actual) != len(predicted):
        print("Lengths of predictions/actuals are different")
    temp = [0] * len(actual)
    for i in range(0, len(actual)):
        temp[i] = 1 * (actual[i] == predicted[i])

    return(sum(temp) / float(len(actual)))

def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

def rankdata(a):
    n = len(a)
    ivec = rank_simple(a)
    svec = [a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0]*n
    for i in xrange(n):
        sumranks += i
        dupcount += 1
        if i == n - 1 or svec[i] != svec[i + 1]:
            averank = sumranks / float(dupcount) + 1
            for j in xrange(i - dupcount + 1, i + 1):
                newarray[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return newarray


def auc(actual, predicted):
    r     = rankdata(predicted)
    n_pos = sum(actual) 
    n_neg = len(actual) - n_pos
    auc   = (sum([r[i] for i in range(0,len(actual)) if actual[i] == 1]) - n_pos * (n_pos + 1)/2) / (n_pos * n_neg)
    
    return(auc)


# TODO implement rse
# TODO implement rrse
# TODO implement rae
# TODO implement ce
# TODO implement logloss
# TODO implement f1
# TODO implement apk
# TODO implement mapk
# TODO implement qwKappa
# TODO implement mqwKappa


















