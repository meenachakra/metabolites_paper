from fuzzywuzzy import process
import pandas as pd

menni_df = pd.read_excel("Menni_Table_S2.xlsx")

microb_metab_df = pd.read_excel("Modified_Chen_Table_S3_Human_Metabolites_Tab.xlsx")

# List to store results
matched_results = []

# Iterate over each metabolite in menni_df
for metabolite in menni_df['Metabolite']:
	# Find the best match in microb_metab_df
	best_match_data = process.extractOne(metabolite, microb_metab_df['name'])
	best_match, score = best_match_data[0], best_match_data[1]

	matched_results.append((metabolite, best_match, score))

# Convert the results into a dataframe
matched_df = pd.DataFrame(matched_results, columns=['Original Name', 'Matched Name', 'Similarity Score'])

matched_df.to_csv('Menni_fuzzy_matches_to_microb_metab.txt', sep='\t', index=False)
