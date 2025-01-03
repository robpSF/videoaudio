import io
import ffmpeg
import streamlit as st

def combine_videos_and_audio_stream(video_paths, audio_path):
    buffer = io.BytesIO()
    try:
        # 1) Read only the video (ignore audio) from each file
        #    so that FFmpeg sees a single video stream in each input.
        input_videos = [ffmpeg.input(v).video for v in video_paths]

        # 2) Concatenate all the video streams into one (no audio)
        #    v=1, a=0 means 1 video stream, 0 audio streams per input
        video_concat = ffmpeg.concat(*input_videos, v=1, a=0).node
        
        # 3) Add external audio as a separate input
        audio_input = ffmpeg.input(audio_path).audio

        # 4) Output to pipe:1 so we can capture in Python memory
        process = (
            ffmpeg
            .output(
                video_concat[0],  # The concatenated video
                audio_input,      # The external audio
                "pipe:1",
                format="mp4",
                vcodec="libx264",
                acodec="aac",
                strict="experimental"
            )
            .run(capture_stdout=True, capture_stderr=True)
        )

        # 5) Write the final bytes to our in-memory buffer
        buffer.write(process[0])
        buffer.seek(0)
        return buffer

    except ffmpeg.Error as e:
        st.error(f"Error combining video and audio: {e.stderr.decode()}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


st.title("Combine Multiple Videos (No Audio) with One Audio File")

# 1) Upload multiple video files
video_files = st.file_uploader("Upload MP4 videos", type=["mp4"], accept_multiple_files=True)
# 2) Upload a single audio file
audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

if video_files and audio_file:
    video_paths = []
    for i, vid in enumerate(video_files):
        video_path = f"uploaded_video_{i}.mp4"
        with open(video_path, "wb") as f:
            f.write(vid.read())
        video_paths.append(video_path)

    audio_path = "uploaded_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())

    if st.button("Combine and Save"):
        output_buffer = combine_videos_and_audio_stream(video_paths, audio_path)
        if output_buffer:
            st.success("Videos and audio combined successfully!")
            st.download_button(
                label="Download combined video",
                data=output_buffer,
                file_name="output_combined.mp4",
                mime="video/mp4"
            )
