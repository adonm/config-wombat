import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="ʕ •ᴥ•ʔ Config Wombat", page_icon="📑")

st.title("ʕ •ᴥ•ʔ Config Wombat")
st.header("Secure Config Summary Utility v0.1")
st.markdown("""
    This tool should interpret and produce a summary output of some well known tools
    aligned with the ACSC ISM. Load csv files below for interpretation.
""")

with st.expander("Please upload files to interpret:"):
    csvfiles = st.file_uploader(
        "CSV Files", accept_multiple_files=True, type={"csv"})

csvs = []
for inputfile in csvfiles:
    csvs.append(pd.read_csv(inputfile))

df = pd.DataFrame(columns=["Strategy", "Source",
                  "Description", "Assessment", "AssessmentDetail"])

source_df = pd.DataFrame(columns=["Source"])
strategies = {
    "Application control": "execution",
    "Patch applications": [],
    "Configure Microsoft Office macro settings": [],
    "User application hardening": [],
    "Restrict administrative privileges": [],
    "Patch operating systems": [],
    "Multi-factor authentication": [],
    "Regular backups": [],
    "Server application hardening": [],
    "Block spoofed emails": [],
    "Network segmentation": [],
    "Continuous incident detection and response": [],
    "Personnel management": []
}

for csv in csvs:
    if (csv.columns[:3].str.lower() == ["rank", "recommended action", "score impact"]).all():
        csv["Source"] = "Microsoft 365 Recommendations"
    elif (csv.columns[:3].str.lower() == ["actualvalue", "commandlet", "control"]).all():
        csv["Source"] = "CISA ScubaGear Baseline"
    elif (csv.columns[:3].str.lower() == ["exportedtimestamp", "subscriptionid", "subscriptionname"]).all():
        csv["Source"] = "Microsoft Azure Recommendations"
    elif (csv.columns[:3].str.lower() == ["tested system", "test timestamp", "mitigation strategy"]).all():
        csv["Source"] = "ACSC E8MVT"
    else:
        continue
    source_df = pd.concat([source_df, csv])


st.markdown(f"Loaded {', '.join(source_df.Source.unique())}")

with st.expander(f"Source Data ({len(source_df)} rows)"):
    st.dataframe(source_df)
    regex = st.text_input("Filter regex")
    exclude_regex = st.text_input("Exclude regex")
    m = source_df.astype(str).apply(lambda col: col.str.contains(regex, case=False)).any(1)
    match_df = source_df[m]
    e = match_df.astype(str).apply(lambda col: col.str.contains(exclude_regex, case=False)).any(1)
    match_df = match_df[~e]
    st.dataframe(match_df)

st.download_button(
    "Download Summary",
    df.to_csv(index=False).encode('utf-8'),
    f"secureconfigsummary_{pd.Timestamp('today').date()}.csv",
    "text/csv",
    key='download-csv'
)

for strategy, regex in strategies.items():
    strategydf = df[df["Strategy"] == strategy]
    st.header(f"{strategy} ({len(strategydf)})")
    st.dataframe(strategydf)
