from aip import AipSpeech
import pyaudio
import wave

APP_ID = '15334156'
API_KEY = 'hhCRS1PiKFArb9F9teqIwaoq'
SECRET_KEY = '31M6jcLKTpjfR2PrbXnI0g62bdfIHhzA'

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


def get_speech(filepath):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ret = client.asr(get_file_content(filepath), 'wav', 16000, {
        'dev_pid': 1536,
    })
    return ret['result'][0]


def record(interval, filename):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("** recording")
    frames = []

    for i in range(0, int(RATE / CHUNK * interval)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("** recording done!")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == "__main__":
    record(5, 'rec.wav')
    print(get_speech('rec.wav'))
