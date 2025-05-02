from math import sqrt
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
            sdnn]

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
    diff = calc_ppidiff(ppis)
    squarediff = [j**2 for j in diff]
    meansquared = sum(squarediff) / (len(ppis)-1)
    return sqrt(meansquared)
    

#calculate the differences in peak to peak intervals (ppi) and compile them into a list.
def calc_ppidiff(ppis: list) -> list:
    return [ppis[i+1] - ppis[i] for i in range(len(ppis)-1)]

#calculate sdnn
def calc_sdnn(ppis):
    deviation = 0
    diffs = calc_ppidiff(ppis)
    meandiffs = sum(diffs)/len(diffs)
    #print(meandiffs)
    for z in diffs:
        deviation += (z - meandiffs)**2
    return sqrt(deviation/(len(diffs)-1))

#test
#ppis = [800,750,700,900,950,888,777,999,666,878,800,750,700,900,950,888,777,999,666,878,800,750,700,900,950,888,777,999,666,878]
#print(calculate(ppis))