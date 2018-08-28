import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import urllib
import os,sys
import BusinessModule

class ttHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        print("url="+self.path)       
        try:           
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()        
            responseHtml="<html><head></head><body>不支持</body></html>"
            # Send the html message
            self.wfile.write(responseHtml.encode())
        except IOError:
            self.send_error(404,"File Not Found"+self.path)
        return

    def do_POST(self):              
        try:
            reqLen=int(self.headers['content-length'])
            requestContent=self.rfile.read(reqLen)
            requestStr=str(requestContent,'utf-8')
            print("收到通知请求"+requestStr)
            #判断是否存在msg=标识，有替换
            requestStr=requestStr.replace('msg=','')
            #调用解析方法形成回复内容
            responseStr=BusinessModule.NoticeDeal(requestStr)
          
            resCon=responseStr.encode()
            resLen=len(resCon)            
            self.send_response(resLen)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(resCon)
        except  Exception as ex:
            self.send_error(404,"File Not Found")
            print(ex)
        
        print("回复请求"+responseStr)
        return
        


def ServerListen(port):
    httpServer=HTTPServer(('',port),ttHandler)
    print("server running")
    httpServer.serve_forever()

ServerListen(8080)