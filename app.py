import streamlit as st
import pandas as pd
import json
from io import BytesIO

def from_json(data_json):
    totals_data = []
    breakdown_data = []

    # Loop through each day's data
    for day_data in data_json:
        day = day_data["day"]
        total_suggestions_count = day_data["total_suggestions_count"]
        total_acceptances_count = day_data["total_acceptances_count"]
        total_lines_suggested = day_data["total_lines_suggested"]
        total_lines_accepted = day_data["total_lines_accepted"]
        total_active_users = day_data["total_active_users"]

        totals_row = {
            "Date": day,
            "Total Suggestions Count": total_suggestions_count,
            "Total Acceptances Count": total_acceptances_count,
            "Total Lines Suggested": total_lines_suggested,
            "Total Lines Accepted": total_lines_accepted,
            "Total Active Users": total_active_users
        }
        totals_data.append(totals_row)

        for breakdown in day_data["breakdown"]:
            row = {
                "Date": day,
                "Language": breakdown["language"],
                "Editor": breakdown["editor"],
                "Suggestions Count": breakdown["suggestions_count"],
                "Acceptances Count": breakdown["acceptances_count"],
                "Lines Suggested": breakdown["lines_suggested"],
                "Lines Accepted": breakdown["lines_accepted"],
                "Active Users": breakdown["active_users"]
            }
            breakdown_data.append(row)

    # Convert to DataFrame
    totals_df = pd.DataFrame(totals_data)
    breakdown_df = pd.DataFrame(breakdown_data)
    return totals_df, breakdown_df

def to_excel(totals_df, breakdown_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        totals_df.to_excel(writer, sheet_name='Totals', index=False)
        breakdown_df.to_excel(writer, sheet_name='Detailed Data', index=False)

    # Get the byte string of the Excel file
    processed_data = output.getvalue()
    return processed_data

st.title('GitHub Copilot Usage Data')

st.write('This tool converts JSON data to an Excel file')

input_file = st.file_uploader('Upload json file',type='json')
if input_file is not None:
    data_json = json.load(input_file)  

    totals_df, breakdown_df = from_json(data_json)

    st.write('Total Data')
    st.dataframe(
        totals_df,
        hide_index=True,
        width=1300,
    )

    st.write('Detailed Data')
    st.dataframe(
        breakdown_df,
        hide_index=True,
        width=1300,
    )

    excel_file = to_excel(totals_df, breakdown_df)
    st.download_button(
        label='Download Excel file',
        data=excel_file,
        file_name='copilot-usage-data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
