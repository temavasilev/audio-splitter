import pydub
import argparse

def main():      
    audio = pydub.AudioSegment.from_file("data/audio2.mp3")
    
    if audio.duration_seconds < 1800: # pointless to split short audio into chunks
        print("Audio is too short")
        exit(1)
    elif audio.duration_seconds > 10400: # pydub can't handle long audio files
        print("Audio is too long")
        exit(1)
    else:
        number_of_chunks = int(audio.duration_seconds // 1800 + 1)
        print("Splitting audio into {} chunks with a duration of 30 minutes".format(number_of_chunks))
    
    split_audio(audio, number_of_chunks)
    
def split_audio(audio, number_of_chunks):
    for i in range(number_of_chunks):
        chunk = audio[i * len(audio) // number_of_chunks:(i + 1) * len(audio) // number_of_chunks]
        chunk.export("data/audio2_{}.mp3".format(i+2), format="mp3", bitrate="32k")
        
if __name__ == "__main__":
    main()


