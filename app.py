import streamlit as st
import numpy as np
import pandas as pd

st.title("Config Wombat")
st.header("Secure Config Assessment Utility")
st.markdown("""
    This tool should interpret and produce a summary output of some well known tools
    aligned with the ACSC ISM. Load csvs and json files below for interpretation.
""")

csvfiles = st.file_uploader("Please upload files to interpret:", accept_multiple_files=True, type={"csv"})

csvs = []
for inputfile in csvfiles:
    csvs.append(pd.read_csv(inputfile))

for csv in csvs:
    st.dataframe(csv)
