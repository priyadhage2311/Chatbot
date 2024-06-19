import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to generate a word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Function to read the text file with proper encoding
def read_file(file):
    encodings = ['utf-8', 'ISO-8859-1', 'utf-16']
    for encoding in encodings:
        try:
            return file.getvalue().decode(encoding)
        except UnicodeDecodeError:
            continue
    st.error("Could not decode the file with utf-8, ISO-8859-1, or utf-16 encodings.")
    return ""

# Streamlit app layout
st.title("Text File Uploader and Word Cloud Generator")

uploaded_file = st.file_uploader("Upload a Text File", type=["txt"])

if uploaded_file is not None:
    # Read the contents of the text file
    file_contents = read_file(uploaded_file)
    
    if file_contents:
        # Display the contents of the text file
        st.subheader("Text File Contents")
        st.text_area("Contents", file_contents, height=200)
        
        # Generate and display the word cloud
        st.subheader("Word Cloud")
        wordcloud = generate_wordcloud(file_contents)
        
        # Display the word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)