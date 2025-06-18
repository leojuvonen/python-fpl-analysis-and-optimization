# python-fantasy-football-analysis

This project shows my journey into learning Python for data analysis using football data from Fantasy Premier League. I explore the significance of various variables within the dataset.

## Overview
The project consists of the tabulation of players in different positions. We'll also examine the top players in terms on price to total points ratio, influence, creativity and threat (ICT). 
Then we will analyze which of the ICT-variables predict total points the best, meaning which one of them is the most essential to look at. Then the age old question of, whether defenders should be picked based on goals and assists or clean sheets, will be assessed. 

## Tools
The tool used in this project is Python. This analysis is mainly designed to help me familiarize myself with Python and it's capabilities in data analysis. The packages used are pandas, statsmodels and matplotlib.

## Data source
The data used in this analysis is from vaastav's Github: https://github.com/vaastav/Fantasy-Premier-League/

## Project structure
<code>  python-fantasy-football-analysis/
  ├── data/ # Sample or anonymized datasets 
  ├── scripts/ # R scripts used in the analysis 
  ├── images/ # output plots
  ├── fpl_analysis.py
  └── README.md # Project overview and usage instructions </code> </code></pre>

## Requirements 

This project uses the following Python packages:

- pandas
- matplotlib
- statsmodels

You can install them using:

```bash
pip install pandas matplotlib statsmodels
```
## Top Performers

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

Next we'll repeat with each position.

### Goalkeepers

```python
top10_gk = df[df["element_type"] == "GK"].sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_gk.index = range(1, len(top10_gk) + 1)
markdown_table_gk = top10_gk[["full_name", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=True)
print(markdown_table_gk)

```
|    | full_name                |   total_points |   goals_scored |   assists |   clean_sheets |   now_cost |
|---:|:-------------------------|---------------:|---------------:|----------:|---------------:|-----------:|
|  1 | Jordan Pickford          |            158 |              0 |         1 |             12 |         52 |
|  2 | Matz Sels                |            150 |              0 |         1 |             13 |         52 |
|  3 | David Raya Martin        |            142 |              0 |         0 |             13 |         56 |
|  4 | Mark Flekken             |            138 |              0 |         2 |              7 |         45 |
|  5 | Dean Henderson           |            135 |              0 |         0 |             11 |         46 |
|  6 | Robert Sánchez           |            126 |              0 |         0 |             10 |         45 |
|  7 | André Onana              |            120 |              0 |         0 |              9 |         49 |
|  8 | Bernd Leno               |            115 |              0 |         2 |              5 |         50 |
|  9 | Alisson Ramses Becker    |            112 |              0 |         0 |             10 |         55 |
| 10 | Emiliano Martínez Romero |            111 |              0 |         0 |              8 |         50 |
