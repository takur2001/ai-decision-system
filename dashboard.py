import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision System",
    layout="wide",
    page_icon="🚀"
)

# ---------------- CONFIG ----------------
API_URL = st.secrets.get(
    "API_URL",
    os.getenv("API_URL", "https://ai-decision-system-mw63.onrender.com")
)

REQUEST_TIMEOUT = 60


# ---------------- SESSION STATE ----------------
DEFAULT_SESSION_VALUES = {
    "token": None,
    "user_email": None,
    "history_data": [],
    "history_error": None,
    "analysis_result": None,
    "dashboard_text": "",
}

for key, value in DEFAULT_SESSION_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- STYLES ----------------
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #030712 0%, #081120 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
        max-width: 100%;
    }

    .header-container {
        padding: 24px;
        border-radius: 20px;
        background: linear-gradient(135deg, #0f172a, #1d4ed8);
        box-shadow: 0 0 30px rgba(59,130,246,0.18);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 14px;
    }

    .header-title {
        color: white;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.2;
    }

    .header-subtitle {
        color: #dbeafe;
        font-size: 14px;
        margin-top: 8px;
    }

    .metric-card {
        background: rgba(255,255,255,0.03);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        min-height: 110px;
    }

    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: white;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-subtitle {
        color: #64748b;
        font-size: 12px;
        margin-top: 8px;
    }

    .section-card {
        background: rgba(255,255,255,0.03);
        padding: 16px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 20px rgba(0,0,0,0.16);
        margin-bottom: 14px;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 13px;
    }

    .case-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        font-weight: 700;
        border: none;
        height: 46px;
        font-size: 14px;
        box-shadow: 0 10px 22px rgba(37,99,235,0.28);
    }

    .stButton > button:hover {
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(37,99,235,0.35);
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 12px;
    }

    .risk-pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- HELPERS ----------------
def risk_badge(level: str) -> str:
    level = (level or "unknown").lower()
    colors = {
        "high": "#ef4444",
        "medium": "#f59e0b",
        "low": "#22c55e",
        "unknown": "#64748b",
    }
    return (
        f'<span class="risk-pill" style="background:{colors.get(level, "#64748b")};">'
        f"{level.upper()}</span>"
    )


def metric_card(title: str, value: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def logout_user() -> None:
    for key, value in DEFAULT_SESSION_VALUES.items():
        st.session_state[key] = value
    fetch_history_cached.clear()
    analyze_text_api_cached.clear()
    st.rerun()


def set_demo_text() -> None:
    st.session_state.dashboard_text = (
        "Unauthorized transaction of $8000 on March 28. "
        "Customer claims fraud and requests urgent review."
    )


def check_backend() -> bool:
    try:
        response = requests.get(f"{API_URL}/", timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except Exception:
        return False


def login_user(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/auth/login-json",
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            return response.json()

        try:
            return {"error": response.json()}
        except Exception:
            return {"error": response.text}

    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=30)
def fetch_history_cached(token: str):
    response = requests.get(
        f"{API_URL}/cases/history",
        headers={"Authorization": f"Bearer {token}"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=10)
def analyze_text_api_cached(text: str, token: str):
    response = requests.post(
        f"{API_URL}/cases/analyze-text",
        json={"text": text},
        headers={"Authorization": f"Bearer {token}"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def load_history_into_state() -> None:
    try:
        st.session_state.history_data = fetch_history_cached(st.session_state.token)
        st.session_state.history_error = None
    except requests.exceptions.ConnectionError:
        st.session_state.history_data = []
        st.session_state.history_error = (
            "Backend is not reachable right now. "
            "If you are using Render free tier, wait for it to wake up and try again."
        )
    except requests.exceptions.HTTPError as e:
        st.session_state.history_data = []
        st.session_state.history_error = f"Failed to load history: {e}"
    except Exception as e:
        st.session_state.history_data = []
        st.session_state.history_error = f"Failed to load history: {e}"


# ---------------- LOGIN SCREEN ----------------
if not st.session_state.token:
    st.markdown(
        """
        <div class="header-container">
            <div class="header-title">🔐 AI Decision System Login</div>
            <div class="header-subtitle">
                Sign in to access fraud analysis, case history, and dashboard analytics.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    backend_ok = check_backend()
    if backend_ok:
        st.success("Backend connected")
    else:
        st.warning("Backend waking up or temporarily unavailable. If using Render free tier, wait 30–60 seconds and try again.")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner("Signing in..."):
            result = login_user(email, password)

        if result and "access_token" in result:
            st.session_state.token = result["access_token"]
            st.session_state.user_email = result.get("email", email)
            fetch_history_cached.clear()
            load_history_into_state()
            st.success("Login successful")
            st.rerun()
        else:
            err = result.get("error") if isinstance(result, dict) else "Login failed"

            if "Read timed out" in str(err):
                st.warning("Backend is waking up on Render. Wait 30–60 seconds and click Login again.")
            elif "127.0.0.1" in str(err):
                st.error("Frontend is still pointing to localhost. Update API_URL to your deployed backend URL.")
            else:
                st.error("Invalid credentials")
                st.caption(f"Debug: {err}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ---------------- MAIN APP ----------------
if not st.session_state.history_data and st.session_state.history_error is None:
    load_history_into_state()

backend_ok = check_backend()

# Header
head_left, head_right = st.columns([0.82, 0.18])
with head_left:
    st.markdown(
        """
        <div class="header-container">
            <div class="header-title">🚀 Autonomous Risk & Decision Intelligence System</div>
            <div class="header-subtitle">
                AI-powered fraud detection, risk scoring, secure decision intelligence, and user-specific case tracking
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with head_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"Logged in as: **{st.session_state.user_email}**")
    if st.button("Logout"):
        logout_user()

meta_left, meta_right = st.columns([0.75, 0.25])
with meta_left:
    st.caption("Built with FastAPI • Streamlit • JWT Auth • Render Deployment")
with meta_right:
    if backend_ok:
        st.success("Backend connected")
    else:
        st.warning("Backend waking up or unavailable")

history_df = pd.DataFrame(st.session_state.history_data) if st.session_state.history_data else pd.DataFrame()

total_cases = len(history_df) if not history_df.empty else 0
high_risk_cases = (
    int((history_df["risk_level"].fillna("").str.lower() == "high").sum())
    if not history_df.empty and "risk_level" in history_df.columns
    else 0
)
avg_risk_score = (
    round(pd.to_numeric(history_df["risk_score"], errors="coerce").mean(), 2)
    if not history_df.empty and "risk_score" in history_df.columns
    else 0.0
)
latest_decision = (
    str(history_df.iloc[0]["decision"])
    if not history_df.empty and "decision" in history_df.columns
    else "No cases yet"
)

# Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Total Cases", str(total_cases), "User-specific cases stored")
with m2:
    metric_card("High-Risk Cases", str(high_risk_cases), "Flagged for escalation")
with m3:
    metric_card("Avg Risk Score", str(avg_risk_score), "Average model/rule score")
with m4:
    metric_card("Latest Decision", latest_decision, "Most recent workflow output")

st.markdown("---")

left_col, right_col = st.columns([1.2, 1], gap="large")

# ---------------- LEFT COLUMN ----------------
with left_col:
    st.markdown("## 🔎 Analyze Case")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.text_area(
        "Enter case description",
        height=150,
        key="dashboard_text",
        placeholder="Example: Unauthorized transaction of $7000 detected on April 3. Suspicious activity reported by customer.",
    )

    btn1, btn2 = st.columns([1, 1], gap="medium")
    analyze_clicked = btn1.button("🚀 Analyze Case")
    btn2.button("⚡ Use Demo Case", on_click=set_demo_text)
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        if not st.session_state.dashboard_text.strip():
            st.warning("Please enter case text first.")
        else:
            try:
                with st.spinner("Analyzing case..."):
                    result = analyze_text_api_cached(
                        st.session_state.dashboard_text,
                        st.session_state.token,
                    )
                st.session_state.analysis_result = result
                fetch_history_cached.clear()
                load_history_into_state()
                st.success("Analysis complete")
                st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("Backend is not reachable right now.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Backend returned an error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    if st.session_state.analysis_result:
        data = st.session_state.analysis_result
        entities = data.get("entities", {})
        decision = data.get("fallback_decision", {})
        risk_level = entities.get("risk_level", "unknown")
        confidence = float(decision.get("confidence_score", 0) or 0)

        st.markdown("### Executive Summary")
        st.info(data.get("summary", "No summary available"))

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Amount", str(entities.get("amount", "N/A")), "Detected transaction value")
        with c2:
            metric_card("Date", str(entities.get("date", "N/A")), "Detected case date")
        with c3:
            metric_card("Issue Type", str(entities.get("issue_type", "N/A")).title(), "Classification result")
        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Risk Level</div>
                    <div style="margin-top:14px;">{risk_badge(risk_level)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if data.get("llm_status") == "available":
            st.success("LLM analysis available")
        else:
            st.info("LLM analysis is currently unavailable. Showing fallback rule-engine output.")

        st.markdown("### Confidence Score")
        st.progress(min(max(confidence, 0.0), 1.0))
        st.write(f"Confidence Score: **{confidence:.2f}**")

        tab1, tab2, tab3 = st.tabs(["Summary", "Entities", "Decision"])

        with tab1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.write(data.get("summary", "No summary available"))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.json(entities)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.json(decision)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("View Full API Response"):
            st.json(data)

# ---------------- RIGHT COLUMN ----------------
with right_col:
    st.markdown("## 📚 Case History")

    refresh_col1, refresh_col2 = st.columns([1, 3])
    with refresh_col1:
        refresh_clicked = st.button("Refresh History")

    if refresh_clicked:
        fetch_history_cached.clear()
        load_history_into_state()
        st.rerun()

    if st.session_state.history_error:
        st.error(st.session_state.history_error)

    elif history_df.empty:
        st.info("No cases found yet. Use the demo case or analyze your first case.")

    else:
        preview_cols = [
            col for col in [
                "id",
                "filename",
                "issue_type",
                "risk_level",
                "risk_score",
                "confidence_score",
                "decision",
            ] if col in history_df.columns
        ]

        st.dataframe(
            history_df[preview_cols],
            use_container_width=True,
            height=240,
        )

        st.markdown("### Most Recent Case")
        latest = history_df.iloc[0].to_dict()

        st.markdown(
            f"""
            <div class="case-box">
                <div><b>Case ID:</b> {latest.get("id", "N/A")}</div>
                <div><b>Filename:</b> {latest.get("filename", "N/A")}</div>
                <div><b>Summary:</b> {latest.get("summary", "N/A")}</div>
                <div><b>Decision:</b> {latest.get("decision", "N/A")}</div>
                <div style="margin-top:10px;">{risk_badge(latest.get("risk_level", "unknown"))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "risk_score" in history_df.columns and len(history_df) > 0:
            chart_df = history_df.copy()
            chart_df["risk_score"] = pd.to_numeric(chart_df["risk_score"], errors="coerce")

            fig_hist = px.histogram(
                chart_df,
                x="risk_score",
                nbins=10,
                title="Risk Score Distribution"
            )
            fig_hist.update_traces(marker_color="#3b82f6")
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=40, b=0),
                height=250,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        if "issue_type" in history_df.columns:
            issue_counts = history_df["issue_type"].fillna("unknown").value_counts().reset_index()
            issue_counts.columns = ["issue_type", "count"]

            fig_issue = px.bar(
                issue_counts,
                x="issue_type",
                y="count",
                title="Issue Type Distribution"
            )
            fig_issue.update_traces(marker_color="#22c55e")
            fig_issue.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=40, b=0),
                height=260,
            )
            st.plotly_chart(fig_issue, use_container_width=True)

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#64748b; font-size:13px;">
        Built by Karthik • AI Decision Intelligence System • 2026
    </div>
    """,
    unsafe_allow_html=True,
)