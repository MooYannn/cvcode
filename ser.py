import serial
import threading
from queue import Queue,Empty
import time

class Ser_warp(threading.Thread):
    def __init__(self,serial_port:str,serial_baud,ser_timeout,msg_size):

        # 串口信息初始化
        self.ser_port = serial_port
        self.baud = serial_baud
        self.ser_timeout = ser_timeout
        self.ser=serial.Serial(self.ser_port,self.baud,timeout=self.ser_timeout)
        self.msg_size = msg_size

        #消息队列初始化
        self.recv_meg_queue:Queue = Queue(msg_size)
        self.send_meg_queue:Queue = Queue(msg_size)

        # 线程初始化
            # 线程事件
        self.stop_event = threading.Event()
            # 创建线程锁
        self._io_lock = threading.Lock()
        self.thread = threading.Thread(target=self._run_loop,name=f"Serial-Thread{self.ser_port}",daemon=True)
        self.thread.start()

    #定义线程来实现对信息的发送和读取
    def _run_loop(self):
        """判断线程"""
        while not self.stop_event.is_set():
            #写入#
            try:
                msg = self.send_meg_queue.get(block=False)
            except Empty:
                pass
            else:
                # 
                with self._io_lock:
                    try:
                        self.ser.write(msg.encode('utf-8'))
                    except Exception as e:
                        print("串口写入失败:", e)
            #读取#
            with self._io_lock:
                try:
                    raw = self.ser.readline()
                except Exception as e:
                    print("串口读取失败:", e)
                    raw = b''
            if raw:
                line = raw.decode('utf-8', errors='ignore').rstrip('\r\n')
                # 如果串口读取已满
                if self.recv_meg_queue.full():
                    try:
                        self.recv_meg_queue.get_nowait()
                    except Empty:
                        pass
                self.recv_meg_queue.put(line)
            time.sleep(0.005)

        #关闭串口
        with self._io_lock:
            self.ser.close()
    #将信息压入queue
    def send(self,msg:str):
        try:
            self.send_meg_queue.put(msg,block=False)
        except:
            pass
    # 从队列中读取queue
    def read(self,time_out:float):
        try:
            if self.recv_meg_queue.empty():
                pass
            else:
                return self.recv_meg_queue.get(timeout=time_out)
        except Empty:
            return None
    
    def stop(self):
        self.stop_event.set()
        self.thread.join()


if __name__ == "__main__":
    my_list=[1,2,3]
    ser = Ser_warp("/dev/ttyAMA2",115200,0.1,2)
    while True:
        ser.send("success\r\n")
        output=ser.read(0.1)
        if output!=None:
            print(output)




