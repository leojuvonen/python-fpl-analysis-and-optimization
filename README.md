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


### Defenders

```python
top10_def = df[df["element_type"] == "DEF"].sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_def.index = range(1, len(top10_def) + 1)
markdown_table_def = top10_def[["full_name", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=False)
print(markdown_table_def)
```

|    | full_name                         |   total_points |   goals_scored |   assists |   clean_sheets |   now_cost |
|---:|:----------------------------------|---------------:|---------------:|----------:|---------------:|-----------:|
|  1 | Joško Gvardiol                    |            153 |              5 |         0 |             13 |         65 |
|  2 | Trent Alexander-Arnold            |            148 |              3 |         7 |             12 |         72 |
|  3 | Nikola Milenković                 |            145 |              5 |         2 |             13 |         52 |
|  4 | Virgil van Dijk                   |            143 |              3 |         1 |             14 |         67 |
|  5 | Daniel Muñoz                      |            142 |              4 |         6 |             11 |         52 |
|  6 | Milos Kerkez                      |            134 |              2 |         6 |              9 |         53 |
|  7 | Marc Cucurella Saseta             |            133 |              5 |         2 |              9 |         54 |
|  8 | William Saliba                    |            130 |              2 |         0 |             12 |         64 |
|  9 | Murillo Santiago Costa dos Santos |            130 |              2 |         0 |             12 |         47 |
| 10 | Ola Aina                          |            128 |              2 |         1 |             12 |         53 |

### Midfielders

```python
top10_mid = df[df["element_type"] == "MID"].sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_mid.index = range(1, len(top10_mid) + 1)
markdown_table_mid = top10_mid[["full_name", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=True)
print(markdown_table_mid)
```
|    | full_name              |   total_points |   goals_scored |   assists |   clean_sheets |   now_cost |
|---:|:-----------------------|---------------:|---------------:|----------:|---------------:|-----------:|
|  1 | Mohamed Salah          |            344 |             29 |        18 |             15 |        136 |
|  2 | Bryan Mbeumo           |            236 |             20 |         9 |              9 |         83 |
|  3 | Cole Palmer            |            214 |             15 |        10 |             10 |        105 |
|  4 | Jarrod Bowen           |            193 |             13 |        11 |              8 |         79 |
|  5 | Luis Díaz              |            183 |             13 |         7 |             15 |         75 |
|  6 | Bruno Borges Fernandes |            174 |              8 |        12 |             10 |         84 |
|  7 | Antoine Semenyo        |            165 |             11 |         7 |             11 |         57 |
|  8 | Morgan Rogers          |            161 |              8 |        11 |             10 |         58 |
|  9 | Jacob Murphy           |            159 |              8 |        13 |             11 |         52 |
| 10 | Justin Kluivert        |            158 |             12 |         6 |             13 |         59 |

### Forwards

```python
top10_fwd = df[df["element_type"] == "FWD"].sort_values(by="total_points", ascending=False).head(10).reset_index(drop=True)
top10_fwd.index = range(1, len(top10_fwd) + 1)
markdown_table_fwd = top10_fwd[["full_name", "total_points", "goals_scored", "assists", "clean_sheets", "now_cost"]].to_markdown(index=True)
print(markdown_table_fwd)
```
|    | full_name                        |   total_points |   goals_scored |   assists |   clean_sheets |   now_cost |
|---:|:---------------------------------|---------------:|---------------:|----------:|---------------:|-----------:|
|  1 | Alexander Isak                   |            211 |             23 |         6 |             12 |         94 |
|  2 | Chris Wood                       |            200 |             20 |         3 |             15 |         72 |
|  3 | Ollie Watkins                    |            186 |             16 |         8 |             10 |         92 |
|  4 | Yoane Wissa                      |            185 |             18 |         6 |              9 |         69 |
|  5 | Erling Haaland                   |            181 |             22 |         3 |             10 |        149 |
|  6 | Matheus Santos Carneiro Da Cunha |            178 |             15 |         7 |              7 |         70 |
|  7 | Jean-Philippe Mateta             |            150 |             14 |         2 |              9 |         75 |
|  8 | Raúl Jiménez                     |            147 |             12 |         3 |              7 |         53 |
|  9 | Jørgen Strand Larsen             |            145 |             14 |         4 |              7 |         52 |
| 10 | Liam Delap                       |            132 |             12 |         2 |              3 |         56 |


## Best Value for Cost
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

