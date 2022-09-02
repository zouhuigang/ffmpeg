## 命令列表
>ffmpeg -formats | less

>GPU查看命令 watch -n 10 nvidia-smi

[http://www.cnblogs.com/wainiwann/p/4128154.html]
[https://blog.csdn.net/zzcchunter/article/details/68060989]
[https://www.cnblogs.com/zxqstrong/p/4555517.html]

## 查看视频信息

[命令]
```shell
ffmpeg -i video.mp4  # [video.mp4] 是视频文件

ffmpeg -i test.flv 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//   # 获取视频文件播放时长

ffprobe -v quiet -print_format json -show_format -show_streams zs_257573_HSCJC_XC_IMG.mp4 # 获取视频文件全部信息
```

```shell
(1) -an: 去掉音频 
(2) -vn: 去掉视频 
(3) -acodec: 设定音频的编码器，未设定时则使用与输入流相同的编解码器。音频解复用在一般后面加copyc表示拷贝 
(4) -vcodec: 设定视频的编码器，未设定时则使用与输入流相同的编解码器，视频解复用一般后面加copy表示拷贝 
(5) –f: 输出格式（视频转码）
(6) -bf: B帧数目控制 
(7) -g: 关键帧间隔控制(视频跳转需要关键帧)
(8) -s: 设定画面的宽和高，分辨率控制(352*278)
(9) -i:  设定输入流
(10) -ss: 指定开始时间（0:0:05）
(11) -t: 指定持续时间（0:05）
(12) -b: 设定视频流量，默认是200Kbit/s
(13) -aspect: 设定画面的比例
(14) -ar: 设定音频采样率
(15) -ac: 设定声音的Channel数
(16)  -r: 提取图像频率（用于视频截图）
(17) -c:v:  输出视频格式
(18) -c:a:  输出音频格式
(18) -y:  输出时覆盖输出目录已存在的同名文件
(19)dropout_transition=3 声音淡出时间为3秒
```

## 转换视频分辨率

[命令]
>ffmpeg -i vodeo_input.mp4 -s 640x480 -b 2000k -c:a copy video_output.mp4 [-s 视频分辨率 -b 码率（rate） -c:a copy代表复制原视频的视频和音频编码不做任何改， 最后输出output文件]

```shell
# 使用gpu
ffmpeg -i input.mp4 -c:v h264_nvenc -s 640x480 -b:v 600k output.mp4
```

### 设置视频比例
```shell
ffmpeg -i jdjc.mp4 -aspect 16:9 -level 31 -b 3000k test.mp4
```

## 视频格式化步骤
>* 提取音频
>* 提取视频
>* 提取的视频 + 音频 + 根据最短（shortest）合并新视频

### 视频提取音频
```shell
ffmpeg -i 3.mp4 -vn -y -acodec copy 3.m4a
```

### 视频提取 视频
```shell
ffmpeg -i ct.mp4 -an -vcodec copy -y ct_1.mp4
```

### 视频对其 音频+视频
```shell
ffmpeg -i ct.mp4 -i ct.m4a -shortest  -y video/ct.mp4
```

## 文件类型设置

[命令]
>ffmpeg -i video_input.avi -target vcd vcd.mpg [target 转换文件为 vcd 格式 并输出]

## 视频转码设置无损 x264

[命令]
>ffmpeg -i video_input.mp4 -c:v libx264 -preset veryslow -crf 18 -c:a copy output.mp4 

[x264提供三种码率控制的方式，bitrate,qp,crf 三种是互斥的，使用时设置其一]

>-bitrate: 会尝试用给定的元率作为整体平均值来编码，这意味着最终编码文件大小是已知的，但文件质量未知，所以通常与 -pass 一起使用
>-qp : 当qp为0 时，无损编码
>-crf: (取值范围 1-51)取值越小质量越好码率越高，降低没有必要的针来提高质量，crf = 0时 与 qp=0 相同

>-preset: 调节编码速率和质量的平衡(有ultrafast、superfast、veryfast、faster、fast、medium、slow、slower、veryslow、placebo这10个选项，从快到慢)
>-tune: 主要配合视频类型和视频优化的参数，

### 参考
> [https://wenku.baidu.com/view/f4e48c087fd5360cba1adbba.html]

>ffmpeg -i vodeo_input.mp4 -s 640x480 -b 2000k -c:a copy video_output.mp4 [-s 视频分辨率 -b 码率（rate） -c:a copy代表复制原视频的视频和音频编码不做任何改， 最后输出output文件]切割

## 视频分割 && 合并
> * 操作流程 [1. 视频分割成一小段mp4格式小视频 2. 将小视频转为 ts 格式小视频 3. 合并所有ts小视频为 mp4 格式视频]

```shell
# t.txt 内容
file 't1.ts'
file 't2.ts'
#  视频合并
ffmpeg -f concat -i t.txt -vcodec h264_nvenc -acodec copy -f mp4 yx_o1.mp4
```

```shell
ffmpeg -i /data1/product/v4/assets/video/ct.ts -i com/zs_710587_CT.mp4 -i /data1/product/v4/assets/video/cw.ts -i com/zs_710587_CW.mp4 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a] concat=n=4:v=1:a=1" -c:v copy -vcodec h264_nvenc -y tt.mp4
```

>* 上面的命令合并了三种不同格式的文件，FFmpeg concat 过滤器会重新编码它们。注意这是有损压缩。 
[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] 分别表示第一个输入文件的视频、音频、第二个输入文件的视频、音频、第三个输入文件的视频、音频。concat=n=3:v=1:a=1 表示有三个输入文件，输出一条视频流和一条音频流。[v] [a] 就是得到的视频流和音频流的名字，注意在 bash 等 shell 中需要用引号，防止通配符扩展   [http://www.voidcn.com/article/p-xzdyrfxk-bhs.html]

## 视频分割 && 合并

### 按时长分割视频
```shell
ffmpeg -ss 60 -t 60  -i input.mp4 -c copy out-2.mp4
```
> * [-ss 开始时间的秒数 或者分钟数(00:01:00) -t 切割 n 秒长的视频，或者截止多长时间的视频(00:01:00)]

```shell
ffmpeg -re -i  input.mp4 -c copy -f segment -segment_format mp4 -segment_times 3,6,9 out.mp4
```
> * [视频按时间点切割 3,6,9  是 3 秒 6 秒 9 秒 分别切割出一段视频]

```shell
ffmpeg -i 33521499_401181_1525176287.mp4 -f segment -strftime 1 -segment_time 60 -segment_format mp4 out%Y-%m-%d_%H-%M-%S.mp4
```
> * [按分钟切割]

### 视频 mp4 转 ts格式
```shell
ffmpeg -y -i input.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb out.ts
```
### 视频合并  多个ts文件视频 合并成 mp4
```python
ffmpeg -y -i "concat:test.ts|test1.ts" -acodec copy -vcodec copy -absf aac_adtstoasc out.mp4
```
```shell
# list.txt 内容 file 'out-1.mp4'
ffmpeg -f concat -i list.txt -c copy concat.mp4

# or
ffmpeg -y -i input.mp4 -ignore_loop 0 -i ICON_01.gif -filter_complex "overlay=x=10:y=10:shortest=1" -vcodec h264_nvenc -acodec copy -f mp4 out.mp4
```

### 视频切割并生成ts文件
```shell
ffmpeg -i input.mp4 -c:v libx264 -c:a copy  -hls_time 60 -hls_list_size 0 -f hls output.m3u8
```
> * hls_time 设置每片的长度，默认值为2。单位为秒
> * hls_list_size 设置播放列表保存的最多条目，设置为0会保存有所片信息，默认值为5
> * hls_wrap  设置多少片之后开始覆盖，如果设置为0则不会覆盖，默认值为0项能够避免在磁盘上存储过多的片，而且能够限制写入磁盘的最多的片的数量
> * start_number 设置播放列表中sequence number的值为number，默认值为0 提示：播放列表的sequence number 对每个segment来说都必须是唯一的，而且它不能和片的文件名混淆，因为在，如果指定了“wrap”选项文件名会出现重复使用

> * -threads 1 使用线程数 

### 视频切割 按每分钟切割
```shell
ffmpeg  -i input.mp4 -c copy -map 0 -f segment -segment_time 60 out_mp4_%d.mp4
```

### 视频切割 按时间进行切割(segment_time 秒)
```shell
ffmpeg -i input_file [-i inputfile] -c copy -map 0 -f segment -segment_time 秒 输出_目录/文件名称_%d.mp4
```
### 硬编码 [url:https://developer.nvidia.com/ffmpeg]
> * [需要机器支持GPU 并支持 NVIDIA 显卡驱动和 CUDA] 
```shell
ffmpeg -y -i input_file.mp4 -c:v h264_nvenc -s 1280x720 -b:v 2000k out.mp4

ffmpeg -y -i input.mp4 -c:v h264_nvenc -vcodec h264_nvenc -s 1280x720 -b:v 2000k -f mp4 out.mp4
```
### 选择使用GPU
```python
    # 生成随机数
    r = random.randint(0,1)
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    # 随机使用第r块GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = str(r)
```
> * 使用 GPU 硬编码
```shell
# 1 to 1
ffmpeg -hwaccel cuvid -c:v h264_cuvid -i <input.mp4> -vf scale_npp=1280:720 -c:v h264_nvenc <output.mp4>
# 1 to n
ffmpeg -hwaccel cuvid -c:v h264_cuvid -i <input.mp4> -vf scale_npp=1280:720 -vcodec h264_nvenc <output0.mp4> -vf scale_npp 640:480 -vcodec h264_nvenc <output1.mp4>
```

### 视频加图片水印
```shell
# 使用 硬编码  50:50（x:y 坐标）
ffmpeg -y -i input.mp4 -vf "movie=logo.png[wm]; [in][wm]overlay=50:50[out]" -c:v h264_nvenc output.mp4

# 正常编码
ffmpeg -y -i input.mp4 -vf "movie=logo.png[wm]; [in][wm]overlay=50:50[out]" output.mp4

# overlay=x=main_w-120:y=40  （logo在视频位置距离：logo左边距,距离视频 右边距 120 px logo 距离顶部 40 px）
ffmpeg -y -i cs_16794_FDJC.mp4 -vf "movie=logo.png[wm]; [in][wm]overlay=x=main_w-120:y=40[out]" output.mp4

# 插入多张图
ffmpeg -y -i input.mp4 -vf "movie=logo.png [wm]; movie=ct.png[wm1];[c][wm]overlay=x=100:y=100 [out];[out][wm1] overlay=x=400:y=400" -f mp4 logo.mp4

# 或者
ffmpeg -i zs_420714_CT.mp4 -i 1.png -i 2.png -filter_complex "overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))',overlay=x=100:y=100:enable='if(gt(t,15),lt(t,20))'" -y 0.mp4
```

# FFmpeg 音频

### ffmpeg 视频静音
```shell
    ffmpeg -i input.mp4 -i mute.mp3 -map 0:0 -map 1:0 -c copy output.mp4
    # 这里，0：0中的第一个数字是输入文件（0代表视频文件，1代表音频文件），第二个数字是来自该文件的数据流（0，因为每个流只有一个视频或音频） 。这两个流将被映射到一个输出文件，所以第一个视频，然后是音频
```

### ffmpeg 视频静音后 添加一段音频
```shell
# 1 将视频流进行分离，分离出没有音频的视频
ffmpeg -i input.mp4 -vcodec copy -an out.mp4   //分离视频流
# 将 mp3 音频文件转成 wav 
ffmpeg -i music.mp3 music.wav
# 或者 阶段相同视频长度的音频
ffmpeg -i music.wav -ss 0 -t 37 musicshort.wav

# 将音频合并到视频中(从第视频起始合并)
ffmpeg -i musicshort.wav -i out.mp4 out1.mp4

# 将音频插入到视频的某一个时间
ffmpeg -y -i mute/cs_16794_FDJC.mp4 -itsoffset 00:00:5 -i yqns.wav -map 0:0 -map 1:0 -c:v copy -preset ultrafast -async 1 o2.mp4

# 视频一次添加多个语音文件在指定时间（先静音,不能为mp3格式）
ffmpeg -i input.mp3 -acodec alac -ab 128k -ar 48000 -ac 2 -y output.m4a 

ffmpeg -i input.mp4 -itsoffset 10.555 -i ct.m4a -itsoffset 20.999 -i ct.m4a -itsoffset 70 -i ct.m4a -map 0:1 -map 1:0 -map 2:0 -map 3:0 -c:v copy -preset ultrafast -f mp4 -y out1.mp4
```

### 视频防抖动
```shell
ffmpeg -y -i o1.mpeg -vf vidstabtransform=smoothing=30 -c:v h264_nvenc o2.mpeg
```

## 视频多宫格处理
```shell
ffmpeg -re -i yx_test_dd.mp4 -re -i o22.mp4 -filter_complex "nullsrc=size=1280x720 [base]; [0:v] setpts=PTS-STARTPTS,scale=680x400 [upperleft]; [1:v] setpts=PTS-STARTPTS, scale=680x480 [upperright]; [base][upperleft] overlay=shortest=1[tmp1];[tmp1][upperright] overlay=shortest=1:x=680" -c:v h264_nvenc o33.mp4
```

### 复制并生成某个时长的音频
```shell
# 循环 5 遍，长 10 秒
ffmpeg -stream_loop 5 -i ct.mp3 -t 10 ct_out.mp3
```

### 将一个 音频 放到 某个静音视频的头部，若音频较短，则生成于视频相同时长的静音进行填补
```shell
ffmpeg -i mute/cs_16794_FDJC.mp4 -i ct.mp3 -filter_complex "[1:0]apad" -shortest o1.mp4
```

### 音频固定时间插入音频
```shell
# 1 将第一个音频 第一个声道 延迟 n 秒播报 （5秒）
ffmpeg -y -i cw.mp3 -filter_complex adelay="5000" cwc.mp3

# 音频批量延迟 自定义各自延迟 n 秒 （10000 = 10秒）
ffmpeg -y -i ct.mp3 -i cw.mp3 -filter_complex "[0:0]adelay=10000[o1];[1:0]adelay=20000[o2]" -map "[o1]" t1.mp3 -map "[o2]" t2.mp3

# 2 将第 主音频 于插入音频混合 
ffmpeg -y -i ovc.mp3 -i cwc.mp3 -filter_complex amix=inputs=2:duration=longest:dropout_transition=3 o3.mp3

# 或者 mp4 直接合并 mp4 
ffmpeg -y -i o1.mp4 -i cwc.mp3 -filter_complex amix=inputs=2:duration=longest:dropout_transition=3 -vcodec copy ov3.mp4

# 多个合并
ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 -filter_complex amix=inputs=3:duration=first:dropout_transition=3 OUTPUT
```

### ffmpeg 视频加文字水印
```shell
#  需要字体 FreeSerif.ttf 文件 [https://fonts2u.com/download/free-serif.family][https://fonts2u.com/free-serif.font]
ffmpeg -y -i 64862406_525441_1526891425.mp4 -vf "drawtext=fontsize=100:fontfile=FreeSerif.ttf:text='hello world' :fontcolor=white"  o4.mp4

# 同时添加多个文字水印，并且 指定某个文字 在第几秒显示 显示截止到第几秒
ffmpeg -y -i zs_420714_ZQCS.mp4 -vf "[in]drawtext=fontsize=36:fontfile=PingFang-SC-Regular.ttf:text='正在检查漆膜厚度':x=100:y=100:enable='if(gt(t,10),lt(t,20))':fontcolor=white[a1];[a1]drawtext=fontsize=36:fontfile=PingFang-SC-Regular.ttf:text='正在检查漆膜厚度':x=200:y=200:fontcolor=white [out]"  o4.mp4
```

### 图片生成视频
```shell
ffmpeg -r 25 -start_number 2 -i img%d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
# or
ffmpeg -r 25 -start_number 2 -i img%d.png -s:v 1280x720 -c:v libx264 -profile:v high -r 30 -pix_fmt yuv420p out.mp4
```

### png 转 gif
```shell
# 将图片生成 png  img1.png img2.png img3.png
ffmpeg -i img%d.png -vf palettegen palette.png

# 将图片根据 生成的 png 生成 gif
ffmpeg -v warning -i img%d.png -i palette.png  -lavfi "paletteuse,setpts=6*PTS" -y out.gif
```

### png 合成 apng
```shell
ffmpeg -framerate 10 -i ../zdtd_%5d.png -f apng -s 1000x500 zdtd.apng
# or
ffmpeg -i jdjc.png -s 230x150 -r 10 -filter_complex "[0:v]format=rgba" jdjc.apng
```

### gif 添加到视频 循环播放
```shell
# apng 图片格式必须是 rgba 不能提供 pal8 （png 针图生成 apng 图url[https://github.com/jiashaokun/doc/blob/master/png_create_apng/ChangeReso.sh]）
# scale 设置缩放比  n 越大 gif 越小
ffmpeg -y -i input.mp4 -ignore_loop 0 -i out1.gif -filter_complex 'overlay=x=100:y=100:shortest=1' out8.mp4

# or

ffmpeg -y -i zs_420714_CT.mp4 -filter_complex 'movie=c_01.png:loop=0[animation];[0:v][animation]overlay=x=100:y=100:shortest=1' out.mp4

# exp
ffmpeg -y -i input.mp4 -ignore_loop 0 -i p1.png -filter_complex '[0:v]scale=iw:ih[a];[1:v]scale=150:98[wm];[a][wm]overlay=x=30:y=30:shortest=1' -preset faster out.mp4
```

### ffmpeg 添加字幕文件

```shell
ffmpeg -i zs_712837_ZQCS.mp4 -vf subtitles=test.srt -vcodec h264_nvenc -y o3.mp4

# 如果视频文件出现乱码的情况，观察编译过程：[Parsed_subtitles_0 @ 0x2012b40] fontselect: (Arial, 400, 0) -> /usr/share/fonts/lyx/msam10.ttf, 0, PingFangSC

# MMB被这个坑了好长时间 走的是 PingFangSC 字体，找的却是 msam10.ttf 外星文，妈的，骂人，反正我不懂，我就开骂，处理如下
# cp /usr/share/fonts/lyx/msam10.ttf /usr/share/fonts/lyx/msam10.ttf_base
# cp ../assets/font/PingFang-SC-Regular.ttf /usr/share/fonts/lyx/msam10.ttf
```
### ffmpeg 同时添加图片和文字水印
```shell
ffmpeg -y -i tt.mp4 -i logo.png -filter_complex "[0:v]drawtext=fontfile=PingFang-SC-Regular.ttf:text='测试一下':fontcolor=#FFFFFF:fontsize=36:x=100:y=100[text];[text][1:v]overlay=0:0[out]" -map "[out]" -map 0:a -codec:v libx264 -codec:a copy output.mp4

# 限制显示时间

ffmpeg -y -i tt.mp4 -i logo.png -filter_complex "[0:v]drawtext=fontfile=PingFang-SC-Regular.ttf:text='测试一下':fontcolor=#FFFFFF:fontsize=36:x=100:y=100:enable='if(gt(t,5),lt(t,10))'[text];[text][1:v]overlay=0:0:enable='if(gt(t,5),lt(t,10))'[out]" -map "[out]" -map 0:a -codec:v libx264 -codec:a copy output.mp4

# 乱序 (文字和图片水印顺序不固定 不支持多个)
ffmpeg -i test.mp4 -vf "movie=logo.png[w1];drawtext=text='HelloWorld':fontfile=PingFang-SC-Regular.ttf:fontsize=25:x=500:y=500:enable='if(gt(t,10),lt(t,20))':fontcolor=white[w2];[w2][w1]overlay=x=100:y=100:enable='if(gt(t,10),lt(t,20))'" -f mp4 -y out.mp4
```

### 同时打入 图片水印 和 字幕
```shell
ffmpeg -i test.mp4 -i logo.png -i logo.png -filter_complex "overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))',overlay=x=100:y=100:enable='if(gt(t,15),lt(t,20))', subtitles=tt.srt" out.mp4
```

### 同时打入 图片水印 字幕 apng 文字水印
```shell
ffmpeg -i test.mp4 -i logo.png -i logo.png -ignore_loop 0 -i ct.apng -filter_complex "overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))',overlay=x=100:y=100:enable='if(gt(t,15),lt(t,20))', overlay=x=300:300:shortest=1, subtitles=tt.srt,drawtext=text='hello':fontfile=PingFang-SC-Regular.ttf:x=100:y=100:enable='if(gt(t,10),lt(t,20))':fontcolor=white,drawtext=text='world':fontfile=PingFang-SC-Regular.ttf:x=200:y=200:enable='if(gt(t,10),lt(t,20))':fontcolor=white" out.mp4

ffmpeg -i input.mp4 -ignore_loop 0 -i ct.apng -i p1.png -i p2.png -filter_complex "overlay=x=300:300:shortest=1, overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))',overlay=x=100:y=100:enable='if(gt(t,15),lt(t,20))', subtitles=txt.srt,drawtext=text='正在检查...':fontfile=siyuan-heiti-normal.ttf:x=100:y=100:enable='if(gt(t,10),lt(t,20))':fontcolor=white,drawtext=text='正在检查...':fontfile=siyuan-heiti-normal.ttf:x=200:y=200:enable='if(gt(t,10),lt(t,20))':fontcolor=white" -af "volume=9" -y -vcodec h264_nvenc o1.mp4
```

### 视频左右拼接到一个屏幕
```shell
# dropout_transition 声音淡出时间   volume 音量
ffmpeg -i input.mp4 -i input2.mp4 -filter_complex "[0:v]pad=w=iw*2:h=ih[b];[b][1:v]overlay=x=W/2" -filter_complex amix=inputs=2:duration=first:dropout_transition=2,volume=1 -y out.mp4
```

### 视频合并并转换 多个 码率
```shell
ffmpeg -y -f concat -safe 0 -i video.ts -af volume=9 -s 1280x720 -b 2000k -vcodec h264_nvenc out1.mp4 -af volume=9 -s 1080x720 -b 1200k -vcodec h264_nvenc out2.mp4
```

### 合并 未测试
```shell
ffmpeg -threads 3 -noautorotate  -max_error_rate 0.99 -fflags +genpts  -y   -loglevel info  -probesize 100000000 -analyzeduration 300000000  -user_agent tmpfs_cache -reconnect 1  -f concat -safe -1 -auto_convert 1  -timeout 30000000 -i "video.txt" -map 0:v? -map 0:a? -vcodec copy  -acodec copy -bsf:a aac_adtstoasc  -f mp4 -movflags +faststart  -threads 6  -metadata description="QNY APD MTS" tmp.mp4
```

### 弹幕效果
```shell
ffmpeg -i face.mp4 -vf "drawtext=text=蜡笔小新为什么喜欢脱裤子:fontcolor=white: fontsize=40 :fontfile=PingFang-SC-Regular.ttf:y=h-line_h:x=w-t*150, drawtext=text=蜡笔小新为什么喜欢脱裤子2:fontcolor=green: fontsize=40 :fontfile=PingFang-SC-Regular.ttf:y=100:x=w-(t-2)*150:enable='gte(t,2)'" -y m1.mp4
# x=横向坐标-（当前时间*2秒）*150 (越大越快)  2秒是要延迟出现的时间
```

### 跑马灯效果 循环播放
```shell
ffmpeg -i input.mp4 -vf “drawtext=text=蜡笔小新为什么喜欢脱裤子 :expansion=normal:fontfile=PingFang-SC-Regular.ttf: y=h-line_h-10:x=(mod(5*n\,w+tw)-tw): fontcolor=white: fontsize=40: shadowx=2: shadowy=2" mn.mp4
```

### 视频插入 gif png 字幕 音频 弹幕
```shell
ffmpeg -i face2.mp4 -ignore_loop 0 -i lbxx.gif -i hz_1.png -i mz_1.png -filter_complex "overlay=x=10:10:shortest=1,overlay=x=105:235:enable='if(gt(t,6.5),lt(t,7.3))', overlay=x=85:y=80:enable='if(gt(t,6.5),lt(t,7.3))', subtitles=pfzl.srt, drawtext=text='蜡笔小新为什么这么喜欢脱裤纸?':fontcolor='white':fontsize=40:fontfile=PingFang-SC-Regular.ttf:y=h-line_h:x=w-t*150, drawtext=text='超人为什么喜欢把内裤穿在外面?':fontcolor='white':fontsize=40:fontfile=PingFang-SC-Regular.ttf:y=100:x=w-(t-2)*150:enable='gte(t,2)'" -an -i pfzl.mp3 -y out.mp4

# + 马赛克
ffmpeg -i face2.mp4 -ignore_loop 0 -i lbxx.gif -i hz_1.png -i mz_1.png -filter_complex "overlay=x=10:10:shortest=1,overlay=x=105:235:enable='if(gt(t,6.5),lt(t,7.3))', overlay=x=85:y=80:enable='if(gt(t,6.5),lt(t,7.3))', subtitles=pfzl.srt, drawtext=text='蜡笔小新为什么这么喜欢脱裤纸?':fontcolor='white':fontsize=40:fontfile=PingFang-SC-Regular.ttf:y=h-line_h:x=w-t*150, drawtext=text='超人为什么喜欢把内裤穿在外面?':fontcolor='white':fontsize=40:fontfile=PingFang-SC-Regular.ttf:y=100:x=w-(t-2)*150:enable='gte(t,2)', delogo=120:150:w=100:h=120:enable='gt(t,8)'" -an -i pfzl.mp3 -y out.mp4

```
视频分割 && 合并
### 音频淡入淡出
```shell
# 12秒视频 3秒淡入 正常播放 6 秒后淡出 3 秒 (如果音频时长 20 秒 淡出后的为静音)
ffmpeg -i acc/pfzl.mp3 -af afade=t=in:st=0:d=3,afade=t=out:st=6:d=3  -y dd.mp3
```

### 镜子效果 水平翻转
```shell
# crop(剪裁视频到给定的大小)里的参数依次为： 左边距：右边距：宽度：高度
ffmpeg -i face2.mp4 -vf "crop=iw:ih:0:0,split[left][tmp];[tmp]hflip[right];[left][right] hstack" -y jz.mp4
```

### 视频颜色复古
```shell
ffmpeg -i face2.mp4 -vf curves=strong_contrast  out.mp4
```

### 视频打马
```shell
ffmpeg -i face2.mp4 -filter_complex "delogo=x=20:y=20:w=100:h=100" out.mp4
```

### 视频增加黑边
```shell
# 原视频 84x702 加入 黑边后变为  692-》732   0:20 上下多 20像素 黑边 
# pad 就是存放图像的画板

ffmpeg -i 384x692.mp4 -vf "pad=384:732:0:20:black" -y hb.mp4
```

### 视频倒放
```shell
ffmpeg -i face2.mp4 -vf reverse -af areverse reversed.mp4
```

### 视频旋转
```shell
# PI = 圆周率 3.14
ffmpeg -i face2.mp4 -vf rotate=PI/6 out.mp4
```

### 音频倍速处理（降一半）
```shell
ffmpeg -i acc/pfzl.mp3 -filter_complex "atempo=tempo=0.5" -acodec aac output.aac
```

### 音频翻转
```shell
ffmpeg -i acc/pfzl.mp3 -af areverse -y fz.mp3 
```

### OS X 下设备采集
```shell
ffmpeg -f avfoundation -list_devices true -i ""
```


### mac 视频录制
```shell
ffmpeg -f avfoundation -capture_cursor 1 -i "Capture screen 0" -r:v 30  -y out.mp4
```

### 直播录制视频
```shell
ffmpeg -f avfoundation -r 30 -i "1:0" -f avfoundation -r 30 -s 640x480 -i "0" -c:v libx264 -preset ultrafast -filter_complex 'overlay=main_w-overlay_w-10:main_h-overlay_h-10' -acodec libmp3lame -ar 44100 -ac 1  -f mp4 -y out.mp4
```

### 直播录制时 加入图片 + 弹幕
```shell
ffmpeg -f avfoundation -r 30 -i "1:0" -f avfoundation -r 30 -s 640x480 -i "0" -i img/hz.png -c:v libx264 -preset ultrafast -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10, overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))', drawtext=text=蜡笔小新为什么喜欢脱裤子:fontcolor=white: fontsize=40 :fontfile=PingFang-SC-Regular.ttf:y=h-line_h:x=w-t*150, drawtext=text=蜡笔小新为什么喜欢脱裤子2:fontcolor=green: fontsize=40 :fontfile=PingFang-SC-Regular.ttf:y=100:x=w-(t-2)*150:enable='gte(t,2)'" -acodec libmp3lame -ar 44100 -ac 1  -f mp4 -y out.mp4
```

### 采集摄像头视频
```shell
ffmpeg -f avfoundation -r 30 -i "FaceTime HD Camera"  -y out.mp4
```

### 采集桌面屏幕视频
```shell
ffmpeg -f avfoundation -capture_cursor 1 -i "Capture screen 0" -r:v 30  -y out.mp4
```

### 采集麦克风
```shell
ffmpeg -f avfoundation -i ":0" -y out.aac
```

### 举例录制ppt分享
```shell
ffmpeg -f avfoundation -capture_cursor 1 -i "1:0" -r:v 30  -vcodec libx264 -preset ultrafast -acodec aac  -y out.mp4 
```

### 视频推流到 udp
```shell
# 1. 打开一个udp播放通道
ffplay -f h264 udp:127.0.0.1:9000 -fflags nobuffer

# 2. 推流 摄像头录制的视频流 到 udp 通道
ffmpeg -f avfoundation -r 30 -i "FaceTime HD Camera" -vcodec h264 -f h264 udp:127.0.0.1:9000
```

### 视频插入一个淡入淡出的图片
```shell
# in 淡入 st 开始时间 d 淡入时长为 1 秒，out 淡出 st 开始时间 d 淡出时长
ffmpeg -i video -filter_complex "[1:v]fade=t=in:st=5:d=1,fade=t=out:st=10:d=1[v1];[0:v][v1]overlay=x=200:y=100" -preset veryfast -y pi.mp4

ffmpeg -i i2.mp4 -loop 1 -i 2.png -filter_complex "[1:v]fade=t=in:st=6:d=1,fade=t=out:st=10:d=1[v1];[0:v][v1]overlay=x=340:y=550:shortest=1" -y i3.mp4
```

### 视频插入淡入淡出的图片，从左入，到某个点停止
```shellal
ffmpeg -i input.mp4 -loop 1 -i 2.png -filter_complex "[1:v]format=rgba,scale=-2:100,fade=in:st=4:d=1.5:alpha=1,fade=out:st=9:d=0.3:alpha=1[png];[0:v][png]overlay=x='min(-11*w/3+2*w*t/3,0)':3*(H-h)/4-0:shortest=1:enable='between(t,3,10)'" -preset veryfast -y output.mp4
```

### 图片缩放成 n 秒的视频
```shell
# 参考命令 [http://trac.ffmpeg.org/ticket/4298]  d 控制深度
ffmpeg -framerate 25 -loop 1 -i in.jpg -vf "zoompan=z='min(zoom+0.0015,1.4)':x=50:d=150" -t 6 -s 640x380 out.mp4

ffmpeg -framerate 25 -loop 1 -i ct.png -vf "zoompan=z='min(zoom+0.0015,2)':d=150" -t 6 -s 640x380  -y out.mp4
```

### apng or gif 加入文字内容
```shell
ffmpeg -i apng/ddchm.apng -vf "drawtext=text='正在检查...':fontfile=PingFang-SC-Regular.ttf:x=100:y=100:fontcolor=white" -y out.apng
```

### demo
```shell
ffmpeg -y -i input.mp4 -i bj.png -filter_complex "[0:v][1:v] overlay=x='if(gte(((t-1)*300)-w,100),w,((t-1)*300)-w)':y=100:enable='lte(t,5)'"  out1.mp4;\
ffmpeg -y -i out1.mp4 -i logo.png -filter_complex "[0:v][1:v] overlay=x='if(gte(((t-2)*300)-w,100),w,((t-2)*300)-w)':y=150:enable='lte(t,5)'"  out2.mp4;\
ffmpeg -y -i out2.mp4 -i logo.png -filter_complex "[0:v][1:v] overlay=x='if(gte(((t-3)*300)-w,100),w,((t-3)*300)-w)':y=200:enable='lte(t,5)'"  out.mp4;
```

### 设置apng大小（小汽车使用）
```shell
ffmpeg -i apng/ic_01.apng -vf "scale=320:320" -y o.apn
```

### 打进视频
```shell
ffmpeg -i input.mp4 -i o.apng -filter_complex "overlay=x=100:y=500:enable='if(gt(t,6),lt(t,10))'" -y output.mp4
```

### 上牌时间
```shell
ffmpeg -i bj.png -vf "drawtext=text='上牌日期2018年12月8日':fontfile=PingFang-SC-Regular.ttf:x=50:y=60:fontcolor=white:fontsize=32, drawtext=text='行驶里程59270公里':fontfile=PingFang-SC-Regular.ttf:x=50:y=110:fontcolor=white:fontsize=32" -y out.png
```

### 阴影坐标
```shell
ffmpeg -i i2.mp4 -loop 1 -i 2.png -filter_complex "[1:v]fade=t=in:st=6:d=1,fade=t=out:st=10:d=1[v1];[0:v][v1]overlay=x=340:y=550:shortest=1" -y i3.mp4
```