
from pathlib import Path
from datetime import datetime

import streamlit as st

# =========================================================
# ClinScribe AI — Premium Clinical Documentation Workspace
# Frontend prototype. Connect your team's backend API
# where indicated; do not treat demo drafts as AI-generated.
# =========================================================

st.set_page_config(
    page_title="ClinScribe AI | Clinical Workspace",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load stylesheet relative to this file
CSS_PATH = Path(__file__).parent / "styles.css"
if CSS_PATH.exists():
    st.markdown(
        f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

# ---------------- SESSION STATE ----------------
DEFAULTS = {
    "navigation": "Dashboard",
    "pending_navigation": None,
    "transcript": "",
    "soap": {
        "Subjective": "",
        "Objective": "",
        "Assessment": "",
        "Plan": "",
    },
    "draft_created": False,
    "review_confirmed": False,
    "saved_notes": [],
    "patient_id": "",
    "patient_name": "",
    "demo_mode": True,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.pending_navigation:
    st.session_state.navigation = st.session_state.pending_navigation
    st.session_state.pending_navigation = None


# ---------------- HELPERS ----------------
def navigate(page):
    st.session_state.pending_navigation = page
    st.rerun()


def section_heading(eyebrow, title, subtitle=""):
    st.markdown(
        f"""
        <div class="page-intro">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_title(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon, label, value, caption, style="blue"):
    st.markdown(
        f"""
        <div class="metric-card {style}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def demo_notice():
    st.info(
        "Prototype mode: sample values and draft content are for demonstration. "
        "Use verified backend output for actual transcription and AI generation."
    )


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✚</div>
            <div>
                <div class="brand-title">ClinScribe <span>AI</span></div>
                <div class="brand-subtitle">CLINICAL INTELLIGENCE</div>
            </div>
        </div>
        <div class="sidebar-label">WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )

    pages = [
        "Dashboard",
        "New Consultation",
        "Review Notes",
        "Patient History",
        "Settings",
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        key="navigation",
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-heart">♡</div>
            <b>Designed for better care</b>
            <p>Less paperwork. More time for patients.</p>
            <span class="prototype-status">● PROTOTYPE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- TOP BAR ----------------
top_left, top_right = st.columns([4, 1])

with top_left:
    st.markdown(
        """
        <div class="search-box">
            ✦ &nbsp; Clinical documentation workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown(
        """
        <div class="profile-box">
            <div class="avatar">CS</div>
            <div>
                <b>Clinical Team</b>
                <small>Workspace</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================
if selected_page == "Dashboard":

    left, right = st.columns([1.6, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="welcome">
                <div class="eyebrow">YOUR CLINICAL WORKSPACE</div>
                <h1>Clinical intelligence,<br>reimagined.</h1>
                <p>Transform consultations into structured documentation,
                with clinician review at every step.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "＋  Start a consultation",
            type="primary",
            use_container_width=False,
        ):
            navigate("New Consultation")

    with right:
        st.markdown(
            """
            <div class="hero-illustration">
                <div class="hero-document">▤</div>
                <div class="hero-heart">✦</div>
                <div class="hero-caption">
                    CLINICAL AI WORKSPACE<br>
                    Conversation to<br>structured documentation
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Prototype values are clearly labelled; replace with API data later.
    panel_title("Workspace overview", "Illustrative prototype metrics")

    m1, m2, m3, m4 = st.columns(4, gap="medium")

    with m1:
        metric_card("▣", "Consultations", "—", "Connect backend for live totals", "blue")
    with m2:
        metric_card("✧", "Draft notes", "—", "Pending documentation", "green")
    with m3:
        metric_card("✓", "Reviewed notes", "—", "Clinician review status", "purple")
    with m4:
        metric_card("◷", "Time saved", "—", "Requires validated usage data", "orange")

    panel_title("Your workflow", "Move from consultation to reviewed clinical notes")

    q1, q2, q3 = st.columns(3, gap="medium")

    with q1:
        st.markdown(
            """
            <div class="quick-card blue-card">
                <div class="quick-icon">🎙</div>
                <h3>Capture</h3>
                <p>Upload consultation audio or enter a transcript.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open consultation →", key="capture", use_container_width=True):
            navigate("New Consultation")

    with q2:
        st.markdown(
            """
            <div class="quick-card purple-card">
                <div class="quick-icon">✧</div>
                <h3>Structure</h3>
                <p>Organize clinical information into SOAP sections.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Review draft →", key="structure", use_container_width=True):
            navigate("Review Notes")

    with q3:
        st.markdown(
            """
            <div class="quick-card green-card">
                <div class="quick-icon">✓</div>
                <h3>Review</h3>
                <p>Check, edit and confirm notes before finalization.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View history →", key="history", use_container_width=True):
            navigate("Patient History")

    st.markdown(
        """
        <div class="bottom-banner">
            <div class="banner-icon">✚</div>
            <div>
                <b>Clinician remains in control</b>
                <p>AI-assisted documentation should be checked by a qualified
                clinician before use in patient care.</p>
            </div>
        </div>
        <div class="footer-note">
            ClinScribe AI · Clinical documentation prototype
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# NEW CONSULTATION
# =========================================================
elif selected_page == "New Consultation":

    section_heading(
        "CONSULTATION WORKSPACE",
        "New consultation",
        "Capture consultation information and prepare a structured clinical note.",
    )

    demo_notice()

    st.markdown(
        '<div class="safety-notice"><b>Privacy reminder</b><br>'
        'For this demonstration, use fictional patient information and '
        'approved sample audio only. Do not upload identifiable patient data '
        'unless your system is authorized to handle it.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        panel_title("01 · Consultation details", "Add basic details for this draft.")

        c1, c2 = st.columns(2)

        with c1:
            patient_name = st.text_input(
                "Patient label",
                value=st.session_state.patient_name,
                placeholder="e.g. Demo Patient 01",
            )

        with c2:
            patient_id = st.text_input(
                "Demo reference ID",
                value=st.session_state.patient_id,
                placeholder="e.g. DEMO-001",
            )

        st.session_state.patient_name = patient_name
        st.session_state.patient_id = patient_id

    with st.container(border=True):
        panel_title("02 · Audio or transcript", "Choose an input method.")

        input_method = st.radio(
            "Input method",
            ["Enter transcript", "Upload audio"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if input_method == "Upload audio":
            audio_file = st.file_uploader(
                "Upload sample consultation audio",
                type=["wav", "mp3", "m4a", "ogg", "mp4"],
                help="Audio upload is not transcription by itself. "
                     "Your backend must process this file.",
            )

            if audio_file is not None:
                st.audio(audio_file)
                st.caption(
                    f"Selected file: {audio_file.name}. "
                    "Connect your team's transcription endpoint to process it."
                )

                st.warning(
                    "Audio preview is available. This frontend code does not "
                    "transcribe the recording without a connected backend."
                )

        else:
            transcript_value = st.text_area(
                "Consultation transcript",
                value=st.session_state.transcript,
                height=230,
                placeholder=(
                    "Paste a fictional sample consultation transcript here..."
                ),
                help="Use approved sample content for your presentation.",
            )
            st.session_state.transcript = transcript_value

    st.write("")

    generate_col, clear_col = st.columns([2, 1])

    with generate_col:
        if st.button(
            "✧  Prepare SOAP draft",
            type="primary",
            use_container_width=True,
        ):
            if not st.session_state.transcript.strip():
                st.warning(
                    "Enter a transcript first. Audio transcription requires "
                    "the connected backend."
                )
            else:
                # This action opens an editable template.
                # It deliberately does NOT claim to generate AI output.
                st.session_state.soap = {
                    "Subjective": "",
                    "Objective": "",
                    "Assessment": "",
                    "Plan": "",
                }
                st.session_state.draft_created = True
                st.session_state.review_confirmed = False
                st.session_state.pending_navigation = "Review Notes"
                st.rerun()

    with clear_col:
        if st.button("Clear transcript", use_container_width=True):
            st.session_state.transcript = ""
            st.session_state.draft_created = False
            st.rerun()

    st.caption(
        "Connect this button to your friend's actual SOAP-generation endpoint "
        "before describing the draft as AI-generated."
    )


# =========================================================
# REVIEW NOTES
# =========================================================
elif selected_page == "Review Notes":

    section_heading(
        "CLINICAL DOCUMENTATION",
        "Review notes",
        "Edit each SOAP section and confirm the draft only after reviewing it.",
    )

    if not st.session_state.draft_created:
        st.info(
            "No draft is open yet. Start a consultation to create a review template."
        )

        if st.button("＋ Start consultation", type="primary"):
            navigate("New Consultation")

    else:
        st.markdown(
            f"""
            <div class="surface-card">
                <div class="eyebrow">DRAFT WORKSPACE</div>
                <h3>{st.session_state.patient_name or "Demo patient"}</h3>
                <p>Reference: {st.session_state.patient_id or "Not provided"}</p>
                <span class="status-pill">● Awaiting clinician review</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        demo_notice()

        with st.form("soap_review_form"):
            st.markdown("### S · Subjective")
            subjective = st.text_area(
                "Reported symptoms and patient history",
                value=st.session_state.soap["Subjective"],
                height=120,
            )

            st.markdown("### O · Objective")
            objective = st.text_area(
                "Observed findings and measurements",
                value=st.session_state.soap["Objective"],
                height=120,
            )

            st.markdown("### A · Assessment")
            assessment = st.text_area(
                "Clinical assessment for clinician verification",
                value=st.session_state.soap["Assessment"],
                height=120,
            )

            st.markdown("### P · Plan")
            plan = st.text_area(
                "Proposed next steps for clinician review",
                value=st.session_state.soap["Plan"],
                height=120,
            )

            save_draft = st.form_submit_button(
                "Save draft changes",
                use_container_width=True,
            )

        if save_draft:
            st.session_state.soap = {
                "Subjective": subjective,
                "Objective": objective,
                "Assessment": assessment,
                "Plan": plan,
            }
            st.session_state.review_confirmed = False
            st.success("Draft changes saved in this session.")

        st.write("")

        if st.button(
            "✓  Confirm review",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.review_confirmed = True
            st.session_state.saved_notes.append(
                {
                    "patient": st.session_state.patient_name or "Demo patient",
                    "reference": st.session_state.patient_id or "Not provided",
                    "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "soap": st.session_state.soap.copy(),
                }
            )
            st.success(
                "Review confirmed for this prototype session. "
                "This is not a permanent backend save."
            )

        if st.session_state.review_confirmed:
            st.success("Review status: confirmed in the current session.")

        st.caption(
            "This prototype stores changes in Streamlit session state only. "
            "Connect your backend to persist records securely."
        )


# =========================================================
# PATIENT HISTORY
# =========================================================
elif selected_page == "Patient History":

    section_heading(
        "RECORDS WORKSPACE",
        "Consultation history",
        "Review notes created during this current demo session.",
    )

    st.markdown(
        '<div class="safety-notice"><b>Demo data only</b><br>'
        'This page displays session records, not a connected medical record system.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.saved_notes:
        st.info(
            "No reviewed notes in this session yet. Create and review a draft "
            "to see it listed here."
        )
    else:
        for index, record in enumerate(
            reversed(st.session_state.saved_notes), start=1
        ):
            with st.expander(
                f"{index}. {record['patient']} · {record['reviewed_at']}"
            ):
                st.write(f"Reference: {record['reference']}")

                for heading, content in record["soap"].items():
                    st.markdown(f"**{heading}**")
                    st.write(content or "No content entered.")


# =========================================================
# SETTINGS
# =========================================================
elif selected_page == "Settings":

    section_heading(
        "WORKSPACE CONFIGURATION",
        "Settings",
        "Review the current frontend prototype configuration.",
    )

    with st.container(border=True):
        st.markdown("### Workspace")

        st.text_input(
            "Application name",
            value="ClinScribe AI",
            disabled=True,
        )

        st.text_input(
            "Frontend framework",
            value="Streamlit",
            disabled=True,
        )

        st.text_input(
            "Current mode",
            value="Frontend prototype",
            disabled=True,
        )

    with st.container(border=True):
        st.markdown("### Integration status")

        st.warning(
            "Backend integration is not verified by this frontend file. "
            "Check the actual API connection before presenting transcription "
            "or SOAP generation as working features."
        )

        st.markdown(
            """
            **Integration checklist**
            - Audio file is sent to the backend transcription endpoint.
            - Transcription response is shown in the consultation form.
            - Transcript is sent to the SOAP-generation endpoint.
            - Returned SOAP fields populate the review editor.
            - Save/review actions persist through the authorized backend.
            """
        )

    st.caption(
        "Do not store API keys in this file. Use environment variables or "
        "your team's approved secrets configuration."
    )
