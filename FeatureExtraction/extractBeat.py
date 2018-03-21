from __future__ import print_function
import librosa
import os


# from visualization import tempoVSautoCorrelation, dTempoOnTempogram


def getBeat(audioName, isDynamic):
    audioFileName = audioName + ".mp3"
    OutputPath = os.path.join(os.getcwd(), 'sampleOutput', audioFileName)

    y, sr = librosa.load(OutputPath)
    onset_env = librosa.onset.onset_strength(y, sr=sr)

    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    # If static tempo

    dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    # If dynamic tempo

    ###############################################################################
    #	*optional plotting
    #	tempoVSautoCorrelation(tempo, 512)
    #		-plotting estimated tempo VS Onset Auto Correlation
    #			-param: static tempo, hop default
    #
    #	dTempoOnTempogram(dtempo)
    #		-plotting dynamic tempo estimates over a tempogram
    #			-param: dynamic tempo
    ###############################################################################

    if isDynamic == 0:
        return tempo
    else:
        return dtempo
