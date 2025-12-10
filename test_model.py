import pandas as pd

def test_data_loads():
    payroll = pd.read_csv("TrainingData/mlb_2000_2015_payrolls.csv")
    standings = pd.read_csv("TrainingData/mlb_2000_2015_standings.csv")
    assert len(payroll) > 0
    assert len(standings) > 0

def test_required_columns():
    standings = pd.read_csv("TrainingData/mlb_2000_2015_standings.csv")
    required = ["Year", "Team", "W", "L", "Wpct"]
    for col in required:
        assert col in standings.columns

def test_merge():
    payroll = pd.read_csv("TrainingData/mlb_2000_2015_payrolls.csv")
    standings = pd.read_csv("TrainingData/mlb_2000_2015_standings.csv")
    merged = standings.merge(payroll, on=["Year", "Team"], how="left")
    assert len(merged) > 0
