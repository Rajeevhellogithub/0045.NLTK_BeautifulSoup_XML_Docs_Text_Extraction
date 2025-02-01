import xml.etree.ElementTree as ET
import string
import unicodedata
from bs4 import BeautifulSoup
import re
from io import BytesIO
import streamlit as st

st.title("XML Text Extractor")
st.write("This app processes XML text")

uploaded_file = st.file_uploader("Choose an XML file", type=["xml"])

if uploaded_file is not None:
    if st.button("Convert", type='primary'):
        try:
            tree = ET.parse(uploaded_file)
            root = tree.getroot()
            root_str = ET.tostring(root, encoding='utf8').decode('utf8')

            def strip_html(text):
                soup = BeautifulSoup(text, "html.parser")
                return soup.get_text()

            def remove_between_square_brackets(text):
                return re.sub('\\[[^]]*\\]', '', text)

            def denoise_text(text):
                text = strip_html(text)
                text = remove_between_square_brackets(text)
                text=re.sub('  ','',text)
                return text
            
            sample = denoise_text(root_str)
            st.write("Text Extracted and Cleaned Sucessfully.")
            st.success(sample)

            download_data = BytesIO(sample.encode())
            st.write("Thanks for using this app")
            st.download_button(
                label="Download Cleaned Text",
                data=download_data,
                file_name="Clean_text.txt",
                mime="text/plain",
                type='primary'
                )

        except ET.ParseError:
            st.error("Invalid XML format. Please check your input.")
