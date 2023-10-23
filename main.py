import pydub
import sys
import os
import subprocess
import time

splice_time = 15

debug = False

if debug:
	path = "C:\\Users\\black\\Documents\\Programation\\Python\\Audio Splitter\\amanda.mp3"
	name, codec = "C:\\Users\\black\\Documents\\Programation\\Python\\Audio Splitter\\amanda.mp3".split('\\')[-1].split('.')
else:
	path = sys.argv[1]
	codec = sys.argv[1].split('\\')[-1].split('.')[1]
	name = input('Song name : ')


if os.path.exists(f"output/{name}"):
	print('Removing old one...\n')
	for i in os.listdir(f"output/{name}"):
		os.remove(f"output/{name}/{i}")
	os.rmdir(f"output/{name}")



print('Splicing Audio...')
startT = time.time()
splice = pydub.AudioSegment.from_file(path, fomrat=codec)[::splice_time*1000]
if name not in os.listdir('output/'):
	os.mkdir(f"output/{name}")
for i, v in enumerate(splice):
	with open(f"output/{name}/{i+1}.mp3", "wb+") as file:
		v.export(file, format="mp3")
print('Finished in', str(round(time.time()-startT, 4)) + "s\n")

print('Converting Audio in DFPWM...')
startTT = time.time()
for i in os.listdir(f"output/{name}"):
	subprocess.run(["ffmpeg", "-i", f"output/{name}/{i}", "-ac", "1", "-hide_banner", "-loglevel", "error", f"output/{name}/"+i.split('.')[0]+".dfpwm"])
print('Finished in', str(round(time.time()-startTT, 4)) + "s\n")

print('Cleaning mess...')
startTT = time.time()
for i in os.listdir(f"output/{name}"):
	if i.split('.')[1] == 'mp3':
		os.remove(f"output/{name}/{i}")
print('Finished in', str(round(time.time()-startTT, 4)) + "s\n")

print('Creating Manifest...')
manifest = []

size = len(os.listdir(f'output/{name}'))
ip = "http://90.0.184.7:25566/song/"

manifest.append(f"shell.run('wget {ip}{name}/1.dfpwm')")
manifest.append("shell.run('clear')")
manifest.append(f"print('1/'..{size})")
manifest.append("shell.run('speaker play 1.dfpwm')")
manifest.append(f"shell.run('wget {ip}{name}/2.dfpwm')")
manifest.append("shell.run('clear')")
manifest.append(f"print('2/'..{size})")
manifest.append("shell.run('speaker play 2.dfpwm')")



for i in range(len(os.listdir(f"output/{name}"))-2):
	manifest.append(f"shell.run('rm {i+1}.dfpwm')")
	manifest.append(f"shell.run('wget {ip}{name}/{i+3}.dfpwm')")
	manifest.append("shell.run('clear')")	
	manifest.append(f"print('{i+3}'..'/'..{size})")	
	manifest.append(f"shell.run('speaker play {i+3}.dfpwm')")

manifest.append(f"shell.run('rm {size-1}.dfpwm')")
manifest.append(f"shell.run('rm {size}.dfpwm')")


with open(f"output/{name}/manifest.lua", "w+") as file:
	file.write("\n".join(manifest))
print('Everything finished in', str(round(time.time()-startT, 4)) + "s\n")

input('Finished !')