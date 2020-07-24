#coding:utf-8
__author__ = 'zhangxd18'
import csv,cv2
#cv2 version 3.4.2
import sys
import os
import codecs
import re
import Tkinter
import tkMessageBox
import tkFileDialog
import Canvas
import numpy
from PIL import Image
from PIL import ImageTk

show_width = 640
show_height = 480
            
def select_file_path():
    path = tkFileDialog.askopenfilename()
    #path = tkFileDialog.askdirectory()
    dstPath.set(path)
    
def start_analyze():
    global img
    global canvas_img
    print dstPath.get()
    if (not os.path.exists(dstPath.get())) or dstPath.get()==None:
        print "Notice the file path!!!"
        return 
    img_width = int(raw_width.get())
    img_height = int(raw_height.get())
    print img_width, img_height

    raw_16uc1_data = numpy.fromfile(dstPath.get(), dtype=numpy.uint16)
    print "raw file size:", raw_16uc1_data.size
    if raw_16uc1_data.size != img_width*img_height*1:
        print "raw file size should be %d, or modify the width and height"%(img_width*img_height*1)
        return
        
    mat16uc1_bayer = raw_16uc1_data.reshape(img_height, img_width, 1)
    mat8uc1_bayer = mat16uc1_bayer.astype(numpy.uint8)
    
    mat8uc3_rgb = cv2.cvtColor(mat8uc1_bayer, cv2.COLOR_BayerRG2RGB)
    #BGGR GBRG GRBG RGGB  RAW8 RAW10 RAW12
    print "-------------------"
    print mat16uc1_bayer.shape, mat16uc1_bayer.size
    print mat8uc1_bayer.shape, mat8uc1_bayer.size
    print mat8uc3_rgb.shape, mat8uc3_rgb.size
    
    img8u_rgb = Image.fromarray(mat8uc3_rgb)
    img8u_rgb.save("rgb8u.bmp")
    
    img_rgb_show = img8u_rgb.resize((show_width, show_height))
    canvas_img = ImageTk.PhotoImage(img_rgb_show)  
    canvas_dst.create_image(2, 2, anchor='nw', image=canvas_img)
    
    #canvas_dst.update()
    root.update()
    root.after(10)
    #tkMessageBox.showinfo('tips', '分析结束')
    
if "__main__" == __name__:
    #print sys.argv[1]
    canvas_img = None
    img = None
    test01 = numpy.array([1920, 1920, 1920])
    print test01
    test02 = test01.astype(numpy.uint8)
    print test02
    
    root = Tkinter.Tk()
    dstPath = Tkinter.StringVar()
    raw_width = Tkinter.StringVar()
    raw_height = Tkinter.StringVar()
    raw_width.set("1920")
    raw_height.set("1080")
    #root.withdraw()
    Tkinter.Label(root, text = '目标文件：').grid(row = 0, column = 0)
    Tkinter.Entry(root, textvariable = dstPath).grid(row = 0, column = 1)
    Tkinter.Button(root, text = '文件选择', command = select_file_path).grid(row = 0, column = 2)
    
    Tkinter.Label(root, text = '宽度：').grid(row = 1, column = 0)
    Tkinter.Entry(root, textvariable = raw_width).grid(row = 1, column = 1)
    
    Tkinter.Label(root, text = '高度：').grid(row = 2, column = 0)
    Tkinter.Entry(root, textvariable = raw_height).grid(row = 2, column = 1)
    
    Tkinter.Button(root, text = '开始分析', command = start_analyze).grid(row = 3, column = 2)
    #'''
    canvas_dst = Tkinter.Canvas(root, width=show_width, height=show_height, bg='blue')  # 设置画布
    canvas_dst.grid(row = 4, column = 1)
    canvas_dst.create_line(0, 100, show_width, 100, width=5, fill='red')
    canvas_dst.create_line(0, 200, show_width, 200, width=15, fill='green')
    
    #'''
    root.mainloop()
