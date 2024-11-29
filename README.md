# YouTube Video to Doc (vid2doc) for Quick Video Content Reading

## Overview

When learning from watching videos, I often find it time consuming to navigate through a long video to find the part that I am interested and learn from it quickly. This project allows you to download a YouTube video, extract its audio transcription, and capture representative frames from the video. The extracted information and frames are then compiled into an HTML report for easy viewing.

## Features

- Downloads YouTube videos in the best available quality.
- Transcribes audio to text using OpenAI's Whisper model.
- Extracts representative frames from the video at specified intervals.
- Generates a neatly formatted HTML report with sections of text and corresponding frames.

## Requirements

This code is tested in a MacOS Sequoia (version 15.1) environment with following packages
- Python 3.12 or higher
- `yt-dlp`
- `whisper`
- `opencv-python`
- `numpy`
- `jinja2`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/youtube-video-processor.git
   cd youtube-video-processor
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   note that for it is better to install using `pip install git+https://github.com/openai/whisper.git`; see https://github.com/openai/whisper/discussions/251

## Usage

To run the video processor, use the following command:

```bash
python main.py --youtube_url "https://www.youtube.com/watch?v=Mn_9W1nCFLo"
```

Replace the URL with the desired YouTube video link.

### Parameters

- `--youtube_url`: The URL of the YouTube video you want to process.

## Output

The output will be saved in the `output` directory as `vid2doc.html`. This file will contain:

- The title of the video.
- Sections of transcribed text with links to the corresponding time in the video.
- Extracted frames from the video.

## Examples:

Pleas reference (Vid2Doc_LLaMA_explained.pdf)[https://github.com/trws2/video2doc/blob/main/Vid2Doc_LLaMA_explained.pdf] for an example.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenCV](https://opencv.org/)
