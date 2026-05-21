import pandas as pd

# Load the Excel file
df = pd.read_excel("Dunn_Supp_Material_2_AGE_tab.xlsx")

# Initialize a list to store the consolidated data
consolidated_data = []

# Iterate over the dataframe to find blocks with the specified structure
for idx in range(len(df) - 2):  # Subtract 2 to avoid going out of bounds during the subsequent checks
    # Check for the structure
    if "_age.g2" in str(df.iloc[idx][0]) and df.iloc[idx+1][1] == "diff":
        # Extract the data
        metabolite_name = df.iloc[idx][0].split("_age.g2")[0]
        diff_value = df.iloc[idx+2][1]
        lwr_value = df.iloc[idx+2][2]
        upr_value = df.iloc[idx+2][3]
        p_adj_value = df.iloc[idx+2][4]
        consolidated_data.append([metabolite_name, diff_value, lwr_value, upr_value, p_adj_value])

# Convert the list to a dataframe
consolidated_df = pd.DataFrame(consolidated_data, columns=["Metabolite", "Diff between groups", "Lwr", "Upr", "P adj"])

consolidated_df.to_csv('reformatted_dunn_supp_mat_2.txt', sep='\t', index=False)

