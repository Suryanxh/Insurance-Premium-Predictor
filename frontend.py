import streamlit as st
import requests

API_URL = " http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(160deg, #F4F7FE 0%, #EEF2FF 45%, #E8F7F5 100%);
        color: #1E293B;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 820px;}

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 55%, #0EA5A4 100%);
        border-radius: 22px;
        padding: 2.2rem 2rem;
        color: #fff;
        text-align: center;
        box-shadow: 0 18px 40px rgba(79, 70, 229, 0.28);
        margin-bottom: 1.6rem;
    }
    .hero h1 {font-size: 2rem; font-weight: 800; margin: 0 0 .4rem 0; color: #fff;}
    .hero p  {font-size: 1rem; margin: 0; opacity: .92; color: #fff;}

    /* Section cards */
    .section-title {
        font-size: 1.05rem; font-weight: 700; color: #3730A3;
        margin: 0 0 .2rem 0;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border-radius: 18px;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    /* Inputs */
    label, .stMarkdown p {color: #334155;}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        background: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="select"]:focus-within > div {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, .18) !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: .85rem 1rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: #fff;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        box-shadow: 0 10px 22px rgba(79, 70, 229, .35);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(79, 70, 229, .45);
        color: #fff;
    }
    .stButton > button:active {transform: translateY(0);}

    /* Result */
    .result-card {
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        color: #fff;
        box-shadow: 0 16px 34px rgba(0,0,0,.14);
        margin: 1rem 0 .8rem 0;
    }
    .result-card .label {font-size: .85rem; letter-spacing: .12em; text-transform: uppercase; opacity: .9; color:#fff;}
    .result-card .value {font-size: 2.6rem; font-weight: 800; margin: .2rem 0; color:#fff;}
    .result-card .conf  {font-size: 1rem; opacity: .95; color:#fff;}

    /* Metric chips */
    .chips {display: flex; gap: .75rem; flex-wrap: wrap; margin: .4rem 0 .2rem 0;}
    .chip {
        flex: 1 1 140px;
        background: #EEF2FF; border-radius: 14px; padding: .8rem 1rem;
        border: 1px solid #E0E7FF;
    }
    .chip .k {font-size: .75rem; color: #64748B; text-transform: uppercase; letter-spacing: .06em;}
    .chip .v {font-size: 1.25rem; font-weight: 700; color: #3730A3;}

    /* Probability bars */
    .bar-row {margin: .55rem 0;}
    .bar-top {display: flex; justify-content: space-between; font-weight: 600; font-size: .92rem; color: #334155;}
    .bar-bg {background: #E2E8F0; border-radius: 999px; height: 10px; overflow: hidden; margin-top: .25rem;}
    .bar-fill {height: 100%; border-radius: 999px;}

    .footer-note {text-align:center; color:#94A3B8; font-size:.8rem; margin-top:1.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
CATEGORY_STYLES = {
    "low":    ("linear-gradient(135deg,#059669,#10B981)", "#10B981", "🟢"),
    "medium": ("linear-gradient(135deg,#D97706,#F59E0B)", "#F59E0B", "🟡"),
    "high":   ("linear-gradient(135deg,#DC2626,#F43F5E)", "#F43F5E", "🔴"),
}
DEFAULT_STYLE = ("linear-gradient(135deg,#4F46E5,#7C3AED)", "#6366F1", "🔵")


def style_for(category: str):
    return CATEGORY_STYLES.get(str(category).strip().lower(), DEFAULT_STYLE)


def bmi_label(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>🛡️ Insurance Premium Predictor</h1>
        <p>Fill in your details and get an instant premium category estimate.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Form ----------
with st.container(border=True):
    st.markdown('<p class="section-title">👤 Personal details</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30)
        weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
    with c2:
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01)
        smoker = st.selectbox(
            "Are you a smoker?",
            options=[True, False],
            index=1,
            format_func=lambda x: "🚬 Yes" if x else "🚭 No",
        )

with st.container(border=True):
    st.markdown('<p class="section-title">💼 Work & location</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
        city = st.text_input("City", value="Mumbai")
    with c4:
        occupation = st.selectbox(
            "Occupation",
            ["retired", "freelancer", "student", "government_job",
             "business_owner", "unemployed", "private_job"],
            index=6,
            format_func=lambda x: x.replace("_", " ").title(),
        )

# Live BMI preview
bmi = weight / (height ** 2)
st.markdown(
    f"""
    <div class="chips">
        <div class="chip"><div class="k">Your BMI</div><div class="v">{bmi:.1f}</div></div>
        <div class="chip"><div class="k">Category</div><div class="v">{bmi_label(bmi)}</div></div>
        <div class="chip"><div class="k">Smoker</div><div class="v">{"Yes" if smoker else "No"}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
predict = st.button("✨ Predict Premium Category")

# ---------- Prediction ----------
if predict:
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation,
    }

    try:
        with st.spinner("Analysing your profile..."):
            response = requests.post(API_URL, json=input_data, timeout=15)
        try:
            result = response.json()
        except ValueError:
            result = {"detail": response.text}

        prediction = result.get("response", result) if isinstance(result, dict) else {}
        if response.status_code == 200 and "predicted_category" in prediction:
            category = prediction["predicted_category"]
            confidence = prediction.get("confidence")
            probs = prediction.get("class_probabilities") or {}

            gradient, bar_color, icon = style_for(category)

            conf_html = ""
            if confidence is not None:
                try:
                    conf_text = f"{float(confidence) * 100:.1f}%" if float(confidence) <= 1 else f"{float(confidence):.1f}%"
                except (TypeError, ValueError):
                    conf_text = str(confidence)
                conf_html = f'<div class="conf">Confidence: <b>{conf_text}</b></div>'

            st.markdown(
                f"""
                <div class="result-card" style="background:{gradient};">
                    <div class="label">Predicted premium category</div>
                    <div class="value">{icon} {str(category).title()}</div>
                    {conf_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

            if probs:
                with st.container(border=True):
                    st.markdown('<p class="section-title">📊 Class probabilities</p>', unsafe_allow_html=True)
                    for name, p in sorted(probs.items(), key=lambda kv: kv[1], reverse=True):
                        try:
                            pct = float(p) * 100 if float(p) <= 1 else float(p)
                        except (TypeError, ValueError):
                            pct = 0.0
                        _, color, _ = style_for(name)
                        st.markdown(
                            f"""
                            <div class="bar-row">
                                <div class="bar-top"><span>{str(name).title()}</span><span>{pct:.1f}%</span></div>
                                <div class="bar-bg"><div class="bar-fill" style="width:{min(pct,100):.1f}%; background:{color};"></div></div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
    except requests.exceptions.Timeout:
        st.error("⏱️ The server took too long to respond. Please try again.")

st.markdown(
    '<p class="footer-note">Predictions are estimates and not an official insurance quote.</p>',
    unsafe_allow_html=True,
)