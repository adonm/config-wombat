import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="ʕ •ᴥ•ʔ Config Wombat")

st.title("ʕ •ᴥ•ʔ Config Wombat")
st.header("Secure Config Summary Utility v0.1")
st.markdown("""
    This tool should interpret and produce a summary output of some well known tools
    aligned with the ACSC ISM. Load csv files below for interpretation.
""")

config_tab, results_tab = st.tabs(["Upload & Configure", "View Results"])

csvfiles = config_tab.file_uploader("Please upload CSVs to interpret", accept_multiple_files=True, type={"csv"})

csvs = []
for inputfile in csvfiles:
    csvs.append(pd.read_csv(inputfile))

base_cols = ["Strategy", "Source", "Description", "Scope", "Assessment", "AssessmentDetail"]
df = pd.DataFrame(columns=base_cols)

strategies = {
    "Application control": "exec",
    "Patch applications": "",
    "Configure Microsoft Office macro settings": "",
    "User application hardening": "",
    "Restrict administrative privileges": "",
    "Patch operating systems": "",
    "Multi-factor authentication": "",
    "Regular backups": "",
    "Server application hardening": "",
    "Block spoofed emails": "",
    "Network segmentation": "",
    "Continuous incident detection and response": "",
    "Personnel management": ""
}

config_tab.header("Assessment filters")
col1, col2 = config_tab.columns(2)
strategy = col1.selectbox(f"ACSC Strategies to Mitigate ({len(strategies)})", strategies.keys())
strategies[strategy] = col2.text_input("Description filter regex", value=strategies[strategy])

for csv in csvs:
    if (csv.columns[:3].str.lower() == ["rank", "recommended action", "score impact"]).all():
        csv["Source"] = "Microsoft 365 Recommendations"
        csv["Description"] = csv["Recommended action"]
        csv["Scope"] = csv.agg('{0[Product]} ({0[Category]})'.format, axis=1)
        csv["Assessment"] = csv.agg('{0[Status]} ({0[Points achieved]})'.format, axis=1)
        csv["AssessmentDate"] = csv.filter(like='synced')
    elif (csv.columns[:3].str.lower() == ["actualvalue", "commandlet", "control"]).all():
        csv["Source"] = "CISA ScubaGear Baseline"
    elif (csv.columns[:3].str.lower() == ["exportedtimestamp", "subscriptionid", "subscriptionname"]).all():
        csv["Source"] = "Microsoft Azure Recommendations"
        csv["Description"] = csv.agg('{0[controls]} - {0[recommendationDisplayName]}'.format, axis=1)
        csv = csv.groupby(["Description", "severity", "state"]).size()
    elif (csv.columns[:3].str.lower() == ["tested system", "test timestamp", "mitigation strategy"]).all():
        csv["Source"] = "ACSC E8MVT"
    else:
        continue
    df = pd.concat([df, csv]).reset_index(drop=True)


results_tab.markdown(f"Loaded {', '.join(df.Source.unique())}")

config_tab.header(f"Source Data ({len(df)} rows)")
config_tab.dataframe(df[base_cols[1:5]], use_container_width=True, hide_index=True)

for strategy, regex in strategies.items():
    if not regex:
        continue
    try:
        df.loc[df['Description'].str.contains(regex, case=False), 'Strategy'] = strategy
    except Exception as e:
        results_tab.write(e)
        continue
    strategydf = df[df["Strategy"] == strategy]
    results_tab.header(f"{strategy} ({len(strategydf)})")
    results_tab.dataframe(strategydf, use_container_width=True, hide_index=True)

results_tab.download_button(
    "Download Summary",
    df[base_cols].dropna(subset = ['Strategy']).to_csv(index=False).encode('utf-8'),
    f"secureconfigsummary_{pd.Timestamp('today').date()}.csv",
    "text/csv",
    key='summary-csv'
)

results_tab.download_button(
    "Download Combined Source data",
    df.to_csv(index=False).encode('utf-8'),
    f"secureconfigsourcedata_{pd.Timestamp('today').date()}.csv",
    "text/csv",
    key='full-csv'
)