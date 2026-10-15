from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="ClinScribe AI | Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state defaults
defaults = {
    "navigation": "Dashboard",
    "pending_navigation": None,
    "draft": None,
    "approved": False,
    "consultations": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Apply navigation changes BEFORE creating the radio widget
pending = st.session_state.pending_navigation
if pending:
    st.session_state.navigation = pending
    st.session_state.pending_navigation = None

# Load CSS
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def navigate_to(page):
    st.session_state.pending_navigation = page


# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✚</div>
            <div>
                <div class="brand-title">ClinScribe <span>AI</span></div>
                <div class="brand-subtitle">Smarter Notes. Better Care.</div>
            </div>
        </div>
        <div class="sidebar-label">WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "New Consultation",
            "Review Notes",
            "Patient History",
            "Settings",
        ],
        key="navigation",
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-heart">♡</div>
            <b>AI-powered documentation</b>
            <p>Save time. Focus on care.</p>
            <span class="prototype-status">● Prototype mode</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Header
left, right = st.columns([3, 1], vertical_alignment="center")

with left:
    st.markdown(
        '<div class="search-box">⌕ &nbsp; Search patients, reports, or keywords...</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="profile-box">
            <span class="avatar">D</span>
            <div><b>Clinician Workspace</b><small>Demo account</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    hero, illustration = st.columns([2, 1])

    with hero:
        st.markdown(
            """
            <div class="welcome">
                <span class="eyebrow">CLINICAL WORKSPACE</span>
                <h1>Welcome to your workspace ✨</h1>
                <p>Spend less time on paperwork and more time focusing on care.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with illustration:
        st.markdown(
            """
            <div class="hero-illustration">
                <div class="hero-document">▤</div>
                <div class="hero-heart">♡</div>
                <div class="hero-caption">From consultation<br>to structured notes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    metrics = [
        ("Total Consultations", st.session_state.consultations, "▤", "blue"),
        ("Draft Notes", int(st.session_state.draft is not None), "✎", "green"),
        ("Reviews Confirmed", int(st.session_state.approved), "✓", "purple"),
        ("AI Integration", "Pending", "✦", "orange"),
    ]

    cols = st.columns(4)
    for col, (label, value, icon, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card {color}">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-caption">Current demo session</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="section-title">
            <h2>Your workspace</h2>
            <p>Everything you need to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    activity, recent = st.columns([1.4, 1], gap="large")

    with activity:
        st.markdown(
            f"""
            <div class="surface-card">
                <h3>📊 Consultation activity</h3>
                <p class="muted">Current browser session</p>
                <div class="activity-number">
                    {st.session_state.consultations}
                    <small>consultations</small>
                </div>
                <div class="activity-bars">
                    <i style="height:28%"></i>
                    <i style="height:42%"></i>
                    <i style="height:35%"></i>
                    <i style="height:65%"></i>
                    <i style="height:48%"></i>
                    <i style="height:82%"></i>
                </div>
                <p class="small-note">Illustrative chart — not historical analytics.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with recent:
        has_draft = st.session_state.draft is not None
        status = (
            "Review confirmed"
            if st.session_state.approved
            else "Review required"
            if has_draft
            else "Ready to start"
        )

        st.markdown(
            f"""
            <div class="surface-card recent-card">
                <h3>📄 Recent activity</h3>
                <p class="muted">Workspace overview</p>
                <div class="recent-document">✎</div>
                <b>{"Clinical note draft" if has_draft else "No draft yet"}</b>
                <p class="muted">
                    {"A draft is ready for review." if has_draft else "Start a consultation to create your first draft."}
                </p>
                <div class="status-pill">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-title">
            <h2>Quick actions</h2>
            <p>Jump straight into your next task.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3, gap="medium")

    with a:
        st.markdown(
            """
            <div class="quick-card blue-card">
                <div class="quick-icon">＋</div>
                <h3>New consultation</h3>
                <p>Enter a fictional transcript and prepare a draft.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Start consultation →",
            type="primary",
            use_container_width=True,
            on_click=navigate_to,
            args=("New Consultation",),
        )

    with b:
        st.markdown(
            """
            <div class="quick-card purple-card">
                <div class="quick-icon">▤</div>
                <h3>Review notes</h3>
                <p>Edit SOAP sections before confirming your review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Review notes →",
            use_container_width=True,
            on_click=navigate_to,
            args=("Review Notes",),
        )

    with c:
        st.markdown(
            """
            <div class="quick-card green-card">
                <div class="quick-icon">♡</div>
                <h3>Patient history</h3>
                <p>Check the current prototype session status.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "View history →",
            use_container_width=True,
            on_click=navigate_to,
            args=("Patient History",),
        )

    st.markdown(
        """
        <div class="bottom-banner">
            <div class="banner-icon">✦</div>
            <div>
                <b>Better documentation. Better healthcare.</b>
                <p>Structured drafts that support clinician judgment.</p>
            </div>
        </div>
        <div class="footer-note">
            ClinScribe AI · Hackathon prototype · Use fictional data only
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- NEW CONSULTATION ----------------
elif page == "New Consultation":
    st.markdown(
        """
        <div class="page-intro">
            <span class="eyebrow">WORKSPACE / NEW CONSULTATION</span>
            <h1>Create a consultation draft</h1>
            <p>Enter a fictional transcript to prepare a draft for review.</p>
        </div>
        <div class="safety-notice">
            <b>Prototype notice</b><br>
            AI medical interpretation and speech recognition are not connected.
            Use fictional data only.
        </div>
        """,
        unsafe_allow_html=True,
    )

    consent = st.checkbox(
        "I confirm appropriate consent for this fictional demo."
    )

    st.markdown(
        """
        <div class="surface-card form-card">
            <h3>01 · Audio sample</h3>
            <p>Optional preview only; audio is not transcribed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audio = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "m4a", "ogg"],
    )

    if audio:
        st.audio(audio)
        st.caption("Preview only — speech recognition is not connected.")

    st.markdown(
        """
        <div class="surface-card form-card">
            <h3>02 · Transcript</h3>
            <p>Use fictional text for this demo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    transcript = st.text_area(
        "Consultation transcript",
        height=210,
        placeholder=(
            "Doctor: What brings you in today?\n"
            "Patient: I have had a headache for two days.\n"
            "Doctor: Do you have a fever?\n"
            "Patient: No, I do not have a fever."
        ),
        label_visibility="collapsed",
    )

    if st.button(
        "Prepare draft note →",
        type="primary",
        use_container_width=True,
    ):
        if not consent:
            st.error("Please confirm consent first.")
        elif not transcript.strip():
            st.error("Please enter a fictional transcript.")
        else:
            st.session_state.draft = {
                "transcript": transcript.strip(),
                "subjective": transcript.strip(),
                "objective": "Not provided in the transcript.",
                "assessment": "Requires clinician assessment.",
                "plan": "Requires clinician input.",
            }
            st.session_state.consultations += 1
            st.session_state.approved = False
            navigate_to("Review Notes")
            st.rerun()

# ---------------- REVIEW NOTES ----------------
elif page == "Review Notes":
    st.markdown(
        """
        <div class="page-intro">
            <span class="eyebrow">WORKSPACE / NOTE REVIEW</span>
            <h1>Review clinical note</h1>
            <p>Inspect and edit each SOAP section.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    draft = st.session_state.draft

    if not draft:
        st.info("No draft yet. Create a new consultation first.")
        st.button(
            "Go to consultation →",
            type="primary",
            on_click=navigate_to,
            args=("New Consultation",),
        )
    else:
        st.warning(
            "Review all sections carefully. This is a demo template, "
            "not a verified medical record."
        )

        with st.expander("View original transcript", expanded=True):
            st.write(draft["transcript"])

        with st.form("soap_review_form"):
            subjective = st.text_area(
                "S · Subjective",
                value=draft["subjective"],
                height=120,
            )
            objective = st.text_area(
                "O · Objective",
                value=draft["objective"],
                height=90,
            )
            assessment = st.text_area(
                "A · Assessment",
                value=draft["assessment"],
                height=90,
            )
            plan = st.text_area(
                "P · Plan",
                value=draft["plan"],
                height=90,
            )

            save = st.form_submit_button(
                "Save draft changes",
                use_container_width=True,
            )

        if save:
            st.session_state.draft = {
                "transcript": draft["transcript"],
                "subjective": subjective,
                "objective": objective,
                "assessment": assessment,
                "plan": plan,
            }
            st.session_state.approved = False
            st.success("Draft changes saved in this session.")
            st.rerun()

        reviewed = st.checkbox(
            "I have reviewed this fictional demo note."
        )

        if st.button(
            "Confirm demo review",
            type="primary",
            use_container_width=True,
        ):
            if reviewed:
                st.session_state.approved = True
                st.success(
                    "Demo review confirmed. No official record created."
                )
            else:
                st.error("Please confirm that you reviewed the note.")

        if st.session_state.approved:
            st.markdown(
                '<div class="status-pill">✓ Demo review confirmed</div>',
                unsafe_allow_html=True,
            )

# ---------------- PATIENT HISTORY ----------------
elif page == "Patient History":
    st.markdown(
        """
        <div class="page-intro">
            <span class="eyebrow">WORKSPACE / HISTORY</span>
            <h1>Session history</h1>
            <p>Prototype status only; no patient records are stored.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    x, y, z = st.columns(3)
    x.metric("Consultations", st.session_state.consultations)
    y.metric(
        "Draft available",
        "Yes" if st.session_state.draft else "No",
    )
    z.metric(
        "Demo review",
        "Confirmed" if st.session_state.approved else "Pending",
    )

    st.info(
        "This prototype uses session state and is not persistent storage."
    )

# ---------------- SETTINGS ----------------
elif page == "Settings":
    st.markdown(
        """
        <div class="page-intro">
            <span class="eyebrow">WORKSPACE / SETTINGS</span>
            <h1>Settings</h1>
            <p>Current prototype capabilities.</p>
        </div>
        <div class="surface-card">
            <h3>Application status</h3>
            <p>AI interpretation: Not connected</p>
            <p>Speech recognition: Not connected</p>
            <p>Storage: Current Streamlit session only</p>
            <p>Clinical use: Not supported</p>
        </div>
        """,
        unsafe_allow_html=True,
    )