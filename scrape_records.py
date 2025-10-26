# mlb_standings_scrape_2000_2015.py
# Scrapes MLB regular-season standings (wins/losses/win%) for seasons 2000-2015
# Source pages: Baseball-Reference (e.g. https://www.baseball-reference.com/leagues/majors/2000-standings.shtml)
# Usage: python mlb_standings_scrape_2000_2015.py
#
# IMPORTANT: Please respect the site's robots.txt and terms of use.
# This script includes polite delays and a custom User-Agent.

import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.baseball-reference.com"
SEASON_URL = BASE_URL + "/leagues/majors/{year}-standings.shtml"
HEADERS = {"User-Agent": "MLB-Standings-Scraper/1.0 (+your_email@example.com) - For research/educational use"}
OUTFILE = "mlb_2000_2015_standings.csv"

def parse_division_table(table):
    rows = []
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    for tr in table.find_all("tr"):
        cols = tr.find_all(["th", "td"])
        if not cols:
            continue
        if tr.get("class") and ("thead" in tr.get("class") or "divider" in tr.get("class")):
            continue
        try:
            team_cell = cols[0]
            team_name = team_cell.get_text(strip=True)
            if team_name in ("Team", ""):
                continue
        except Exception:
            continue

        text_cols = [c.get_text(strip=True) for c in cols]
        w = l = wpct = ""
        for i, col_text in enumerate(text_cols):
            h = headers[i] if i < len(headers) else ""
            if h.lower().startswith("w") and w == "":
                w = col_text
            elif h.lower().startswith("l") and l == "":
                l = col_text
            elif ("w-l%" in h.lower() or "w-l" in h.lower() or "pct" in h.lower()) and wpct == "":
                wpct = col_text
        rows.append({"Team": team_name, "W": w, "L": l, "Wpct": wpct})
    return rows

def scrape_year(year):
    url = SEASON_URL.format(year=year)
    print(f"Fetching {url}")
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    season_rows = []
    tables = soup.find_all("table")
    candidate_tables = []
    for t in tables:
        header_texts = " ".join(th.get_text(" ", strip=True).lower() for th in t.find_all("th"))
        if "w" in header_texts and ("w-l%" in header_texts or "pct" in header_texts or "wins" in header_texts):
            candidate_tables.append(t)

    if not candidate_tables:
        candidate_tables = tables

    for t in candidate_tables:
        division = None
        parent = t.find_previous(["h2", "h3", "h4"])
        if parent:
            division = parent.get_text(strip=True)
        parsed = parse_division_table(t)
        for r in parsed:
            r["Year"] = year
            if division:
                if "american" in division.lower():
                    r["League"] = "AL"
                elif "national" in division.lower():
                    r["League"] = "NL"
                else:
                    if "al" in division.lower():
                        r["League"] = "AL"
                    elif "nl" in division.lower():
                        r["League"] = "NL"
                    else:
                        r["League"] = ""
                r["Division"] = division
            else:
                r["League"] = ""
                r["Division"] = ""
            season_rows.append(r)

    return season_rows

def main():
    years = list(range(2000, 2016))
    with open(OUTFILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Year","League","Division","Team","W","L","Wpct"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for y in years:
            try:
                rows = scrape_year(y)
            except Exception as e:
                print(f"Error fetching/parsing {y}: {e}")
                rows = []
            for r in rows:
                out = {k: r.get(k, "") for k in fieldnames}
                writer.writerow(out)
            time.sleep(3.0)

    print(f"Done. CSV written to {OUTFILE}")

if __name__ == "__main__":
    main()
