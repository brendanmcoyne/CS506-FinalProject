#!/usr/bin/env python
# coding: utf-8

# # MLB Payroll vs Team Success
# 
# This project analyzes whether MLB teams with higher payrolls experience greater on-field success. The notebook follows these steps:
# 
# - Loading payroll and standings datasets
# - Merging data (from 2 CSV files)
# - Exploratory visualizations
# - Modeling:
#   - Linear Regression
#   - Decision Tree Classification
#   - Clustering (K-Means)
# - Train evaluation using 2000–2015 data and 2016–2025 for testing
# - Interpretation of results
# 
# This notebook corresponds directly to the project proposal and midterm report.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# In[2]:


# Load payroll and standings CSVs
payroll = pd.read_csv("TestData/mlb_2000_2015_payrolls.csv")
standings = pd.read_csv("TestData/mlb_2000_2015_standings.csv")

# Merge in memory (dataset not saved to disk)
df = standings.merge(payroll, on=["Year", "Team"], how="left")

# Remove any missing payroll rows (only 1 missing in your data)
df = df.dropna(subset=["Payroll"])

df.head()


# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Load Data
standings = pd.read_csv("TestData/mlb_2000_2015_standings.csv")
payrolls = pd.read_csv("TestData/mlb_2000_2015_payrolls.csv")

standings = standings[standings["Team"] != "Tm"]

# Strip whitespace
payrolls["Team"] = payrolls["Team"].str.strip()

# Merge datasets
merged = pd.merge(standings, payrolls, on=["Year", "Team"], how="inner")
df = merged.copy()

merged["Wpct"] = merged["Wpct"].astype(str).apply(lambda x: float(x) if float(x) > 1 else float("0"+str(x)))
merged["Payroll"] = merged["Payroll"].astype(float)

def assign_color(row):
    if row["WorldSeriesWin"] == 1:
        return "yellow"
    elif row["DivisionWin"] == 1:
        return "blue"
    elif row["Playoffs"] == 1:
        return "green"
    else:
        return "red"

merged["Color"] = merged.apply(assign_color, axis=1)

# Plot
plt.figure(figsize=(14,8))
plt.scatter(merged["Payroll"], merged["Wpct"], color=merged["Color"], s=40, alpha=0.7)

plt.title("MLB 2000–2015: Payroll vs Win Percentage")
plt.xlabel("Team Payroll ($ in hundred millions)")
plt.ylabel("Win Percentage")
plt.grid(True)

# Add legend
legend_patches = [
    mpatches.Patch(color='yellow', label='World Series Win'),
    mpatches.Patch(color='blue', label='Division Win'),
    mpatches.Patch(color='green', label='Playoffs'),
    mpatches.Patch(color='red', label='No Playoffs')
]
plt.legend(handles=legend_patches, loc='lower right')

plt.tight_layout()
plt.show()


# In[4]:


import numpy as np
import matplotlib.pyplot as plt

# Extract variables
X = df["Payroll"].values
y = df["Wpct"].values

# Fit regression using numpy
coef, intercept = np.polyfit(X, y, 1)
reg_line = coef * X + intercept

# Plot
plt.figure(figsize=(14,8))
plt.scatter(X, y, alpha=0.6, s=40, color="gray", label="Teams (2000–2015)")

# Add regression line
plt.plot(X, reg_line, color="red", linewidth=2.5, label=f"Regression Line (slope={coef:.2e})")

plt.title("MLB 2000–2015: Payroll vs Win Percentage with Regression Line")
plt.xlabel("Team Payroll ($ in hundred millions)")
plt.ylabel("Win Percentage")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# In[5]:


import seaborn as sns

plt.figure(figsize=(10,6))
sns.boxplot(data=df, x="DivisionWin", y="Payroll")
plt.xlabel("Division Win (0 = No, 1 = Yes)")
plt.ylabel("Payroll ($)")
plt.title("Payroll Distribution for Division Winners vs Non-Winners")
plt.grid(True)
plt.show()


# ### 2. Linear Regression — Relationship Between Payroll and Win Percentage
# 
# This section answers the research question:
# 
# “Does spending more money correlate with better performance?”
# 
# We model win percentage (Wpct) as a function of team payroll.
# 
# A positive coefficient indicates that increases in payroll are associated with increases in win percentage.
# The R² score shows how much of team success payroll can explain.

# In[6]:


# Linear Regression: Wpct ~ Payroll
X = df[["Payroll"]]
y = df["Wpct"]

lr = LinearRegression()
lr.fit(X, y)

print("Linear Regression Coefficient (Payroll → Win%):", lr.coef_[0])
print("Intercept:", lr.intercept_)
print("R² Score:", lr.score(X, y))


# ### Interpretation
# 
# Preliminary results show:
# 
# A small but positive regression coefficient
# 
# R² ≈ 0.10
# 
# This means payroll explains about 10% of the variation in win percentage across MLB teams (2000–2015).
# 
# Higher payroll teams tend to perform slightly better, but payroll alone does not guarantee success.
# 
# This supports the project’s hypothesis of correlation but not causation.

# ### 3. Decision Tree Classification — Predicting Playoff Appearance
# 
# This model predicts whether a team makes the playoffs based on:
# 
# Payroll
# 
# Payroll Rank
# 
# Win Percentage
# 
# The decision tree uses training data from 2000–2015 to learn what distinguishes playoff teams from non-playoff teams.

# In[7]:


# Features: payroll, payroll rank, win%
features = ["Payroll", "Rank", "Wpct"]
X2 = df[features]
y2 = df["Playoffs"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X2, y2, test_size=0.2, random_state=42
)

# Train tree
dt = DecisionTreeClassifier(max_depth=4)
dt.fit(X_train, y_train)

# Predictions + metrics
pred = dt.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, pred))

print("ROC-AUC:", roc_auc_score(y_test, dt.predict_proba(X_test)[:,1]))


# ### 4. K-Means Clustering — Grouping Teams by Payroll and Performance
# 
# Clustering visually groups teams with similar:
# 
# Payroll
# 
# Win percentage
# 
# This helps identify natural tiers in MLB economics:
# 
# Low-payroll teams
# 
# Mid-market teams
# 
# High-payroll contenders
# 
# Clustering is not a predictive model — it’s exploratory and reveals structural patterns in team spending.

# In[8]:


# Clustering features
Xc = df[["Payroll", "Wpct"]]

# Standardize data
scaler = StandardScaler()
Xc_scaled = scaler.fit_transform(Xc)

# 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
df["Cluster"] = kmeans.fit_predict(Xc_scaled)

df["Cluster"].value_counts()


# In[9]:


plt.figure(figsize=(10,6))
plt.scatter(df["Payroll"], df["Wpct"], c=df["Cluster"], cmap="viridis")

plt.xlabel("Team Payroll ($)")
plt.ylabel("Win Percentage")
plt.title("K-Means Clustering of MLB Teams (2000–2015)")
plt.grid(True)
plt.show()


# ### Interpretation
# 
# The clustering produces three clear groups:
# 
# Low payroll, low win%
# 
# Medium payroll, medium win%
# 
# High payroll, high win%
# 
# This reinforces the hypothesis that teams’ financial resources strongly influence their competitive tier.

# In[10]:


payroll_test = pd.read_csv("mlb_2016_2025_payrolls.csv")
standings_test = pd.read_csv("mlb_2016_2025_standings.csv")

test_df = standings_test.merge(payroll_test, on=["Year","Team"], how="left")
test_df = test_df.dropna(subset=["Payroll"])


# ### 6. Evaluating Model Performance on 2016–2025 Data
# 
# This section checks:
# 
# Whether payroll still predicts win percentage
# 
# Whether the decision tree still accurately predicts playoff appearances
# 
# This is essential for validating the model across time.

# In[11]:


X_test_lr = test_df[["Payroll"]]
y_test_lr = test_df["Wpct"]

test_r2 = lr.score(X_test_lr, y_test_lr)
print("Test Set R²:", test_r2)


# In[12]:


X_test_tree = test_df[["Payroll", "Rank", "Wpct"]]
y_test_tree = test_df["Playoffs"]

pred_test = dt.predict(X_test_tree)

print("Test Classification Report:")
print(classification_report(y_test_tree, pred_test))

print("Test ROC-AUC:", roc_auc_score(y_test_tree, dt.predict_proba(X_test_tree)[:,1]))


# ### 7. Conclusion
# 
# Across the analysis:
# 
# Payroll correlates weakly/moderately with win percentage
# 
# Payroll strongly relates to playoff probability (via decision tree)
# 
# Clustering naturally divides MLB teams into low-, mid-, and high-spending tiers
# 
# Testing on 2016–2025 confirms whether these patterns persist
# 
# Overall, spending more generally increases a team’s likelihood of success, but many outliers prove the correlation is far from perfect.
