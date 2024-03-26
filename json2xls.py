import pandas as pd
import json

BASE_PATH = '~/drive/copilot'

# INPUT = BASE_PATH + '/copilot-usage-data.json'
INPUT = 'copilot-usage-data.json'
OUTPUT = BASE_PATH + '/copilot-usage-data.xlsx'

# load the JSON data from file
print('Loading JSON data from: ' + INPUT)
with open(INPUT, 'r') as file:
    data_json = json.load(file)

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
print(totals_df)
print(breakdown_df)

# Creating an Excel file with two sheets
with pd.ExcelWriter(OUTPUT, engine='xlsxwriter') as writer:
    totals_df.to_excel(writer, sheet_name='Totals', index=False)
    breakdown_df.to_excel(writer, sheet_name='Detailed Data', index=False)
print('Saved to: ' + OUTPUT)

