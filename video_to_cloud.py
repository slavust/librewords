#!/usr/bin/python3
from moviepy.editor import VideoFileClip
import tempfile
import os.path
import speech_to_cloud
import argparse

def convert_video_to_audio_moviepy(video_file, out_audio_path):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(out_audio_path)

def render_cloud_from_video(video_path, output_image_path, language, exclude_obvious):
    with tempfile.TemporaryDirectory() as dir:
        filename = os.path.split(video_path)[-1]
        temp_audio_path = os.path.join(dir, filename + '.wav')
        convert_video_to_audio_moviepy(video_path, temp_audio_path)
        speech_to_cloud.render_cloud_from_audio(temp_audio_path, output_image_path, language, exclude_obvious)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', help='input video', required=True)
    parser.add_argument('-o', '--output', help='output image path', required=True)
    parser.add_argument('-ro', 
                        '--remove-obvious', 
                        help='Exclude 15 percents of most frequent words',
                        required=False, 
                        dest='remove_obvious',
                        action='store_true')
    parser.add_argument('-l', '--lang', help='audio language', default='en', required=False)
    parser.set_defaults(remove_obvious=False)
    args = parser.parse_args()
    
    render_cloud_from_video(args.video, args.output, args.lang, args.remove_obvious)