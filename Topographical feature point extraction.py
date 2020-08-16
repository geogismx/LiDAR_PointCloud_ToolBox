##targetIDarray1 = []
##for source in sas:
##    TID = source.getValue("TARGET_FID")
##    targetIDarray1.append(TID)

#联合数组，一对多

# -*- coding: cp936 -*-
import arcpy,math
sourceshp = r"D:\Users\ZhangMingxi\Desktop\yutest\sourcepoints.shp"
identityshp = r"D:\Users\ZhangMingxi\Desktop\yutest\sourceidentity6.shp"
sjxtinnode = r"D:\Users\ZhangMingxi\Desktop\yutest\sjxtinnode.shp"
sapshp = r"D:\Users\ZhangMingxi\Desktop\yutest\sjxAppendpolygon6.shp"
passhp=r"D:\Users\ZhangMingxi\Desktop\yutest\polygonAppendsjx6.shp"


arcpy.MakeFeatureLayer_management(sapshp,"sjxAppendpolygonlyr")
arcpy.MakeFeatureLayer_management(passhp,"polygonAppendsjxlyr")
arcpy.MakeFeatureLayer_management(sjxtinnode,"sjxtinnodelyr")

def getFID(array):
    pointselect = ""
    for i in range(len(array)):
        pointselect = pointselect + "\"FID\"="+str(array[i])+"OR"
    pointselect = pointselect[:-2]
    return pointselect   



dic = {}
sas = arcpy.SearchCursor(identityshp)
for so in sas:
    SID = so.getValue("FID_source")  
    TID = so.getValue("FID_sjxtin")
    dic[SID] = TID
del sas

print "part1,well done"


array3 = []
array4 = []
total1 = len(dic)
for i in range(total1):
    targetID = dic[i]
    selectpolygon="\"TARGET_FID\"="+str(targetID)
    arcpy.SelectLayerByAttribute_management("sjxAppendpolygonlyr", "NEW_SELECTION", selectpolygon)
    ptroundpolys = arcpy.SearchCursor("sjxAppendpolygonlyr")
    for ptroundpoly in ptroundpolys:
        JID1 = ptroundpoly.getValue("JOIN_FID")
        array3.append(JID1)
    array4.append(array3)
    array3 = []
del ptroundpoly,ptroundpolys

print "part2,well done" 

array5 = []
array6 = []
array7 = []
total2 = len(array4)
for i in range(total2):
    array5 = array4[i]
    for j in range(len(array5)):
        JID2 = array5[j]
        selectpoints = "\"TARGET_FID\"="+str(JID2)
        arcpy.SelectLayerByAttribute_management("polygonAppendsjxlyr", "NEW_SELECTION", selectpoints)
        polythreepoints = arcpy.SearchCursor("polygonAppendsjxlyr")
        for polythreepoint in polythreepoints:
            JFID = polythreepoint.getValue("JOIN_FID")
            array6.append(JFID)          
    array6 = list(set(array6))
    array7.append(array6)
    array6 = []
    array5= []
del polythreepoint,polythreepoints

print "part3,well done"


array8 = []
for i in range(len(array7)):
    Zarray = []
    pointselect = getFID(array7[i])
    arcpy.SelectLayerByAttribute_management("sjxtinnodelyr", "NEW_SELECTION", pointselect)
    points = arcpy.SearchCursor("sjxtinnodelyr")
    for point in points:
        Zarray.append(point.getValue("Zvalue"))
    maxZ = max(Zarray)
    array8.append(maxZ)
del point,points
print "part4,well done"

sjxlast = arcpy.UpdateCursor(sourceshp)
for oo in sjxlast:
    outpt = oo.getValue("Zvalue")
    ID = oo.FID
    if outpt == array8[ID]:
        oo.setValue("sign",1)
    sjxlast.updateRow(oo)
    
del sjxlast,oo
    
print "ok!"





