###### FPL analysis

import pandas as pd

df = pd.read_csv("../data/cleaned_players.csv")

# add full_name variable for clarity and readibility of the tables
df["full_name"] = df["first_name"] + " " + df["second_name"]

print(df.head())

### top 10 players
top10_players = df.sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_players.index = range(1, len(top10_players) + 1)
markdown_table_top10 = top10_players[["full_name", "element_type", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=True)
print(markdown_table_top10)


# New variable: value for money (value)
df["value"] = df["total_points"]/df["now_cost"]

# Value for money
top10_qty = df[df["element_type"] != "AM"].sort_values(by="value", ascending=False).head(10).reset_index(drop=True)
top10_qty.index = range(1, len(top10_qty)+1)
markdown_table_qty = top10_qty[["full_name", "element_type", "total_points", "now_cost", "value"]].to_markdown(index=True)
print(markdown_table_qty)


#### Analyze the ICT - variables (influence, creativity and threat)

import statsmodels.api as sm
### regression
# influence
model_influence = sm.OLS(df[["total_points"]], df[["influence"]]).fit()
print(model_influence.summary())

# creativity
model_creativity = sm.OLS(df[["total_points"]], df[["creativity"]]).fit()
print(model_creativity.summary())

# threat
model_threat = sm.OLS(df[["total_points"]], df[["threat"]]). fit()
print(model_threat.summary())

# ict index
model_ict = sm.OLS(df[["total_points"]], df[["ict_index"]]).fit()
print(model_ict.summary())

# all variables
model_all = sm.OLS(df[["total_points"]], df[["influence", "creativity", "threat"]]).fit()
print(model_all.summary())


### Defenders
# goals/assists or clean sheets?
# create a variable that includes both goals and assists
df["goals_assists"] = df["goals_scored"] + df["assists"]
df_def = df[df["element_type"] == "DEF"]

# goals and assists - model
model_def_ga = sm.OLS(df_def[["total_points"]], df_def[["goals_assists"]]).fit()
print(model_def_ga.summary())

# clean sheet - model
model_def_cs = sm.OLS(df_def[["total_points"]], df_def[["clean_sheets"]]).fit()
print(model_def_cs.summary())

# both variables model
model_def_all = sm.OLS(df_def[["total_points"]], df_def[["goals_assists", "clean_sheets"]]).fit()
print(model_def_all.summary())






