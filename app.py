import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="💳Transaction AI Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white;
}

.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    border: 1px solid #374151;
}

.metric-title {
    color: #9CA3AF;
    font-size: 16px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: bold;
}

.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
}

div[data-testid="stFileUploader"] {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center; color:white;'>
 AI Bank Transaction Monitoring Dashboard
</h1>
<p style='text-align:center; color:gray; font-size:18px;'>
💳Smart Monitoring • Fraud Detection • Transaction Analytics
</p>
""", unsafe_allow_html=True)

st.write("")

uploaded_file = st.file_uploader(
    "📂 Upload Transaction Dataset",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a CSV file to start analysis.")
    st.stop()

df = pd.read_csv(uploaded_file)

df = df.fillna(0)

st.subheader("📊 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

total_tx = len(df)

success_rate = (df["status"] == "Success").mean() * 100

avg_amount = df["amount"].mean()

failed_tx = (df["status"] == "Failed").sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Transactions</div>
        <div class="metric-value">{total_tx}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Success Rate</div>
        <div class="metric-value">{success_rate:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Amount</div>
        <div class="metric-value">${avg_amount:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Failed Transactions</div>
        <div class="metric-value">{failed_tx}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:

    st.subheader("💳 Transaction Types")

    type_counts = df["transaction_type"].value_counts()

    fig_bar = px.bar(
        x=type_counts.index,
        y=type_counts.values,
        labels={"x": "Transaction Type", "y": "Count"},
        template="plotly_dark"
    )

    fig_bar.update_layout(
        height=400
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with col2:

    st.subheader("📡 Channel Usage")

    channel_counts = df["channel"].value_counts()

    fig_pie = px.pie(
        values=channel_counts.values,
        names=channel_counts.index,
        template="plotly_dark"
    )

    fig_pie.update_layout(
        height=400
    )

    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("⚠️ AI Risk Detection")

def detect_risk(row):

    if row["status"] == "Failed":
        return "High Risk"

    elif row["amount"] > df["amount"].mean() * 3:
        return "Suspicious Amount"

    else:
        return "Normal"

df["Risk_Level"] = df.apply(detect_risk, axis=1)

risk_counts = df["Risk_Level"].value_counts()

fig_risk = px.bar(
    x=risk_counts.index,
    y=risk_counts.values,
    color=risk_counts.index,
    template="plotly_dark"
)

fig_risk.update_layout(
    height=400,
    xaxis_title="Risk Level",
    yaxis_title="Count"
)

st.plotly_chart(fig_risk, use_container_width=True)

st.subheader("🛑 Suspicious Transactions")

suspicious_df = df[df["Risk_Level"] != "Normal"]

st.dataframe(
    suspicious_df,
    use_container_width=True
)

st.subheader("⏰ Hourly Transaction Activity")

hour_counts = df["hour"].value_counts().sort_index()

fig_line = go.Figure()

fig_line.add_trace(
    go.Scatter(
        x=hour_counts.index,
        y=hour_counts.values,
        mode='lines+markers'
    )
)

fig_line.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_title="Hour",
    yaxis_title="Transactions",
)

st.plotly_chart(fig_line, use_container_width=True)

st.subheader("🔍 Filter Transactions")

risk_filter = st.selectbox(
    "Select Risk Level",
    df["Risk_Level"].unique()
)

filtered_df = df[df["Risk_Level"] == risk_filter]

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.subheader("⬇️ Download Analysis")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Processed CSV",
    data=csv,
    file_name="transaction_analysis.csv",
    mime="text/csv"
)

st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Built with Streamlit • AI Transaction Monitoring System
</p>
""", unsafe_allow_html=True)