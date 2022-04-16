#!/usr/bin/env python
# NOTE: ffmpeg
import sh
import re
from moviepy.editor import *
INPUT_FILE = "test.mov"
OUTPUT_FILE = "test.wav"


def video2gif(inputFile, outputFile, quality=1):
    if(quality != 1):
        clip = VideoFileClip(inputFile).resize(quality)
    else:
        clip = VideoFileClip(inputFile)

    clip.write_gif(outputFile)


def m4a2wav(inputFile, outputFile):
    sh.ffmpeg("-i", inputFile, outputFile)


def video2audio(inputFile, outputFile):
    video = VideoFileClip(inputFile)
    audio = video.audio
    audio.write_audiofile(outputFile)


def run():
    if re.search('mov', INPUT_FILE) != None and re.search('gif', OUTPUT_FILE) != None:
        video2gif(INPUT_FILE, OUTPUT_FILE)
    elif re.search('m4a', INPUT_FILE) != None and re.search('wav', OUTPUT_FILE) != None:
        m4a2wav(INPUT_FILE, OUTPUT_FILE)
    elif re.search('[mov|mp4]', INPUT_FILE) != None and re.search('wav', OUTPUT_FILE) != None:
        video2audio(INPUT_FILE, OUTPUT_FILE)
    else:
        pass


if __name__ == '__main__':
    run()
