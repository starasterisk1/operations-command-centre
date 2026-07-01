import pandas as pd
import streamlit as st
from logic.risk_scoring import calculate_risk

st.set_page_config(page_title="Operations Command Centre", layout="wide")

st.title("Operations Command Centre")
st.subheader("AI-ready operational intelligence platform for multi-site organisations")

df = pd.read_csv("data/sample_sites.csv")

df[["risk_score", "risk_level"]] = df.apply(
    lambda row: pd.Series(calculate_risk(row)),
    axis=1
)

st.metric("Total Sites", len(df))
st.metric("High Risk Sites", len(df[df["risk_level"] == "High"]))

st.dataframe(df, use_container_width=True)

st.subheader("Sites Requiring Attention")

high_risk_sites = df[df["risk_level"] == "High"]

if high_risk_sites.empty:
    st.success("No high-risk sites identified.")
else:
    for _, row in high_risk_sites.iterrows():
        st.warning(
            f"{row['site_name']} is high risk with a score of {row['risk_score']}."
        )
