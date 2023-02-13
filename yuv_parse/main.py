import cv2
import os
import numpy as np

#使用numpy

def main():
    path = r"C:\Users\pc\Desktop\python\yuv_parse"
    file_name_list = os.listdir(path)
    for item in file_name_list:
        if "yuv" in item:
            height = 486
            width = 864
            # print(item)
            fp = open(path + "\\" + item, 'rb')
            framesize = height * width * 3 // 2
            data_bytes = fp.read(framesize)
            data = np.reshape(np.frombuffer(data_bytes, np.uint8) ,((int)(height * 1.5), width))
            img = cv2.cvtColor(data, cv2.COLOR_YUV2BGR_I420)
            cv2.imshow("yuv y", img)
            cv2.waitKey(0)

if __name__ == '__main__':
    main()