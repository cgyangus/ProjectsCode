import hashlib
import requests
import xml.dom.minidom
from xml.dom.minidom import parse

#生成key函数
def GetKey(headTup,body,pwd):
    Key=""
    keyStr=headTup[0]+headTup[1]+headTup[2]+headTup[3]+pwd+body
    keyMd5=hashlib.md5(keyStr.encode(encoding='utf-8'))
    key=keyMd5.hexdigest()
    return Key

#组成http请求的报文
def GetRequestXml(headTup,body,pwd):
    keyStr=headTup[0]+headTup[1]+headTup[2]+headTup[3]+pwd+body
    keyMd5=hashlib.md5(keyStr.encode(encoding='utf-8'))
    key=keyMd5.hexdigest()
    msgHead='<head><command>'+headTup[0]+'</command><agentid>'+headTup[1]+'</agentid><messageid>'+headTup[2]+'</messageid><timestamp>'+headTup[3]+'</timestamp><key>'+key+'</key></head>'
    requestXml='<?xml version=\'1.0\' encoding=\'UTF-8\'?><message>'+msgHead+body+'</message>'
    return requestXml

def HpptPost(reqUrl,reqData):
    headersType={'Content-Type': 'application/xml'}
    res=requests.post(reqUrl,data=reqData,headers=headersType)
    responseXml=res.text
    return responseXml

#解析返回的报文，分级成head、body
def ResolveReqContent(reqCon):
    head=[]
    body=''
    reqConXml=xml.dom.minidom.parseString(reqCon)
    #报文头
    cmd=reqConXml.getElementsByTagName("command")[0].childNodes[0].data 
    agentId=reqConXml.getElementsByTagName("agentid")[0].childNodes[0].data 
    messageId=reqConXml.getElementsByTagName("messageid")[0].childNodes[0].data
    timeStamp=reqConXml.getElementsByTagName("timestamp")[0].childNodes[0].data 
    key=reqConXml.getElementsByTagName("key")[0].childNodes[0].data 
    headInfo=[cmd,agentId,messageId,timeStamp,key]
    head.extend(headInfo)

    #报文体
    bodyXml=reqConXml.getElementsByTagName("body")[0]
    body=bodyXml.toprettyxml()   
    body="<body>"+body+"</body>"

    return head,body

