# Audio File Splitter

`audio-splitter` is a command-line tool for splitting audio files into equally-sized chunks or based on silence. This Python script uses the `pydub` library for handling various audio formats.

## Why does this exist?

As someone who enjoys to listen to spoken word every night, I often listen to podcasts on my old MP3 player before going to sleep. However, I found myself growing bored of listening to the same first 5 minutes of each episode every night. To mix things up and always have something new to listen to, I created this script to break down podcast episodes into smaller chunks. Now I can jump around different parts of the episodes and enjoy a fresh listening experience each time.

## Installation

You can install `audio-splitter` using `pip`:

```bash
pip install audio-splitter
```

## Usage

To use the script, follow these steps:

```bash
python audio_splitter/main.py input_file output_dir [--chunk_length CHUNK_LENGTH] [--output_format OUTPUT_FORMAT] [--silence_based]
```

Replace input_file with the path to your audio file and output_dir with the path to the output directory where you want to save the chunks.

## Options
```bash
--chunk_length CHUNK_LENGTH: Length of each chunk in milliseconds (default: 300000 ms, or 5 minutes). Ignored if --silence_based is set.
--output_format OUTPUT_FORMAT: Output format for the audio chunks (default: wav). Supported formats include wav, mp3, and ogg.
--silence_based: Split the audio based on silence instead of fixed-size chunks. If set, --chunk_length is ignored and the script ensures that the generated chunks are at least the specified length.
```

## Features

- Split audio files into equally-sized chunks or based on periods of silence.
- Parallel processing for faster audio processing.
- Progress feedback to provide a better user experience.
- Option to specify the desired output format for audio chunks.
- Ensures generated chunks are at least the specified length when splitting based on silence.

## Potential Improvements

- Automatic format detection: Instead of requiring users to specify the output format, automatically detect the input file's format and use it as the default output format.
- Error handling: Improve error handling and user feedback for various edge cases, such as invalid input file paths, unsupported file formats, and incorrect output directories.
- Metadata preservation: Preserve metadata (e.g., ID3 tags) from the original audio file when splitting it into chunks.
- Configurable silence detection: Allow users to configure the silence detection parameters, such as the minimum silence length and silence threshold.

## Examples

Split an audio file into 5-minute (default) chunks:
```bash
python audio_splitter/main.py input_file.mp3 output_dir
```

Split an audio file into 10-minute chunks and save them in the MP3 format:
```bash
python audio_splitter/main.py input_file.mp3 output_dir --chunk_length 600000 --output_format mp3
```

Split an audio file based on silence, ensuring that the chunks are at least 5 minutes long:
```bash
python audio_splitter/main.py input_file.mp3 output_dir --silence_based
```

Split an audio file based on silence, ensuring that the chunks are at least 10 minutes long:
```bash
python audio_splitter/main.py input_file.mp3 output_dir --chunk_length 600000 --silence_based
```
