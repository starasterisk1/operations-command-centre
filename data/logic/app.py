import pandas as pd
import streamlit as st

from logic.risk_scoring import calculate_risk
from logic.recommendations import generate_recommendations


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
        for recommendation in generate_recommendations(row):
            st.write(f"- {recommendation}")

    elif row["risk_level"] == "Medium":
        st.warning(f"{row['site_name']} should be monitored.")
        for recommendation in generate_recommendations(row):
            st.write(f"- {recommendation}")

st.divider()

st.subheader("AI Operations Assistant")

question = st.text_input("Ask an operational question")

if question:
    question_lower = question.lower()

    if "attention" in question_lower or "risk" in question_lower:
        top_sites = df.sort_values("risk_score", ascending=False).head(3)

        st.write("The sites needing the most attention are:")

        for _, row in top_sites.iterrows():
            st.write(f"### {row['site_name']}")
            st.write(
                f"Risk level: **{row['risk_level']}** | "
                f"Risk score: **{row['risk_score']}**"
            )

            for recommendation in generate_recommendations(row):
                st.write(f"- {recommendation}")

    elif "compliance" in question_lower:
        compliance_sites = df[df["compliance_overdue"] > 0]

        st.write("Sites with overdue compliance actions:")

        for _, row in compliance_sites.iterrows():
            st.write(
                f"- **{row['site_name']}** has "
                f"{row['compliance_overdue']} overdue compliance action(s)."
            )

    elif "satisfaction" in question_lower:
        lowest_satisfaction = df.sort_values("client_satisfaction").head(3)

        st.write("Sites with the lowest client satisfaction:")

        for _, row in lowest_satisfaction.iterrows():
            st.write(
                f"- **{row['site_name']}**: "
                f"{row['client_satisfaction']}%"
            )

    else:
        st.write(
            "I can currently answer questions about risk, attention areas, "
            "compliance, and client satisfaction."
        )
