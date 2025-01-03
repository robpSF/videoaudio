import streamlit as st
import ffmpeg

def combine_video_audio(video_path, audio_path, output_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, output_path, vcodec='libx264', acodec='aac', strict='experimental')
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        st.error(f"Error combining video and audio: {e.stderr.decode()}")

st.title("Combine Video and Audio")

# Upload video file
video_file = st.file_uploader("Upload MP4 video", type=["mp4"])
# Upload audio file
audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

if video_file and audio_file:
    with open("uploaded_video.mp4", "wb") as f:
        f.write(video_file.read())
    with open("uploaded_audio.mp3", "wb") as f:
        f.write(audio_file.read())

    output_file = "output_combined.mp4"

    if st.button("Combine and Save"):
        combine_video_audio("uploaded_video.mp4", "uploaded_audio.mp3", output_file)
        st.success("Video and audio combined successfully!")
        with open(output_file, "rb") as f:
            st.download_button("Download combined video", f, file_name=output_file, mime="video/mp4")
