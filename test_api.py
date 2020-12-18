
import pyaudio
import wave
import time

CHUNK    = 1024
CHANNELS = 2
FORMAT   = pyaudio.paInt16
RATE     = 44100
WAVE_OUTPUT_FILENAME = "test.wav"





wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
wf.setframerate(RATE)





sample_size = wf.getsampwidth()
print ("wf sample_size %s" % sample_size)

channels = wf.getnchannels()
print ("wf channels %s" % channels)

frame_rate = wf.getframerate() 
print ("wf frame_rate %s" % frame_rate)



portaudio_version = pyaudio.get_portaudio_version()
print ("portaudio version = %s" % portaudio_version)

portaudio_version_text = pyaudio.get_portaudio_version_text()
print ("portaudio version_text = %s" % portaudio_version_text)


p = pyaudio.PyAudio()

portaudio_sample_format = p.get_format_from_width(wf.getsampwidth())
print ("portaudio sample format = %s" % portaudio_sample_format)

sample_size = p.get_sample_size(portaudio_sample_format)
print ("sample size = %s" % sample_size)


frames = []
def callback(in_data, frame_count, time_info, status_flags):
    wf.writeframes(in_data)
#    print ("in_data = %s" % in_data)
    print ("frame_count = %s" % frame_count)
    print ("time_info = %s" % time_info)
    print ("status_flags = %s" % status_flags)

    return (None, pyaudio.paContinue)


stream = p.open(format = portaudio_sample_format,
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                input = True,
                stream_callback=callback)


stream.start_stream()

while stream.is_active():
    time.sleep(0.1)


stream.stop_stream()
stream.close()


wf.close()

p.terminate()