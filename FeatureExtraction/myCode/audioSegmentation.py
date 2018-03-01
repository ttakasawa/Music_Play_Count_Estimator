from __future__ import print_function
import librosa
from pydub import AudioSegment
import os

def split(inputFile, name, dest):
	
	if inputFile == "":
		inputFile = librosa.util.example_audio_file()

	if dest == "":
		dest = os.getcwd()
		#If not specified, save it on ~/musicName/ 

	if name == "":
		name = 'sampleOutput'

	music = AudioSegment.from_file(inputFile)
	numSegments = len(music) / 5000 + 1
	#splitting audio file into 5 seconds pieces

	################################################################################
	#copying original mp3 file for testing purpose
	#
	#relPath = 'original.mp3'
	#OutputPath = os.path.join(currentPath, 'sampleOutput', relPath)
	#music.export(OutputPath, format="mp3")
	################################################################################

	for x in range(0, numSegments):
		print("We're on segment %d" % (x))
    	startPoint = len(music) / numSegments * (x)
    	endPoint = len(music) / numSegments * (x+1)
    	newAudio = music[startPoint:endPoint]
    	relPath = 'a' + str(x)  + '.mp3'
    	OutputPath = os.path.join(dest, name, relPath)
    	newAudio.export(OutputPath, format="mp3")


