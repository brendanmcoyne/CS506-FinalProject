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
HEADERS = {
    "User-Agent": "MLB-Standings-Scraper/1.0 (+your_email@example.com) - For research/educational use"
}
OUTFILE = "mlb_2000_2015_standings.csv"

def parse_division_table(table):
    """
    Given a BeautifulSoup <table> element for a division, return list of dict rows:
    {Team, W, L, Wpct, RS, RA, League, Division}
    Some columns may be missing depending on table format; we'll grab W, L, W-L%, and Team name.
    """
    rows = []
    # table header columns help identify indices
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    # find body rows
    for tr in table.find_all("tr"):
        cols = tr.find_all(["th", "td"])
        if not cols:
            continue
        # skip subheader rows
        if tr.get("class") and ("thead" in tr.get("class") or "divider" in tr.get("class")):
            continue
        # team cell normally has 'team' class or a link
        try:
            team_cell = cols[0]
            team_name = team_cell.get_text(strip=True)
            # Skip rows like "Notes" or empty
            if team_name in ("Team", ""):
                continue
        except Exception:
            continue

        # Find W, L, W-L% by searching header names
        text_cols = [c.get_text(strip=True) for c in cols]
        # naive approach: find typical columns
        w = l = wpct = ""
        for i, col_text in enumerate(text_cols):
            h = headers[i] if i < len(headers) else ""
            # match by header text heuristics
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
    # Baseball-Reference uses several tables for divisions on the majors standings page.
    # We'll look for all division tables under the page's main content.
    # Division tables usually appear with class "standings" or are the only <table> in each div.section.
    tables = soup.find_all("table")
    # To be safer, filter to tables that contain a "W" header or "W-L%" header
    candidate_tables = []
    for t in tables:
        header_texts = " ".join(th.get_text(" ", strip=True).lower() for th in t.find_all("th"))
        if "w" in header_texts and ("w-l%" in header_texts or "pct" in header_texts or "wins" in header_texts):
            candidate_tables.append(t)

    # If none detected via heuristic, fall back to all tables (best-effort)
    if not candidate_tables:
        candidate_tables = tables

    for t in candidate_tables:
        # Attempt to determine the division name from the preceding heading
        division = None
        parent = t.find_previous(["h2", "h3", "h4"])
        if parent:
            division = parent.get_text(strip=True)
        parsed = parse_division_table(t)
        for r in parsed:
            r["Year"] = year
            # attempt to split league/division if division contains "American League" or "National League"
            if division:
                if "american" in division.lower():
                    r["League"] = "AL"
                elif "national" in division.lower():
                    r["League"] = "NL"
                else:
                    # if division is like "AL East" or "NL West"
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
    years = list(range(2000, 2016))  # inclusive 2000-2015
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
            # Polite pause between requests so we don't hammer the server
            time.sleep(3.0)

    print(f"Done. CSV written to {OUTFILE}")

if __name__ == "__main__":
    main()
