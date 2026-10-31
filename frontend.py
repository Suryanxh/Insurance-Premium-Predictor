import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #F5F6FA;
    color: #1E293B;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    max-width: 780px;
}

/* ── Hero banner ── */
.hero {
    background: #4F46E5;
    border-radius: 16px;
    padding: 2rem 1.5rem 1.8rem;
    text-align: center;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 1.75rem; font-weight: 800;
    color: #fff; margin: 0 0 .4rem;
}
.hero p {
    font-size: .95rem; color: rgba(255,255,255,.85); margin: 0;
}

/* ── White cards ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fff !important;
    border-radius: 16px !important;
    border: 1.5px solid #E8ECF4 !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── Section titles ── */
.sec-title {
    font-size: 1rem; font-weight: 700; color: #4F46E5;
    margin: 0 0 .8rem; display: flex; align-items: center; gap: .5rem;
}
.sec-title::before {
    content: ""; display: inline-block;
    width: 14px; height: 14px; border-radius: 3px;
    border: 2px solid #4F46E5; flex-shrink: 0;
}

/* ── Inputs ── */
label {
    color: #64748B !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    margin-bottom: .15rem !important;
}
div[data-baseweb="input"] > div {
    border-radius: 10px !important;
    background: #fff !important;
    border: 1.5px solid #D1D9E8 !important;
    font-size: .95rem !important;
}
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    background: #fff !important;
    border: 1.5px solid #D1D9E8 !important;
    font-size: .95rem !important;
}
div[data-baseweb="input"]:focus-within > div {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.12) !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.12) !important;
}

/* ── BMI summary strip ── */
.bmi-strip {
    display: flex; gap: 0;
    background: #EEF0FB;
    border-radius: 14px;
    overflow: hidden;
    margin: .8rem 0;
    border: 1.5px solid #E0E4F8;
}
.bmi-cell {
    flex: 1; padding: .75rem 1.1rem;
    border-right: 1.5px solid #E0E4F8;
}
.bmi-cell:last-child { border-right: none; }
.bmi-cell .k { font-size: .72rem; color: #7C85AD; text-transform: uppercase; letter-spacing: .08em; margin-bottom: .2rem; }
.bmi-cell .v { font-size: 1.35rem; font-weight: 700; color: #3730A3; }

/* ── Predict button ── */
.stButton > button {
    width: 100%; border: none;
    border-radius: 12px;
    padding: .85rem 1rem;
    font-size: 1rem; font-weight: 700;
    color: #fff;
    background: #4F46E5;
    box-shadow: none;
    transition: background .15s ease, transform .1s ease;
    display: flex; align-items: center; justify-content: center; gap: .4rem;
}
.stButton > button:hover { background: #4338CA; transform: translateY(-1px); color: #fff; }
.stButton > button:active { transform: translateY(0); }

/* ── Result card ── */
.result-card {
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    color: #fff;
    margin: .8rem 0;
}
.result-card .rc-tag {
    font-size: .72rem; letter-spacing: .14em;
    text-transform: uppercase; color: rgba(255,255,255,.8);
    margin-bottom: .5rem;
}
.result-card .rc-value {
    font-size: 3rem; font-weight: 800; color: #fff;
    margin: 0 0 .6rem; line-height: 1;
}
.result-card .rc-conf {
    font-size: .95rem; color: rgba(255,255,255,.9);
}

/* ── Probability section ── */
.pc-title {
    font-size: 1rem; font-weight: 700; color: #4F46E5;
    margin: 0 0 .6rem;
    display: flex; align-items: center; gap: .5rem;
}
.pc-title::before {
    content: ""; display: inline-block;
    width: 14px; height: 14px; border-radius: 3px;
    border: 2px solid #4F46E5; flex-shrink: 0;
}
.prob-row { margin: .65rem 0; }
.prob-row .pr-top {
    display: flex; justify-content: space-between;
    font-size: .9rem; color: #334155;
    margin-bottom: .28rem;
}
.prob-row .pr-pct { font-weight: 600; }
.prob-row .pr-bg  {
    background: #EEF0FB; border-radius: 999px;
    height: 9px; overflow: hidden;
}
.prob-row .pr-fill { height: 100%; border-radius: 999px; }

.footer { text-align: center; color: #B0B8CC; font-size: .78rem; margin-top: 1.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
STYLES = {
    "low":    ("#059669", "#10B981"),   # (card-bg, bar-color)
    "medium": ("#D97706", "#F59E0B"),
    "high":   ("#DC2626", "#F43F5E"),
}
DEFAULT_BG, DEFAULT_BAR = "#4F46E5", "#818CF8"

def card_style(cat: str):
    s = STYLES.get(str(cat).strip().lower())
    return (s[0], s[1]) if s else (DEFAULT_BG, DEFAULT_BAR)

def bmi_label(bmi: float) -> str:
    if bmi < 18.5: return "Underweight"
    if bmi < 25:   return "Normal"
    if bmi < 30:   return "Overweight"
    return "Obese"

def to_pct(v) -> float:
    v = float(v)
    return v * 100 if v <= 1 else v

def parse_result(data):
    if not isinstance(data, dict):
        return None
    # Unwrap wrapper keys
    for wk in ("predicted_category", "response"):
        if wk in data and isinstance(data[wk], dict):
            data = data[wk]
            break
    category, confidence, probs = None, None, {}
    for raw_key, value in data.items():
        k = raw_key.lower()
        if "categ" in k and isinstance(value, str):
            category = value
        elif "confid" in k and not isinstance(value, dict):
            try: confidence = float(value)
            except (TypeError, ValueError): pass
        elif "prob" in k and isinstance(value, dict):
            probs = value
    return (category, confidence, probs) if category else None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🛡 Insurance premium predictor</h1>
    <p>Fill in your details and get an instant premium category estimate.</p>
</div>
""", unsafe_allow_html=True)

# ── Personal details ──────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="sec-title">Personal details</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age    = st.number_input("Age", min_value=1, max_value=119, value=30)
        weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, step=0.5)
    with c2:
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.5,
                                  value=1.70, step=0.01, format="%.2f")
        smoker = st.selectbox("Are you a smoker?", [False, True],
                              format_func=lambda x: "Yes" if x else "No")

# ── Work & location ───────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="sec-title">Work and location</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        income_lpa = st.number_input("Annual income (LPA)", min_value=0.1, value=10.0, step=0.5)
        city       = st.text_input("City", value="Mumbai")
    with c4:
        occupation = st.selectbox(
            "Occupation",
            ["retired","freelancer","student","government_job",
             "business_owner","unemployed","private_job"],
            index=6,
            format_func=lambda x: x.replace("_"," ").title(),
        )

# ── BMI strip ─────────────────────────────────────────────────────────────────
bmi = weight / (height ** 2)
st.markdown(f"""
<div class="bmi-strip">
  <div class="bmi-cell"><div class="k">Your BMI</div><div class="v">{bmi:.1f}</div></div>
  <div class="bmi-cell"><div class="k">Category</div><div class="v">{bmi_label(bmi)}</div></div>
  <div class="bmi-cell"><div class="k">Smoker</div><div class="v">{"Yes" if smoker else "No"}</div></div>
</div>
""", unsafe_allow_html=True)

st.write("")
clicked = st.button("□  Predict premium category")

# ── Prediction ────────────────────────────────────────────────────────────────
if clicked:
    payload = {
        "age": age, "weight": weight, "height": height,
        "income_lpa": income_lpa, "smoker": smoker,
        "city": city, "occupation": occupation,
    }
    try:
        with st.spinner("Analysing your profile…"):
            resp = requests.post(API_URL, json=payload, timeout=15)
        try:
            raw = resp.json()
        except ValueError:
            raw = {}

        parsed = parse_result(raw) if resp.status_code == 200 else None

        if parsed:
            category, confidence, probs = parsed
            bg_color, bar_color = card_style(category)
            conf_str = f"{to_pct(confidence):.1f}%" if confidence is not None else "—"

            st.markdown(f"""
            <div class="result-card" style="background:{bg_color};">
                <div class="rc-tag">Predicted premium category</div>
                <div class="rc-value">{str(category).title()}</div>
                <div class="rc-conf">Confidence: {conf_str}</div>
            </div>
            """, unsafe_allow_html=True)

            if probs:
                with st.container(border=True):
                    st.markdown('<div class="pc-title">Class probabilities</div>', unsafe_allow_html=True)
                    for name, p in sorted(probs.items(), key=lambda kv: kv[1], reverse=True):
                        try:    pct = to_pct(p)
                        except: pct = 0.0
                        _, b_color = card_style(name)
                        st.markdown(f"""
                        <div class="prob-row">
                            <div class="pr-top">
                                <span>{str(name).title()}</span>
                                <span class="pr-pct">{pct:.1f}%</span>
                            </div>
                            <div class="pr-bg">
                                <div class="pr-fill" style="width:{min(pct,100):.1f}%;background:{b_color};"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error(f"Unexpected response (HTTP {resp.status_code})")
            st.json(raw)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API. Make sure the server is running.")
    except requests.exceptions.Timeout:
        st.error("⏱️ The server took too long. Please try again.")

st.markdown(
    '<p class="footer">Predictions are estimates only — not an official insurance quote.</p>',
    unsafe_allow_html=True,
)