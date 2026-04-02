import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Decision System",
    layout="wide",
    page_icon="🚀"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ---------- SESSION STATE ----------
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "history_data" not in st.session_state:
    st.session_state.history_data = []
if "history_error" not in st.session_state:
    st.session_state.history_error = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "dashboard_text" not in st.session_state:
    st.session_state.dashboard_text = ""


# ---------- API HELPERS ----------
def login_user(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/auth/login-json",
            json={
                "email": email,
                "password": password
            },
            timeout=10,
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
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=10)
def analyze_text_api_cached(text: str, token: str):
    response = requests.post(
        f"{API_URL}/cases/analyze-text",
        json={"text": text},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def load_history_into_state():
    try:
        history = fetch_history_cached(st.session_state.token)
        st.session_state.history_data = history
        st.session_state.history_error = None
    except requests.exceptions.ConnectionError:
        st.session_state.history_data = []
        st.session_state.history_error = "Backend is not running. Start FastAPI with: uvicorn app.main:app --reload"
    except requests.exceptions.HTTPError as e:
        st.session_state.history_data = []
        st.session_state.history_error = f"Failed to load history: {str(e)}"
    except Exception as e:
        st.session_state.history_data = []
        st.session_state.history_error = f"Failed to load history: {str(e)}"


def logout_user():
    st.session_state.token = None
    st.session_state.user_email = None
    st.session_state.history_data = []
    st.session_state.history_error = None
    st.session_state.analysis_result = None
    st.session_state.dashboard_text = ""
    fetch_history_cached.clear()
    analyze_text_api_cached.clear()
    st.rerun()


def set_demo_text():
    st.session_state.dashboard_text = (
        "Unauthorized transaction of $8000 on March 28. Customer claims fraud."
    )


# ---------- UI HELPERS ----------
def risk_badge(level: str):
    colors = {
        "high": "#ef4444",
        "medium": "#f59e0b",
        "low": "#22c55e"
    }
    return f"""
    <span style="
        background:{colors.get((level or '').lower(), '#64748b')};
        padding:6px 12px;
        border-radius:999px;
        color:white;
        font-weight:700;
        font-size:12px;
        display:inline-block;
        letter-spacing:0.3px;
    ">
        {(level or 'unknown').upper()}
    </span>
    """


def metric_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- STYLE ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.main {
    background: linear-gradient(180deg, #030712 0%, #07111f 100%);
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 1.2rem;
    max-width: 100%;
}

.header-container {
    padding: 22px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    box-shadow: 0 0 35px rgba(59,130,246,0.20);
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.08);
}

.header-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.2;
}

.header-subtitle {
    color: #cbd5f5;
    font-size: 14px;
    margin-top: 6px;
}

.metric-card {
    background: rgba(255,255,255,0.03);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 16px rgba(37,99,235,0.10);
    min-height: 110px;
}

.metric-title {
    color: #aab4c5;
    font-size: 13px;
}

.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin-top: 4px;
}

.metric-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 6px;
}

.section-card {
    background: rgba(255,255,255,0.03);
    padding: 16px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    margin-bottom: 14px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    font-weight: 600;
    border: none;
    height: 44px;
    font-size: 14px;
}

.stButton > button:hover {
    color: white;
}

div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------- LOGIN SCREEN ----------
if not st.session_state.token:
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🔐 AI Decision System Login</div>
        <div class="header-subtitle">
            Sign in to access fraud analysis, case history, and dashboard analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner("Logging in..."):
            result = login_user(email, password)

        if result and "access_token" in result:
            st.session_state.token = result["access_token"]
            st.session_state.user_email = result.get("email", email)
            fetch_history_cached.clear()
            load_history_into_state()
            st.success("Login successful")
            st.rerun()
        else:
            err = result.get("error") if isinstance(result, dict) else "Invalid credentials"
            st.error(f"Invalid credentials")
            st.caption(f"Debug: {err}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ---------- LOAD HISTORY ----------
if not st.session_state.history_data and st.session_state.history_error is None:
    load_history_into_state()


# ---------- HEADER ----------
h1, h2 = st.columns([0.82, 0.18])
with h1:
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🚀 Autonomous Risk & Decision Intelligence System</div>
        <div class="header-subtitle">
            AI-powered fraud detection, risk scoring, and decision intelligence platform
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"Logged in as: **{st.session_state.user_email}**")
    if st.button("Logout"):
        logout_user()

st.caption("Built with FastAPI • Streamlit • SQLite • JWT Auth")


# ---------- DATA ----------
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

# ---------- METRICS ----------
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Total Cases", str(total_cases), "Stored in database")
with m2:
    metric_card("High-Risk Cases", str(high_risk_cases), "Flagged for escalation")
with m3:
    metric_card("Avg Risk Score", str(avg_risk_score), "Across your saved cases")
with m4:
    metric_card("Latest Decision", latest_decision, "Most recent workflow outcome")

st.markdown("---")

# ---------- LAYOUT ----------
left_col, right_col = st.columns([1.2, 1], gap="large")

# ---------- LEFT ----------
with left_col:
    st.markdown("## 🔍 Analyze Case")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.text_area(
        "Enter case description",
        height=145,
        key="dashboard_text",
        placeholder="Example: Unauthorized transaction of $7000 detected on April 3. Suspicious activity reported by customer."
    )

    c1, c2 = st.columns([1, 1], gap="medium")
    analyze_clicked = c1.button("🚀 Analyze Case")
    c2.button("⚡ Use Demo Case", on_click=set_demo_text)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_clicked:
        if not st.session_state.dashboard_text.strip():
            st.warning("Please enter case text first.")
        else:
            try:
                result = analyze_text_api_cached(
                    st.session_state.dashboard_text,
                    st.session_state.token
                )
                st.session_state.analysis_result = result
                fetch_history_cached.clear()
                load_history_into_state()
                st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI with: uvicorn app.main:app --reload")
            except requests.exceptions.HTTPError as e:
                st.error(f"Backend returned an error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

    if st.session_state.analysis_result:
        data = st.session_state.analysis_result
        entities = data.get("entities", {})
        decision = data.get("fallback_decision", {})
        risk_level = entities.get("risk_level", "unknown")
        confidence = float(decision.get("confidence_score", 0) or 0)

        st.success("Analysis complete")

        st.markdown("### Executive Summary")
        st.markdown(
            f"""
            <div class="section-card">
                <div style="font-size:17px; color:white; font-weight:600;">
                    {data.get("summary", "No summary available")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
                unsafe_allow_html=True
            )

        st.markdown("### Confidence Score")
        st.progress(min(max(confidence, 0.0), 1.0))
        st.write(f"Confidence Score: **{confidence:.2f}**")

        tab1, tab2, tab3 = st.tabs(["Summary", "Entities", "Decision"])
        with tab1:
            st.write(data.get("summary", "No summary available"))
        with tab2:
            st.json(entities)
        with tab3:
            st.json(decision)

# ---------- RIGHT ----------
with right_col:
    st.markdown("## 📚 Case History")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    refresh_clicked = st.button("Refresh History")
    st.markdown('</div>', unsafe_allow_html=True)

    if refresh_clicked:
        fetch_history_cached.clear()
        load_history_into_state()
        st.rerun()

    if st.session_state.history_error:
        st.error(st.session_state.history_error)
    elif history_df.empty:
        st.info("No cases found yet. Analyze or upload a case first.")
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

        st.dataframe(history_df[preview_cols], use_container_width=True, height=250)

        latest = history_df.iloc[0].to_dict()
        st.markdown("### Most Recent Case")
        st.markdown(
            f"""
            <div class="section-card">
                <div><b>Case ID:</b> {latest.get("id", "N/A")}</div>
                <div><b>Filename:</b> {latest.get("filename", "N/A")}</div>
                <div><b>Summary:</b> {latest.get("summary", "N/A")}</div>
                <div><b>Decision:</b> {latest.get("decision", "N/A")}</div>
                <div style="margin-top:10px;">{risk_badge(latest.get("risk_level", "unknown"))}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if "risk_score" in history_df.columns and len(history_df) > 3:
            chart_df = history_df.copy()
            chart_df["risk_score"] = pd.to_numeric(chart_df["risk_score"], errors="coerce")

            fig = px.histogram(
                chart_df,
                x="risk_score",
                nbins=10,
                title="Risk Score Distribution"
            )
            fig.update_traces(marker_color="#3b82f6")
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=30, b=0),
                height=220,
            )
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#64748b; font-size:13px;">
        Built by Karthik Chalamalasetty • AI Decision Intelligence System • 2026
    </div>
    """,
    unsafe_allow_html=True
)