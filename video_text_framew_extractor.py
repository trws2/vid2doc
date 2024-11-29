import os
import yt_dlp
import whisper
import cv2
import numpy as np
from jinja2 import Template



class YouTubeVideoProcessor:
    def __init__(self, youtube_url):
        """
        Initialize the video processor with a YouTube URL
        
        :param youtube_url: URL of the YouTube video
        """
        # Download the YouTube video
        self.video_path = self._download_video(youtube_url)
        
        # Create output directories
        os.makedirs('frames', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        # Initialize Whisper model 
        self.whisper_model = whisper.load_model("base")
    
    def _post_process_title(self, title):
        return title.replace("?", "？")
    
    def _download_video(self, video_url):
        if True:
            ydl_opts = {
                'format': 'best',  # Download the best quality
                'outtmpl': '%(title)s.%(ext)s',  # Save as the video title
                'quiet': True,  # Suppress output during download
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video information
                try:
                    info_dict = ydl.extract_info(video_url, download=False)
                    video_title = info_dict.get('title', 'Unknown Title')  # Get the video title
                    video_title = self._post_process_title(video_title)
                    video_extension = info_dict.get('ext', 'mp4')  # Get the file extension                    
                    output_file_path = f"{video_title}.{video_extension}"
                                        
                    # Print the path of the downloaded file
                    self.yt_title = video_title
                    video_path = os.path.abspath(output_file_path)
                    print(f"Downloaded file path: <START>{video_path}<END>")
                    return video_path
                except Exception as e:
                    print("An error occurred while downloading the video:", str(e))

    def extract_text_and_frames(self, section_duration=60, frame_interval=30):
        """
        Extract text and frames from the video
        
        :param section_duration: Duration of each text section in seconds
        :param frame_interval: Interval for extracting frames in seconds
        :return: List of sections with text and frames
        """
        print("Transcribe the video ...")
        result = self.whisper_model.transcribe(self.video_path)
        
        # Process video for frames
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        
        sections = []
        current_section = {
            'start_time': 0,
            'text': '',
            'frames': []
        }
        
        for segment in result['segments']:
            # Add text to current section
            current_section['text'] += segment['text'] + ' '
            
            # Check if section is complete
            if segment['end'] - current_section['start_time'] >= section_duration:
                # Extract frames for this section
                current_section['frames'] = self._extract_representative_frames(
                    video, fps, 
                    current_section['start_time'], 
                    segment['end'], 
                    frame_interval
                )
                
                sections.append(current_section)
                
                # Start a new section
                current_section = {
                    'start_time': segment['end'],
                    'text': '',
                    'frames': []
                }
        
        # Process final section if not empty
        if current_section['text']:
            current_section['frames'] = self._extract_representative_frames(
                video, fps, 
                current_section['start_time'], 
                video.get(cv2.CAP_PROP_FRAME_COUNT) / fps, 
                frame_interval
            )
            sections.append(current_section)
        
        video.release()
        return sections
    
    def _extract_representative_frames(self, video, fps, start_time, end_time, interval):
        """
        Extract representative frames from a video segment
        
        :param video: OpenCV video capture object
        :param fps: Frames per second
        :param start_time: Start time of segment
        :param end_time: End time of segment
        :param interval: Interval for frame extraction
        :return: List of frame paths
        """
        frames = []
        for t in np.arange(start_time, end_time, interval):
            video.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = video.read()
            if ret:
                frame_path = f'frames/frame_{t:.2f}.jpg'
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
        return frames
    
    def generate_html(self, youtube_url, sections):
        """
        Generate HTML report of video sections
        
        :param sections: List of video sections
        
        .frames { display: flex; overflow-x: auto; }
        .frames img { max-width: 200px; margin-right: 10px; }        
        
        """
        html_template = Template('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .section { margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 20px; }
                .frames { display: block; } /* Change to block for one image per row */
                .frames img { max-width: 100%; margin-bottom: 10px; } /* Adjust margin for spacing */                
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <p><a href="{{ youtube_url }}">{{ youtube_url }}</a></p>
            {% for section in sections %}
            <div class="section">
                <h2>Section {{ loop.index }}</h2>
                <p>{{ section.text }}</p>
                <div class="frames">
                    {% for frame in section.frames %}
                    <img src="{{ current_directory }}/{{ frame }}" alt="Frame at {{ frame }}">
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </body>
        </html>
        ''')
        current_directory = os.getcwd()
        
        rendered_html = html_template.render(
            title=f'Vid2Doc: {self.yt_title}', 
            sections=sections,
            current_directory=current_directory,
            youtube_url=youtube_url,
        )
        
        with open('output/video_analysis.html', 'w', encoding='utf-8') as f:
            f.write(rendered_html)
    
    def cleanup(self):
        """
        Clean up temporary video file
        """
        os.remove(self.video_path)

def main(youtube_url):
    """
    Main function to process YouTube video
    
    :param youtube_url: URL of the YouTube video to process
    """
    processor = YouTubeVideoProcessor(youtube_url)
    try:
        sections = processor.extract_text_and_frames()
        processor.generate_html(youtube_url, sections)
        print("Vid2Doc complete. Check output/video_analysis.html")
    finally:
        processor.cleanup()

if __name__ == "__main__":
    # youtube_url = "https://www.youtube.com/watch?v=dxGLaYdVizs"
    youtube_url = "https://www.youtube.com/watch?v=Mn_9W1nCFLo"
    main(youtube_url)