import subprocess
import os

# 把一张图片合成视频，设置视频时长
'''
-loop 1 循环。因为就一张图片
-r 1  帧率。1 是每秒一帧
-t 5  时长。秒为单位。生成5秒长的视频
-c:v h264  视频输出的编码格式。 h264是mp4格式常用的编码
-pix_fmt yux420p  像素格式。支持的类型可以查看ffmpeg帮助查询
'''
cmdLine = "/Applications/ffmpeg -r 25 -loop 1 -i images/1.png -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 30 -s 720x576 -vframes 250 -r 25 -t 10 a.mp4"
subprocess.call(cmdLine, shell=True)
