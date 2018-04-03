from __future__ import print_function
from pydub import AudioSegment
import os


def AudioSegmentationPrep(input_file, name, destination, step_size=5000):
    """
    AudioSegmentationPrep creates the directories needed to save off the audio data and loads information
    to be used for further processing

    Args:
        input_file: String to the audio file to load
        name: Name of the song
        destination: Output directory the audio segments will be saved to
        step_size: Number of milliseconds per audio segment

    Returns:
        audio_data: MP3 data loaded by pydub
        num_segments: Number of 5 second segments in song
        song_directory: String containing the path to the song directory where clips and FFT will be saved
        segment_path: String containing the path of where the actual segments will be saved
    """

    song_directory = os.path.join(destination, name)
    segment_path = os.path.join(song_directory, 'split')
    fft_path = os.path.join(song_directory, 'fft')
    tempo_path = os.path.join(song_directory, 'tempo')

    # Create directory for song files if it doesn't exist
    for path in (song_directory, segment_path, fft_path, tempo_path):
        if not os.path.exists(path):
            os.makedirs(path)

    # Load audio and calculate number of segments to create
    audio_data = AudioSegment.from_file(input_file)
    num_segments = int(len(audio_data) / step_size) + 1

    return audio_data, num_segments, song_directory, segment_path, fft_path, tempo_path


def GetNextSegment(audio_data, current_segment, step_size=5000):
    """
    GetNextSegment simply gathers the next segment of audio and returns it

    Args:
        audio_data: MP3 data loaded by pydub in AudioSegmentationPrep function
        current_segment: The current segment number ranging from 0 to num_segments calculated in AudioSegmentationPrep
        step_size: Number of milliseconds per audio segment

    Returns:
        Audio segment of length specified by step_size starting at step_size * current_segment
    """

    start_point = step_size * current_segment
    end_point = step_size * (current_segment + 1)
    return audio_data[start_point:end_point]


def SaveAudio(name, audio_segment_data, current_segment, segment_path):
    """
    SaveAudio saves off any given audio data to the given segment path

    Args:
        name: Name of audio file
        audio_segment_data: Current audio clip being processed
        current_segment: Current segment number, used to create the file name
        segment_path: String to where the audio file will be saved

    Returns:
        True if save was successful, false otherwise
    """

    rel_path = name + '_part_' + str(current_segment) + '.mp3'
    output_path = os.path.join(segment_path, rel_path)
    if audio_segment_data.export(output_path, format="mp3"):
        return output_path
    else:
        return False


def MoveOriginalFile(input_file, name, dir_path):
    """
    MoveOriginalFile moves the original mp3 file into the song directory outside of the clip directory
    """

    os.rename(input_file, os.path.join(dir_path, name + '.mp3'))
