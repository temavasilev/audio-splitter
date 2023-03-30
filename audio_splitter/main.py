import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

def save_chunk(chunk, start_time, output_dir, output_format):
    chunk.export(os.path.join(output_dir, f'chunk_{start_time}.{output_format}'), format=output_format)

def merge_short_chunks(chunks, min_chunk_length_ms):
    merged_chunks = []
    current_chunk = chunks[0]

    for chunk in chunks[1:]:
        if len(current_chunk) + len(chunk) < min_chunk_length_ms:
            current_chunk += chunk
        else:
            merged_chunks.append(current_chunk)
            current_chunk = chunk

    merged_chunks.append(current_chunk)
    return merged_chunks

def split_audio(input_file, output_dir, chunk_length_ms, output_format, silence_based):
    # Load the input audio file using Pydub
    audio = AudioSegment.from_file(input_file)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if silence_based:
        # Split the audio file based on silence
        min_silence_len = 100  # Minimum length of silence in milliseconds
        silence_thresh = -40   # Silence threshold in dB
        chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

        # Merge adjacent chunks shorter than the specified length
        chunks = merge_short_chunks(chunks, chunk_length_ms)

        # Set up progress bar with tqdm
        pbar = tqdm(total=len(chunks), desc="Processing chunks based on silence")

        # Save chunks in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            for i, chunk in enumerate(chunks):
                executor.submit(save_chunk, chunk, i, output_dir, output_format).add_done_callback(lambda x: pbar.update(1))

    else:
        # Calculate the total length of the audio in milliseconds and the number of full chunks
        audio_length_ms = len(audio)
        num_chunks = audio_length_ms // chunk_length_ms

        # Set up progress bar with tqdm
        pbar = tqdm(total=num_chunks + (audio_length_ms % chunk_length_ms != 0), desc="Processing fixed-size chunks")

        # Split and save chunks in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            for i in range(num_chunks):
                start_time = i * chunk_length_ms
                end_time = (i + 1) * chunk_length_ms
                chunk = audio[start_time:end_time]
                executor.submit(save_chunk, chunk, start_time, output_dir, output_format).add_done_callback(lambda x: pbar.update(1))

            # Handle the last chunk if there is any remainder
            if audio_length_ms % chunk_length_ms != 0:
                start_time = num_chunks * chunk_length_ms
                end_time = audio_length_ms
                chunk = audio[start_time:end_time]
                executor.submit(save_chunk, chunk, start_time, output_dir, output_format).add_done_callback(lambda x: pbar.update(1))

    # Close progress bar
    pbar.close()
    

def main():
    # Set up argument parser for the CLI app
    parser = argparse.ArgumentParser(description="Split an audio file into equally sized chunks.")
    parser.add_argument("input_file", help="Path to the input audio file.")
    parser.add_argument("output_dir", help="Path to the output directory where chunks will be saved.")
    parser.add_argument("--chunk_length", type=int, default=300000, help="Length of each chunk in milliseconds (default: 300000 ms / 5 minutes).")
    parser.add_argument("--output_format", type=str, default="wav", help="Output format for the audio chunks (default: wav). Supported formats include wav, mp3, and ogg.")
    parser.add_argument("--silence_based", action="store_true", help="Split the audio based on silence instead of fixed-size chunks. If set, --chunk_length is ignored.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the split_audio function with the provided arguments
    split_audio(args.input_file, args.output_dir, args.chunk_length, args.output_format, args.silence_based)

if __name__ == "__main__":
    main()