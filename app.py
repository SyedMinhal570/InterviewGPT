import streamlit as st
from io import BytesIO
import speech_recognition as sr
from utils.pdf_parser import extract_text_from_pdf
from utils.question_gen import generate_questions
from utils.evaluator import evaluate_answer

# ------------------ Page Config ------------------
st.set_page_config(page_title="InterviewGPT", page_icon="🎤", layout="wide")

# ------------------ Custom CSS for Aesthetics ------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .css-1d391kg, .st-bd, .st-c0, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7 {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FE6B8B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(254,107,139,0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(254,107,139,0.6);
    }
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(15px);
    }
    .score-card {
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        color: #FFD700;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.markdown('<div class="title-text">🎤 InterviewGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">AI Mock Interview Platform — Speak. Get Scored. Improve.</div>', unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    num_questions = st.slider("Number of Questions", 3, 10, 5)
    st.markdown("---")
    st.markdown("### 📊 Scoring Factors")
    st.markdown("""
    - **Relevance**  \nSemantic similarity to question
    - **Grammar**  \nSentence complexity & punctuation
    - **Readability**  \nFlesch Reading Ease
    - **Keyword Match**  \nJob-specific keywords
    """)
    st.markdown("---")
    st.caption("Built with ❤️ by [SyedMinhal570](https://github.com/SyedMinhal570)")

# ------------------ Native Voice-to-Text (st.audio_input) ------------------
def voice_to_text_from_audio_input(q_idx):
    """Record audio using native Streamlit widget (unique key per question)."""
    audio_bytes = st.audio_input("🎙️ Record your answer", key=f"audio_{q_idx}")
    if audio_bytes is not None:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes.read())
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("✅ Voice captured!")
            return text
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please try again.")
            return ""
        except sr.RequestError as e:
            st.error(f"Speech recognition service error: {e}")
            return ""
    return ""

# ------------------ Main App ------------------
col1, col2 = st.columns(2)
with col1:
    uploaded_resume = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
    if uploaded_resume is not None:
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("✅ Resume parsed successfully!")
    else:
        resume_text = None
with col2:
    job_desc = st.text_area("📝 Paste Job Description", height=200)

if uploaded_resume and job_desc and st.button("🚀 Start Interview"):
    st.session_state['questions'] = generate_questions(resume_text, job_desc, num_questions)
    st.session_state['current_q'] = 0
    st.session_state['answers'] = []
    st.session_state['evaluation'] = []
    st.rerun()

if 'questions' in st.session_state:
    q_idx = st.session_state['current_q']
    total_q = len(st.session_state['questions'])
    
    if q_idx < total_q:
        question = st.session_state['questions'][q_idx]
        st.markdown(f"""
        <div class="score-card">
            <h3 style="color:white;">Question {q_idx+1}/{total_q}</h3>
            <p style="font-size:1.2rem; color:white;">{question}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice recording (native widget)
        voice_text = voice_to_text_from_audio_input(q_idx)
        
        # Text area for answer (pre-filled if voice gave result)
        if voice_text:
            answer = st.text_area("✏️ Your Answer (edit if needed)", value=voice_text, height=150, key=f"edit_ans_{q_idx}")
        else:
            answer = st.text_area("✏️ Your Answer (type)", key=f"ans_{q_idx}", height=150)
        
        if st.button("✅ Submit Answer & Next"):
            if answer.strip():
                score = evaluate_answer(question, answer)
                st.session_state['answers'].append(answer)
                st.session_state['evaluation'].append(score)
                st.session_state['current_q'] += 1
                if st.session_state['current_q'] < total_q:
                    st.rerun()
                else:
                    st.rerun()
            else:
                st.warning("Please provide an answer.")
    else:
        st.success("🎉 Interview Completed!")
        st.markdown("<h2 style='color:white; text-align:center;'>Your Performance Report</h2>", unsafe_allow_html=True)
        
        overall = 0
        for i, (q, ans, ev) in enumerate(zip(st.session_state['questions'],
                                              st.session_state['answers'],
                                              st.session_state['evaluation'])):
            st.markdown(f"""
            <div class="score-card">
                <p style="color:white;"><strong>Q{i+1}:</strong> {q}</p>
                <p style="color:#ddd;">Your Answer: <em>{ans[:200]}...</em></p>
                <div style="display:flex; gap:10px; flex-wrap:wrap; margin:10px 0;">
                    <span style="background:#00c6ff; padding:5px 10px; border-radius:8px;">Relevance: {ev['relevance']}%</span>
                    <span style="background:#38f9d7; padding:5px 10px; border-radius:8px;">Grammar: {ev['grammar']}%</span>
                    <span style="background:#ff9a9e; padding:5px 10px; border-radius:8px;">Readability: {ev['readability']}%</span>
                    <span style="background:#fad0c4; padding:5px 10px; border-radius:8px;">Keyword Match: {ev['keyword_match']}%</span>
                    <span style="background:#a18cd1; padding:5px 10px; border-radius:8px; font-weight:bold;">Overall: {ev['overall_score']}%</span>
                </div>
                <div class="stProgress" style="height:10px;">
                    <div style="width:{ev['overall_score']}%; background:linear-gradient(90deg, #43e97b, #38f9d7); height:100%; border-radius:10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            overall += ev['overall_score']
        
        avg_score = overall / len(st.session_state['evaluation'])
        st.metric("🏆 Average Score", f"{avg_score:.1f}%")
        
        if st.button("🔄 Restart Interview"):
            for key in ['questions', 'current_q', 'answers', 'evaluation']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()