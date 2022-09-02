import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os
from subprocess import call
from scipy.interpolate import UnivariateSpline
import numpy as np

def LookupTable(x, y):
	spline = UnivariateSpline(x, y)
	return spline(range(256))

# 夏季
def Summer(img):
	increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
	decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
	blue_channel, green_channel, red_channel  = cv2.split(img)
	red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
	blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
	sum = cv2.merge((blue_channel, green_channel, red_channel ))
	return sum

# 冬季
def Winter(img):
	increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
	decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
	blue_channel, green_channel, red_channel = cv2.split(img)
	red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
	blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
	win = cv2.merge((blue_channel, green_channel, red_channel))
	return win

# 反相
def invert(img):
	inv = cv2.bitwise_not(img)
	return inv
img_root = 'images/'
out_root = 'pig.avi'
fps = 1
fourcc = VideoWriter_fourcc(*"MJPG")  # 支持jpg
videoWriter = cv2.VideoWriter(out_root, fourcc, fps, (640, 480))
im_names = os.listdir(img_root)
print(len(im_names))
for im_name in range(1, 4):
	string = img_root + str(im_name) + '.png'
	print(string)
	frame = cv2.imread(string)
	frame = cv2.resize(frame, (640, 480))
	# 油画效果
	# frame = cv2.xphoto.oilPainting(frame, 2, 1)
	# hdr
	# frame = cv2.detailEnhance(frame, sigma_s=12, sigma_r=0.15)
	# 冬季效果
	# frame = Winter(frame)
	# 反相
	frame = invert(frame)
	# frame = Summer(frame)
	videoWriter.write(frame)
videoWriter.release()
# 将输出的视频变为mp4格式或者压缩
dir = out_root.strip(".avi")
command = "/Applications/ffmpeg -i %s.avi %s.mp4" % (dir, dir)
call(command.split())
