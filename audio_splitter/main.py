import pydub
import argparse
import pathlib
import os


def main():
    if args.audio:
        for file in args.audio:
            print(f"Processing {file}")
            try:
                audio = pydub.AudioSegment.from_file(file)
                file_name = os.path.basename(file).split(".")[0]
            except FileNotFoundError:
                print(f"{file} not found!")
                continue
            except pydub.exceptions.CouldntDecodeError:
                print(f"{file} is not an audio file!")
                continue
            split_audio(audio, file_name)
    if args.input:
        files = [f for f in os.listdir(args.input) if f.endswith(".mp3")]
        print(f"Found {len(list(files))} files, named {files}")
        for file in files:
            print(f"Processing {args.input}/{file}")
            audio = pydub.AudioSegment.from_file(f"{args.input}/{file}")
            file_name = os.path.basename(file).split(".")[0]
            split_audio(audio, file_name)
        exit(0)
    
def split_audio(audio, name: str):
    number_of_chunks = get_chunk_number(audio)
    audio = audio.set_channels(1)
    export_path = pathlib.Path(f"{args.output}") if args.output else pathlib.Path(os.getcwd())
    for i in range(number_of_chunks):
        chunk = audio[i * len(audio) // number_of_chunks:(i + 1) * len(audio) // number_of_chunks]
        chunk.export(f"{export_path}/{name}_{i+1:02d}.mp3", format="mp3", bitrate="32k")

def get_chunk_number(audio: pydub.AudioSegment) -> int:
    if args.number:
        print(f"Splitting audio into {args.number} chunks with a duration of {audio.duration_seconds // args.number // 60} minutes")
        return args.number
    if audio.duration_seconds < 1800: # pointless to split short audio into chunks
        print("Audio is too short")
        return 1
    else:
        number_of_chunks = int(audio.duration_seconds // 1800 + 1)
        print(f"Splitting audio into {number_of_chunks} chunks with a duration of {audio.duration_seconds // number_of_chunks // 60} minutes")
        return number_of_chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="Path to audio file", nargs="*")
    parser.add_argument("-i", "--input", help="Split all audio files in the directory", type=pathlib.Path)
    parser.add_argument("-d", "--directory", help="Path to directory")
    parser.add_argument("-n", "--number", help="Number of chunks", type=int)
    parser.add_argument("-o", "--output", help="Path to output directory")
    args = parser.parse_args()
    if args.number and args.number < 1:
        print("Number of chunks must be greater than 0")
        exit(1)
    main()

