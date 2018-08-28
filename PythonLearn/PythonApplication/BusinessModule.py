import time
import CommonFun
import xml.dom.minidom
#url地址
#ttUrl='http://10.44.16.151:8090?Handler=TTHandler'
ttUrl='http://10.44.16.85:8090/?Handler=TTHandler'
#ttUrl='http://127.0.0.1:8897?Handler=TTHandler'
agentInfo=('1001','123456')
global messageId
messageId=int(time.time())


#取新期参数
def GetTermList(lotType):
    global messageId
    messageId+=1
    timeStamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head=('1001',agentInfo[0],str(messageId),timeStamp)
    body='<body><lottype>'+lotType+'</lottype></body>'
    reqData=CommonFun.GetRequestXml(head,body,agentInfo[1])
    termList=CommonFun.HpptPost(ttUrl,reqData)
    return termList

#解析新期存储于列表
def SetTermListToList(termListStr):
    termList=[]
    try:
        termListXml=xml.dom.minidom.parseString(termListStr)
        root=termListXml.documentElement

        lotType=termListXml.getElementsByTagName("lottype")[0].childNodes[0].data 

        #取得所有期号集合
        terms=root.getElementsByTagName("dataitem")        

        #循环生成参数
        for term in terms:
            termcode=term.getAttribute("periodical")
            termStatus=term.getAttribute("status")
            startTime=term.getAttribute("starttime")
            endTime=term.getAttribute("endtime")
            apiStartTime=term.getAttribute("apistarttime")
            apiEndTime=term.getAttribute("apiendtime")
            termInfo=[lotType,termcode,termStatus,startTime,endTime,apiStartTime,apiEndTime]
            termList.append(termInfo)
    except:
        print("新期返回有误："+termListStr)
        return
    return termList


#投注请求
def LotBet(lotType,termCode,money,ticketCount,dataList):
    global messageId
    messageId+=1
    timeStamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head=('2001',agentInfo[0],str(messageId),timeStamp)
    body='<body><lottype>'+lotType+'</lottype><periodical>'+termCode+'</periodical><money>'+money+'</money><ticketcount>'+ticketCount+'</ticketcount><datalist>'+dataList+'</datalist></body>'
    reqData=CommonFun.GetRequestXml(head,body,agentInfo[1])
    betResult=CommonFun.HpptPost(ttUrl,reqData)
    return betResult

#投注结果解析，并存储于列表
def BetResultInList(betResultStr):
    betResultList=[]
    try:
        betResultXml=xml.dom.minidom.parseString(betResultStr)

        dataItems=betResultXml.getElementsByTagName("dataitem")

        for item in dataItems:
            ticketsn=item.getAttribute("ticketsn")
            status=item.getAttribute("status")
            message=item.getAttribute("message")

            itemInfo=[ticketsn,status,message]

            betResultList.append(itemInfo)
    except:
        print("收单失败"+betResultStr)

    return betResultList

#票成功通知回复body
def GetBetNoticeBody(body):
    newBody=""
    try:
        bodyXml=xml.dom.minidom.parseString(body)
        lotType=bodyXml.getElementsByTagName("lottype")[0].childNodes[0].data        
        termCode=bodyXml.getElementsByTagName("periodical")[0].childNodes[0].data
        status='200'
        newBody="<body><return><code>0</code><message>成功</message></return><lottype>"+lotType+"</lottype><periodical>"+termCode+"</periodical><status>200</status></body>"
    except:
        print("通知结果有误"+body)
    return newBody

#票面信息通知回复
def GetTicketInfoNoticeBody(body):
    _newBody=""
    try:
        bodyXml=xml.dom.minidom.parseString(body)
        lotType=bodyXml.getElementsByTagName("lottype")[0].childNodes[0].data        
        status='200'

        _newBody="<body><return><code>0</code><message>成功</message></return><lottype>"+lotType+"</lottype><status>200</status></body>"
    except:
        print("通知结果有误"+body)
    return _newBody



#接收处理投回调通知
def NoticeDeal(reqCon):
    resCon="ok"
    #调用解析出报文头和报文体
    reqDetail=CommonFun.ResolveReqContent(reqCon)
    head=reqDetail[0]
    body=reqDetail[1]

    #判断通知类型
    cmd=head[0]
    if (cmd=='2101'):
        body=GetBetNoticeBody(body)  
    elif(cmd=='3002'):
        body=GetTicketInfoNoticeBody(body)
    else:
        pass
    resCon=CommonFun.GetRequestXml(head,body,agentInfo[1])
    return resCon



#取开奖公告
def GetPrizeInfo(lotType,termCode):
    global messageId
    messageId+=1
    timeStamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    head=('1002',agentInfo[0],str(messageId),timeStamp)
    body='<body><lottype>'+lotType+'</lottype><periodical>'+termCode+'</periodical></body>'
    reqData=CommonFun.GetRequestXml(head,body,agentInfo[1])
    prizeInfo=CommonFun.HpptPost(ttUrl,reqData)
    return prizeInfo
