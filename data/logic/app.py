import pandas as pd
import streamlit as st
from logic.risk_scoring import calculate_risk

st.set_page_config(page_title="Operations Command Centre", layout="wide")

st.title("Operations Command Centre")
st.caption("Operational intelligence platform for multi-site organisations")

df = pd.read_csv("data/sample_sites.csv")

df[["risk_score", "risk_level"]] = df.apply(
    lambda row: pd.Series(calculate_risk(row)),
    axis=1
)

total_sites = len(df)
high_risk_sites = len(df[df["risk_level"] == "High"])
medium_risk_sites = len(df[df["risk_level"] == "Medium"])
average_satisfaction = round(df["client_satisfaction"].mean(), 1)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sites", total_sites)
col2.metric("High Risk Sites", high_risk_sites)
col3.metric("Medium Risk Sites", medium_risk_sites)
col4.metric("Avg Client Satisfaction", f"{average_satisfaction}%")

st.divider()

st.subheader("Site Risk Overview")

risk_filter = st.selectbox(
    "Filter by risk level",
    ["All", "High", "Medium", "Low"]
)

if risk_filter != "All":
    filtered_df = df[df["risk_level"] == risk_filter]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)

st.divider()

st.subheader("Recommended Operational Actions")

for _, row in df.sort_values("risk_score", ascending=False).iterrows():
    if row["risk_level"] == "High":
        st.error(f"{row['site_name']} requires urgent attention.")
        st.write(
            "- Review staffing coverage\n"
            "- Escalate overdue compliance actions\n"
            "- Review complaints trend\n"
            "- Schedule leadership check-in"
        )
    elif row["risk_level"] == "Medium":
        st.warning(f"{row['site_name']} should be monitored.")
        st.write(
            "- Review local performance indicators\n"
            "- Confirm any overdue actions\n"
            "- Monitor client satisfaction"
        )
