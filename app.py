import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐")
st.title("🌐 Language Translation Tool")
st.caption("CodeAlpha AI Internship - Task 1")

LANGS = GoogleTranslator().get_supported_languages(as_dict=True)  # {'english': 'en', ...}
names = sorted(LANGS.keys())

col1, col2 = st.columns(2)
src = col1.selectbox("Source language", ["auto detect"] + names)
tgt = col2.selectbox("Target language", names, index=names.index("tamil") if "tamil" in names else 0)

text = st.text_area("Enter text to translate", height=150)

if st.button("Translate", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            source = "auto" if src == "auto detect" else LANGS[src]
            result = GoogleTranslator(source=source, target=LANGS[tgt]).translate(text)
            st.session_state["result"] = result
            st.session_state["tgt_code"] = LANGS[tgt]
        except Exception as e:
            st.error(f"Translation failed: {e}")

if "result" in st.session_state:
    st.subheader("Translated text")
    st.text_area("Result", st.session_state["result"], height=150)
    st.code(st.session_state["result"], language=None)  # code block has a built-in copy button

    if st.button("🔊 Listen"):
        try:
            buf = io.BytesIO()
            gTTS(st.session_state["result"], lang=st.session_state["tgt_code"]).write_to_fp(buf)
            st.audio(buf.getvalue(), format="audio/mp3")
        except Exception as e:
            st.error(f"Text-to-speech not available for this language: {e}")
