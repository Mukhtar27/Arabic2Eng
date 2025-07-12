import streamlit as st
import pandas as pd
import requests
import io

st.title("📗 Arabic Name Translator (Excel Upload)")
st.write("Upload an Excel file with Arabic names. This app will translate them to English.")

# LibreTranslate function
def translate_text(text):
    url = "https://libretranslate.de/translate"
    payload = {
        'q': text,
        'source': 'ar',
        'target': 'en',
        'format': 'text'
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()['translatedText']
    except:
        return "⚠️ Error"

# File upload
uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.write("### Preview", df.head())
    
    col_name = st.selectbox("Select the column with Arabic names", df.columns)
    
    if st.button("Translate"):
        df['Translated'] = df[col_name].astype(str).apply(translate_text)
        st.write("### Translated Data", df)
        
        # Download option
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        st.download_button(
            label="📥 Download Translated File",
            data=output.getvalue(),
            file_name="translated_names.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
