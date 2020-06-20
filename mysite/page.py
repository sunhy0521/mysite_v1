from django.http import HttpResponse
import random
import numpy as np
import json
from scipy.fft import fft
#设备1的FFT操作
def device1(request):
    data=request.POST.get('code','')
    segmetation=data.split(',')
    tempdata=strArray2numArray(segmetation)
    print(tempdata)
    temp=(abs(fft(tempdata))).tolist()
    print(temp)
    # fftdata=abs(fft(temdata))
    #]tempdata=str(tempdata).replace('\'','')
    
    res ="{\"data\": "+json.dumps(temp)+"}"
    return HttpResponse(res)
#设备2的FFT操作
def device2(request):
    val_rand = (random.random())*100
    res ="{\"data\": "+str(val_rand)+"}"
    return HttpResponse(res)

def strArray2numArray(strArray):
    numArary=[]
    for i in range(0,len(strArray)):
        numArary.append(strArray[i])
    return numArary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               