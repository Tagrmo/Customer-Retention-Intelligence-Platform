import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

st.set_page_config(
    page_title="Customer Retention Intelligence Platform",
    page_icon="💼",
    layout="wide"
)

# =========================
# Styling
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 18% 10%, rgba(37,99,235,0.30), transparent 32%),
        radial-gradient(circle at 88% 8%, rgba(6,182,212,0.24), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(30,64,175,0.18), transparent 35%),
        linear-gradient(135deg, #020617 0%, #07111F 42%, #08213A 100%);
    color: #F8FAFC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.24), transparent 35%),
        linear-gradient(180deg, #020617 0%, #061527 52%, #08213A 100%) !important;
    border-right: 1px solid rgba(125,211,252,0.25);
}

.sidebar-hero {
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(125,211,252,0.26);
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 12px 32px rgba(2,6,23,0.35);
    margin-bottom: 20px;
}

.sidebar-title {
    color: #FFFFFF !important;
    font-size: 25px;
    font-weight: 900;
    line-height: 1.25;
    margin-bottom: 8px;
}

.sidebar-subtitle {
    color: #BFDBFE !important;
    font-size: 14px;
    line-height: 1.7;
    font-weight: 600;
}

.sidebar-badge {
    background: linear-gradient(135deg,#059669,#10B981);
    padding: 15px;
    border-radius: 16px;
    text-align: center;
    font-weight: 900;
    font-size: 15px;
    color: white !important;
    box-shadow: 0 8px 25px rgba(16,185,129,0.25);
    margin: 18px 0;
}

.sidebar-note-box {
    background: rgba(14,165,233,0.13);
    border: 1px solid rgba(56,189,248,0.28);
    border-radius: 16px;
    padding: 14px;
    color: #E0F2FE !important;
    line-height: 1.7;
    font-weight: 650;
    margin-top: 16px;
}

section[data-testid="stSidebar"] label {
    color: #E0F2FE !important;
    font-size: 14px !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {
    color: #D6E4FF !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stSelectbox {
    margin-bottom: 16px !important;
}

.streamlit-expanderHeader {
    background: rgba(15,23,42,0.82) !important;
    border: 1px solid rgba(125,211,252,0.22) !important;
    border-radius: 14px !important;
    padding: 12px !important;
    color: #FFFFFF !important;
    font-size: 14px !important;
    font-weight: 850 !important;
}

.streamlit-expanderHeader:hover {
    border-color: #38BDF8 !important;
    background: rgba(30,64,175,0.28) !important;
}

.streamlit-expanderContent {
    color: #D6E4FF !important;
    font-size: 14px !important;
}

/* =========================
   MAIN CARDS
========================= */
.hero-card {
    background:
        linear-gradient(135deg, rgba(15,23,42,0.96), rgba(29,78,216,0.92)),
        radial-gradient(circle at top right, rgba(56,189,248,0.45), transparent 35%);
    padding: 46px;
    border-radius: 32px;
    color: white;
    box-shadow: 0px 20px 55px rgba(37,99,235,0.35);
    border: 1px solid rgba(147,197,253,0.30);
    margin-bottom: 32px;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 19px;
    color: #DBEAFE;
    line-height: 1.8;
}

.section-title {
    font-size: 30px;
    font-weight: 900;
    color: #FFFFFF;
    margin-top: 34px;
    margin-bottom: 18px;
}

.kpi-card, .insight-grid-card, .data-section, .predictor-card {
    background: rgba(15,23,42,0.88);
    border: 1px solid rgba(148,163,184,0.28);
    border-radius: 24px;
    box-shadow: 0 16px 40px rgba(2,6,23,0.45);
    backdrop-filter: blur(14px);
}

.kpi-card {
    padding: 26px;
}

.kpi-label {
    color: #93C5FD;
    font-size: 15px;
    font-weight: 800;
}

.kpi-value {
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 900;
}

.insight-grid-card {
    padding: 26px;
    min-height: 200px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.insight-grid-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 50px rgba(37,99,235,0.28);
}

.insight-icon {
    font-size: 34px;
    margin-bottom: 14px;
}

.insight-title {
    color: #7DD3FC;
    font-size: 16px;
    font-weight: 900;
}

.insight-value {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 900;
}

.insight-note, .data-note {
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.7;
}

.recommendation-card {
    background: rgba(6,78,59,0.42);
    border: 1px solid rgba(52,211,153,0.45);
    color: #D1FAE5;
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 14px;
}

.prediction-card-high {
    background: rgba(127,29,29,0.42);
    border: 1px solid rgba(248,113,113,0.55);
    color: #FEE2E2;
    padding: 30px;
    border-radius: 26px;
}

.prediction-card-low {
    background: rgba(6,78,59,0.45);
    border: 1px solid rgba(52,211,153,0.55);
    color: #DCFCE7;
    padding: 30px;
    border-radius: 26px;
}

.data-section {
    padding: 28px;
}

div[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(125,211,252,0.25);
}

/* =========================
   PREDICTOR SECTION
========================= */
.predictor-card {
    padding: 30px;
    margin-bottom: 28px;
}

.predictor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 26px;
    gap: 20px;
}

.predictor-header h2 {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 900;
    margin-bottom: 6px;
}

.predictor-header p {
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}

.predictor-badge {
    background: linear-gradient(135deg, #2563EB, #06B6D4);
    color: white;
    padding: 12px 18px;
    border-radius: 999px;
    font-weight: 900;
    white-space: nowrap;
    box-shadow: 0 8px 25px rgba(14,165,233,0.25);
}

.form-group-title {
    color: #38BDF8;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(56,189,248,0.35);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* =========================
   PROFESSIONAL FORM FIELDS
========================= */
label {
    color: #E2E8F0 !important;
    font-size: 14px !important;
    font-weight: 750 !important;
}

/* Select containers */
div[data-baseweb="select"] > div {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 14px !important;
    min-height: 42px !important;
    box-shadow: 0 3px 10px rgba(2,6,23,0.18) !important;
}

/* Selected text */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #0F172A !important;
    font-weight: 750 !important;
    font-size: 15px !important;
}

/* Number input */
.stNumberInput input,
input {
    background: #F8FAFC !important;
    color: #0F172A !important;
    font-weight: 750 !important;
    font-size: 15px !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 10px rgba(2,6,23,0.18) !important;
}

/* Dropdown menu */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: 0 16px 38px rgba(15,23,42,0.22) !important;
}

/* Dropdown options */
div[role="option"],
li[role="option"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 15px !important;
    font-weight: 750 !important;
}

div[role="option"] span,
li[role="option"] span {
    color: #0F172A !important;
    font-size: 15px !important;
    font-weight: 750 !important;
}

/* Hover / focus option */
div[role="option"]:hover,
li[role="option"]:hover,
div[aria-selected="true"] {
    background: #DBEAFE !important;
    color: #0F172A !important;
}

.stDownloadButton > button,
.stButton > button,
button[kind="formSubmit"] {
    background: linear-gradient(135deg, #0EA5E9, #2563EB, #7C3AED) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.85rem 1.4rem !important;
    font-size: 16px !important;
    font-weight: 900 !important;
    box-shadow: 0 12px 30px rgba(37,99,235,0.35) !important;
    margin-top: 14px !important;
}

button[kind="formSubmit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 38px rgba(14,165,233,0.45) !important;
}

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
    padding: 32px;
}
/* Fix AI Predictor submit button */
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #06B6D4, #2563EB, #7C3AED) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 28px !important;
    font-size: 15px !important;
    font-weight: 900 !important;
    opacity: 1 !important;
    box-shadow: 0 12px 30px rgba(37,99,235,0.45) !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button p {
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #22D3EE, #3B82F6, #8B5CF6) !important;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)
# =========================
# Load Data & Model
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("Customer_Churn.csv")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
    return df

@st.cache_resource
def load_model():
    model = joblib.load("churn_model.pkl")
    model_columns = joblib.load("model_columns.pkl")
    return model, model_columns

df = load_data()
model, model_columns = load_model()

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-hero">
        <div class="sidebar-title">💼 Retention AI</div>
        <div class="sidebar-subtitle">
            Customer churn intelligence workspace for retention analytics and AI-powered decision support.
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected_contract = st.selectbox(
        "Contract Type",
        ["All"] + sorted(df["Contract"].unique().tolist())
    )

    selected_churn = st.selectbox(
        "Churn Status",
        ["All", "Yes", "No"]
    )

    selected_internet = st.selectbox(
        "Internet Service",
        ["All"] + sorted(df["InternetService"].unique().tolist())
    )

    st.markdown("""
    <div class="sidebar-badge">
        🤖 AI Churn Predictor Enabled
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📌 Platform Modules"):
        st.markdown("""
        - Executive KPIs  
        - Churn Analytics  
        - Risk Segmentation  
        - AI Prediction  
        - Customer Records
        """)

    with st.expander("🧰 Technologies"):
        st.markdown("""
        - Python  
        - Pandas  
        - Scikit-Learn  
        - Streamlit  
        - Plotly  
        - Power BI
        """)

    st.markdown("""
    <div class="sidebar-note-box">
        Built for retention analysis, churn prediction, and executive decision support.
    </div>
    """, unsafe_allow_html=True)

# =========================
# Calculations
# =========================

total_customers = len(df)
churned_customers = len(df[df["Churn"] == "Yes"])
retained_customers = len(df[df["Churn"] == "No"])

churn_rate = (churned_customers / total_customers) * 100 if total_customers else 0
retention_rate = (retained_customers / total_customers) * 100 if total_customers else 0
avg_monthly_charges = df["MonthlyCharges"].mean() if total_customers else 0

overall_churn_rate = df["Churn"].eq("Yes").mean() * 100

contract_churn_rate = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
)

if "Yes" in contract_churn_rate.columns:
    riskiest_contract = contract_churn_rate["Yes"].sort_values(ascending=False).index[0]
    riskiest_rate = contract_churn_rate["Yes"].max() * 100
else:
    riskiest_contract = "N/A"
    riskiest_rate = 0

churn_avg_charge = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
retained_avg_charge = df[df["Churn"] == "No"]["MonthlyCharges"].mean()
churn_avg_tenure = df[df["Churn"] == "Yes"]["tenure"].mean()
retained_avg_tenure = df[df["Churn"] == "No"]["tenure"].mean()

# =========================
# Hero
# =========================

st.markdown("""
<div class="hero-card">
    <div class="hero-title">Customer Retention Intelligence</div>
    <div class="hero-subtitle">
        Monitor churn behavior, detect high-risk customer groups, and generate AI-powered retention recommendations through a modern dark analytics workspace.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='color:#CBD5E1;
font-size:15px;
line-height:1.8;
margin-bottom:10px;'>

Advanced analytics workspace for customer retention,
churn prediction, and executive decision support.

</div>
""", unsafe_allow_html=True)

# =========================
# KPIs
# =========================

st.markdown('<div class="section-title">Executive KPIs</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Customers</div>
        <div class="kpi-value">{total_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Churned Customers</div>
        <div class="kpi-value">{churned_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Churn Rate</div>
        <div class="kpi-value">{churn_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Monthly Charges</div>
        <div class="kpi-value">${avg_monthly_charges:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Executive Intelligence Cards
# =========================

st.markdown('<div class="section-title">Executive Intelligence</div>', unsafe_allow_html=True)

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(f"""
    <div class="insight-grid-card">
        <div class="insight-icon">📉</div>
        <div class="insight-title">Overall Churn Rate</div>
        <div class="insight-value">{overall_churn_rate:.1f}%</div>
        <div class="insight-note">
            Percentage of customers who left the service across the full dataset.
        </div>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="insight-grid-card">
        <div class="insight-icon">⚠️</div>
        <div class="insight-title">Highest Risk Segment</div>
        <div class="insight-value">{riskiest_contract}</div>
        <div class="insight-note">
            This contract group records the highest churn rate at {riskiest_rate:.1f}%.
        </div>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="insight-grid-card">
        <div class="insight-icon">💳</div>
        <div class="insight-title">Churn Billing Signal</div>
        <div class="insight-value">${churn_avg_charge:.2f}</div>
        <div class="insight-note">
            Average monthly charge among churned customers compared with ${retained_avg_charge:.2f} for retained customers.
        </div>
    </div>
    """, unsafe_allow_html=True)

with i4:
    st.markdown(f"""
    <div class="insight-grid-card">
        <div class="insight-icon">⏳</div>
        <div class="insight-title">Tenure Signal</div>
        <div class="insight-value">{churn_avg_tenure:.1f} mo</div>
        <div class="insight-note">
            Average tenure for churned customers versus {retained_avg_tenure:.1f} months for retained customers.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Charts
# =========================

st.markdown('<div class="section-title">Churn Analytics</div>', unsafe_allow_html=True)

plotly_template = "plotly_dark"

c1, c2 = st.columns(2)

with c1:
    churn_counts =df["Churn"].value_counts().reset_index()
    churn_counts.columns = ["Churn", "Customers"]

    fig = px.pie(
        churn_counts,
        values="Customers",
        names="Churn",
        hole=0.58,
        title="Churn Distribution",
        template=plotly_template
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    contract_churn = pd.crosstab(
        df["Contract"],
        df["Churn"]
    ).reset_index()

    fig = px.bar(
        contract_churn,
        x="Contract",
        y=[col for col in contract_churn.columns if col != "Contract"],
        barmode="group",
        title="Churn by Contract Type",
        template=plotly_template
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    charge_df = (
        df.groupby("Churn")["MonthlyCharges"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        charge_df,
        x="Churn",
        y="MonthlyCharges",
        title="Average Monthly Charges by Churn",
        template=plotly_template
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    tenure_df = (
        df.groupby("Churn")["tenure"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        tenure_df,
        x="Churn",
        y="tenure",
        title="Average Tenure by Churn",
        template=plotly_template
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Risk Segmentation
# =========================

st.markdown('<div class="section-title">Customer Risk Segmentation</div>', unsafe_allow_html=True)

high_risk = (
    (df["Contract"] == "Month-to-month")
    & (df["tenure"] < 18)
    & (df["MonthlyCharges"] > df["MonthlyCharges"].mean())
)

medium_risk = (
    (~high_risk)
    & (
        (df["Contract"] == "Month-to-month")
        | (df["tenure"] < 18)
        | (df["MonthlyCharges"] > df["MonthlyCharges"].mean())
    )
)

low_risk = ~(high_risk | medium_risk)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">High Risk Customers</div>
        <div class="kpi-value">{high_risk.sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Medium Risk Customers</div>
        <div class="kpi-value">{medium_risk.sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Low Risk Customers</div>
        <div class="kpi-value">{low_risk.sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

risk_df = pd.DataFrame({
    "Risk Segment": ["High Risk", "Medium Risk", "Low Risk"],
    "Customers": [high_risk.sum(), medium_risk.sum(), low_risk.sum()]
})

fig = px.bar(
    risk_df,
    x="Risk Segment",
    y="Customers",
    title="Risk Segment Distribution",
    template=plotly_template
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E5E7EB"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# Model Drivers
# =========================

st.markdown('<div class="section-title">Top Model Drivers</div>', unsafe_allow_html=True)

if hasattr(model, "feature_importances_"):
    feature_importance = pd.DataFrame({
        "Feature": model_columns,
        "Importance": model.feature_importances_
    })

    feature_importance["Feature"] = (
        feature_importance["Feature"]
        .str.replace("_Yes", "", regex=False)
        .str.replace("_No", "", regex=False)
        .str.replace("_Month-to-month", " - Month-to-month", regex=False)
        .str.replace("_One year", " - One year", regex=False)
        .str.replace("_Two year", " - Two year", regex=False)
        .str.replace("_Fiber optic", " - Fiber optic", regex=False)
    )

    top_features = (
        feature_importance
        .sort_values("Importance", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_features,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top Churn Prediction Drivers",
        template=plotly_template
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Recommendations
# =========================

st.markdown('<div class="section-title">Retention Strategy Recommendations</div>', unsafe_allow_html=True)

st.markdown("""
<div class="recommendation-card">
<b>1. Prioritize month-to-month customers:</b> Offer loyalty discounts, upgrade incentives, or annual-contract benefits.
</div>

<div class="recommendation-card">
<b>2. Review high monthly charges:</b> Customers with higher bills show stronger churn risk and may need pricing review.
</div>

<div class="recommendation-card">
<b>3. Support early lifecycle customers:</b> Short-tenure customers need onboarding, engagement, and proactive support.
</div>
""", unsafe_allow_html=True)



# =========================
# AI Prediction
# =========================

st.markdown('<div class="section-title">AI Churn Risk Predictor</div>', unsafe_allow_html=True)

st.markdown("""
<div class="predictor-card">
    <div class="predictor-header">
        <div>
            <h2>Customer Churn Risk Assessment</h2>
            <p>
                Enter customer profile details to estimate churn probability and generate a retention recommendation.
            </p>
        </div>
        <div class="predictor-badge">AI Model Active</div>
    </div>
""", unsafe_allow_html=True)

with st.form("churn_prediction_form"):

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown('<div class="form-group-title">Customer Profile</div>', unsafe_allow_html=True)

        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])

    with p2:
        st.markdown('<div class="form-group-title">Contract & Billing</div>', unsafe_allow_html=True)

        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
        total_charges = st.number_input("Total Charges", min_value=0.0, value=800.0)

    with p3:
        st.markdown('<div class="form-group-title">Service Profile</div>', unsafe_allow_html=True)

        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        payment_method = st.selectbox("Payment Method", sorted(df["PaymentMethod"].unique().tolist()))

    submitted = st.form_submit_button("Run Churn Prediction")

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    input_data = pd.DataFrame({
        "gender": [gender],
        "SeniorCitizen": [senior_citizen],
        "Partner": [partner],
        "Dependents": [dependents],
        "tenure": [tenure],
        "PhoneService": ["Yes"],
        "MultipleLines": ["No"],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "OnlineBackup": ["No"],
        "DeviceProtection": ["No"],
        "TechSupport": [tech_support],
        "StreamingTV": ["No"],
        "StreamingMovies": ["No"],
        "Contract": [contract],
        "PaperlessBilling": ["Yes"],
        "PaymentMethod": [payment_method],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
    })

    input_encoded = pd.get_dummies(input_data, drop_first=True)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(input_encoded)[0]
    probability = model.predict_proba(input_encoded)[0][1]
    risk_score = probability * 100

    st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Churn Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#38BDF8"},
                "steps": [
                    {"range": [0, 40], "color": "rgba(34,197,94,0.28)"},
                    {"range": [40, 70], "color": "rgba(234,179,8,0.28)"},
                    {"range": [70, 100], "color": "rgba(239,68,68,0.28)"},
                ],
            },
        )
    )
    gauge_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )

    st.plotly_chart(gauge_fig, use_container_width=True)

    if prediction == 1:
        st.markdown(f"""
        <div class="prediction-card-high">
            <h2>High Churn Risk</h2>
            <h1>Risk Score: {risk_score:.1f}%</h1>
            <p>This customer is likely to leave the service.</p>
        </div>
        """, unsafe_allow_html=True)

        recommendation = "Offer retention incentives, review pricing, and encourage a longer-term contract."
        st.warning(recommendation)

    else:
        st.markdown(f"""
        <div class="prediction-card-low">
            <h2>Low Churn Risk</h2>
            <h1>Risk Score: {risk_score:.1f}%</h1>
            <p>This customer is likely to stay with the service.</p>
        </div>
        """, unsafe_allow_html=True)

        recommendation = "Maintain engagement and continue monitoring customer satisfaction."
        st.success(recommendation)

    report_text = f"""
Customer Retention Intelligence Platform
Prediction Report

Prediction Result: {"High Churn Risk" if prediction == 1 else "Low Churn Risk"}
Risk Score: {risk_score:.1f}%

Recommended Action:
{recommendation}
"""

    st.download_button(
        label="Download Prediction Report",
        data=report_text,
        file_name="customer_churn_prediction_report.txt",
        mime="text/plain"
    )

# =========================
# Customer Data
# =========================

st.markdown('<div class="section-title">Customer Records Explorer</div>', unsafe_allow_html=True)

st.markdown("""
<div class="data-section">
    <div class="data-note">
        Explore customer records based on the selected filters. This section keeps the raw customer view available
        while presenting it inside a controlled analytics workspace.<br>
        Developed by <strong>Taghreed Mohammed</strong>
    </div>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df, 
    use_container_width=True,
    height=420
)

csv = df.to_csv(index=False)

st.download_button(
    label="Download Filtered Customer Records",
    data=csv,
    file_name="filtered_customer_churn_data.csv",
    mime="text/csv"
)

# =========================
# Footer
# =========================

st.markdown("---")

st.markdown("""
<div class="footer">
Customer Retention Intelligence Platform © 2026<br>
AI-powered churn analytics and retention decision support.
</div>
""", unsafe_allow_html=True)