"""
UDPでデータを受け取ってcsvファイルに保存するプログラム
ctrl+cで停止
"""

import socket
import time
import datetime
from contextlib2 import closing
IPaddr = socket.gethostbyname(socket.gethostname())
print(f'myIPaddress: {IPaddr}')
UDP_IP = IPaddr #自分のIPアドレス
UDP_PORT=9000

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
sock.bind((UDP_IP,UDP_PORT))

count = 0


def recoder(file_name=f'./test.csv',w_data='',w_mode='w'):
   """データ記録関数"""
   open_f = open(file_name, mode=w_mode)
   open_f.write(w_data+"\n")
   open_f.close()


if __name__=="__main__":
   dt_now = datetime.datetime.now()
   dt_now = dt_now.strftime('%Y%m%d-%H%M%S')
   
   #id=input()
   
   filename = f'./static/csv/Pulse_{dt_now}.csv'
   print(f'file_name: {filename}')
   header = "num1,num2,data,bpm,ibi"
   recoder(filename, header, 'w')
   

   with closing(sock): 
      while True:
         try:
            count +=1
            data,addr = sock.recvfrom(1024)
            data = data.decode()
            #print("Send from ESP",addr,"-",data)
            data1 = data.split(",")
            data = f'{count},{data}'
            #if int(data1[1]) > 4000:
            print(data) #ファイル内の通し番号,心拍計が起動してからの通し番号,データ
            recoder(filename, data, 'a')
            
            time.sleep(0.002)
            ##UDPで送ってきた相手に送り返す部分
            #mes = (str(count)+'\0').encode()
            #mes = ("送信完了\0").encode()
            #sock.sendto(mes,addr)
         except KeyboardInterrupt:
            print("ctrl+c")
            break

