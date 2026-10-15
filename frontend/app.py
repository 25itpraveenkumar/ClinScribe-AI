
import streamlit as st

from pathlib import Path

css_path = Path(__file__).parent / "styles.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="ClinScribe AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "draft" not in st.session_state:
    st.session_state.draft = None

if "approved" not in st.session_state:
    st.session_state.approved = False

if "consultations" not in st.session_state:
    st.session_state.consultations = 0

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #f4f7fb;
    color: #172b4d;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #14243e;
}

[data-testid="stSidebar"] * {
    color: #f1f5f9;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #f1f5f9 !important;
}

.hero {
    background: linear-gradient(120deg, #14243e, #187b82);
    padding: 32px;
    border-radius: 18px;
    color: white;
    margin-bottom: 24px;
}

.hero h1 {
    color: white !important;
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.hero p {
    color: #e0f2f1 !important;
    font-size: 1.05rem;
    margin-bottom: 0;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1e8f0;
    padding: 18px;
    border-radius: 14px;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #172b4d !important;
}

h1, h2, h3, h4, p, label {
    color: #172b4d;
}

.panel {
    background: white;
    border: 1px solid #e1e8f0;
    padding: 22px;
    border-radius: 14px;
    min-height: 145px;
}

.panel h3 {
    margin-top: 0;
    color: #14243e;
}

.panel p {
    color: #64748b;
}

div.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
}

div.stButton > button[kind="primary"] {
    background: #176b70;
    border: 1px solid #176b70;
    color: white;
}

div.stButton > button[kind="primary"]:hover {
    background: #12565a;
    border-color: #12565a;
}

div[data-testid="stAlert"] p {
    color: inherit;
}

.footer {
    color: #64748b;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 24px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.markdown("# 🩺 ClinScribe AI")
    st.caption("Clinical Documentation Assistant")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "New Consultation",
            "Review Notes",
        ],
        key="navigation",
    )

    st.divider()
    st.markdown("**Prototype status**")
    st.caption("AI integration: Pending")
    st.caption("Storage: Session only")
    st.caption("Use fictional patient data only.")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Clinical Documentation Workspace</h1>
        <p>
            Less paperwork. More time for patient care.
            Prepare structured drafts for clinician review.
        </p>
    </div>
    """, unsafe_allow_html=True)

    draft_exists = st.session_state.draft is not None
    approved_count = int(st.session_state.approved)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Consultations",
        st.session_state.consultations,
        help="Consultations started in this session.",
    )

    col2.metric(
        "Draft Notes",
        int(draft_exists),
        help="A draft currently available for review.",
    )

    col3.metric(
        "Approved Demo Notes",
        approved_count,
        help="Demo approvals in this session.",
    )

    st.write("")
    st.subheader("Welcome, Doctor")
    st.write(
        "Start a consultation or review an existing draft. "
        "All notes require clinician verification."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="panel">
            <h3>🎙️ New Consultation</h3>
            <p>
                Enter a fictional consultation transcript
                and prepare a draft note.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Start Consultation →",
            key="start_consultation",
            use_container_width=True,
        ):
            st.session_state.navigation = "New Consultation"
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="panel">
            <h3>📋 Review Notes</h3>
            <p>
                Inspect and edit SOAP sections before
                confirming a demo review.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Review Draft →",
            key="review_draft",
            use_container_width=True,
        ):
            st.session_state.navigation = "Review Notes"
            st.rerun()

    st.markdown("""
    <div class="footer">
        ClinScribe AI · Hackathon Prototype · Not for clinical use
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# NEW CONSULTATION
# --------------------------------------------------
elif page == "New Consultation":

    st.title("🎙️ New Consultation")
    st.write(
        "Record consent, enter a transcript, and prepare "
        "a draft for clinician review."
    )

    st.info(
        "This prototype does not yet perform speech recognition "
        "or AI-based medical interpretation."
    )

    consent = st.checkbox(
        "I confirm that appropriate consent has been obtained "
        "for this fictional demo consultation.",
        key="consent",
    )

    st.subheader("Consultation Audio")

    audio = st.file_uploader(
        "Upload an optional audio sample",
        type=["wav", "mp3", "m4a", "ogg"],
        help="Audio upload is available for the future transcription integration.",
    )

    if audio is not None:
        st.audio(audio)

        st.caption(
            "Audio preview only. This prototype does not "
            "transcribe the uploaded audio."
        )

    st.divider()
    st.subheader("Consultation Transcript")

    transcript = st.text_area(
        "Transcript text",
        height=220,
        placeholder=(
            "Doctor: What brings you in today?\n"
            "Patient: I have had a headache for two days.\n"
            "Doctor: Do you have a fever?\n"
            "Patient: No, I do not have a fever."
        ),
        key="transcript_input",
    )

    if st.button(
        "Prepare Draft Note",
        type="primary",
        use_container_width=True,
    ):

        if not consent:
            st.error(
                "Please confirm consent before processing."
            )

        elif not transcript.strip():
            st.error(
                "Please enter a fictional transcript first."
            )

        else:
            st.session_state.draft = {
                "transcript": transcript.strip(),
                "subjective": transcript.strip(),
                "objective": "Not provided in the transcript.",
                "assessment": "Requires clinician assessment.",
                "plan": "Requires clinician input.",
            }

            st.session_state.approved = False
            st.session_state.consultations += 1

            st.success(
                "Draft template prepared. Verify all content "
                "against the transcript."
            )

            st.warning(
                "This is a template, not an AI-generated clinical "
                "interpretation. The source transcript has not been "
                "automatically analyzed."
            )

    st.caption(
        "Demo data is held in Streamlit session state. "
        "This is not secure clinical storage."
    )


# --------------------------------------------------
# REVIEW AND APPROVAL
# --------------------------------------------------
elif page == "Review Notes":

    st.title("📋 Review Clinical Note")

    draft = st.session_state.draft

    if draft is None:

        st.info(
            "No draft is available. Open New Consultation "
            "and enter a fictional transcript first."
        )

        if st.button("Go to New Consultation"):
            st.session_state.navigation = "New Consultation"
            st.rerun()

    else:

        st.warning(
            "Review every section. The draft is not a verified "
            "medical record and may contain unstructured source text."
        )

        with st.expander("View Original Transcript", expanded=True):
            st.write(draft["transcript"])

        st.markdown("### S — Subjective")

        subjective = st.text_area(
            "Patient-reported information",
            value=draft["subjective"],
            height=140,
            key="edit_subjective",
        )

        st.markdown("### O — Objective")

        objective = st.text_area(
            "Observed findings",
            value=draft["objective"],
            key="edit_objective",
        )

        st.markdown("### A — Assessment")

        assessment = st.text_area(
            "Clinical assessment",
            value=draft["assessment"],
            key="edit_assessment",
        )

        st.markdown("### P — Plan")

        plan = st.text_area(
            "Care plan",
            value=draft["plan"],
            key="edit_plan",
        )

        st.info(
            "Evidence linking, clinical fact extraction, and "
            "automatic uncertainty detection are not implemented yet."
        )

        if st.button(
            "Save Draft Changes",
            use_container_width=True,
        ):

            st.session_state.draft = {
                "transcript": draft["transcript"],
                "subjective": subjective,
                "objective": objective,
                "assessment": assessment,
                "plan": plan,
            }

            st.session_state.approved = False

            st.success(
                "Changes retained in this demo session only."
            )

        st.divider()

        reviewed = st.checkbox(
            "I have reviewed this fictional demo note.",
            key="review_confirmation",
        )

        if st.button(
            "Confirm Demo Review",
            type="primary",
            use_container_width=True,
        ):

            if reviewed:
                st.session_state.draft = {
                    "transcript": draft["transcript"],
                    "subjective": subjective,
                    "objective": objective,
                    "assessment": assessment,
                    "plan": plan,
                }

                st.session_state.approved = True

                st.success(
                    "Demo review confirmed for this session. "
                    "No official medical record was created."
                )

            else:
                st.error(
                    "Please confirm that you reviewed the note."
                )

        if st.session_state.approved:
            st.success("Status: Demo review confirmed")


# --------------------------------------------------
# END OF APPLICATION
# --------------------------------------------------
