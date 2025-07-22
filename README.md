# python-fantasy-football-analysis

This project shows my journey into learning Python for data analysis using football data from Fantasy Premier League. I explore the significance of various variables within the dataset.

## Table of Contents

- [Overview](#overview)
- [Tools](#tools)
- [Data Source](#data-source)
- [Requirements](#requirements)
- [Analysis](#analysis)
  - [Top Performers](#top-performers)
  - [Best Value for Cost](#best-value-for-cost)
  - [Influence, Creativity and Threat](#influence-creativity-and-threat)
  - [Defenders: Attack or Defence](#defenders-attack-or-defence)
- [Optimization](#optimization)
- [Notes](#notes)


## Overview
The project consists of the analysis of premier league players in the context of Fantasy Premier League, where players are given points depending on actions in games like goals scored, assists or clean sheets. The top players will be assessed terms on price to total points ratio, influence, creativity and threat (ICT).

The analysis will start by assessing which of the ICT-variables predict total points the best, meaning which one of them is the most essential to look at when choosing a player for your FPL-team. Then the age old question of, whether defenders should be picked based on goals and assists or clean sheets, will hopefully be answered. 

Lastly three approaches for optimizing a team will be conducted. The first approach is to maximize the full 15 player squad. The second approach will be to only maximize the points of the players that are on the field, minimizing any wasted points on the bench. Lastly a hybrid where there will be some efficient players on the bench in case of injurys, but the main focus is on the players that will be on the field.

## Tools
The tool used in this project is Python. This analysis is mainly designed to help me familiarize myself with Python and it's capabilities in data analysis. The packages used are pandas, statsmodels, requests, unicodedata and pulp.

## Data Source
The data used in this analysis is from vaastav's Github: https://github.com/vaastav/Fantasy-Premier-League/

## Requirements 

This project uses the following Python packages:

- pandas
- statsmodels
- requests
- unicodedata
- pulp

You can install them using:

```console
pip install pandas statsmodels requests unicodedata pulp
```
## Analysis

The code for this section is provided as fpl_analysis.py.

### Top Performers

First let's simply determine the ten top players in FPL in the 24/25 season. 

```python
import pandas as pd
# add full_name variable for clarity and readibility of the tables
df["full_name"] = df["first_name"] + " " + df["second_name"]

top10_players = df.sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_players.index = range(1, len(top10_players) + 1)
markdown_table_top10 = top10_players[["full_name", "element_type", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=True)
print(markdown_table_top10)

```

|    | full_name      | element_type   |   total_points |   goals_scored |   assists |   clean_sheets |   now_cost |
|---:|:---------------|:---------------|---------------:|---------------:|----------:|---------------:|-----------:|
|  1 | Mohamed Salah  | MID            |            344 |             29 |        18 |             15 |        136 |
|  2 | Bryan Mbeumo   | MID            |            236 |             20 |         9 |              9 |         83 |
|  3 | Cole Palmer    | MID            |            214 |             15 |        10 |             10 |        105 |
|  4 | Alexander Isak | FWD            |            211 |             23 |         6 |             12 |         94 |
|  5 | Chris Wood     | FWD            |            200 |             20 |         3 |             15 |         72 |
|  6 | Jarrod Bowen   | MID            |            193 |             13 |        11 |              8 |         79 |
|  7 | Ollie Watkins  | FWD            |            186 |             16 |         8 |             10 |         92 |
|  8 | Yoane Wissa    | FWD            |            185 |             18 |         6 |              9 |         69 |
|  9 | Luis Díaz      | MID            |            183 |             13 |         7 |             15 |         75 |
| 10 | Erling Haaland | FWD            |            181 |             22 |         3 |             10 |        149 |

These are the players that provide the most points in the Premier League on FPL. However, you can't have all of them because the budget constraint of 100. Next, we will assess which players can provide most points for a more modest price.

Note that the price in the dataset is presented without decimal points (136=13.6).


### Best Value for Cost
Let's create a new variable ("value") which represents the value for money a player provides. 

```python
df["value"] = df["total_points"]/df["now_cost"]
```

Now let's create a table of the top 10 players that provided the best value. We'll exclude the managers.

```python
top10_qty = df[df["element_type"] != "AM"].sort_values(by="value", ascending=False).head(10).reset_index(drop=True)
top10_qty.index = range(1, len(top10_qty)+1)
markdown_table_qty = top10_qty[["full_name", "element_type", "total_points", "now_cost", "value"]].to_markdown(index=True)
print(markdown_table_qty)
```
|    | full_name       | element_type   |   total_points |   now_cost |   value |
|---:|:----------------|:---------------|---------------:|-----------:|--------:|
|  1 | Mark Flekken    | GK             |            138 |         45 | 3.06667 |
|  2 | Jacob Murphy    | MID            |            159 |         52 | 3.05769 |
|  3 | Jordan Pickford | GK             |            158 |         52 | 3.03846 |
|  4 | Dean Henderson  | GK             |            135 |         46 | 2.93478 |
|  5 | Antoine Semenyo | MID            |            165 |         57 | 2.89474 |
|  6 | Alex Iwobi      | MID            |            156 |         54 | 2.88889 |
|  7 | Matz Sels       | GK             |            150 |         52 | 2.88462 |
|  8 | Enzo Fernández  | MID            |            135 |         47 | 2.87234 |
|  9 | Bryan Mbeumo    | MID            |            236 |         83 | 2.84337 |
| 10 | Kevin Schade    | MID            |            149 |         53 | 2.81132 |

These are players that can give the team the most points for a lower cost according to the 24/25 season. 


### Influence, Creativity and Threat

Strictly looking at the goals scored, assists or clean sheets is of course the safest way of assessing a player's value in terms of FPL points. But in order to look for a competetive advantage, it could be useful to use less obvious metrics, that may provide information on long term effectiviness that isn't as apparent as goals etc. 
For example, these variables could be Influence, Creativity and Threat. There is also the ICT-index that contains all these variables. Let's test the predictive value of all these variables, and which should be given the most weight. 

The analysis will be conducted with Ordinary Least Squares (OLS) -regression, which will shine a light on which of these variables predict the amout of fpl-points the most.

All the variables will have their univariate models and the last model will include all the ICT variables.

```python
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

```
The results:

| Variable        | model_influence | model_creativity| model_threat | model_ict    | model_all |
| --------------- | ------------- | ------------- | ------------- | ------------- | ------------|
| Influence       | 0.1733\*\*\* | -               |-               |   -           |   0.1197\*\*\*    |
|                 | (0.002)       |                |              |                |      (0.003)       |
| Creativity      | -             | 0.1973\*\*\* |  -              |    -            |    0.0267\*\*\*        |
|                 |               | (0.005)      |                 |                |     (0.005)       |
| Threat          | -             | -             | 0.2004\*\*\* | -               |     0.0612\*\*\*       |
|                 |               |                | (0.005)      |                 |      (0.004)      |
| ICT-index       | -             | -             | -               | 0.7367\*\*\* |     -       |
|                 |               |                 |               | (0.009)      |            |
| **$R^2$**           | 0.870         | 0.699         | 0.711         | 0.891         | 0.913      |

---

* (*): Statistically significant at 90% level  
* (**): Statistically significant at 95% level  
* (***): Statistically significant at 99% level  

The regression results show that out of all the individual variables, the Threat first looks like the biggest contributor to total points. The coefficient is the largest and it is statistically significant. After all of the variables are included in the model in model_all, it seems that Influence has the greatest impact. 
None of the individual variables however can hold a candle to the ICT-index which has by far the greatest impact of total points according to these regressions. 

The main giveaway is that Influence seems to be the most prominent  variable when the other ICT-variables are controlled. Still, the ICT-index is by far more relevant.

### Defenders: Attack or Defence?

All FPL-managers face this dilemma when considering which defenders to include in their team. Should they prioritize the strength of the team's defence, or the potential for goal contributions?

Let's start by creating a variable that holds goals scored and assists. This way we can examine goal contributions' effect instead of one or the another. We will also create a new dataframe that only has the players who are classified as defenders by FPL.

```python
df["goals_assists"] = df["goals_scored"] + df["assists"]
df_def = df[df["element_type"] == "DEF"]
```

Next we will construct regression models for how goal contributions and clean sheet predict total points. The third model includes both models.

```python
# goals and assists - model
model_def_ga = sm.OLS(df_def[["total_points"]], df_def[["goals_assists"]]).fit()
print(model_def_ga.summary())

# clean sheet - model
model_def_cs = sm.OLS(df_def[["total_points"]], df_def[["clean_sheets"]]).fit()
print(model_def_cs.summary())

# both variables model
model_def_all = sm.OLS(df_def[["total_points"]], df_def[["goals_assists", "clean_sheets"]]).fit()
print(model_def_all.summary())

```

The results:

| Variable        | model_def_ga | model_def_cs| model_def_all | 
| --------------- | ------------- | ------------- | ------------- | 
| goals_assits       | 19.0482\*\*\* | -               |5.9643\*\*\*      |
|                 | (0.703)       |                |   (0.337)           |
| clean_sheets      | -             | 11.7244\*\*\* |  9.2442\*\*\*        | 
|                 |               | (0.173)      |    (0.183)            |
| **$R^2$**           | 0.733         | 0.945         | 0.975         | 

---

* (*): Statistically significant at 90% level  
* (**): Statistically significant at 95% level  
* (***): Statistically significant at 99% level  

At first glance, goal contributions (goals and assisits) seems to have a bigger impact. The coefficient is larger and it is statistically significant. The $R^2$ however is lower than with the clean sheets - model. After including both variables to the model, it is also apparent that clean sheets are more impactful when predicting total points. This can be seen by the change in the coefficient's relative size and also by the $R^2$ value.

Both variables are still important to consider. The optimal allocation of attacking and defending can be interpreted as being $\frac{5.9643}{5.9643+9.2442} \approx 0.3922$ for attacking and $\frac{9.2442}{5.9643+9.2442} \approx 0.6078$ for defending, meaning that the importance of attacking is around 39% and defending is around 61%.

## Optimization

Optimization process starts by merging the previous dataframe's total_points variable into a new dataframe that includes the player's new prices for the 25/26 season. The new dataframe also includes updated positions and teams.

``` python
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
```

Next we will start the optimization.

```python
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

# budget constraint
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
```

The code will provide us with this group of players that will maximize total_points while staying under the 100(0) budget constraint.

|    | full_name         |   position |   team |   new_cost |   total_points |
|---:|:------------------|-----------:|-------:|-----------:|---------------:|
|  1 | Jordan Pickford   |          GK |      Everton |         55 |            158 |
| 2 | Matz Sels         |          GK |     Nottingham Forest |         50 |            150 |
| 3 | Ola Aina          |          DEF |     Nottingham Forest |         50 |            128 |
|  4 | Nathan Collins    |          DEF |      Brentford |         50 |            127 |
|  5 | Tyrick Mitchell   |          DEF |      Crystal Palace |         50 |            123 |
|6 | Aaron Wan-Bissaka |          DEF |     West Ham |         45 |            118 |
|  7 | Ezri Konsa Ngoyo  |          DEF |      Aston Villa |         45 |            103 |
|  8 | Mohamed Salah     |          MID |     Liverpool |        145 |            344 |
| 9 | Bryan Mbeumo      |          MID |      Manchester United |         80 |            236 |
|  10 | Antoine Semenyo   |          MID |      Bournemouth |         70 |            165 |
|  11 | Jacob Murphy      |          MID |     Newcastle |         65 |            159 |
|  12 | Alex Iwobi        |          MID |     Fulham |         65 |            156 |
| 13 | Chris Wood        |          FWD |     Nottingham Forest |         75 |            200 |
|  14 | Yoane Wissa       |          FWD |      Brentford |         75 |            185 |
| 15 | Jarrod Bowen      |          FWD |     West Ham |         80 |            193 |

It should be noted that this team would probably not be optimal because 4 players would have to be benched each gameweek. Depending on the fpl-manager's level of risk aversion and personal preference, bench player's could be selected separately to direct more funds towards outfield players. The level of this change would depend solely on the independent managers.

## Notes

The code used to generate these results was developed with the assistance of AI tools, specifically ChatGPT and Microsoft Copilot. 

