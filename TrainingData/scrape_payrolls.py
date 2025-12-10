import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_steve_the_ump():
    url = "https://www.stevetheump.com/Payrolls.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    all_data = []

    tables = soup.find_all("table")
    for table in tables:
        prev_text = table.find_previous(["b", "h3", "h2"])
        if prev_text:
            match = re.search(r'(\d{4})', prev_text.get_text())
            if match:
                year = int(match.group(1))
            else:
                continue
        else:
            continue

        for tr in table.find_all("tr"):
            cols = tr.find_all("td")
            if len(cols) >= 2:
                team = cols[0].get_text(strip=True)
                payroll = cols[1].get_text(strip=True)
                if not team or not payroll:
                    continue
                if "League Avg" in team or "Top ML Player" in team or "Totals" in team:
                    continue
                all_data.append({"Year": year, "Team": team, "Payroll": payroll})

    df = pd.DataFrame(all_data)

    df['Payroll'] = df['Payroll'].replace('[\$,]', '', regex=True)
    df['Payroll'] = pd.to_numeric(df['Payroll'], errors='coerce')
    df = df.dropna(subset=['Payroll'])

    df = df[(df['Year'] >= 2000) & (df['Year'] <= 2015)]

    expected_teams = 30
    for y in range(2000, 2016):
        count = len(df[df['Year'] == y])
        if count < expected_teams:
            print(f"Warning: Year {y} only has {count} teams.")

    return df

payroll_df = scrape_steve_the_ump()
payroll_df.to_csv("mlb_2000_2015_payrolls.csv", index=False)
print("Saved payroll data to mlb_2000_2015_payrolls.csv")
print(payroll_df.head(20))
