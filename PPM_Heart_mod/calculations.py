import math
import test

#call all of the functions and return them in a list
def calculate(ppis):
    meanppi=calc_meanppi(ppis)
    meanhrv=calc_meanhrv(ppis,meanppi)
    rmssd=calc_rmssd(ppis)
    sdnn=calc_sdnn(ppis)
    sns="wip" #sns & pns on kubios
    pns="wip"
    return [meanhrv,
            meanppi,
            rmssd,
            sdnn,
            sns,
            pns]

#calculate mean heart rate value
def calc_meanhrv(ppis,meanppi):
    return 60/(meanppi/1000)
    

#calculate mean ppi
def calc_meanppi(ppis):
    sum = 0
    for i in ppis:
        sum += i
    return sum/len(ppis)
    

#calculate rmssd
def calc_rmssd(ppis):
    meandiff = calc_ppidiff(ppis)
    squarediff = [j**2 for j in meandiff]
    meansquared = sum(squarediff) / len(squarediff)
    return math.sqrt(meansquared)
    

#calculate the differences in peak to peak intervals (ppi) and compile them into a list.
def calc_ppidiff(ppis):
    return [ppis[i+1] - ppis[i] for i in range(len(ppis)-1)]

#calculate sdnn
def calc_sdnn(ppis):
    meandiffs = calc_ppidiff(ppis)
    for z in ppis:
        deviation += (z - meandiffs)**2
    return sqrt(deviation/(len(ppis)-1))
    
