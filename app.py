import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Transaction AI", layout="wide")

st.title("💳 Bank Transaction Monitoring System")

# =========================
# LOAD DATA
# =========================
file = st.file_uploader("Upload transaction CSV", type=["csv"])

if file is None:
    st.info("Please upload your dataset")
    st.stop()

df = pd.read_csv(file)

st.subheader("📊 Data Preview")
st.dataframe(df.head())

# =========================
# BASIC CLEANING
# =========================
df = df.fillna(0)

# =========================
# KPI SECTION
# =========================
st.subheader("📈 Key Metrics")

total_tx = len(df)
success_rate = (df["status"] == "Success").mean() * 100
avg_amount = df["amount"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", total_tx)
col2.metric("Success Rate (%)", round(success_rate, 2))
col3.metric("Avg Amount", round(avg_amount, 2))

# =========================
# TRANSACTION TYPE ANALYSIS
# =========================
st.subheader("💳 Transaction Types")

type_counts = df["transaction_type"].value_counts()

fig, ax = plt.subplots()
ax.bar(type_counts.index, type_counts.values)
ax.set_title("Transaction Types")

st.pyplot(fig)


st.subheader("📡 Channel Usage")

channel_counts = df["channel"].value_counts()

fig, ax = plt.subplots()
ax.pie(channel_counts.values, labels=channel_counts.index, autopct="%1.1f%%")

st.pyplot(fig)


st.subheader("⚠️ Risk Detection")

def risk(row):
    if row["status"] == "Failed":
        return "High Risk"
    elif row["amount"] > df["amount"].mean() * 3:
        return "Suspicious Amount"
    else:
        return "Normal"

df["Risk_Level"] = df.apply(risk, axis=1)

st.dataframe(df[["transaction_id", "amount", "status", "Risk_Level"]].head(20))

# =========================
# TIME ANALYSIS
# =========================
st.subheader("⏰ Hourly Activity")

hour_counts = df["hour"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(hour_counts.index, hour_counts.values)

ax.set_title("Transactions by Hour")
ax.set_xlabel("Hour")
ax.set_ylabel("Count")

st.pyplot(fig)

# =========================
# DOWNLOAD
# =========================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Analysis",
    data=csv,
    file_name="transaction_analysis.csv",
    mime="text/csv"
)