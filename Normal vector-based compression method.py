# ---------------------------------------------------------------------------
# aaa.py
# Created on: 2015-01-08 20:03:53.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,math,itertools
from arcpy import env
env.overwriteOutput=True

# Local variables:
node = r"D:\Users\ZhangMingxi\Desktop\table\field4mountain.shp"
#pointtemp_shp = r"E:\河道处数据\tin\yyc\pointb.shp"
triangleshp=r"D:\Users\ZhangMingxi\Desktop\table\field4mountainangle.shp"


#要素浅拷贝一份生成layer
arcpy.MakeFeatureLayer_management(triangleshp,"triangleshplyr")
arcpy.MakeFeatureLayer_management(node,"nodelyr")

#定义法向量
class nitem:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
#根据坡度坡向计算法向量
def getcanshu(Sl,As):
    if (Sl == 0) and (As == -1):
        dx = 0
        dy = 0   
    Sl1 = math.radians(Sl)
    As1 = math.radians(As)
    temp1 = math.tan(Sl1)
    temp2 = math.tan(As1)
    temp3 = math.pow(temp1,2)
    temp4 = math.pow(temp2,2)
    temp11 = (1+temp3)*(1+temp4)
    temp12 = math.sqrt(temp3/temp11)
    if(As>=0) and (As<=90):
        dx = temp12
        dy = dx*temp2
    elif (As>90) and (As<=180):
        dx = temp12
        dy = dx*temp2
    elif (As>180) and (As<=270):
        dx = -temp12
        dy = dx*temp2
    elif (As>270) and (As<=360):
        dx = -temp12
        dy = dx*temp2
    dz = math.sqrt(1/(1+ temp3))
    n = nitem()
    n.dx = dx
    n.dy = dy
    n.dz = dz
    return n



#根据法向量计算二平面夹角
def getangle(n1,n2):
    distance = math.pow((n2.dx-n1.dx),2)+math.pow((n2.dy-n1.dy),2)+math.pow((n2.dz-n1.dz),2)
    angle = math.acos(1-0.5*distance)
    angle = math.degrees(angle)
    return angle

#获取二夹角列表中的最大角
def getAngleList(n2nlistGet):
    n2nlistRes=[]
    for ii in range(0,len(n2nlistGet)):
        n1=n2nlistGet[ii][0]
        n2=n2nlistGet[ii][1]
        tempangle = getangle(n1,n2)
        n2nlistRes.append(tempangle)
    largestangle = max(n2nlistRes)
    smallestangle = min(n2nlistRes)
    slopegap = largestangle-smallestangle
    return slopegap
#添加坡度差字段
arcpy.AddField_management(node, "slopegap", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#移到点要素头
noderows=arcpy.UpdateCursor(node)
for noderow in noderows:
    nodefid=noderow.FID
    print "*********"+str(nodefid)
    nodeselect="\"FID\"="+str(nodefid)
    #arcpy.Select_analysis(node, pointtemp_shp, nodeselect)
    arcpy.SelectLayerByAttribute_management("nodelyr", "NEW_SELECTION", nodeselect)
    arcpy.SelectLayerByLocation_management("triangleshplyr","INTERSECT","nodelyr","","NEW_SELECTION")
    #选择集向量列表
    selectArray=[]
    #坡度集列表
    SlopeArray = []
    trianglerows=arcpy.SearchCursor("triangleshplyr")
    for trianglerow in trianglerows:
        Sl = trianglerow.getValue("Slope_Deg")
        trianglerowshape = trianglerow.shape
        points = [point for point in trianglerowshape.getPart(0)]
        As = trianglerow.getValue("Aspect")
        SlopeArray.append(Sl)
        ntemp = getcanshu(Sl,As)
        selectArray.append(ntemp)
    #averageAspect = sum(selectArray)/len(selectArray)
    n2nlist = list(itertools.combinations(selectArray,2))
    slgap = getAngleList(n2nlist)
    print str(slgap)
    noderow.setValue("slopegap",slgap)
    noderows.updateRow(noderow)
    del trianglerow,trianglerows
    print "****************************"  

del noderow
del noderows
print "done!"






