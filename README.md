# CS506 Midterm Report

1. Preliminary Visualizations of Data
I created several visualizations to explore the relationship between team payroll and on-field performance from 2000–2015.

1. Win% vs Payroll (2000 and 2015)

- Scatterplots showing each team’s winning percentage versus total payroll for the years 2000 and 2015.
- These plots illustrate how the league’s payroll landscape and win distributions have changed over time.

2. Win% vs Payroll (2000–2015, All Teams)

- Scatterplot of all teams from 2000–2015.
- Each point is color-coded based on whether the team made the playoffs, won their division, or won the World Series.

This helps visualize whether higher payrolls are associated with postseason success.

3. Payroll Rank vs Win%

- Two scatterplots: one including all teams, and one including only playoff teams.
- These visualizations highlight whether top payroll rankings correspond to higher win percentages.

4. Team-Specific Trend 

- Two plots showing payroll vs win% and payroll rank vs win% for one specific team from 2000–2015.
- This helps analyze whether the league-wide correlation between payroll and success holds true for an individual franchise.

2. Data Processing

- Data was collected and cleaned using Python scraping functions.

Data Sources:
SteveTheUmp: Active roster payroll data for all MLB teams (2000–2015).
Pro Baseball Reference: Team win–loss records, division placements, and postseason results.

All data was saved into CSV files. 

Data Cleaning Steps:

Combined datasets by year and team name.
Handled missing data (e.g., removed incomplete seasons).
Updated team names to present day for consistency 
Created new features:
Payroll Rank (rank within league for that season)
Binary playoff/division/World Series win indicators
Normalized key numeric fields for modeling.

Final Dataset:

~480 total team-seasons (30 teams × 16 years).

Columns include: Team, Year, Payroll, Payroll_Rank, Win_Percentage, Made_Playoffs, Won_Division, Won_WS


3. Data Modeling Methods

So far, the focus of the project has been on exploratory data analysis (EDA) and visualization to identify potential relationships between team payroll and success metrics.

Work Completed to Date

Conducted visual analysis through scatterplots of payroll vs. win percentage for 2000 and 2015.

Created a combined scatterplot (2000–2015) showing all teams, color-coded by playoff/division/World Series outcomes.

Generated payroll rank vs win% graphs (for all teams and for playoff teams only).

Produced team-specific visualizations to see whether the overall correlation holds for a single franchise.

Planned Modeling Approaches

In the next phase (November–December), I plan to implement the following models using scikit-learn:

Linear Regression

To quantify the correlation between Payroll, Payroll Rank, and Win Percentage.

Will help determine how much payroll explains variation in win%.

Decision Tree Classifier (Planned)

To predict binary outcomes such as playoff appearances or division wins.

Evaluation metrics will include Precision, Recall, and ROC-AUC.

Clustering (Planned)

To identify natural groupings (“spending tiers”) of teams based on Payroll, Win Percentage, and Playoff Success.

4. Preliminary Results

League-Wide Findings:

There is a clear positive correlation between payroll and win percentage.

Most playoff and World Series teams fall within the top half of payroll rankings.

However, several outliers demonstrate that success is possible without top spending (e.g., smaller-market teams performing above expectations).

Team-Specific Findings for Boston Red Sox:

The relationship between payroll and win% for the Boston Red Sox is moderate.

Certain seasons show that even with below-average payroll, [Team Name] achieved above-average success, indicating factors beyond payroll (such as player development or management quality) can influence results.

Quantitative Insights:

Pearson correlation between payroll and win%: r = .20

Average payroll of playoff teams: $[value]M vs non-playoff teams $[value]M.