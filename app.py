import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="ʕ •ᴥ•ʔ Config Wombat")

st.title("ʕ •ᴥ•ʔ Config Wombat")
st.header("Secure Config Assessment Utility")
st.markdown("""
    This tool should interpret and produce a summary output of some well known tools
    aligned with the ACSC ISM. Load csv files below for interpretation.
""")

with st.expander("Please upload files to interpret:"):
    csvfiles = st.file_uploader("CSV Files", accept_multiple_files=True, type={"csv"})

csvs = []
for inputfile in csvfiles:
    csvs.append(pd.read_csv(inputfile))

dataframes = {}

for csv in csvs:
    if (csv.columns[:3].str.lower() == ["rank", "recommended action", "score impact"]).all():
        dataframes["Microsoft 365 Recommendations"] = csv
    elif (csv.columns[:3].str.lower() == ["actualvalue", "commandlet", "control"]).all():
        dataframes["CISA ScubaGear Baseline"] = csv
    elif (csv.columns[:3].str.lower() == ["exportedtimestamp", "subscriptionid", "subscriptionname"]).all():
        dataframes["Microsoft Azure Recommendations"] = csv
    elif (csv.columns[:3].str.lower() == ["tested system", "test timestamp", "mitigation strategy"]).all():
        dataframes["ACSC E8MVT"] = csv

if dataframes:
    st.markdown(f"Loaded {', '.join(dataframes.keys())}")
