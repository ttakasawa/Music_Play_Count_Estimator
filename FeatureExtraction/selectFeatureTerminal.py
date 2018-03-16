from __future__ import print_function
import librosa
from pydub import AudioSegment
import os
#from audioSegmentation.py import function(a,b)
from extractBeat import getBeat
from audioSegmentation import split

AddressOfInputAudio = ""
NameOfSong = ""

#######################    splitting audio    ################################
# get estimated tempo, beat per minute
#	-> param: Name of audio w/o .mp3, isDynamic
#										-> Static: 0, dynamic: 1
#
dest = ""
split(AddressOfInputAudio, NameOfSong, dest)
#
###############################################################################


###########################    getTempo    ####################################
# get estimated tempo, beat per minute
#	-> param: Name of audio w/o .mp3, isDynamic
#										-> Static: 0, dynamic: 1
#audioName = 'a2'
#print(getBeat(audioName, 1))
#
###############################################################################






