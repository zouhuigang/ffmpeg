import requests

subtitle_url = 'https://i0.hdslb.com/bfs/subtitle/e837950453ea3e4f6e81a5709449af173d2604dc.json'  # 获取字幕的网址示例
subtitle_r = requests.get(subtitle_url)
sub_content = subtitle_r.json()['body']  # 提取弹幕内容的json


def s2hms(x):  # 把秒转为时分秒
	m, s = divmod(x, 60)
	h, m = divmod(m, 60)
	hms = "%02d:%02d:%s" % (h, m, str('%.3f' % s).zfill(6))
	hms = hms.replace('.', ',')  # 把小数点改为逗号
	return hms


with open('字幕.srt', 'w', encoding='utf-8') as f:
	write_content = [str(n + 1) + '\n' + s2hms(i['from']) + ' --> ' + s2hms(i['to']) + '\n' + i['content'] + '\n\n' for
	                 n, i in enumerate(sub_content)]  # 序号+开始-->结束+内容
	f.writelines(write_content)
