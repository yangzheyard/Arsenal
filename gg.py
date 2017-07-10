# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from PIL import ImageGrab
import win32gui
import shapefile
import os
import zipfile
import random
import time
import pandas as pd
from tkinter import *  
import tkinter.filedialog as tkFD
import tkinter.colorchooser as tkCC
import tkinter.messagebox as tkMB

shplist = []
shptype = []
shpDF = pd.DataFrame(columns=('shpName','Type','FillColor'))


def getShpUrl():
    shpUrl = tkFD.askdirectory()
    print(shpUrl)
    #fileUrl.append(shpUrl)
    tShpUrl.set("shp file URL: " + shpUrl)
    for root,dirs,files in os.walk(shpUrl):
        for file in files:
            #print(root+'/'+file)
            if 'shp' in file and 'xml' not in file:
                shplist.append(root+'/'+file)
                sf = shapefile.Reader(root+'/'+file)
                shapes = sf.shapes() 
                shptype.append(shapes[len(shapes)-1].shapeType)
    shpDF['shpName'] = shplist
    shpDF['Type'] = shptype

def shpToTxt():
    lineTemp = ['SimpleLineSymbol','\nColor:','\nWidth:3','\nUsePoint:0','\nName:Name','\nSize:32','\nTextColor:255']
    polygonTemp = ['SimpleFillSymbol','\nFillColor:','\nFillOpacity:0.75','\nLineColor:7237230','\nWidth:0.05']
    polygonColors = [7582323,15915927,7602175,15915927,12500735,12511999,12517375,12517353\
              ,12517331,15269822,16771262,16765630,16760552,15253247,6725342,9012694\
              ,13611248,12510447,6800886,11596206,10547694]
    lineColors = [1127674,8846335,0,16552714,11184810,6967742,15855268]
    
    for i in range(len(shpDF)):
        if shpDF.loc[i,'Type'] == 5 or shpDF.loc[i,'Type'] == 15:
            polygonTempC = polygonTemp
            polygonTempC[1] = '\nFillColor:' + str(polygonColors[random.randint(0,len(polygonColors)-1)])
            f = open(shpDF.loc[i,'shpName'].replace('.shp','.txt'),'a')
            f.writelines(polygonTempC)
            f.close
        elif shpDF.loc[i,'Type'] == 3 or shpDF.loc[i,'Type'] == 13:
            lineTempC = lineTemp
            lineTempC[1] = '\nColor:' + str(lineColors[random.randint(0,len(lineColors)-1)])
            f = open(shpDF.loc[i,'shpName'].replace('.shp','.txt'),'a')
            f.writelines(lineTempC)
            f.close  
    tShpUrl.set(u"TXT加载完毕")
    
def pickColor():
    color = tkCC.askcolor()
    print(color)
    r = int(color[0][0])
    g = int(color[0][1])
    b = int(color[0][2])
    colorEncoding = r+g*256+b*256*256
    print(colorEncoding)
    tShpUrl.set(colorEncoding)
    #return colorEncoding

def saveTxt():
    shpUrl = tkFD.askdirectory()
    savetxt = shpUrl+ '/' + time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())+'.zip'
    newSave = zipfile.ZipFile(savetxt,'w')
    
    for root,dirs,files in os.walk(shpUrl):
        for file in files:
            if ".txt" in file:
                newSave.write(root+'/'+file,compress_type = zipfile.ZIP_DEFLATED)
    newSave.close()
    tShpUrl.set("Successfully saved txt files")
    #tkMB.showinfo(message="Successfully saved txt files")
    
    

    
  
def getRGB():
    screenshot = ImageGrab.grab()
    
    position = win32gui.GetCursorInfo()
    (x,y) = position[2]
    
    pix = screenshot.convert('RGB')
    r,g,b = pix.getpixel((x,y))
    
    #print("RGB color:"+r,g,b)  
    print(r+g*256+b*256*256)
    return str(r+g*256+b*256*256)+' / '+'R'+str(r)+' G'+str(g)+' B'+str(b)
    #updateLabel(str(r+g*256+b*256*256))

def listenkey(event):
    if event:
        print("RGB color encoding")
        colorcode.set("RGB color encoding: "+getRGB())
        
    else: 
        print('Pressing on:'+event.char)
        
        
#def updateLabel(colorstr):
#    colorcode.set(colorstr)

root = Tk()

colorcode = StringVar()
canvas = Canvas(root,width = 500,height=300)

label = Label(root,width = 50, textvariable = colorcode)
label.pack() 
root.bind('<Key-space>',listenkey)

tShpUrl = StringVar()
lShpUrl = Label(root,width = 50, textvariable = tShpUrl)
lShpUrl.pack()

btnGetUrl = Button(root,text = "Find the shp", command = getShpUrl)
btnGetUrl.pack()

btnShpToTxt = Button(root,text = "Shp To Txt", command = shpToTxt)
btnShpToTxt.pack()

btnPickColor = Button(root,text = "Pick a Color", command = pickColor)
btnPickColor.pack()

btnSaveTxt = Button(root,text = "Save the Scheme", command = saveTxt)
btnSaveTxt.pack()


button_ok = Button(root,text = "ok",width = 10)  
button_cancel = Button(root,text = "cancel",width = 10)  
button_ok.pack()  
button_cancel.pack()
  
root.mainloop()


      
