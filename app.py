# ==========================================
# Customer Retention Intelligence Platform
# Streamlit Dashboard
# ==========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import numpy as np
import plotly.graph_objects as go
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Customer Retention Intelligence Platform",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# Custom Styling
# ==========================================

st.markdown(
    """
    <style>
        .main {
            background-color: #F7F9FC;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero-card {
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
            padding: 32px;
            border-radius: 22px;
            color: white;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.20);
        }

        .hero-title {
            font-size: 38px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .hero-subtitle {
            font-size: 17px;
            color: #DBEAFE;
            max-width: 850px;
            line-height: 1.6;
        }

        .section-title {
            font-size: 26px;
            font-weight: 800;
            color: #0F172A;
            margin-top: 25px;
            margin-bottom: 14px;
        }

        .insight-box {
            background-color: white;
            border-left: 6px solid #2563EB;
            padding: 18px;
            border-radius: 14px;
            margin-bottom: 12px;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        }

        .recommendation-box {
            background-color: #ECFDF5;
            border-left: 6px solid #10B981;
            padding: 18px;
            border-radius: 14px;
            margin-bottom: 12px;
            color: #064E3B;
        }

        div[data-testid="stMetric"] {
            background-color: white;
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.07);
            border: 1px solid #E5E7EB;
        }

        div[data-testid="stMetricLabel"] {
            color: #64748B;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: #0F172A;
            font-weight: 800;
        }

        .modern-card {
            background-color: white;
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
            min-height: 150px;
        }

        .modern-card-title {
            font-size: 15px;
            font-weight: 700;
            color: #64748B;
            margin-bottom: 8px;
        }

        .modern-card-value {
            font-size: 26px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 8px;
        }

        .modern-card-note {
            font-size: 14px;
            color: #475569;
            line-height: 1.5;
        }

        .risk-high {
            background-color: #FEF2F2;
            border: 1px solid #FCA5A5;
            color: #7F1D1D;
        }

        .risk-medium {
            background-color: #FFFBEB;
            border: 1px solid #FCD34D;
            color: #78350F;
        }

        .risk-low {
            background-color: #ECFDF5;
            border: 1px solid #86EFAC;
            color: #064E3B;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Load Data
# ==========================================

DATA_PATH = "Customer_Churn.csv"
df = pd.read_csv(DATA_PATH)

# ==========================================
# PDF Report Generator
# ==========================================

def create_pdf_report():

    pdf_file = "customer_churn_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Customer Retention Intelligence Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Total Customers: {total_customers}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Churn Rate: {churn_rate:.2f}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Retention Rate: {retention_rate:.2f}%",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Key Business Insights",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "- Month-to-month contracts show the highest churn risk.",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "- Customers with higher monthly charges churn more frequently.",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "- Long-tenure customers are significantly more loyal.",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_file
# ==========================================
# Load Machine Learning Model
# ==========================================

model = joblib.load("churn_model.pkl")
model_columns = joblib.load("model_columns.pkl")
# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.title("Filters")
st.sidebar.caption("Refine the customer segment shown in the dashboard.")

selected_contract = st.sidebar.selectbox(
    "Contract Type",
    ["All"] + sorted(df["Contract"].unique().tolist())
)

selected_churn = st.sidebar.selectbox(
    "Churn Status",
    ["All", "Yes", "No"]
)

selected_internet = st.sidebar.selectbox(
    "Internet Service",
    ["All"] + sorted(df["InternetService"].unique().tolist())
)

filtered_df = df.copy()

if selected_contract != "All":
    filtered_df = filtered_df[
        filtered_df["Contract"] == selected_contract
    ]

if selected_churn != "All":
    filtered_df = filtered_df[
        filtered_df["Churn"] == selected_churn
    ]

if selected_internet != "All":
    filtered_df = filtered_df[
        filtered_df["InternetService"] == selected_internet
    ]


# ==========================================
# Header / Hero Section
# ==========================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Customer Retention Intelligence Platform 📊</div>
        <div class="hero-subtitle">
            A business-focused analytics dashboard for understanding customer churn,
            identifying high-risk segments, and supporting retention decisions with data-driven insights.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Current filters → Contract: {selected_contract} | Churn: {selected_churn} | Internet Service: {selected_internet}"
)


# ==========================================
# KPI Dashboard
# ==========================================

st.markdown('<div class="section-title">Executive KPIs</div>', unsafe_allow_html=True)

total_customers = len(filtered_df)
churned_customers = len(filtered_df[filtered_df["Churn"] == "Yes"])
retained_customers = len(filtered_df[filtered_df["Churn"] == "No"])

if total_customers > 0:
    churn_rate = (churned_customers / total_customers) * 100
    retention_rate = (retained_customers / total_customers) * 100
    avg_monthly_charges = filtered_df["MonthlyCharges"].mean()
else:
    churn_rate = 0
    retention_rate = 0
    avg_monthly_charges = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", f"{total_customers:,}")

with col2:
    st.metric("Churned Customers", f"{churned_customers:,}")

with col3:
    st.metric("Churn Rate", f"{churn_rate:.1f}%")

with col4:
    st.metric("Avg Monthly Charges", f"${avg_monthly_charges:.2f}")


# ==========================================
# Executive Summary
# ==========================================

st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    highest_churn_contract = (
        pd.crosstab(df["Contract"], df["Churn"], normalize="index")["Yes"]
        .sort_values(ascending=False)
        .index[0]
    )

    churn_avg_charge = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
    retained_avg_charge = df[df["Churn"] == "No"]["MonthlyCharges"].mean()

    churn_avg_tenure = df[df["Churn"] == "Yes"]["tenure"].mean()
    retained_avg_tenure = df[df["Churn"] == "No"]["tenure"].mean()

    st.markdown(
        f"""
        <div class="insight-box">
            <b>Key Finding:</b> The strongest churn risk appears among customers with
            <b>{highest_churn_contract}</b> contracts. Customers who churn also show higher average monthly charges
            (${churn_avg_charge:.2f}) than retained customers (${retained_avg_charge:.2f}).
        </div>
        <div class="insight-box">
            <b>Tenure Insight:</b> Churned customers have a shorter average tenure
            ({churn_avg_tenure:.1f} months) compared with retained customers
            ({retained_avg_tenure:.1f} months).
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("No data available for the selected filters.")




# ==========================================
# AI Business Insights
# ==========================================

st.markdown('<div class="section-title">AI Business Insights</div>', unsafe_allow_html=True)

overall_churn_rate = (df["Churn"].eq("Yes").mean()) * 100
contract_risk = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
)

if "Yes" in contract_risk.columns:
    riskiest_contract = contract_risk["Yes"].sort_values(ascending=False).index[0]
    riskiest_contract_rate = contract_risk["Yes"].max() * 100
else:
    riskiest_contract = "N/A"
    riskiest_contract_rate = 0

churn_avg_charge = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
churn_avg_tenure = df[df["Churn"] == "Yes"]["tenure"].mean()

insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)

with insight_col1:
    st.markdown(
        f'''
        <div class="modern-card">
            <div class="modern-card-title">Overall Churn Rate</div>
            <div class="modern-card-value">{overall_churn_rate:.1f}%</div>
            <div class="modern-card-note">Percentage of customers who left the company.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with insight_col2:
    st.markdown(
        f'''
        <div class="modern-card">
            <div class="modern-card-title">Highest Risk Segment</div>
            <div class="modern-card-value">{riskiest_contract}</div>
            <div class="modern-card-note">Churn rate: {riskiest_contract_rate:.1f}%</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with insight_col3:
    st.markdown(
        f'''
        <div class="modern-card">
            <div class="modern-card-title">Avg Churn Charges</div>
            <div class="modern-card-value">${churn_avg_charge:.2f}</div>
            <div class="modern-card-note">Average monthly bill among churned customers.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with insight_col4:
    st.markdown(
        f'''
        <div class="modern-card">
            <div class="modern-card-title">Avg Churn Tenure</div>
            <div class="modern-card-value">{churn_avg_tenure:.1f}</div>
            <div class="modern-card-note">Average months before churn occurs.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# ==========================================
# Charts
# ==========================================

st.markdown('<div class="section-title">Churn Analytics</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Churn Distribution")

    churn_counts = filtered_df["Churn"].value_counts()

    if not churn_counts.empty:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            churn_counts,
            labels=churn_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No churn data available for the selected filters.")

with chart_col2:
    st.subheader("Churn by Contract Type")

    contract_churn = pd.crosstab(
        filtered_df["Contract"],
        filtered_df["Churn"]
    )

    if not contract_churn.empty:
        st.bar_chart(contract_churn)
    else:
        st.info("No contract data available for the selected filters.")


chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Average Monthly Charges by Churn")

    monthly_charges = (
        filtered_df.groupby("Churn")["MonthlyCharges"]
        .mean()
    )

    if not monthly_charges.empty:
        st.bar_chart(monthly_charges)
    else:
        st.info("No monthly charges data available.")

with chart_col4:
    st.subheader("Average Tenure by Churn")

    tenure_analysis = (
        filtered_df.groupby("Churn")["tenure"]
        .mean()
    )

    if not tenure_analysis.empty:
        st.bar_chart(tenure_analysis)
    else:
        st.info("No tenure data available.")




# ==========================================
# Risk Segmentation
# ==========================================

st.markdown('<div class="section-title">Risk Segmentation</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    high_risk_mask = (
        (filtered_df["Contract"] == "Month-to-month")
        & (filtered_df["tenure"] < 18)
        & (filtered_df["MonthlyCharges"] > df["MonthlyCharges"].mean())
    )

    medium_risk_mask = (
        (~high_risk_mask)
        & (
            (filtered_df["Contract"] == "Month-to-month")
            | (filtered_df["tenure"] < 18)
            | (filtered_df["MonthlyCharges"] > df["MonthlyCharges"].mean())
        )
    )

    low_risk_mask = ~(high_risk_mask | medium_risk_mask)

    high_risk_count = int(high_risk_mask.sum())
    medium_risk_count = int(medium_risk_mask.sum())
    low_risk_count = int(low_risk_mask.sum())

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:
        st.markdown(
            f'''
            <div class="modern-card risk-high">
                <div class="modern-card-title">High Risk</div>
                <div class="modern-card-value">{high_risk_count:,}</div>
                <div class="modern-card-note">Month-to-month, low tenure, and high charges.</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with risk_col2:
        st.markdown(
            f'''
            <div class="modern-card risk-medium">
                <div class="modern-card-title">Medium Risk</div>
                <div class="modern-card-value">{medium_risk_count:,}</div>
                <div class="modern-card-note">Customers with one or more churn risk signals.</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with risk_col3:
        st.markdown(
            f'''
            <div class="modern-card risk-low">
                <div class="modern-card-title">Low Risk</div>
                <div class="modern-card-value">{low_risk_count:,}</div>
                <div class="modern-card-note">Customers with stronger retention signals.</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    risk_segment_df = pd.DataFrame(
        {
            "Risk Segment": ["High Risk", "Medium Risk", "Low Risk"],
            "Customers": [high_risk_count, medium_risk_count, low_risk_count]
        }
    ).set_index("Risk Segment")

    st.bar_chart(risk_segment_df)
else:
    st.info("No customer data available for risk segmentation.")


# ==========================================
# Model Explainability
# ==========================================

st.markdown('<div class="section-title">Top Model Drivers</div>', unsafe_allow_html=True)

if hasattr(model, "feature_importances_"):
    feature_importance = pd.DataFrame(
        {
            "Feature": model_columns,
            "Importance": model.feature_importances_
        }
    )

    feature_importance["Feature"] = (
        feature_importance["Feature"]
        .str.replace("_Yes", "", regex=False)
        .str.replace("_No", "", regex=False)
        .str.replace("_Fiber optic", " - Fiber optic", regex=False)
        .str.replace("_Month-to-month", " - Month-to-month", regex=False)
        .str.replace("_One year", " - One year", regex=False)
        .str.replace("_Two year", " - Two year", regex=False)
    )

    top_features = (
        feature_importance
        .sort_values("Importance", ascending=False)
        .head(10)
        .set_index("Feature")
    )

    st.write(
        "These are the strongest signals the model uses when estimating churn risk."
    )

    st.bar_chart(top_features)
else:
    st.info("Feature importance is not available for this model type.")

# ==========================================
# AI-Style Recommendations
# ==========================================

st.markdown('<div class="section-title">Retention Recommendations</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="recommendation-box">
        <b>1. Prioritize month-to-month customers:</b> Create retention offers for customers with flexible contracts.
    </div>
    <div class="recommendation-box">
        <b>2. Review high monthly charges:</b> Customers with higher bills show stronger churn risk.
    </div>
    <div class="recommendation-box">
        <b>3. Focus on early lifecycle customers:</b> Short-tenure customers need onboarding support and loyalty incentives.
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Data Table
# ==========================================

st.markdown('<div class="section-title">Customer Data</div>', unsafe_allow_html=True)

st.dataframe(
    filtered_df,
    width="stretch"
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data CSV",
    data=csv,
    file_name="filtered_customer_churn_data.csv",
    mime="text/csv"
)
# ==========================================
# Executive Report Center
# ==========================================

st.markdown("---")
st.markdown('<div class="section-title">Executive Report Center</div>', unsafe_allow_html=True)

report_col1, report_col2 = st.columns([2, 1])

with report_col1:
    st.markdown(
        """
        <div class="insight-box">
            <b>Executive Report:</b> Generate a PDF summary that includes core KPIs,
            churn insights, and recommended retention actions for the selected dashboard view.
        </div>
        """,
        unsafe_allow_html=True
    )

with report_col2:
    if st.button("Generate Executive PDF"):

        pdf_file = create_pdf_report()

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="Download Executive PDF",
                data=file,
                file_name="Customer_Churn_Executive_Report.pdf",
                mime="application/pdf"
            )

# ==========================================
# About The Model
# ==========================================

st.markdown('<div class="section-title">About the Model</div>', unsafe_allow_html=True)

model_col1, model_col2, model_col3 = st.columns(3)

with model_col1:
    st.markdown(
        """
        <div class="modern-card">
            <div class="modern-card-title">Model Type</div>
            <div class="modern-card-value">Random Forest</div>
            <div class="modern-card-note">A classification model used to estimate customer churn risk.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with model_col2:
    st.markdown(
        """
        <div class="modern-card">
            <div class="modern-card-title">Business Goal</div>
            <div class="modern-card-value">Retention</div>
            <div class="modern-card-note">Identify customers who may leave and support proactive retention actions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with model_col3:
    st.markdown(
        """
        <div class="modern-card">
            <div class="modern-card-title">Output</div>
            <div class="modern-card-value">Risk Score</div>
            <div class="modern-card-note">A probability-based churn risk score from 0% to 100%.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================
# AI Churn Prediction
# ==========================================

st.markdown("---")
st.markdown('<div class="section-title">AI Churn Risk Predictor</div>', unsafe_allow_html=True)

st.write(
    "Estimate the likelihood of customer churn based on contract, tenure, charges, and service profile."
)

st.markdown(
    """
    <div style="
        background-color:#F8FAFC;
        padding:24px;
        border-radius:18px;
        border:1px solid #E5E7EB;
        margin-bottom:20px;
    ">
        <h4 style="color:#0F172A; margin-bottom:6px;">Customer Profile</h4>
        <p style="color:#64748B; margin-bottom:0;">
            Fill in the customer details below to generate a churn risk prediction and recommended retention action.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("churn_prediction_form"):

    form_col1, form_col2, form_col3 = st.columns(3)

    with form_col1:
        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

        partner = st.selectbox(
            "Partner",
            ["No", "Yes"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"]
        )

    with form_col2:
        tenure = st.number_input(
            "Tenure (Months)",
            min_value=0,
            max_value=100,
            value=12
        )

        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"]
        )

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=800.0
        )

    with form_col3:
        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online Security",
            ["No", "Yes", "No internet service"]
        )

        tech_support = st.selectbox(
            "Tech Support",
            ["No", "Yes", "No internet service"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            sorted(df["PaymentMethod"].unique().tolist())
        )

    submitted = st.form_submit_button(
        "Predict Customer Churn Risk"
    )

if submitted:

    input_data = pd.DataFrame(
        {
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
        }
    )

    input_encoded = pd.get_dummies(
        input_data,
        drop_first=True
    )

    input_encoded = input_encoded.reindex(
        columns=model_columns,
        fill_value=0
    )

    prediction = model.predict(input_encoded)[0]
    probability = model.predict_proba(input_encoded)[0][1]
    risk_score = probability * 100

    st.markdown("### Prediction Result")

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Churn Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 40], "color": "#DCFCE7"},
                    {"range": [40, 70], "color": "#FEF9C3"},
                    {"range": [70, 100], "color": "#FEE2E2"},
                ],
            },
        )
    )

    st.plotly_chart(
        gauge_fig,
        width="stretch"
    )

    if prediction == 1:

        st.markdown(
            f"""
            <div style="
                background-color:#FEF2F2;
                padding:24px;
                border-radius:18px;
                border:1px solid #FCA5A5;
            ">
                <h3 style="color:#B91C1C; margin-bottom:8px;">High Churn Risk</h3>
                <p style="font-size:18px;color:#7F1D1D; margin-bottom:10px;">
                    This customer is likely to leave the service.
                </p>
                <h2 style="color:#B91C1C; margin-bottom:0;">Risk Score: {risk_score:.1f}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Recommended action: offer retention incentives, review pricing, and encourage a longer-term contract."
        )

    else:

        st.markdown(
            f"""
            <div style="
                background-color:#ECFDF5;
                padding:24px;
                border-radius:18px;
                border:1px solid #86EFAC;
            ">
                <h3 style="color:#047857; margin-bottom:8px;">Low Churn Risk</h3>
                <p style="font-size:18px;color:#064E3B; margin-bottom:10px;">
                    This customer is likely to stay with the service.
                </p>
                <h2 style="color:#047857; margin-bottom:0;">Risk Score: {risk_score:.1f}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Recommended action: maintain engagement and continue monitoring customer satisfaction."
        )

    # ==========================================
    # Download Prediction Report
    # ==========================================

    prediction_label = "High Churn Risk" if prediction == 1 else "Low Churn Risk"
    recommended_action = (
        "Offer retention incentives, review pricing, and encourage a longer-term contract."
        if prediction == 1
        else "Maintain engagement and continue monitoring customer satisfaction."
    )

    report_text = f'''
Customer Retention Intelligence Platform
Prediction Report

Prediction Result: {prediction_label}
Risk Score: {risk_score:.1f}%

Customer Profile
- Gender: {gender}
- Senior Citizen: {senior_citizen}
- Partner: {partner}
- Dependents: {dependents}
- Tenure: {tenure} months
- Contract: {contract}
- Monthly Charges: ${monthly_charges:.2f}
- Total Charges: ${total_charges:.2f}
- Internet Service: {internet_service}
- Online Security: {online_security}
- Tech Support: {tech_support}
- Payment Method: {payment_method}

Recommended Action
{recommended_action}
'''

    st.download_button(
        label="Download Prediction Report",
        data=report_text,
        file_name="customer_churn_prediction_report.txt",
        mime="text/plain"
    )
