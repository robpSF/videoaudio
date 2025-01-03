import streamlit as st
import ffmpeg
import io

def combine_videos_and_audio_stream(video_paths, audio_path):
    buffer = io.BytesIO()
    try:
        # Combine all videos into one
        input_videos = [ffmpeg.input(video) for video in video_paths]
        video_concat = ffmpeg.concat(*input_videos, v=1, a=1).node
        process = (
            ffmpeg
            .output(video_concat[0], audio_path, "pipe:1", format="mp4", vcodec="libx264", acodec="aac", strict="experimental")
            .run(capture_stdout=True, capture_stderr=True)
        )
        buffer.write(process[0])  # Write output to buffer
        buffer.seek(0)  # Reset buffer position
        return buffer
    except Exception as e:
        st.error(f"Error combining video and audio: {e}")
        return None

st.title("Combine Multiple Videos and Audio")

# Upload multiple video files
video_files = st.file_uploader("Upload MP4 videos", type=["mp4"], accept_multiple_files=True)
# Upload audio file
audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

if video_files and audio_file:
    video_paths = []
    for i, video_file in enumerate(video_files):
        video_path = f"uploaded_video_{i}.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        video_paths.append(video_path)

    audio_path = "uploaded_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())

    if st.button("Combine and Save"):
        output_buffer = combine_videos_and_audio_stream(video_paths, audio_path)
        if output_buffer:
            st.success("Videos and audio combined successfully!")
            st.download_button("Download combined video", output_buffer, file_name="output_combined.mp4", mime="video/mp4")
