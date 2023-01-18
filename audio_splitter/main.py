import pydub
import argparse
import pathlib
import os


def main():
    if args.audio:
        try:
            audio = pydub.AudioSegment.from_file(args.audio)
            file_name = os.path.basename(args.audio).split(".")[0]
            print(audio)
        except FileNotFoundError:
            print("File not found!")
            return
        split_audio(audio, file_name)
        exit(0)
    elif args.all != "/data":
        files = [f for f in os.listdir(args.all) if f.endswith(".mp3")]
        print(f"Founds {len(list(files))} files, named {files}")
        for file in files:
            print(f"Processing {args.all}/{file}")
            audio = pydub.AudioSegment.from_file(f"{args.all}/{file}")
            file_name = os.path.basename(file).split(".")[0]
            split_audio(audio, file_name)
        exit(0)
    
def split_audio(audio, name: str):
    number_of_chunks = get_chunk_number(audio)
    export_path = pathlib.Path(f"{args.output}") if args.output else pathlib.Path("/data")
    for i in range(number_of_chunks):
        chunk = audio[i * len(audio) // number_of_chunks:(i + 1) * len(audio) // number_of_chunks]
        chunk.export(f"{export_path}/{name}_{i+1:02d}.mp3", format="mp3")

def get_chunk_number(audio) -> int:
    if audio.duration_seconds < 1800: # pointless to split short audio into chunks
        print("Audio is too short")
        return 1
    else:
        number_of_chunks = int(audio.duration_seconds // 1800 + 1)
        print("Splitting audio into {} chunks with a duration of 30 minutes".format(number_of_chunks))
        return number_of_chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="Path to audio file", nargs="?")
    parser.add_argument("-a", "--all", help="Split all audio files in the directory", type=pathlib.Path, default="/data")
    parser.add_argument("-d", "--directory", help="Path to directory")
    parser.add_argument("-o", "--output", help="Path to output directory")
    args = parser.parse_args()
    main()

