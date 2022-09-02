from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from auditok import split
from os import walk
import io
import os
import subprocess
import wave
import math
import audioop
import tempfile
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "assets/Cloud_Speech_API.json"


def find_speech_regions_V2(source_file):
	"""
    pip install forked-auditok-split-without-data
    """
	audio_regions = split(source_file)
	regions = []
	for region in audio_regions:
		region_start = float(region.get('start'))
		region_end = float(region.get('end'))
		regions.append((region_start, region_end))
	return regions


def find_speech_regions(source_file, frame_width=4096, min_region_size=0.5, max_region_size=10, percent=0.2):
	"""
	撈出有聲音的部分
	"""

	reader = wave.open(source_file)
	sample_width = reader.getsampwidth()
	rate = reader.getframerate()
	n_channels = reader.getnchannels()
	chunk_duration = float(frame_width) / rate

	n_chunks = int(math.ceil(reader.getnframes() * 1.0 / frame_width))
	energies = []

	for _ in range(n_chunks):
		chunk = reader.readframes(frame_width)
		energies.append(audioop.rms(chunk, sample_width * n_channels))

	threshold = percentile(energies, percent)
	elapsed_time = 0
	regions = []
	region_start = None

	for energy in energies:
		is_silence = energy <= threshold

		max_exceeded = region_start and elapsed_time - region_start >= max_region_size

		if (max_exceeded or is_silence) and region_start:
			if elapsed_time - region_start >= min_region_size:
				regions.append((region_start, elapsed_time))
				region_start = None

		elif (not region_start) and (not is_silence):
			region_start = elapsed_time
		elapsed_time += chunk_duration

	return regions


def percentile(arr, percent):
	"""
	計算arr的percentile
	"""
	arr = sorted(arr)
	index = (len(arr) - 1) * percent
	floor = math.floor(index)
	ceil = math.ceil(index)
	if floor == ceil:
		return arr[int(index)]

	low_value = arr[int(floor)] * (ceil - index)
	high_value = arr[int(ceil)] * (index - floor)

	return low_value + high_value


def ffmpeg_cut_slience(source_file, output_file):
	"""
	用ffmpeg_cut_slience移除
	Args:
	  source_file : source
	  output_file : slience removed file
	"""
	# ffmpeg -i input/g591154478336.20200723101259087-in.wav -af "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse" output/sample2.wav
	program_ffmpeg = "ffmpeg"

	slience_command = "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse"

	command = [str(program_ffmpeg), "-y", "-i", source_file,
	           "-af", slience_command, output_file]

	use_shell = True if os.name == "nt" else False
	subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)


def ffmpeg_split_audio(source_file, region):
	"""
	傳入音檔，拆出片段
	"""
	program_ffmpeg = "ffmpeg"

	try:
		start, end = region
		start = max(0, start - 0.25)
		end += 0.25
		temp = tempfile.NamedTemporaryFile(suffix='.wav')
		file_head, file_name = os.path.split(temp.name)
		output_file = "output/" + file_name

		command = [program_ffmpeg, "-ss", str(start), "-t", str(end - start),
		           "-y", "-i", source_file,
		           "-loglevel", "error", output_file]

		use_shell = True if os.name == "nt" else False
		subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)

		return output_file
	except:
		pass


def sample_recognize(local_file_path, type):
	"""
	Transcribe a short audio file using synchronous speech recognition
	Args:
	  local_file_path : source
	  type : speaker
	"""

	client = speech_v1.SpeechClient()
	language_code = "zh-TW"
	sample_rate_hertz = 8000
	encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
	enable_automatic_punctuation = True
	enable_word_time_offsets = False

	config = {
		"language_code": language_code,
		"sample_rate_hertz": sample_rate_hertz,
		"encoding": encoding,
		"enable_automatic_punctuation": enable_automatic_punctuation,
		"enable_word_time_offsets": enable_word_time_offsets,
	}

	with io.open(local_file_path, "rb") as f:
		content = f.read()

	audio = {"content": content}

	response = client.recognize(config, audio)

	for result in response.results:
		alternative = result.alternatives[0]
		print(type + u": {}".format(alternative.transcript))


# Demo
regions = find_speech_regions("input/g591154478336.20200723101259087-in.wav")

for i, extracted_region in enumerate(regions):
	output_file = ffmpeg_split_audio("input/g591154478336.20200723101259087-in.wav", extracted_region)
	sample_recognize(output_file, "Agent")
	os.remove(output_file)
