import cv2
import threading
import time
from queue import Queue,Empty


class Cam_warp(threading.Thread):
    def __init__(self,cam_index,cam_targetsize,queue_size:int = 2):
        #相机初始化
        self.cam_index = cam_index
        self.cap = cv2.VideoCapture(self.cam_index)
        self.frame_weight,self.frame_height = cam_targetsize
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.frame_weight)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        #变量名加：变量类型方便阅读，这里定义frame_queue是一个类的变量
        self.frame_queue:Queue = Queue(maxsize=queue_size)
        #线程配置
            #停止标志
        self.stop_event = threading.Event()
            #线程配置
        self.thread = threading.Thread(target=self.run_updata, name=f"Camera-Thread{self.cam_index}",daemon=True)
            #线程启动
        self.thread.start()
    def run_updata(self):
        while not self.stop_event.is_set():
            ret,frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            #如果当前队列已满，这个时候就需要丢帧
            if self.frame_queue.full():
                try:
                    #这里非阻塞的读取一帧，及丢一帧数据
                    _frame = self.frame_queue.get(block=False)
                except Empty:
                    pass
            #如果不丢帧，而且队列没有满则压入一帧
            self.frame_queue.put(frame)
    #数据读取函数
    def read(self):
        try:
            #非阻塞的获取一帧
            frame = self.frame_queue.get(block=False)
            return frame
        except Empty:
            return None

    def stop(self):
        #时间触发，等待线程结束
        self.stop_event.set()
        self.thread.join()
        self.cap.release()
        time.sleep(0.5)
    
    def nots(self):
        pass
    #set是用来置标志位为True的
    #is_set是用来判断标志位的，及是否满足退出线程的条件

if __name__ == "__main__":
    cap=Cam_warp(0,(480,640),3)
    try:
        while True:
            frame=cap.read()
            if frame is None:
                time.sleep(0.1)
                continue
            cv2.imshow("1",frame)
            if cv2.waitKey(1) & 0XFF==ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.stop()
        cv2.destroyAllWindows()



