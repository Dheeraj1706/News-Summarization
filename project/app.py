import streamlit as st
import pandas as pd
from gtts import gTTS
from googletrans import Translator
import os
from pathlib import Path

vidno=0
st.set_page_config(layout="wide")
st.write(f"# News Articles")
# Define CSV file paths for each category
csv_folder = Path(__file__).resolve().parent  # Get the directory of the script
category_csv_files = {
    'India': csv_folder / 'india.csv',
    'World': csv_folder / 'world.csv',
    'Business': csv_folder / 'business.csv',
    'Technology': csv_folder / 'tech.csv',
    'Sports': csv_folder / 'sports.csv'
}
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr"
}
# Separate mapping for gTTS-supported languages
gtts_languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr"
}
#Dropdown menu for language selection
selected_language = st.selectbox("Select Language", list(languages.keys()))
# Dropdown menu for category selection
selected_category = st.selectbox('Select Category', ['India', 'World', 'Business', 'Technology', 'Sports'])
st.write(f"## {selected_category}")
# Read the CSV file based on the selected category
csv_file = category_csv_files[selected_category]
df = pd.read_csv(csv_file)

# Initialize Google Translator
translator = Translator()
# Display containers for each news article

for i in range(min(50, len(df))):
    article_title = df.iloc[i]['Article Title']
    article_summary = df.iloc[i]['Article Summary']
    article_link = df.iloc[i]['Article Link']
    article_image = df.iloc[i]['Article Image']
    
    # Check if all required fields are not empty and valid
    if all(isinstance(field, str) and field.strip() for field in [article_title, article_summary, article_link, article_image]):
        # Display article container
        translated_title = translator.translate(article_title, dest=languages[selected_language]).text
        translated_summary = translator.translate(article_summary, dest=languages[selected_language]).text
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("")
            st.write("")
            st.image(article_image, width=250)  # Display article image on the left side with specified height and width
            # Display "Read Full Article" button
            st.write(f"[Read Full Article]({article_link})")
        with col2:
            st.write(f"### {translated_title}")
            st.write(translated_summary)

            
            
            # Display "Convert to Audio" button
            convert_button_key = f"convert_button_{i}"
            if st.button("Convert to Audio", key=convert_button_key):
                # Convert summarized text to audio
                audio_filename = f"{vidno}_summary_audio.mp3"
                vidno=vidno+1
                # Check if selected language is supported by gTTS
                tts_language = gtts_languages.get(selected_language, "en")  # Default to English if not found
                tts = gTTS(translated_summary, lang=tts_language)
                tts.save(audio_filename)
                st.audio(audio_filename, format='audio/mp3')

                # Remove audio file after playing
                if os.path.exists(audio_filename):
                    os.remove(audio_filename)
                    print(translated_title, "- Audio file deleted")
            st.write("")
            st.write("")       
    else:
        print("One or more required fields are empty or invalid. Skipping article display.")

st.markdown("<p style='font-size: small; color: grey; text-align: center;'>A NLP project. <a href='https://github.com/Dheeraj1706/News-Summarization'>GitHub Link</a> . Disclaimer: This project is intended for educational purposes only. Web scraping without proper authorization is not encouraged or endorsed.</p>", unsafe_allow_html=True)    
#hello