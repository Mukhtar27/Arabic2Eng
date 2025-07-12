import streamlit as st
import pandas as pd
from googletrans import Translator

st.title("📗 Arabic to English Translator (Google Translate Free)")

uploaded_file = st.file_uploader("Upload Excel (.xlsx) with Arabic Names", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    column = st.selectbox("Select the column with Arabic names", df.columns)

    if st.button("Translate"):
        st.info("Translating using Google Translate (no API key)...")
        translator = Translator()
        translated = []
        progress = st.progress(0)

        for i, text in enumerate(df[column]):
            try:
                result = translator.translate(str(text), src='ar', dest='en')
                translated.append(result.text)
            except:
                translated.append("⚠️ Error")
            progress.progress((i + 1) / len(df))

        df["Translated"] = translated
        st.success("✅ Translation Complete!")
        st.dataframe(df)

        st.download_button(
            "📥 Download Translated Excel",
            data=df.to_excel(index=False, engine="openpyxl"),
            file_name="translated_names.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
