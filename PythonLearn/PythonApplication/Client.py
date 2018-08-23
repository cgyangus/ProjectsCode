import BusinessModule
import xml.dom
from xml.dom.minidom import parse
import time
import sys
import _thread

  #取双色玩法参数
termList=BusinessModule.GetTermList('301')

#调用解析新期
terms=BusinessModule.SetTermListToList(termList)
lotType=terms[0][0]
termCode=terms[0][1]
print("游戏"+lotType+"期号"+termCode+"可以销售")


def SellTest(threadId,sellCount,termCode): 
    try:
        #双色球销售
        while sellCount > 0 :
            print("线程"+str(threadId)+"销售序号为"+str(sellCount)+"2元双色一张")
            a=time.time()
            ticketsn=time.strftime("%Y%m%d%H%M%S", time.localtime())+str(int(time.time()))
            dataList="<dataitem ticketsn =\"" + ticketsn + "\" playtype=\"30101\" code=\"01,02,03,04,05,06|07\" zhushu=\"1\" money=\"2.00\" multiple=\"1\" expand=\"\" /> "
            betResult=BusinessModule.LotBet(lotType,termCode,"2","1",dataList)
            #解析投注结果
            betResultList=BusinessModule.BetResultInList(betResult)
            #打印销售结果
            for result in  betResultList:
                print(result[0]+"    "+result[1]+"    "+result[2])
            print("线程"+str(threadId)+"销售序号为"+str(sellCount)+"的2元双色销售完毕")
            sellCount -=1
         
    except Exception as ex:
        print(ex)

 #取得双色球开奖信息
def GetPrizeInfo(termCode):
    prizeTermCode=str(int(termCode)-1)
    prizeInfo=BusinessModule.GetPrizeInfo('301',prizeTermCode)
    print(prizeInfo)      
#SellTest(1,1,termCode)
threadCount=1
while threadCount>0:
    _thread.start_new_thread(SellTest,(threadCount,1,termCode,))
    threadCount-=1
#取得开奖公告
GetPrizeInfo(termCode)

    

