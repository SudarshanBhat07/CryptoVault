import streamlit as st

# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from modules.hill_cipher import render_hill_cipher
from modules.aes_encryption import render_aes_encryption
from modules.key_management import render_key_management
from modules.authentication import render_authentication
from modules.cryptanalysis import render_cryptanalysis
from modules.cryptoguard import render_cryptoguard
from modules.performance import render_performance


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CryptoVault | Security Suite",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# ENTERPRISE CYBERSECURITY DESIGN SYSTEM
# ==========================================

st.html("""
<style>

/* ==========================================
   GLOBAL
========================================== */

:root {
    --background: #0B1220;
    --sidebar: #101B2D;
    --surface: #152238;
    --surface-hover: #1B2D47;
    --border: #293B55;
    --primary: #3B82F6;
    --accent: #38BDF8;
    --text: #E2E8F0;
    --muted: #94A3B8;
    --success: #4ADE80;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--background) !important;
    color: var(--text) !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Main text */

p, li, label {
    color: var(--text);
}

/* Header */

[data-testid="stHeader"] {
    background: var(--background) !important;
}

/* ==========================================
   SIDEBAR
========================================== */

[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    background: var(--sidebar) !important;
    padding-top: 1.5rem;
}

.sidebar-brand {
    text-align: center;
    padding: 12px 0 20px 0;
}

.sidebar-logo {
    font-size: 43px;
    font-weight: 800;
    color: #60A5FA;
    letter-spacing: 2px;
}

.sidebar-name {
    font-size: 19px;
    font-weight: 700;
    color: #F1F5F9;
    margin-top: 4px;
}

.sidebar-caption {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 5px;
}

[data-testid="stSidebar"] h3 {
    color: #F1F5F9 !important;
    font-size: 15px;
    letter-spacing: 1px;
}

/* Sidebar radio navigation */

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 5px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent;
    border-radius: 8px;
    padding: 9px 10px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #1B2D47 !important;
    border-color: #344761;
}

[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #CBD5E1 !important;
    font-size: 14px;
}

/* ==========================================
   HEADINGS
========================================== */

h1, h2, h3, h4 {
    color: #F1F5F9 !important;
    font-weight: 650 !important;
    letter-spacing: -0.3px;
}

.main-title {
    color: #60A5FA !important;
    font-size: 43px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 1px;
    margin-top: 10px;
}

.subtitle {
    color: #94A3B8 !important;
    text-align: center;
    font-size: 15px;
    margin-bottom: 32px;
}

.section-title {
    color: #E2E8F0 !important;
    font-size: 21px;
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 17px;
}

/* ==========================================
   WELCOME PANEL
========================================== */

.welcome-box {
    background: linear-gradient(
        120deg,
        #172D4A,
        #142238
    );
    border: 1px solid #31547B;
    border-left: 4px solid #3B82F6;
    border-radius: 13px;
    padding: 28px 30px;
    margin: 20px 0 28px 0;
}

.welcome-box h2 {
    color: #60A5FA !important;
    font-size: 25px;
    margin-top: 0;
}

.welcome-box p {
    color: #C5D2E2 !important;
    font-size: 14px;
    line-height: 1.9;
}

/* ==========================================
   METRICS
========================================== */

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px;
    padding: 18px;
    transition: border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--primary) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    color: #60A5FA !important;
    font-weight: 750;
}

/* ==========================================
   MODULE CARDS
========================================== */

.module-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 15px;
    transition: all 0.2s ease;
}

.module-card:hover {
    background: var(--surface-hover);
    border-color: var(--primary);
    transform: translateY(-3px);
}

.module-card h4 {
    color: #60A5FA !important;
    font-size: 16px;
    margin-top: 0;
    margin-bottom: 12px;
}

.module-card p {
    color: #B6C4D6 !important;
    font-size: 13px;
    line-height: 1.8;
    margin-bottom: 0;
}

/* ==========================================
   TECHNOLOGY CARDS
========================================== */

.tech-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px 15px;
    min-height: 105px;
    text-align: center;
    transition: all 0.2s ease;
}

.tech-card:hover {
    border-color: var(--accent);
    background: var(--surface-hover);
}

.tech-card h4 {
    color: #60A5FA !important;
    font-size: 17px;
    margin: 0;
}

.tech-card p {
    color: var(--muted) !important;
    font-size: 12px;
    margin-bottom: 0;
}

/* ==========================================
   BUTTONS
========================================== */

.stButton > button {
    background: #2563EB !important;
    color: white !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 8px !important;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #1D4ED8 !important;
    border-color: #60A5FA !important;
}

/* ==========================================
   INPUT FIELDS
========================================== */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #172338 !important;
    color: #E2E8F0 !important;
    border: 1px solid #344761 !important;
    border-radius: 8px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label {
    color: #CBD5E1 !important;
}

/* Select boxes */

[data-baseweb="select"] > div {
    background: #172338 !important;
    border-color: #344761 !important;
    color: #E2E8F0 !important;
}

/* ==========================================
   EXPANDERS
========================================== */

[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary {
    color: #E2E8F0 !important;
}

/* ==========================================
   ALERTS
========================================== */

[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ==========================================
   FILE UPLOADER
========================================== */

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed #3B526F !important;
    border-radius: 10px !important;
    padding: 12px;
}

/* ==========================================
   DATAFRAMES
========================================== */

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
}

/* ==========================================
   STATUS
========================================== */

.status {
    background: #123524;
    color: #86EFAC;
    padding: 10px;
    border: 1px solid #166534;
    border-radius: 8px;
    text-align: center;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* ==========================================
   FOOTER
========================================== */

.footer {
    text-align: center;
    color: #64748B !important;
    font-size: 12px;
    margin-top: 45px;
    padding: 22px;
    border-top: 1px solid var(--border);
}

/* ==========================================
   DIVIDERS AND SCROLLBAR
========================================== */

hr {
    border-color: var(--border) !important;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0B1220;
}

::-webkit-scrollbar-thumb {
    background: #344761;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #3B82F6;
}

</style>
""")


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">🔐 CV</div>

        <div class="sidebar-name">CryptoVault</div>

        <div class="sidebar-caption">
            Cryptography Security Suite
        </div>

    </div>
    """)

    st.divider()

    st.markdown("### NAVIGATION")

    page = st.radio(
        "Select Module",
        [
            "Home",
            "Classical Cryptography",
            "Modern Cryptography",
            "Key Management",
            "Authentication Lab",
            "Cryptanalysis Lab",
            "CryptoGuard",
            "Performance Analysis"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.html("""
    <div class="status">
        ● SYSTEM ONLINE
    </div>
    """)

    st.markdown("")

    st.caption("Advanced Cryptography Project")
    st.caption("Version 1.0")


# ==========================================
# HOME DASHBOARD
# ==========================================

if page == "Home":

    # MAIN TITLE

    st.html("""
    <div class="main-title">
        🔐 CryptoVault
    </div>

    <div class="subtitle">
        Advanced Cryptography and Secure File Encryption
    </div>
    """)

    # WELCOME PANEL

    st.html("""
    <div class="welcome-box">

        <h2>Welcome to CryptoVault</h2>

        <p>
            An integrated cryptography platform designed
            to demonstrate classical encryption, modern
            encryption, secure key management,
            authentication and cryptanalysis.
        </p>

        <p>
            Explore cryptographic algorithms, understand
            their working principles and perform practical
            security experiments through a unified
            learning environment.
        </p>

    </div>
    """)

    # PROJECT OVERVIEW

    st.html("""
    <div class="section-title">
        Project Overview
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Functional Modules",
            "7",
            help="Seven integrated functional modules"
        )

    with col2:
        st.metric(
            "Project Stages",
            "8"
        )

    with col3:
        st.metric(
            "Core Algorithms",
            "7+"
        )

    with col4:
        st.metric(
            "System Status",
            "Online"
        )

    # MODULE CARDS

    st.html("""
    <div class="section-title">
        Explore Project Modules
    </div>
    """)

    modules = [
        (
            "01 | Classical Cryptography",
            "Hill Cipher encryption and decryption "
            "with matrix calculations."
        ),
        (
            "02 | Modern Cryptography",
            "AES-256-GCM file encryption, "
            "decryption and tamper detection."
        ),
        (
            "03 | Key Management",
            "Scrypt, PBKDF2 and HKDF key derivation."
        ),
        (
            "04 | Authentication Lab",
            "HMAC-SHA256 authentication and "
            "ECDH key exchange."
        ),
        (
            "05 | Cryptanalysis Lab",
            "Frequency analysis and graphical "
            "ciphertext examination."
        ),
        (
            "06 | CryptoGuard",
            "Algorithm advisor, encryption "
            "visualizer and tamper detection."
        ),
        (
            "07 | Performance Analysis",
            "Execution-time comparison and "
            "performance graphs."
        ),
        (
            "08 | Final Integration & Testing",
            "Integration and testing of all "
            "project modules."
        )
    ]

    for i in range(0, len(modules), 2):

        col1, col2 = st.columns(2)

        for col, item in zip(
            [col1, col2],
            modules[i:i + 2]
        ):

            with col:

                # st.html renders the HTML directly.
                # This prevents HTML tags appearing
                # as visible code inside the cards.

                st.html(f"""
<div class="module-card">
    <h4>{item[0]}</h4>
    <p>{item[1]}</p>
</div>
""")

    # TECHNOLOGY STACK

    st.html("""
    <div class="section-title">
        Technology Stack
    </div>
    """)

    t1, t2, t3 = st.columns(3)

    with t1:
        st.html("""
<div class="tech-card">
    <h4>🐍 Python</h4>
    <p>Programming Language</p>
</div>
""")

    with t2:
        st.html("""
<div class="tech-card">
    <h4>🌐 Streamlit</h4>
    <p>Interactive Web Framework</p>
</div>
""")

    with t3:
        st.html("""
<div class="tech-card">
    <h4>🔒 Cryptography</h4>
    <p>Security Libraries</p>
</div>
""")

    # ABOUT PROJECT

    with st.expander("About CryptoVault"):

        st.write("""
        CryptoVault is an educational cryptography
        application that combines classical and modern
        cryptographic techniques.

        It demonstrates encryption, decryption,
        key derivation, authentication, key exchange,
        cryptanalysis and performance measurement.

        The application is designed for learning and
        demonstrating cryptographic concepts.
        """)

    # SECURITY NOTE

    st.info(
        "Security Note: The Hill Cipher is included "
        "for educational purposes. Use authenticated "
        "modern encryption such as AES-256-GCM for "
        "protecting sensitive files."
    )

    # FOOTER

    st.html("""
    <div class="footer">

        🔐 CryptoVault | Advanced Cryptography Project

        <br><br>

        Built with Python and Streamlit

    </div>
    """)


# ==========================================
# MODULE PAGE ROUTING
# ==========================================

elif page == "Classical Cryptography":

    render_hill_cipher()


elif page == "Modern Cryptography":

    render_aes_encryption()


elif page == "Key Management":

    render_key_management()


elif page == "Authentication Lab":

    render_authentication()


elif page == "Cryptanalysis Lab":

    render_cryptanalysis()


elif page == "CryptoGuard":

    render_cryptoguard()


elif page == "Performance Analysis":

    render_performance()
