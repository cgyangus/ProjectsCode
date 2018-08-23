using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Web;

namespace httpServer
{
    class Program
    {
        public static Socket serverSocket;
        public static bool isRunning = false;
        public static string serverIP;
        public static int serverPort;
        static void Main(string[] args)
        {
        }

        /// <summary>
        /// 开启服务器
        /// </summary>
        public void Start()
        {
            if (isRunning)
                return;

            //创建服务端Socket
            serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            serverSocket.Bind(new IPEndPoint(IPAddress.Parse(serverIP), serverPort));
            serverSocket.Listen(10);
            isRunning = true;

            //输出服务器状态
            Console.WriteLine("Sever is running at http://{0}:{1}/.", ServerIP, ServerPort);

            //连接客户端
            while (isRunning)
            {
                Socket clientSocket = serverSocket.Accept();
                Thread requestThread = new Thread(() => { ProcessRequest(clientSocket); });
                requestThread.Start();
            }
        }

        /// <summary>
        /// 处理客户端请求
        /// </summary>
        /// <param name="handler">客户端Socket</param>
        private void ProcessRequest(Socket handler)
        {
            //构造请求报文
            
            HttpRequest request = new HttpRequest(handler);

            //根据请求类型进行处理
            if (request.Method == "GET")
            {
                OnGet(request);
            }
            else if (request.Method == "POST")
            {
                OnPost(request);
            }
            else
            {
                OnDefault();
            }
        }

        public override void OnGet(HttpRequest request)
        {
            HttpResponse response = new HttpResponse("<html><body><h1>Hello World</h1></body></html>", Encoding.UTF8);
            response.StatusCode = "200";
            response.Server = "A Simple HTTP Server";
            response.Content_Type = "text/html";
            ProcessResponse(request.Handler, response);
        }

    }
}
