import cv2
import numpy


class Img_proc:

    #本类用于存放对图像形态学的一些操作
    @staticmethod
    def kernal_init(kernal_size):
        if isinstance(kernal_size,int):
            kernal_size = (kernal_size,kernal_size)
        return numpy.ones(kernal_size,numpy.uint8)
    
    @staticmethod
    def img_open(ori_frame,kernal_size):
        _K = Img_proc.kernal_init(kernal_size)
        return cv2.morphologyEx(ori_frame,cv2.MORPH_OPEN,_K)
    
    @staticmethod
    def img_close(ori_frame,kernal_size):
        _K = Img_proc.kernal_init(kernal_size)
        return cv2.morphologyEx(ori_frame,cv2.MORPH_CLOSE,_K)


    #对图像滤波算法
    #平滑滤波，低通滤波器
    @staticmethod
    def smoo_filter(ori_frame,kernal_size):
        if isinstance(kernal_size,int):
            kernal_size = (kernal_size,kernal_size)
        _blur = cv2.blur(ori_frame,kernal_size)
        return _blur

    @staticmethod 
    #高斯滤波
    def gauss_filter(ori_frame,kernal_size):
        if isinstance(kernal_size,int):
            kernal_size = (kernal_size,kernal_size)
        _blur = cv2.GaussianBlur(ori_frame,kernal_size,0)
        return _blur
    
    @staticmethod
    #中值模糊
    def median_filter(ori_frame,kernal_size):
        if isinstance(kernal_size,int):
            kernal_size = (kernal_size,kernal_size)
        _median = cv2.medianBlur(ori_frame,kernal_size)
        return _median
    
    @staticmethod
    #双边滤波
    def bilater_filter(ori_frame,filter_d,sigma_color,sigma_space):
        if isinstance(filter_d,int):
            _blur = cv2.bilateralFilter(ori_frame,sigma_color,sigma_space)
            return _blur
    


    

    