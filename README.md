# CS506 Final Project

1. Project Description:
This project focuses on whether Major League Baseball teams are more successful if they spend more money on player salaries than other teams. By analyzing
historical financial records, win-loss records, and playoff performances, this project aims to identify correlations and patterns between payroll spending
and team success.

This project will explore correlation, not causation — spending more does not necessarily cause success, but may correlate with other factors such 
as franchise management quality, player development, or market size.

3. Goal:
My goals for this project are:
- To determine if teams have a higher chances of making the playoffs if they spend more money.
- To determine if there's a correlation between winning the division and teams spending more money.
- To determine if there's a correlation between winning the World Series and teams spending more money.
- To identify and visualize trends in team payroll versus performance across time.
- To explore which features (e.g., average player salary, payroll rank, team market size, etc.) best predict playoff or division outcomes.

3. Data Collection:
For this, I would need to collect data by:
- Scraping from websites like Spotrac in order to get every teams amount of money spent each year. (Active Roster payroll) 
- Scraping off of Pro Baseball Reference in order to get their record, division placement, and performance each year in the playoffs.

The data will be scraped and downloaded into CSV files for analysis. Data cleaning steps will include handling missing data and creating new features 
such as payroll rank and payroll-to-league-average ratio.

4. Modeling:
To model the data, I will use:
- Linear regression models to display teams payroll and team record per year.
- Decision Tree models for binary outcomes such as playoff appearances or World Series wins.
- Clustering to identify groups of teams with similar payroll, winning percentage, and playoff success.

The metrics I will be using to measure accuracy will be Precision, Recall, and ROC-AUC.

6. Visualization:
I plan on using scatterplots to display my data, plotting the total money spent versus the number of wins each year. I may try and use
an interactive plot team performance relative to their payroll over time. 

7. Test Plan:
My goal is to train on the years 2000-2015, and then test in 2016-2025. I will be cross validating within the training data to tune model parameters.
October will be using for data collection, clean, and beginning visualization. November will be for extraction, modeling, and analysis. December will
be for model evaluation and any refinements. 
