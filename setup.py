from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audio-splitter",
    version="0.1.0",
    author="Artem Vasilev",
    author_email="temavasilev@pm.me",
    description="A CLI tool for splitting audio files into equally-sized chunks or based on periods of silence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/temavasilev/audio-splitter",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "audio-splitter = audio_splitter.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pydub",
        "tqdm",
    ],
)
