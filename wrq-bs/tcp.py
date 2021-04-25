import socket
import json
import sql

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

#开启ip和端口
ip_port = ('0.0.0.0',39126)
#生成一个句柄
sk = socket.socket()
#退出程序后立即释放端口
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#绑定ip端口
sk.bind(ip_port)
#最多连接数
sk.listen(5)

#开启死循环
while True:
    conn,addr = sk.accept()
    #获取客户端请求数据
    msg = conn.recv(2048).decode()
    print("str: ", msg)
    if(is_json(msg)):
        msg_json = json.loads(msg)
        data = sql.sql_dict(0, msg_json['adc1'], msg_json['adc2']).__dict__
        sql.mysql().insert_data(data)
    # print("json: ",msg_json)
    # conn.sendall(str(upload_time).encode(encoding='utf_8', errors='strict'))
    #关闭链接
    conn.close()