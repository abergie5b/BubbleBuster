import soundfile as sf
import sys
data, samplerate = sf.read(sys.argv[0])
sf.write(sys.argv[1], data, samplerate, subtype='PCM_16')
