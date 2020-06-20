import numpy as np
import scipy as sp
from scipy.fft import fft, ifft
from scipy import signal #利用升采样功能
from scipy.stats import entropy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import json
from django.http import HttpResponse, JsonResponse
import random

#...........单系列数据操作............#
#获取数据
#Get the data
def getDateInfo():
    gestureData=np.loadtxt("data.csv",delimiter=",")
    indexGesture =gestureData[:,0]
    valueGesture=gestureData[:,1:]
    return indexGesture, valueGesture

def getDataOffline():
    gestureDataFallF=np.loadtxt("../data/fall.csv", delimiter=",")
    gestureDataFallL=np.loadtxt("../data/fallleft.csv", delimiter=",")
    gestureDataFallR=np.loadtxt("../data/fallright.csv", delimiter=",")
    gestureDatajum=np.loadtxt("../data/jump.csv",  delimiter=",")
    gestureDatarun=np.loadtxt("../data/runVer.csv", delimiter=",")
    gestureDataWalkHor=np.loadtxt("../data/walkHor.csv", delimiter=",")
    gestureDataWalkVer=np.loadtxt("../data/walkVer.csv", delimiter=",")
    # a=(gestureDataFallF[1,:])
    # updateData=np.array([a,a])
    updateData=np.array([gestureDataFallF[1,:],gestureDataFallL[1,:],gestureDataFallR[1,:],gestureDatajum[1,:],gestureDatarun[1,:],gestureDataWalkHor[1,:],gestureDataWalkVer[1,:]])
    return updateData

def parameters(data):
    minValue=np.min(data)
    maxValue=np.max(data)
    meanValue=np.mean(data)
    medianValue=np.median(data)
    # entro= entropy(data, base=2)
    stdValue=np.std(data)
    varValue=np.var(data)
    # updateData=np.append(minValue,maxValue)
    updateData=np.array([minValue,maxValue,meanValue,medianValue,stdValue,varValue])
    return updateData

#对数据进行升采样
#Upsample the data
def upSampling(data):
    oriLength=len(data)
    updateData = signal.resample(data, 10*oriLength)
    return updateData

# 求数据的能量值
# Get the fine-grained energy
def finePower(data):
    updateData = pow(10,data/10)
    return updateData

#对数据进行傅里叶变换
# STFT work
def fftSignal(data):
    # winSize=128
    segSize=512
    overlap=120
    fs=1000
    frequency, time, mag = signal.stft(data, fs, 'hann', segSize, overlap)
    mag=np.abs(mag)
    return frequency, time, mag


#........多序列数据训练............#
# 对Mag进行聚类

def kMeansMag(mag):

    return 0
def rssread():
    
    return 0

def gesturemsg(request):
    data=request.POST.get('code','')
    segmetation=data.split(',')
    tempdata=strArray2numArray(segmetation)
    SataPara=(parameters(tempdata)).tolist()
    upsamData=(upSampling(tempdata)).tolist()
    fineData=(finePower(upsamData)).tolist()
    f,t,m=fftSignal(fineData)
    freq=f.tolist()
    time=t.tolist()
    mag=m.tolist()

    retList = {
        'Para': SataPara,
        'upsamData': upsamData,
        'fineData': finePower,
        'freData': freq,
        'timeData': time,
        'magData': mag,
    }
    return HttpResponse(json.dumps(retList), content_type='application/json')


def gesturemsgoffline(request):
    gestureDataFallF=np.loadtxt("./data/fall.csv", delimiter=",")[0,1:].tolist()
    gestureDataFallL=np.loadtxt("./data/fallleft.csv", delimiter=",")[0,1:].tolist()
    gestureDataFallR=np.loadtxt("./data/fallright.csv", delimiter=",")[0,1:].tolist()
    gestureDatajum=np.loadtxt("./data/jump.csv",  delimiter=",")[0,1:].tolist()
    gestureDatarun=np.loadtxt("./data/runVer.csv", delimiter=",")[0,1:].tolist()
    gestureDataWalkHor=np.loadtxt("./data/walkHor.csv", delimiter=",")[0,1:].tolist()
    gestureDataWalkVer=np.loadtxt("./data/walkVer.csv", delimiter=",")[0,1:].tolist()
    retList={
        'FallF': gestureDataFallF,
        'FallL': gestureDataFallL,
        'FallR': gestureDataFallR,
        'Jump': gestureDatajum,
        'Run': gestureDatarun,
        'WalkH':gestureDataWalkHor,
        'WalkV':gestureDataWalkVer
    }
    return HttpResponse(json.dumps(retList))

def finedata(request):
    FallF=finePower(upSampling(np.loadtxt("./data/fall.csv", delimiter=",")[0,1:])).tolist()
    FallL=finePower(upSampling(np.loadtxt("./data/fallleft.csv", delimiter=",")[0,1:])).tolist()
    FallR=finePower(upSampling(np.loadtxt("./data/fallright.csv", delimiter=",")[0,1:])).tolist()
    Jump =finePower(upSampling(np.loadtxt("./data/jump.csv",  delimiter=",")[0,1:])).tolist()
    Run =finePower(upSampling(np.loadtxt("./data/runVer.csv", delimiter=",")[0,1:])).tolist()
    WalkH=finePower(upSampling(np.loadtxt("./data/walkHor.csv", delimiter=",")[0,1:])).tolist()
    WalkV=finePower(upSampling(np.loadtxt("./data/walkVer.csv", delimiter=",")[0,1:])).tolist() 
    retList={
        'FallF':FallF,
        'FallL':FallL,
        'FallR': FallR,
        'Jump': Jump,
        'Run': Run,
        'WalkH': WalkH,
        'WalkV': WalkV
    }
    return HttpResponse(json.dumps(retList))
   
def parametersreq(request):
    data=request.POST.get('code','')
    segmetation=data.split(',')
    tempdata=strArray2numArray(segmetation)
    print(tempdata)
    temp=(parameters(tempdata)).tolist()
    retList={
        'data':temp,
    }
    return HttpResponse(json.dumps(retList))

def finedatareq(request):
    data=request.POST.get('code','')
    segmetation=data.split(',')
    tempdata=strArray2numArray(segmetation)
    # print(tempdata)
    temp=(finePower(upSampling(tempdata))).tolist()
    retList={
        'data':temp,
    }
    return HttpResponse(json.dumps(retList))

def fftonline(request):
    data=request.POST.get('code','')
    segmetation=data.split(',')
    tempdata=strArray2numArray(segmetation)
    frequency,time,mag=fftSignal(finePower(upSampling(tempdata)))
    magMax=(np.max(mag)).tolist()
    magMin=(np.min(mag)).tolist()
    frequency=frequency.tolist()
    time=time.tolist()
    #mag=mag.flatten()
    mag=mag.tolist()
    
    retList={
        'freq':frequency,
        'time':time,
        'mag':mag,
        'max':magMax,
        'min':magMin
    }
    return HttpResponse(json.dumps(retList))


def strArray2numArray(strArray):
    numArary=[]
    for i in range(0,len(strArray)):
        numArary.append(float(strArray[i]))
    return numArary

if __name__ == '__main__':
    res=getDataOffline()
    print(res[0])
    print(res)