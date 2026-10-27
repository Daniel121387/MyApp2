import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LANGUAGES = {"영어": "English", "일본어": "Japanese", "중국어": "Simplified Chinese"}

st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 간단 번역기")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(".env 파일에 OPENAI_API_KEY를 설정해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)


def translate(text: str, target: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the user's text into {target}. "
                    "Output only the translation, without explanations."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


text = st.text_area("번역할 글을 입력하세요", height=200)
language = st.radio("번역할 언어", list(LANGUAGES), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해주세요.")
    else:
        with st.spinner("번역 중..."):
            try:
                result = translate(text, LANGUAGES[language])
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
            else:
                st.subheader(f"{language} 번역 결과")
                st.text_area("결과", result, height=200, label_visibility="collapsed")
