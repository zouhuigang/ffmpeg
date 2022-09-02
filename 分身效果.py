from moviepy.editor import VideoFileClip, clips_array, vfx

clip1 = VideoFileClip("pig.mp4").margin(10)
clip2 = clip1.fx(vfx.mirror_x)#x轴镜像
clip3 = clip1.fx(vfx.mirror_y)#y轴镜像
clip4 = clip1.resize(0.6)#尺寸等比缩放0.6

final_clip = clips_array([
	[clip1, clip2],
	[clip3, clip3]
])
final_clip.resize(width=640).write_videofile("my_stack.mp4")
