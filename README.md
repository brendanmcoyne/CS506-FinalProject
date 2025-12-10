### CS506 Final Project — MLB Payroll vs Team Success

Author: Brendan Coyne

Final Presentation Link: 

### How to Build and Run the Code

This project includes a Makefile that installs dependencies, prepares the environment, runs the notebook, and executes the automated tests.

1. Clone the Repository
```bash
git clone <your-repo-url>
cd CS506-FinalProject
```

2. Build the environment
```bash
make setup
```

This will:

- Create a Python virtual environment (venv/)

- Install all dependencies from requirements.txt

3. Run the Project
```bash
make run
```

This command:

- Converts Graphs.ipynb → Graphs.py

- Executes the notebook from start to finish

- Generates all visualizations and stores outputs

4. Run the Tests
```bash
make test
```

This runs automated tests defined in test_model.py using pytest.


Automated Testing & GitHub Workflow

The project includes:

A file called test_model.py that helps to:

- Ensure the merged dataset is not empty

- Confirm Win% values are valid

- Verify payroll and standings year ranges

- Test linear regression can fit without errors

A GitHub Actions workflow (.github/workflows/tests.yml) runs automatically whenever code is pushed.

This ensures reproducibility and correctness of the core logic.

### Project Overview
Goal of Project:

To analyze whether higher payroll spending in Major League Baseball correlates with higher win percentage and playoff success. Success is measured using:

- Win percentage

- Playoff appearances

- Division titles

- World Series wins

This project explicitly studies correlation, not causation — spending more money does not cause success but may be associated with it.

### Data Sources
1. Payroll Data (2000–2015 and 2016–2025)

Scraped from SteveTheUmp / Spotrac-style reports showing:

- Team active roster payroll

- Payroll rank per season

2. Standings & Performance Data

Scraped from Pro Baseball Reference, including:

- Wins, losses, win percentage

- Division placement

- Playoff appearance

- Division win

- World Series win

Final Dataset Features

Each team-season includes:

- Year
  
- Team
  
- Wins, losses, and win percentage
  
- Playoffs	Binary (1 = playoffs, 0 = non-playoffs)
  
- DivisionWin	Binary
  
- WorldSeriesWin	Binary
  
- Payroll	Total
  
- Payroll Rank within league

Total rows per dataset: roughly 480 rows per era.

### Data Processing
Steps taken:

- Cleaned team names and standardized formatting
- Converted win percent strings to numeric
- Merged payroll and standings datasets

  
Created new features:
- Payroll Rank
- Binary outcome variables
- Removed or imputed missing values

Train/Test Split (Project Structure)

Training set: 2000–2015
Test set: 2016–2025

All model development + parameter tuning uses the training set

Evaluation and regression comparison use the test set

### Visualizations (Exploratory Data Analysis)

The notebook generates all of the following:

1. Win% vs Payroll (2000-2015, 2016-2025)

  Scatterplot colored by:

- Playoff appearance

- Division winner

- World Series winner

- Shows that elite payroll teams frequently outperform low-payroll clubs.

2. Payroll Rank vs Win% (2000-2015, 2016-2025)

  One for playoff teams, one for all teams.

  Reveals that high payroll rank (low number) correlates with higher playoff probability.

3. Box Plot for Division Winners vs Non-Division Winners (2000-2015, 2016-2025)

  Shows a slight increase in spending for division winners on average.

4. Regression Line (2000–2015 Training Set)

Shows a weak but positive correlation between payroll and win percentage.

5. Regression Line (2016–2025 Test Set)

Confirms a similar trend, validating that the relationship persists in modern baseball.

7. Cluster Analysis (K-Means)

Teams cluster into:

- High-payroll contenders

- Mid-market competitive teams

- Low-payroll over/underperformers


### Modeling

The project applies three modeling approaches.

1. Linear Regression

Goal: Estimate how strongly payroll predicts win percentage.

Model:
Wpct = β * Payroll + Intercept

Training Results (2000–2015):

Slope: Positive

R² ≈ small but nonzero (weak/moderate correlation)

Interpretation:
Higher payroll tends to increase win percentage, but many outliers exist.

2. Decision Tree Classifier

Target: Playoffs (1 = Yes, 0 = No)

Features:

- Payroll

- Payroll Rank

- Win Percentage

Metrics Reported:

- Precision

- Recall

- ROC–AUC

Findings:

Model identifies high-payroll teams as most playoff-likely. Low-payroll teams almost never predicted as playoff contenders.

3. K-Means Clustering (Unsupervised)

Features Used:

- Payroll

- Win Percentage

Clusters Identified:

- High-payroll, high-performance

- Mid-spending, average teams

- Low-payroll, low-performance

This visualization helps identify structural tiers in MLB spending.

### Results and Conclusions
Major Findings:
1. Payroll moderately correlates with win percentage

Correlation coefficient ~ 0.20, but meaningful trends emerge.

2. High payroll significantly increases playoff probability

Top-5 payroll teams make playoffs far more often than bottom-5 payroll teams.

3. Division winners and World Series winners are typically above median payroll

Champions rarely come from the league’s bottom payroll tier.

4. Modern MLB (2016–2025) confirms the trend

Regression slopes for the modern test set remain positive.

5. Payroll isn't an absolute for winning

Outliers exist, especially small-market teams with strong development pipelines.
