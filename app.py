import streamlit as st
import os
import sys
import random
import json
import traceback
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Ensure env is loaded with override
load_dotenv(override=True)

# 1. IMPORT BACKEND MODULES
try:
    import main_backend as backend
    import database as db
except Exception as e:
    st.error(f"❌ CRITICAL ERROR: Could not import backend modules.")
    st.error(f"Error Details: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

# 2. PAGE CONFIGURATION
# 2. PAGE CONFIGURATION
st.set_page_config(
    page_title="Sophy • AI Learning Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. MODERN SOPHY THEME
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* ==========================================
BACKGROUND
========================================== */

.stApp{

background:
radial-gradient(circle at top right,#273B72 0%,transparent 35%),
radial-gradient(circle at bottom left,#1D2947 0%,transparent 30%),
linear-gradient(180deg,#09111F,#111C2E);

color:#F8FAFC !important;

}

/* ==========================================
CONTENT
========================================== */

.main .block-container{

max-width:1100px;

padding-top:2rem;

padding-bottom:3rem;

}

/* ==========================================
SIDEBAR
========================================== */

section[data-testid="stSidebar"]{

background:#111C2E;

border-right:1px solid rgba(255,255,255,.05);

}

/* ==========================================
HEADINGS & TEXTS
========================================== */

h1,h2,h3,h4{

font-weight:700;

color:white !important;

}

label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown strong {
    color: #F8FAFC !important;
}

/* ==========================================
BUTTONS
========================================== */

div.stButton>button{

width:100%;

border:none;

border-radius:14px;

padding:12px;

font-weight:700;

font-size:15px;

background:
linear-gradient(
135deg,
#6366F1,
#3B82F6
);

color:white !important;

transition:.25s;

box-shadow:
0 12px 25px rgba(0,0,0,.30);

}

div.stButton>button:hover{

transform:translateY(-2px);

box-shadow:
0 18px 35px rgba(0,0,0,.35);

}

/* ==========================================
INPUTS & SELECTBOXES
========================================== */

.stTextInput input, .stNumberInput input {

background:#16253A !important;

border-radius:14px !important;

border:1px solid rgba(255,255,255,.08)!important;

color:white !important;

padding:12px !important;

}

/* Style Selectboxes */
div[data-baseweb="select"] > div {
    background-color: #16253A !important;
    color: #F8FAFC !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,.08) !important;
}

div[data-baseweb="select"] span {
    color: #F8FAFC !important;
}

/* Style Popovers and dropdown list containers */
div[data-baseweb="popover"], ul[role="listbox"], div[role="listbox"] {
    background-color: #16253A !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255,255,255,.1) !important;
}

li[role="option"], div[role="option"] {
    background-color: #16253A !important;
    color: #F8FAFC !important;
}

li[role="option"]:hover, div[role="option"]:hover {
    background-color: #3B82F6 !important;
    color: white !important;
}

/* ==========================================
TABS
========================================== */

button[data-baseweb="tab"]{

font-weight:700;

border-radius:12px;

}

button[data-baseweb="tab"] p {
    color: #CBD5E1 !important;
}

button[data-baseweb="tab"][aria-selected="true"] p {
    color: #F8FAFC !important;
}

/* ==========================================
RADIO & CHECKBOX COLOURED TEXTS
========================================== */

div[data-testid="stRadio"] label, div[data-testid="stRadio"] p, div[data-testid="stRadio"] span {
    color: #F8FAFC !important;
}

div[data-testid="stCheckbox"] label, div[data-testid="stCheckbox"] p, div[data-testid="stCheckbox"] span {
    color: #F8FAFC !important;
}

/* ==========================================
METRICS
========================================== */

div[data-testid="metric-container"]{

background:#16253A;

border-radius:18px;

padding:20px;

border:1px solid rgba(255,255,255,.06);

}

div[data-testid="metric-container"] label, div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

/* ==========================================
CARD
========================================== */

.sophy-card{

background:rgba(255,255,255,.05);

backdrop-filter:blur(14px);

border-radius:22px;

padding:30px;

border:1px solid rgba(255,255,255,.06);

box-shadow:
0 18px 40px rgba(0,0,0,.30);

}

/* ==========================================
QUIZ CARD
========================================== */

.quiz-card{

background:rgba(255,255,255,.08);

backdrop-filter:blur(14px);

color:#F8FAFC !important;

padding:30px;

border-radius:22px;

border:1px solid rgba(255,255,255,.1);

box-shadow:
0 15px 30px rgba(0,0,0,.25);

margin-bottom:20px;

}

/* ==========================================
ALERTS
========================================== */

div[data-testid="stAlert"]{

border-radius:14px;

}

/* ==========================================
HIDE STREAMLIT
========================================== */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# 4. SESSION STATE INITIALIZATION
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'cards_queue' not in st.session_state:
    st.session_state.cards_queue = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'wrong_attempts_on_card' not in st.session_state:
    st.session_state.wrong_attempts_on_card = set()
if 'failed_cards_pool' not in st.session_state:
    st.session_state.failed_cards_pool = []
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False
if 'active_deck_name' not in st.session_state:
    st.session_state.active_deck_name = None
if 'active_deck_subject' not in st.session_state:
    st.session_state.active_deck_subject = None

# Helper directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# =============================================================================
# SCREEN A: LOGIN & SIGN UP
# =============================================================================

def login_screen():

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#6366F1,#3B82F6);
        padding:42px;
        border-radius:26px;
        text-align:center;
        margin-bottom:28px;
        box-shadow:0 20px 45px rgba(0,0,0,.30);
    ">

    <h1 style="
        margin:0;
        color:white;
        font-size:3rem;
        font-weight:800;
    ">
        🧠 Sophy
    </h1>

    <p style="
        margin-top:14px;
        color:#E2E8F0;
        font-size:1.1rem;
    ">
        Your AI-powered learning companion.
        Study smarter, stay organized, and master every lesson.
    </p>

    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:

        st.markdown("""
        <div class="sophy-card">

        <h3 style="margin-top:0;color:white;">
        Welcome Back 👋
        </h3>

        <p style="color:#CBD5E1;">
        Sign in to continue learning with Sophy.
        </p>

        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])

        with tab1:

            st.subheader("Sign In")

            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="login_pass"
            )

            if st.button(
                "🚀 Sign In",
                type="primary",
                use_container_width=True
            ):

                if not email or not password:

                    st.warning("Please fill out your credentials.")

                else:

                    with st.spinner("Signing you in..."):

                        result = backend.login_user(email, password)

                        if result and result.get('success'):

                            st.session_state.user_id = result['user_id']
                            st.session_state.profile = result['profile']

                            st.success(
                                "🎉 Welcome back! Redirecting..."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"Login failed: {result.get('message', 'Invalid credentials.')}"
                            )

        with tab2:

            st.subheader("Create your Sophy account")

            username = st.text_input(
                "Username",
                placeholder="Choose a username",
                key="reg_user"
            )

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com",
                key="reg_email"
            )

            password = st.text_input(
                "Password",
                placeholder="Create a strong password",
                type="password",
                key="reg_pass"
            )

            if st.button(
                "✨ Create Account",
                type="primary",
                use_container_width=True
            ):

                if not all([username, email, password]):

                    st.warning("Please complete all required fields.")

                else:

                    with st.spinner("Creating your account..."):

                        result = backend.register_user(
                            username,
                            email,
                            password,
                            10
                        )

                        if result and result.get('success'):

                            st.success(
                                "🎉 Your Sophy account has been created successfully! Please sign in using the Login tab."
                            )

                        else:

                            st.error(
                                f"Signup failed: {result.get('message', 'Failed to register.')}"
                            )

# =============================================================================
# SCREEN B: MAIN APP DASHBOARD
# =============================================================================
def dashboard():

    username = st.session_state.profile.get('username', 'Learner')
    mastery = st.session_state.profile.get('mastery_score', 0.0)

    # ------------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------------

    st.sidebar.markdown(
        f"""
        <div style="
            text-align:center;
            padding:18px;
            margin-bottom:18px;
        ">
            <h2 style="margin-bottom:0;">🧠 Sophy</h2>
            <p style="color:#CBD5E1;margin-top:4px;">
                Welcome back,<br><b>{username}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.metric(
        "Learning Mastery",
        f"{mastery:.1%}"
    )

    st.sidebar.divider()

    app_mode = st.sidebar.radio(
        "Navigation",
        [
            "📚 Study Dojo",
            "✨ Create Reviewer",
            "📁 Saved Files",
            "💬 AI Tutor Chat"
        ]
    )

    st.sidebar.divider()

    st.sidebar.subheader("Preferences")

    st.sidebar.selectbox(
        "Language Style",
        [
            "Taglish",
            "English",
            "Tagalog"
        ],
        key="global_lang_pref"
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Log Out",
        use_container_width=True
    ):
        st.session_state.user_id = None
        st.session_state.profile = None
        st.session_state.quiz_started = False
        st.session_state.cards_queue = []
        st.rerun()

    # ------------------------------------------------------------------
    # HERO
    # ------------------------------------------------------------------

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#6366F1,#3B82F6);
        padding:34px;
        border-radius:24px;
        margin-bottom:28px;
        color:white;
        box-shadow:0 18px 40px rgba(0,0,0,.25);
    ">

    <h1 style="margin:0;">
        Welcome back, {username}! 👋
    </h1>

    <p style="
        margin-top:10px;
        font-size:18px;
        color:#E2E8F0;
    ">
        Continue your learning journey with Sophy.
        Build stronger mastery one session at a time.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # DASHBOARD METRICS
    # ------------------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎯 Mastery",
            f"{mastery:.1%}"
        )

    with col2:
        st.metric(
            "📚 Active Deck",
            st.session_state.active_deck_name
            if st.session_state.active_deck_name
            else "None"
        )

    with col3:
        st.metric(
            "🧠 Quiz Status",
            "Active"
            if st.session_state.quiz_started
            else "Ready"
        )

    st.write("")

    # ------------------------------------------------------------------
    # STUDY DOJO
    # ------------------------------------------------------------------

    if app_mode == "📚 Study Dojo":

        st.markdown("## 📚 Study Dojo")
        st.caption("Choose one of your reviewers and begin a focused study session.")

        decks_and_cards = backend.get_user_decks_and_cards(
            st.session_state.user_id
        )

        if not decks_and_cards:

            st.info(
                "No reviewers available yet.\n\n"
                "Create your first reviewer in **✨ Create Reviewer**."
            )

        else:

            if st.session_state.quiz_started:
                # Active Quiz Session
                deck_cards = st.session_state.cards_queue
                current_idx = st.session_state.current_index
                total_cards = len(deck_cards)
                
                if current_idx < total_cards:
                    current_card = deck_cards[current_idx]
                    progress_value = current_idx / total_cards
                    st.progress(progress_value)
                    
                    col_info_1, col_info_2 = st.columns([3, 1])
                    with col_info_1:
                        st.markdown(f"📖 **Active Reviewer**: `{st.session_state.active_deck_name}`")
                        st.markdown(f"🏷️ **Subject**: `{st.session_state.active_deck_subject}`")
                    with col_info_2:
                        if st.button("🚪 Quit Session", key="quit_quiz_session"):
                            st.session_state.quiz_started = False
                            st.session_state.cards_queue = []
                            st.rerun()
                            
                    st.write(f"Question **{current_idx + 1}** of **{total_cards}**")
                    
                    # Question Card
                    st.markdown(f"""
                    <div style="
                        background:rgba(255,255,255,.05);
                        border:1px solid rgba(255,255,255,.08);
                        border-radius:22px;
                        padding:30px;
                        margin-bottom:20px;
                        box-shadow:0 15px 30px rgba(0,0,0,.25);
                        backdrop-filter:blur(12px);
                    ">
                        <h3 style="margin-top:0;color:#6366F1;">🤖 Sophy AI Companion:</h3>
                        <p style="font-weight: 500; font-size: 1.15rem; color: white; margin-bottom: 0;">{current_card["question"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    options = current_card["options"]
                    correct = current_card["correct_answer"]
                    
                    # Option buttons
                    if not st.session_state.answered_correctly:
                        cols = st.columns(2)
                        for i, option in enumerate(options):
                            col_choice = cols[i % 2]
                            with col_choice:
                                if option in st.session_state.wrong_attempts_on_card:
                                    st.button(f"❌ {option}", key=f"opt_{current_idx}_{i}", disabled=True)
                                else:
                                    if st.button(option, key=f"opt_{current_idx}_{i}"):
                                        if option == correct:
                                            st.session_state.answered_correctly = True
                                            backend.update_flashcard_review(st.session_state.user_id, current_card["id"], is_correct=True)
                                            if st.session_state.profile:
                                                cur = st.session_state.profile.get('mastery_score', 0.0) or 0.0
                                                st.session_state.profile['mastery_score'] = min(1.0, cur + 0.05)
                                            st.rerun()
                                        else:
                                            st.session_state.wrong_attempts_on_card.add(option)
                                            if current_card not in st.session_state.failed_cards_pool:
                                                st.session_state.failed_cards_pool.append(current_card)
                                                backend.update_flashcard_review(st.session_state.user_id, current_card["id"], is_correct=False)
                                                if st.session_state.profile:
                                                    cur = st.session_state.profile.get('mastery_score', 0.0) or 0.0
                                                    st.session_state.profile['mastery_score'] = max(0.0, cur - 0.02)
                                            st.rerun()
                    else:
                        # Correct choice selected review screen
                        cols = st.columns(2)
                        for i, option in enumerate(options):
                            col_choice = cols[i % 2]
                            with col_choice:
                                if option == correct:
                                    st.button(f"✅ {option}", key=f"opt_{current_idx}_{i}", type="primary", disabled=True)
                                else:
                                    st.button(option, key=f"opt_{current_idx}_{i}", disabled=True)
                                    
                        st.success("🎯 Tama ang sagot mo! Great job, Tropa!")
                        
                        # Next Question button
                        if st.button("Next Scenario ➡️", type="primary"):
                            st.session_state.current_index += 1
                            st.session_state.wrong_attempts_on_card.clear()
                            st.session_state.answered_correctly = False
                            st.rerun()
                else:
                    # Round cleared screen
                    st.balloons()
                    st.markdown("""
                    <div style="
                        background:linear-gradient(135deg,#10B981,#059669);
                        padding:34px;
                        border-radius:24px;
                        margin-bottom:28px;
                        color:white;
                        text-align:center;
                        box-shadow:0 18px 40px rgba(0,0,0,.25);
                    ">
                        <h2 style="margin:0;">🏁 Dojo Round Cleared!</h2>
                        <p style="margin-top:10px;font-size:18px;color:#E2E8F0;">
                            Excellent effort. You have finished reviewing all cards in this session.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show missed count
                    missed_count = len(st.session_state.failed_cards_pool)
                    if missed_count > 0:
                        st.warning(f"⚠️ You missed {missed_count} question(s) on the first attempt in this session.")
                    else:
                        st.success("🎉 Perfect score on first attempt! You aced this deck!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("🔄 Reflash Entire Deck", use_container_width=True):
                            deck_cards = decks_and_cards.get(st.session_state.active_deck_name, [])
                            if deck_cards:
                                random.shuffle(deck_cards)
                                st.session_state.cards_queue = deck_cards
                            st.session_state.current_index = 0
                            st.session_state.wrong_attempts_on_card.clear()
                            st.session_state.failed_cards_pool = []
                            st.session_state.answered_correctly = False
                            st.rerun()
                    with col2:
                        if st.button("❌ Reflash Missed Questions", disabled=(missed_count == 0), use_container_width=True):
                            st.session_state.cards_queue = list(st.session_state.failed_cards_pool)
                            random.shuffle(st.session_state.cards_queue)
                            st.session_state.current_index = 0
                            st.session_state.wrong_attempts_on_card.clear()
                            st.session_state.failed_cards_pool = []
                            st.session_state.answered_correctly = False
                            st.rerun()
                    with col3:
                        if st.button("🧠 Generate Focus Set", disabled=(missed_count == 0), use_container_width=True):
                            with st.spinner("Generating new questions based on your mistakes..."):
                                g_lang = st.session_state.get("global_lang_pref", "Taglish")
                                res = backend.generate_focus_deck(
                                    user_id=st.session_state.user_id,
                                    deck_name=st.session_state.active_deck_name,
                                    subject=st.session_state.active_deck_subject,
                                    failed_questions=st.session_state.failed_cards_pool,
                                    total_questions=max(3, len(st.session_state.failed_cards_pool)),
                                    language=g_lang
                                )
                                if res and res.get("success"):
                                    st.success(f"Successfully created focus deck: '{res['deck_name']}'!")
                                    st.session_state.quiz_started = False
                                    st.rerun()
                                else:
                                    st.error(f"Failed to generate focus set: {res.get('message', 'AI error')}")
            else:
                # Show list of reviewers to start
                deck_names = list(decks_and_cards.keys())
                selected_deck = st.selectbox(
                    "Study Reviewer",
                    deck_names
                )
                
                deck_subject = decks_and_cards[selected_deck][0].get(
                    "subject",
                    "General"
                )
                st.info(f"📖 Subject: **{deck_subject}**")
                
                if st.button(
                    "🚀 Start Study Session",
                    type="primary",
                    use_container_width=True
                ):
                    deck_cards = decks_and_cards[selected_deck]
                    random.shuffle(deck_cards)
                    st.session_state.cards_queue = deck_cards
                    st.session_state.current_index = 0
                    st.session_state.wrong_attempts_on_card = set()
                    st.session_state.failed_cards_pool = []
                    st.session_state.answered_correctly = False
                    st.session_state.active_deck_name = selected_deck
                    st.session_state.active_deck_subject = deck_cards[0].get(
                        "subject",
                        "General"
                    )
                    st.session_state.quiz_started = True
                    st.rerun()

    # -------------------------------------------------------------------------
    # MODE 2: CREATE REVIEWER
    # -------------------------------------------------------------------------
    elif app_mode == "✨ Create Reviewer":

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#312E81,#4338CA);
            padding:30px;
            border-radius:22px;
            margin-bottom:25px;
            color:white;
            box-shadow:0 15px 35px rgba(0,0,0,.25);
        ">
            <h2 style="margin:0;">✨ Craft a New Reviewer</h2>
            <p style="margin-top:10px;color:#E2E8F0;font-size:16px;">
                Upload your slides or modules and let Sophy build a customized, adaptive Reviewer Dojo for you.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sophy-card" style="margin-bottom: 20px;">
            <h3 style="margin-top:0;color:white;">📚 1. Upload Study Materials</h3>
            <p style="color:#CBD5E1;font-size:14px;margin-bottom:15px;">
                Upload the PDF/PPTX chapters or notes that you want to study.
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload Modules",
            type=['pdf', 'pptx'],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="reviewer_file_uploader"
        )

        saved_paths = []
        if uploaded_files:
            for file in uploaded_files:
                path = save_uploaded_file(file)
                saved_paths.append(file.name)
            st.success(f"✅ Uploaded {len(uploaded_files)} file(s)!")

        st.markdown("""
        <div class="sophy-card" style="margin-top: 25px; margin-bottom: 20px;">
            <h3 style="margin-top:0;color:white;">📋 2. Upload Sample Exam format (Optional)</h3>
            <p style="color:#CBD5E1;font-size:14px;margin-bottom:15px;">
                Upload a file containing sample questions. Sophy will mimic its layout, difficulty, and question style.
            </p>
        </div>
        """, unsafe_allow_html=True)

        sample_file = st.file_uploader(
            "Upload Sample Questions Format",
            type=['pdf', 'pptx', 'txt'],
            label_visibility="collapsed",
            key="reviewer_sample_uploader"
        )

        sample_path = None
        if sample_file:
            sample_path = save_uploaded_file(sample_file)
            st.success(f"✅ Sample formatting loaded: {sample_file.name}")

        st.markdown("""
        <div class="sophy-card" style="margin-top: 25px; margin-bottom: 20px;">
            <h3 style="margin-top:0;color:white;">⚙️ 3. Reviewer Configuration</h3>
            <p style="color:#CBD5E1;font-size:14px;margin-bottom:15px;">
                Specify the title, subject category, language, and size of the reviewer dojo.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("custom_reviewer_form"):
            deck_name = st.text_input("Reviewer Title (e.g. Midterm Unit 2)", placeholder="Enter title...")
            subject_name = st.text_input("Subject Category (e.g. Philippine History)", placeholder="Enter subject...")

            g_lang = st.session_state.get("global_lang_pref", "Taglish")
            g_index = ["Taglish", "English", "Tagalog"].index(g_lang) if g_lang in ["Taglish", "English", "Tagalog"] else 0
            language_pref = st.selectbox("Language Preference", ["Taglish", "English", "Tagalog"], index=g_index)

            num_questions = st.number_input("Total Questions to Generate", 3, 50, 10, step=1)

            submit = st.form_submit_button("Generate Reviewer Dojo 🚀", type="primary")

            if submit:
                if not saved_paths:
                    st.error("❌ Please upload at least one study module PDF/PPTX first!")
                elif not deck_name or not subject_name:
                    st.error("❌ Please provide a Reviewer Title and Subject Category.")
                else:
                    with st.spinner("🧠 Sophy is reading, digesting, and validating questions..."):
                        for fname in saved_paths:
                            db.save_document_metadata(st.session_state.user_id, fname, os.path.join(UPLOAD_DIR, fname))

                        res = backend.generate_reviewer_deck(
                            user_id=st.session_state.user_id,
                            deck_name=deck_name,
                            subject=subject_name,
                            selected_files=saved_paths,
                            total_questions=num_questions,
                            sample_format_file=sample_path,
                            language=language_pref
                        )

                        if res and res.get("success"):
                            st.success(f"🎉 Successfully created '{deck_name}' deck with {res.get('cards_count', 0)} cards!")
                            st.balloons()
                        else:
                            st.error(f"❌ Failed to generate deck: {res.get('message', 'AI model error')}")

    # -------------------------------------------------------------------------
    # MODE 3: SAVED FILES
    # -------------------------------------------------------------------------
    elif app_mode == "📁 Saved Files":

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#4F46E5,#2563EB);
            padding:30px;
            border-radius:22px;
            margin-bottom:25px;
            color:white;
            box-shadow:0 15px 35px rgba(0,0,0,.25);
        ">
            <h2 style="margin:0;">📁 Learning Vault</h2>
            <p style="margin-top:10px;color:#E2E8F0;font-size:16px;">
                All your uploaded reviewers are stored here for quick access.
                Files remain available for <b>4 days</b> before automatic removal.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Load user documents
        docs = db.get_user_documents(st.session_state.user_id)

        if not docs:

            st.info("📭 Your Learning Vault is currently empty.")

        else:

            active_docs = []

            for doc in docs:

                uploaded_at_str = doc.get("uploaded_at") or doc.get("created_at")

                if uploaded_at_str:

                    try:

                        uploaded_at = datetime.fromisoformat(
                            uploaded_at_str.replace("Z", "+00:00")
                        )

                        age = datetime.now(timezone.utc) - uploaded_at

                        if age < timedelta(days=4):

                            time_left = timedelta(days=4) - age

                            hours_left = int(time_left.total_seconds() // 3600)

                            minutes_left = int(
                                (time_left.total_seconds() % 3600) // 60
                            )

                            doc["expires_in"] = f"{hours_left}h {minutes_left}m"

                            active_docs.append(doc)

                    except:

                        doc["expires_in"] = "Active"

                        active_docs.append(doc)

                else:

                    doc["expires_in"] = "Active"

                    active_docs.append(doc)

            if not active_docs:

                st.warning(
                    "⚠️ All cached reviewers have expired.\n\nUpload them again to continue studying."
                )

            else:

                st.markdown("### 📚 Available Study Materials")

                for doc in active_docs:

                    st.markdown(f"""
                    <div style="
                        background:rgba(255,255,255,.06);
                        border:1px solid rgba(255,255,255,.08);
                        border-radius:18px;
                        padding:22px;
                        margin-bottom:18px;
                        backdrop-filter:blur(12px);
                        box-shadow:0 10px 25px rgba(0,0,0,.20);
                    ">

                    <h3 style="
                        margin-top:0;
                        margin-bottom:10px;
                        color:white;
                    ">
                        📄 {doc['filename']}
                    </h3>

                    <p style="
                        color:#CBD5E1;
                        margin-bottom:6px;
                    ">
                        📅 <b>Uploaded</b>:
                        {doc.get('uploaded_at','Unknown')[:10]}
                    </p>

                    <p style="
                        color:#CBD5E1;
                        margin-bottom:0;
                    ">
                        ⏳ <b>Expires In</b>:
                        {doc.get('expires_in')}
                    </p>

                    </div>
                    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MODE 4: AI TUTOR CHAT
    # -------------------------------------------------------------------------
    elif app_mode == "💬 AI Tutor Chat":

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#4F46E5,#2563EB);
            padding:30px;
            border-radius:22px;
            margin-bottom:25px;
            color:white;
            box-shadow:0 15px 35px rgba(0,0,0,.25);
        ">
            <h2 style="margin:0;">💬 Sophy AI Tutor</h2>
            <p style="margin-top:10px;color:#E2E8F0;font-size:16px;">
                Ask questions about your lessons, reviewers,
                assignments, or anything you are currently studying.
            </p>
        </div>
        """, unsafe_allow_html=True)

        top_left, top_right = st.columns([4,1])

        with top_right:

            search_online = st.checkbox(
                "🌐 Web Search"
            )

        st.divider()

        if not st.session_state.chat_messages:

            st.info(
                "👋 Welcome!\n\n"
                "Start a conversation with Sophy by typing your first question below."
            )

        # Display chat history
        for msg in st.session_state.chat_messages:

            with st.chat_message(msg['role']):

                st.write(msg['content'])

        # Input block
        if prompt := st.chat_input("Ask Sophy anything..."):

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):

                st.write(prompt)

            with st.chat_message("assistant"):

                with st.spinner("🧠 Sophy is thinking..."):

                    g_lang = st.session_state.get(
                        "global_lang_pref",
                        "Taglish"
                    )

                    res = backend.ask_study_companion(
                        st.session_state.user_id,
                        prompt,
                        search_online=search_online,
                        language=g_lang
                    )

                    if res and res.get("success"):

                        ans = res["data"].get(
                            "explanation_taglish",
                            "Pasensya na, hindi ko nagawa ang sagot."
                        )

                        consensus = res["data"].get(
                            "ai_consensus_note",
                            ""
                        )

                        if consensus:

                            ans += f"\n\n> 📌 **Note:** {consensus}"

                        quote = res["data"].get(
                            "motivation_quote",
                            ""
                        )

                        if quote:

                            ans += (
                                f"\n\n---\n"
                                f"💡 **Sophy's Motivation**\n\n"
                                f"*{quote}*"
                            )

                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "content": ans
                            }
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Error answering: {res.get('error', 'Unknown Error')}"
                        )

# =============================================================================
# MAIN ORCHESTRATION
# =============================================================================
if __name__ == "__main__":
    if st.session_state.user_id:
        dashboard()
    else:
        login_screen()