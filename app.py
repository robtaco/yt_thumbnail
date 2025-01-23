import streamlit as st
import requests
from pytube import YouTube
import yt_dlp
from io import BytesIO
from PIL import Image
from streamlit_lottie import st_lottie, st_lottie_spinner   

st.title("YouTube Video Thumbnail Downloader")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style/style.css')

# --- Load Assets ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/7f4555de-0643-4d96-8e2a-d5a28c955417/i5aXMsGTzu.json")


def main():
    with st.container():
        with st.sidebar:
            st_lottie_spinner(lottie_coding, speed=1, loop=True, quality="high", height=200, width=200) 
            st_lottie(lottie_coding, speed=1, loop=True, quality="high", height=200, width=200)
        st.write("##")
# Input field for YouTube video URL
    video_url = st.text_input("Enter the YouTube video URL:")

    if video_url:
        try:
            # Create a YouTube object
            yt = YouTube(video_url)

        # yt-dlp options
            ydl_opts = {
                'skip_download': True,  # Skip downloading the video
                'outtmpl': '%(title)s.%(ext)s',  # Output template
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                filename_title = f"Title: {info_dict['title']}"

            # Get the thumbnail URL
            thumbnail_url = yt.thumbnail_url

            # Display the thumbnail image
            st.image(thumbnail_url, caption="Thumbnail Image")

            # Download the thumbnail image
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                # Open the image using PIL
                image = Image.open(BytesIO(response.content))

                # Prepare the image for download
                buf = BytesIO()
                image.save(buf, format="JPEG")
                byte_im = buf.getvalue()

                filename = yt

                # Download button
                st.download_button(
                    label="Download Thumbnail",
                    data=byte_im,
                    file_name=f"{filename_title}.jpg",
                    mime="image/jpeg"
                )
            else:
                st.error("Failed to retrieve the thumbnail image.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()