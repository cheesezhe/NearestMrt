# NearestMrt
计算距离用户最近的地铁站（Singapore）

文件说明：

[1] mrt.txt
新加坡mrt名称列表

[2] postalcode.txt
用户的邮编号码列表

[3] result.txt
部分结果：第一列为邮编  第二列为最近的MRT

[4] findMrt.py
class Mrts
    def __init__(self,mrtFile='',postFile='')//初始化，需要提供mrt名称列表和用户邮编列表
    def getMrtsFromFile(self)//根据mrt名称列表获取全部mrt的坐标信息
    def getJsonbyQuery(self,query)//根据query（mrt名称或者postalcode）获取go.there API返回的Json数据
    def findNearestMrt(self,lat=1,lon=103)//计算距离lat,lon最近的mrt
    def process(self)//完整的处理流程（按需调整）
