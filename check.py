import librosa
import numpy as np
audio, sr = librosa.load('./dist/aa.wav', sr = 16000)
audio = np.array(audio)
print("audio shape :", audio.shape)
print('audio length:', audio.shape[0]/float(sr), 'secs')
np.savetxt("./aa.txt", audio)
