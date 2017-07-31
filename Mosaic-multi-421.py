# -*- coding: cp936 -*-
import arcpy
from arcpy import env
import multiprocessing as mp
import time
import os
import shutil

#利用多线程的方法来做栅格影像拼接，利用ArcGIS的工具实现，只能在python 2.7环境上运行
#思路大致是，将所有栅格数据分成四份，四个线程同时运行进行拼接，最后将四个大影像合成最终影像

def mos1(root,part,imglist):
#第一个函数，输入栅格影像根目录root，目标文件夹part和栅格数据名列表
    target = root+part+imglist[0]
    for i in imglist:
        inputs = root + "/" + i
        arcpy.Mosaic_management(inputs,target,'','','',255)
        print("Mosaic %s dem" %i)

def mos2(partNum):
#第二个函数，输入四个栅格文件夹1，将文件夹2拼接到1
    target = rootfile+ "/part" + str(partNum) + "/" + sepRasList[partNum][0]
    inputs = rootfile+ "/part" + str(partNum+1) + "/" + sepRasList[partNum+1][0]
    arcpy.Mosaic_management(inputs,target,'','','',255)
    print("Mosaic %s dem" %i)

def mos3(partNum):
#第二个函数，输入四个栅格文件夹3，将文件夹4拼接到3
    target = rootfile+ "/part" + str(partNum) + "/" + sepRasList[partNum][0]
    inputs = rootfile+ "/part" + str(partNum+2) + "/" + sepRasList[partNum+2][0]
    arcpy.Mosaic_management(inputs,target,'','','',255)
    print("Mosaic %s dem" %i)

if __name__ == '__main__':
    start = time.clock()
    rootfile = u"Y:/ÖØÇìÓåÎ÷dom/èµÉ½DOMok/composite"
    #删个文件根目录
    env.workspace = rootfile
    
    rasList = []

    for row in arcpy.ListRasters():
        rasList.append(row)
    #将栅格文件名录入到rasList

    sepRasList = []
    for i in range(0,len(rasList),int(len(rasList)/4)):
        s = rasList[i:i+int(len(rasList)/4)]
        sepRasList.append(s)
    print(sepRasList)
    if len(rasList)/4 > int(len(rasList)/4):
        for j in sepRasList[4]:
            sepRasList[0].append(j)
        del sepRasList[4]
    else:
        pass
    #将rasList分成四个列表，存在sepRasList，如果有余数，都放到第一个列表种
        
    os.chdir(rootfile)
    try:
        os.mkdir("part0")
        os.mkdir("part1")
        os.mkdir("part2")
        os.mkdir("part3")
    except:
        pass
    
    
    #sepRasList = [[u'h48h092149.tif', u'h48h093148.tif', u'h48h093149.tif'], [u'h48h093150.tif', u'h48h094147.tif', u'h48h094148.tif'], [u'h48h094149.tif', u'h48h094150.tif', u'h48h095147.tif'], [u'h48h095148.tif']]
    for num in range(4):
        firImgName = sepRasList[num][0]
        extend = ['tif.xml','tif.ovr','tif.aux.xml','tif','tfw']
        for ext in extend:
            shutil.copy(firImgName[:-3]+ext,"part"+str(num))
        print(firImgName+' to file '+'part'+str(num))
    #将每个列表第一个栅格复制到目标文件夹种

    
    #lock = mp.Lock()
    
    work1 = mp.Process(target = mos1,args=(rootfile,"/part0/",sepRasList[0]))
    work2 = mp.Process(target = mos1,args=(rootfile,"/part1/",sepRasList[1]))
    work3 = mp.Process(target = mos1,args=(rootfile,"/part2/",sepRasList[2]))
    work4 = mp.Process(target = mos1,args=(rootfile,"/part3/",sepRasList[3]))
    
#    work5 = mp.Process(target = mos2,args=(0,))
#    work6 = mp.Process(target = mos2,args=(2,))
#    work7 = mp.Process(target = mos3,args=(0,))
    
    work1.start()
    work2.start()
    work3.start()
    work4.start()
#    work5.start()
#    work6.start()
#    work7.start()
    
    work1.join()
    work2.join()
    work3.join()
    work4.join()
#    work5.join()
#    work6.join()
#    work7.join()
    #多线程运算栅格拼接，暂时无法做到4to2和2to1也用多线程，因为还不懂多线程队列机制
    print("many to 4 completed")
    
    mos2(0)
    mos2(2)

    print("4 to 2 completed")
    
    mos3(0)


    print("2 to 1 completed")
    elapsed = (time.clock()-start)
    print("Total time is "+str(elapsed)+" s")
