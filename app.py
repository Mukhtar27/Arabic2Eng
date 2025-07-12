import streamlit as st
import pandas as pd
import requests

def translate_arabic_to_english(text):
    try:
        response = requests.post(
            "https://libretranslate.com/translate",
            data={
                "q": text,
                "source": "ar",
                "target": "en",
                "format": "text"
            }
        )
        return response.json()["translatedText"]
    except:
        return "⚠️ Error"

st.title("📗 Arabic to English Translator (Free)")

uploaded_file = st.file_uploader("Upload Excel (.xlsx) with Arabic Names", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    column = st.selectbox("Select the column with Arabic names", df.columns)

    if st.button("Translate"):
        st.info("Translating... Please wait ⏳")
        translated = []
        progress = st.progress(0)

        for i, text in enumerate(df[column]):
            translated.append(translate_arabic_to_english(str(text)))
            progress.progress((i + 1) / len(df))

        df["Translated"] = translated
        st.success("✅ Translation Complete!")
        st.dataframe(df)

        st.download_button(
            "📥 Download Translated Excel",
            data=df.to_excel(index=False, engine='openpyxl'),
            file_name="translated_names.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
