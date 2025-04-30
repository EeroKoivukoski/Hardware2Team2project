import math
import test

def calculate(ppis):
    meanppi=calc_meanppi(ppis)
    meanhrv=calc_meanhrv(ppis,meanppi)
    rmssd=calc_rmssd(ppis)
    sdnn="wip"
    sns="wip"
    pns="wip"
    return [meanhrv,
            meanppi,
            rmssd,
            sdnn,
            sns,
            pns]
#calculate mean heart rate value
def calc_meanhrv(ppis,meanppi):
    meanhrv = 60/(meanppi/1000)
    return meanhrv

#calculate mean ppi
def calc_meanppi(ppis):
    sum = 0
    for i in ppis:
        sum += i
    meanppi = sum/len(ppis)
    return meanppi

#calculate rmssd
def calc_rmssd(ppis):
    diff = listdiff(ppis)
    squarediff = [j**2 for j in diff]
    meansquared = sum(squarediff) / len(squarediff)
    rmssd = math.sqrt(meansquared)
    return rmssd

def listdiff(ppis):
    return [ppis[i+1] - ppis[i] for i in range(len(ppis)-1)]


#long ahh rmssd calculation ting function (difference between peaks squared then the average of that square-rooted or something)