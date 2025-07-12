import streamlit as st
import pandas as pd
from googletrans import Translator
import io
import time

st.title("📗 Arabic Name Translator (Excel Upload)")
st.write("Upload an Excel file with Arabic names. This app will translate them to English.")

# File uploader
uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully.")

        # Ask user to select the column with Arabic names
        columns = df.columns.tolist()
        column = st.selectbox("Select column with Arabic names:", columns)

        # Button to start translation
        if st.button("🔁 Translate"):
            translator = Translator()
            translations = []
            errors = 0

            progress = st.progress(0)
            status_text = st.empty()
            start_time = time.time()

            for i, text in enumerate(df[column]):
                try:
                    translated = translator.translate(str(text), src="ar", dest="en").text
                except Exception:
                    translated = "⚠️ Error"
                    errors += 1
                translations.append(translated)
                progress.progress((i + 1) / len(df))
                status_text.text(f"Translating... {int((i + 1) / len(df) * 100)}%")

            end_time = time.time()
            elapsed = end_time - start_time

            # Add translated column
            df["Translated"] = translations
            df = df.astype(str)  # Prevent Excel export errors

            # Show preview
            st.subheader("Preview")
            st.dataframe(df)

            # Prepare for download
            output = io.BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="📥 Download Translated Excel",
                data=output,
                file_name="translated_names.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Summary
            st.success(f"✅ Translation complete. Errors: {errors}")
            st.info(f"⏱️ Time elapsed: {elapsed:.2f} seconds")

    except Exception as e:
        st.error("⚠️ Something went wrong. Please check your file format.")
        st.exception(e)
