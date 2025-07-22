import pandas as pd

df = pd.read_csv("C:/Users/Leo/OneDrive/Documents/koodausta/data/cleaned_players.csv")
df["full_name"] = df["first_name"] + " " + df["second_name"]

# we will get the prices of 25/26 season and add them to the dataframe as new_cost
# note: we wont be able to assess new players because they wont have values in the total_points variable from last season

import requests as rq

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = rq.get(url).json()

new_df = pd.DataFrame(data["elements"])
new_df = new_df[["first_name", "second_name", "now_cost", "team", "element_type"]]
new_df['new_cost']=new_df['now_cost']
new_df["position"] = new_df["element_type"]
new_df["full_name"]=new_df["first_name"]+ " " + new_df["second_name"]

# remove accents from names to allow easier merging of dataframes
import unicodedata

def remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return nfkd.encode("ASCII", "ignore").decode("ASCII")

new_df["full_name"] = new_df["full_name"].apply(remove_accents)

# add total_points to new_df
df_unique = df.drop_duplicates(subset="full_name")
new_df = new_df.merge(
    df_unique[["full_name", "total_points"]],
    how="left",
    on="full_name"
)


print(new_df)

### optimization

import pulp

# we will omit players that have left the league and don't have a new_cost variable
# we will also omit players who are new or for other reasons do not have total_points from previous season

new_df = new_df.dropna(subset=["new_cost"]).reset_index(drop=True)
new_df = new_df.dropna(subset=["total_points"]).reset_index(drop=True)


n_players = len(new_df)

# optimization problem
prob =pulp.LpProblem("FPL_Selection", pulp.LpMaximize)

# create selection variables
x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(n_players)]

# objective function (maximize total points)
prob += pulp.lpSum(new_df.loc[i, "total_points"]*x[i] for i in range(n_players))

# max 15 players
prob += pulp.lpSum(x) == 15 

# positional restrictions (1=GK, 2=DEF, 3=MID, 4=FWD)
for pos, req in [(1, 2), (2, 5), (3, 5), (4, 3)]:
    prob += pulp.lpSum(x[i] for i in range(n_players) if new_df.loc[i, "position"] == pos) == req

# bucject constraint
prob += pulp.lpSum(new_df.loc[i, "new_cost"] * x[i] for i in range(n_players)) <= 1000

# 3 players per team max
teams = new_df["team"].unique()
for team in teams:
    prob += pulp.lpSum(x[i] for i in range (n_players) if new_df.loc[i, "team"] == team) <= 3

prob.solve()
print("Status:", pulp.LpStatus[prob.status])

selected_indices = [
    i
    for i in range(n_players)
    if x[i].value() == 1          # or x[i].varValue == 1
]

# build a dataframe of your chosen squad
df_selected_max = new_df.loc[
    selected_indices,
    ["second_name", "position", "team", "new_cost", "total_points"]
].reset_index(drop=True)

print(df_selected_max)
# table


# to markdown
markdown_table_optimized = df_selected_max[["full_name", "element_type", "team", "new_cost", "total_points"]].to_markdown(index=True)
print(markdown_table_optimized)


### must change positions
