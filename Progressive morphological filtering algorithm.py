# -*- coding: cp936 -*-
import arcpy,math,itertools
from arcpy import env
env.overwriteOutput=True

# Local variables:
pointshp = r"D:\Users\ZhangMingxi\Desktop\newtest\simplepoints.shp"
fishshp=r"D:\Users\ZhangMingxi\Desktop\newtest\fishnetss.shp"

#要素浅拷贝一份生成layer
arcpy.MakeFeatureLayer_management(fishshp,"fishshplyr")
arcpy.MakeFeatureLayer_management(pointshp,"pointshplyr")
gwidth = 134

#获取窗口内元素
def getselection(nid,w):
    rowx = nid//gwidth
    listy = nid%gwidth
    ii = rowx
    jj = listy
    netselect = ""
    for i in range(w):
        for j in range(w):
            nid =  (i+ii)*gwidth+j+jj
            netselect = netselect + "\"FID\"="+str(nid)+"OR"
    netselect = netselect[:-2]
    return netselect

#腐蚀操作
def erode(window):
    netrows = arcpy.UpdateCursor(fishshp)
    w = window
    for netrow in netrows:
        netid = netrow.FID
        selectpolygon="\"FID\"="+str(netid)
        selectmutipolygon = getselection(netid,w)
        arcpy.SelectLayerByAttribute_management("fishshplyr", "NEW_SELECTION", selectmutipolygon)
        arcpy.SelectLayerByLocation_management("pointshplyr","INTERSECT","fishshplyr","","NEW_SELECTION")

        pointrowm=arcpy.SearchCursor("pointshplyr")
        windowZmin = 0
        if pointrowm != None:
            Zarray = []
            for pointrow in pointrowm:
                Zarray.append(pointrow.getValue("pointZ"))
            if len(Zarray)>0:
                windowZmin = min(Zarray)
            netrow.setValue("erodeZ",windowZmin)
            netrows.updateRow(netrow)
            print str(windowZmin)
        arcpy.SelectLayerByAttribute_management("fishshplyr", "NEW_SELECTION", selectpolygon)
        arcpy.SelectLayerByLocation_management("pointshplyr","INTERSECT","fishshplyr","","NEW_SELECTION")

        pointrows=arcpy.UpdateCursor("pointshplyr")
        if pointrows!= None:
            for pointrow in pointrows:
                pointrow.setValue("erodeZ",windowZmin)
                pointrows.updateRow(pointrow)
            print "单元格网腐蚀结束"
    del pointrows,pointrowm,netrows,netrow
    


#膨胀操作
def dilate(w):
    #netrows = arcpy.UpdateCursor("fishshplyr")注意图层和要素的差别
    netrows = arcpy.UpdateCursor(fishshp)
    for netrow in netrows:
        netid = netrow.FID
        selectpolygon="\"FID\"="+str(netid)
        selectmutipolygon = getselection(netid,w)
        arcpy.SelectLayerByAttribute_management("fishshplyr", "NEW_SELECTION", selectmutipolygon)

        fishnetrows=arcpy.SearchCursor("fishshplyr")
        windowZmax = 0
        if fishnetrows!= None:
            Zarray = []
            for fishnetrow in fishnetrows:
                Zarray.append(fishnetrow.getValue("erodeZ"))
            if len(Zarray)>0:
                windowZmax = max(Zarray)
            netrow.setValue("dilateZ",windowZmax)
            netrows.updateRow(netrow)
            print str(windowZmax)   
        arcpy.SelectLayerByAttribute_management("fishshplyr", "NEW_SELECTION", selectpolygon)
        arcpy.SelectLayerByLocation_management("pointshplyr","INTERSECT","fishshplyr","","NEW_SELECTION")

        pointrows=arcpy.UpdateCursor("pointshplyr")
        if pointrows!= None:
            for pointrow in pointrows:
                pointrow.setValue("dilateZ",windowZmax)
                pointrows.updateRow(pointrow)
            print "单元格网膨胀结束"
    del pointrows,fishnetrows,netrows,netrow
    


#判别地物类别
def judgeObject(heightThd):
    pointrows = arcpy.UpdateCursor(pointshp)
    for pointrow in pointrows:
        if pointrow.getValue("pointZ") - pointrow.getValue("dilateZ") > heightThd:
            pointrow.setValue("sortTag",1)
            dilateZ= pointrow.getValue("dilateZ")
            pointrow.setValue("pointZ",dilateZ)
            print "判别:%s" % pointrow.FID

            

#点云处理过程
if __name__ == '__main__':
    for k in range(0,6):
        w = 2*k + 1
        heightThd = k+1
        erode(w)
        dilate(w)
        judgeObject(k)
        print "well done!"
























