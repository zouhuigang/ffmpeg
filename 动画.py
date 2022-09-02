import subprocess

# https://trac.ffmpeg.org/wiki/Xfades

'''
/Applications/ffmpeg -f concat -i mylist.txt -c copy output.mp4
/Applications/ffmpeg -i output.mp4 -i 有字幕.mp4 -filter_complex "[0]settb=AVTB[v0];[1]settb=AVTB[v1];[v0][v1]xfade=transition=fade:offset=2:duration=1,format=yuv420p" out.mp4
'''
cmdLine = '''/Applications/ffmpeg -i pig.mp4 -i 有字幕.mp4 -filter_complex "xfade=transition=radial:duration=1:offset=0,format=yuv420p" -y radialVideo.mp4'''
subprocess.call(cmdLine, shell=True)
