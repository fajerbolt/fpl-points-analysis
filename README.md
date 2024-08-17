# fpl-points-analysis
Analysing stats and cost of players from Fantasy Premier League 2023-24 season

### Topic
Focus of this analysis is to determine which stats brought the most points during the 2023-24 season of Fantasy Premier League, in order to give guidelines for building teams in the future. 

Fantasy Premier Leagues is a fantasy sports game centered around the English Premier League. It allows users to build teams, consisting of real Premier League players, who then earn points by achieving various statistical outcomes. 
When building a team a user has to make sure he picks players that will bring in most points, but also manage the budget and determine where he can spend or save. So, this analysis focuses on two main points that should help when constructing a team:
1. Determine which stats earn most points during the season for each position
2. Determine if it's worth spending the budget on more expensive players and in which situations

### Techniques Used
The two main questions were answered by comparing sources of points between top 10% of players and the rest by position, and by looking at the distribution of points relative to cost of the players.

### Findings Summary
1. Medium priced goalkeepers with high number of clean sheets are the best value
2. There is a big potential to save budget for other positions by going for defenders on teams that don't conced goals
3. Spending large portion of the budget on midfielders who score a lot of goals pays off
4. Finding low costing forwards who are in form could save money without losing out on points 

### Repo Structure
dataset.py file contains code used to preprocess the gathered data<br>
player_points.csv file contains the data used in analysis<br>
analysis_notebook.ipynb is the notebook with the analysis and the code used for it<br>
FPL 2023-24 Points Analysis.pdf is the final report<br>

### Data Source
This notebook contains some data manipulation of the processed data gathered from: https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/cleaned_players.csv
