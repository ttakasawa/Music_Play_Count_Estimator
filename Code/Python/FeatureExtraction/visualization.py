# Modifications of sample code appeares in https://librosa.github.io

import librosa
import matplotlib.pyplot as plt


def tempoVSautoCorrelation(tempo, hop_length):
    tempo = np.asscalar(tempo)
    ac = librosa.autocorrelate(onset_env, 2 * sr // hop_length)
    freqs = librosa.tempo_frequencies(len(ac), sr=sr, hop_length=hop_length)
    plt.figure(figsize=(8, 4))
    plt.semilogx(freqs[1:], librosa.util.normalize(ac)[1:], label='Onset autocorrelation', basex=2)
    plt.axvline(tempo, 0, 1, color='r', alpha=0.75, linestyle='--', label='Tempo: {:.2f} BPM'.format(tempo))
    plt.xlabel('Tempo (BPM)')
    plt.grid()
    plt.title('Static tempo estimation')
    plt.legend(frameon=True)
    plt.axis('tight')


def dTempoOnTempogram(dtempo):
    plt.figure()
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop_length)
    librosa.display.specshow(tg, x_axis='time', y_axis='tempo')
    plt.plot(librosa.frames_to_time(np.arange(len(dtempo))), dtempo, color='w', linewidth=1.5, label='Tempo estimate')
    plt.title('Dynamic tempo estimation')
    plt.legend(frameon=True, framealpha=0.75)
