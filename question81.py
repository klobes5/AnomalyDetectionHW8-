# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:57:57 2015

@author: Kevin Anthony Smith
"""
from scipy.stats import norm
import math


#Read the all history file to calculate the mu0 and sigma0
arrayAll = [[0 for x in range(9)] for x in range(101)]
#arrayAll = []
row = 0
col = 0
with open('/Users/Kevin/Downloads/hw6/data/q8.txt','r+') as file:
    for line in file:
        data = line.split()
        for x in data:
            if col == 9:
                col = 0
                row = row + 1
            arrayAll[row][col] = float(x)
            col = col + 1
        #arrayAll = [float(x) for x in data]
#print arrayAll,'\n'

print arrayAll

## calculate mu0 and sigma0, build the basic normal distribution
def calculateMu0Sigma0(array):
    summary = 0    # the sum of history data
    count = 0
    for i in range(len(array) - 1):
        for j in range(len(array[0])):
            summary += array[i][j]
            count += 1
    avg = summary/count
    print count
    var = 0
    for i in range(len(array) - 1):
        for j in range(len(array[0])):
            var += (array[i][j] - avg)**2
    var = var / count
    std = (var)**(.5)
    return avg,std
            
mu0, sigma0 = calculateMu0Sigma0(arrayAll)
print "mu0 : ",mu0," sigma0 : ",sigma0
   
dist0 = norm(mu0,sigma0)   

alpha = 0.05
print 'left side test'
cutoff = dist0.ppf(alpha)
print 'critical region: (-oo,{0}'.format(cutoff),']'

# define a function to calculate each mu1 but the singma is fixed!
def calculateMuSigma(array):
    summary = 0
    for i in range(len(array)):
        summary += array[i]
    avg = summary/len(array)
    dist1 = norm(avg,sigma0)
    return dist1

#define a function to calculate LLR
def calculateLLR(array,dist0,dist1):
    LLR = 0
    for i in range(len(array)):
        LLR += (math.log(dist1.pdf(array[i]))- math.log(dist0.pdf(array[i])))
    return LLR
    

## print the LLR for history
def printArray(array):
    for i in range(len(array)):
        print '\n'
        for j in range(len(array[0])):
            print round(array[i][j],3),


#define a function to find the maximum value for each row.
def findMax(array):
    tempArr = []
    for i in range(len(array)):
        tempArr += [round(max(array[i]),3)]
    print tempArr
#    print "length of Max array : ",len(tempArr)
    return tempArr
#        print round(max(array[i]),3),
    #print array,
    
    
##find how many bigger than the best score in data new
def findCount(array):
    count = 0
    print "the max value of LLR dataNew: ",array[len(array) - 1]
    for i in range(len(array) - 1):
        if(array[i] < array[len(array) - 1]):
            print array[i]
            count += 1
    print "count: ",count

        
def possible_subsets():
    subsets = []
    for i in range(3):
        for j in range(3):
            for k in range(i, 3):
                for l in range(j, 3):
                    S = []
                    for a in range(i, k+1):
                        for b in range(j, l+1):
                            S.append(a * 3 + b)
                    subsets.append(S)
    
    all_nodes = []
    for i in range(3):
        for j in range(3):
            all_nodes.append(i * 3 + j)
    return subsets 

subsets = possible_subsets() # save it for indecs

#print subsets

arrayTemp=[[0 for x in range(36)] for x in range(101)]
def prepareAllPossibleSubset():
    for i in range(len(arrayAll)):
        for j in range(len(subsets)):
            temp = []
            for k in range(len(subsets[j])):
                temp += [arrayAll[i][subsets[j][k]]]
            arrayTemp[i][j] = temp

prepareAllPossibleSubset()
## calculate the LLR for history data.
LLRArr = [[0 for x in range(36)] for x in range(101)]
for i in range(len(arrayTemp)):
    for k in range(len(arrayTemp[i])):
        TempArr = []
        TempArr = arrayTemp[i][k]
        distTemp = calculateMuSigma(TempArr)
        LLRArr[i][k] = round(calculateLLR(TempArr,dist0,distTemp),3)

print "Final LLR : "        
for arr in LLRArr:
    print arr
        
#print len(arrayTemp) 
#print len(arrayTemp[0])    

## all possible subsets from history data.
#print arrayTemp

print "All possible rectangle subsets:"
for subset in subsets:
    print subset

MaxLLRArr = findMax(LLRArr)
print MaxLLRArr
print len(MaxLLRArr)
findCount(MaxLLRArr)
"""
print "\n All data include the new data: "
printArray(arrayAll)
print "\n History Data LLR : "
printArray(LLRArr)
print "count for Hist LLR"
print len(LLRArr)
"""
