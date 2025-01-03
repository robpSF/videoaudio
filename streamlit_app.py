import streamlit as st
import ffmpeg

def combine_videos_and_audio(video_paths, audio_path, output_path):
    try:
        # Combine all videos into one
        input_videos = [ffmpeg.input(video) for video in video_paths]
        video_concat = ffmpeg.concat(*input_videos, v=1, a=1).node
        output = ffmpeg.output(video_concat, audio_path, output_path, vcodec='libx264', acodec='aac', strict='experimental')
        output.run(overwrite_output=True)
    except Exception as e:
        st.error(f"Error combining video and audio: {e}")

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

    output_file = "output_combined.mp4"

    if st.button("Combine and Save"):
        combine_videos_and_audio(video_paths, audio_path, output_file)
        st.success("Videos and audio combined successfully!")
        with open(output_file, "rb") as f:
            st.download_button("Download combined video", f, file_name=output_file, mime="video/mp4")
