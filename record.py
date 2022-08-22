import pyaudio
import wave
import shutil
import os
import math
from tempfile import mkstemp
"""
http://people.csail.mit.edu/hubert/pyaudio/
"""
"""
MSI main board mic driver has problem.
Found a phenomenon in which recording was not possible for about 0.3 to 0.5 seconds in thr front part
"""
class record_process():
    def __init__(self, arg, time):
        # record param
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # 44100
        self.RECORD_SECONDS = int(time)
        self.arg = arg
        self.fd, self.WAVE_OUTPUT_FILENAME = mkstemp(suffix='.wav')

    def record(self, time):
        self.RECORD_SECONDS = time
        self.arg.Timer_thread.get_arg(self.RECORD_SECONDS)

        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
            self.arg.button_disable()
            self.update_label_txt("Ready...")

            frames = []

            for i in range(0, int(math.ceil(self.RATE / self.CHUNK * self.RECORD_SECONDS))+10):
                if i == 8:
                    self.update_label_txt("Start to record the audio. ")
                    data = stream.read(self.CHUNK)
                elif i == 9:
                    self.arg.Timer_thread.start()
                    self.update_label_txt("recording...")
                    data = stream.read(self.CHUNK)
                elif i > 9:
                    data = stream.read(self.CHUNK)
                    frames.append(data)
                else:
                    data = stream.read(self.CHUNK)

            stream.stop_stream()
            stream.close()
            p.terminate()
            self.update_label_txt("Done!")

            # exit thread flag
            self.arg.Timer_thread.stop()

            # save *.wav file
            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            # for check stream data
            """
            for i in range(len(frames)):
                print('a')
                f = open(f"./check{i}.bin", "wb")
                print(frames[i])
                f.write(frames[i])
                f.close()
            """
        except Exception as e:
            self.update_label_txt("There are no recordable devices.")
            # print('잘못된 인덱스입니다.', e)
            p.terminate()

    def listen(self):

        if os.path.isfile(self.WAVE_OUTPUT_FILENAME):

            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')

            p = pyaudio.PyAudio()
            try:
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)
                self.update_label_txt("Start to listen the audio.")
                self.arg.Timer_thread.start()
                data = wf.readframes(self.CHUNK)
                self.update_label_txt("Listening...")

                while data != b'':
                    stream.write(data)
                    data = wf.readframes(self.CHUNK)  # listen

                # exit thread flag
                self.arg.Timer_thread.stop()
                self.update_label_txt("Done!")
                stream.stop_stream()
                stream.close()

                p.terminate()
                wf.close()

            except Exception:
                self.update_label_txt("There are no listenable devices.")
                p.terminate()
                wf.close()
        else:
            self.update_label_txt("There is no audio file. Record first!")

    def save(self, filename):
        if os.path.isfile(self.WAVE_OUTPUT_FILENAME):
            if filename:
                if os.path.isfile(filename):
                    os.remove(filename)
                shutil.copy(self.WAVE_OUTPUT_FILENAME, filename)
                self.arg.label_inform.setText("Save "+filename.split('/')[-1])
                self.arg.label_inform.repaint()
                self.arg.button_disable_2()
        else:
            self.update_label_txt("There is no audio file. Record first!")

    def delete_tmp_file(self):
        os.close(self.fd)
        if os.path.exists(self.WAVE_OUTPUT_FILENAME):
            os.unlink(self.WAVE_OUTPUT_FILENAME)

    def update_label_txt(self, text):
        self.arg.label_inform.setText(text)
        self.arg.label_inform.repaint()

