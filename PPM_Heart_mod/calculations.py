 #oled.fill(0)
    #oled.text("MEAN HR:", 0, 0)
    #oled.text("MEAN PPI:", 0, 10)
    #oled.text("RMSSD:", 0, 20)
    #oled.text("SDNN:", 0, 30)
    #oled.text("SNS:", 0, 40)
    #oled.text("PNS:", 0, 50)
import math
import test
    
beatz = 47
time = 7500
#ppis=[156,154,155,160, 170, 150, 181, 150, 167, 177,156,154,155,160, 170, 150, 181, 150, 167, 177,156,154,155,160, 170, 150, 181, 150, 167, 177,156,154,155,160, 170, 150, 181, 150, 167, 177]
ppis=test.calculate_hr()
count = 0


# "meanhr" is the mean heart rate, take the beats calculated in 30 seconds (7500ms) and times that by 2 (=60 seconds, bpm)

#meanhr = len(ppis) * 2
#print(meanhr)


def meanhrppi(ppis):
    sumppis = 0
    for i in ppis:
        sumppis += i
    meanppi = sumppis/len(ppis)
    meanhr = 60/(meanppi/1000)
    return meanhr, meanppi

def listdiff(ppis):
    return [ppis[i+1] - ppis[i] for i in range(len(ppis)-1)]
# calc ppis together and calc how many of them there are
#for i in ppis:
    #sumppis = sumppis + i
#then if there are more than 0 of them calc the mean
#if len(ppis) > 0:
    #meanppi = sumppis/len(ppis)
    #print(meanppi)

#long ahh rmssd calculation ting function (difference between peaks squared then the average of that square-rooted or something)
def rmssdcalc(ppis):
    diff = listdiff(ppis)
    squarediff = [j**2 for j in diff]
    meansquared = sum(squarediff) / len(squarediff)
    rmssd = math.sqrt(meansquared)
    return rmssd


rmssdvalue = rmssdcalc(ppis)
meanhrppivalue = meanhrppi(ppis)
print("rmssd = ",rmssdvalue, ", mean heart rate and PPI = ", meanhrppivalue) 