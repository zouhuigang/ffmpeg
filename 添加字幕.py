import subprocess
videopath ="pig.mp4"
srtpath ="字幕.srt"
outpath ="有字幕"+".mp4"
subprocess.call(("/Applications/ffmpeg -i " + videopath + " -vf subtitles="+srtpath+" "+ outpath ),shell=True)
